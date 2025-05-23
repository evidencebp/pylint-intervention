# Copyright 2016 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc
import contextlib
import datetime

from neutron_lib import context as neutron_context
from neutron_lib.plugins import constants
from neutron_lib.plugins import directory
from neutron_lib.utils import helpers
from oslo_config import cfg
from oslo_log import log
from oslo_utils import timeutils
from ovs.db import idl as ovs_idl_mod
from ovs.stream import Stream
from ovsdbapp.backend.ovs_idl import connection
from ovsdbapp.backend.ovs_idl import event as row_event
from ovsdbapp.backend.ovs_idl import idlutils

from neutron.common.ovn import constants as ovn_const
from neutron.common.ovn import exceptions
from neutron.common.ovn import hash_ring_manager
from neutron.common.ovn import utils
from neutron.conf.plugins.ml2.drivers.ovn import ovn_conf
from neutron.db import ovn_hash_ring_db
from neutron.plugins.ml2.drivers.ovn.agent import neutron_agent as n_agent


CONF = cfg.CONF
LOG = log.getLogger(__name__)


class BaseEvent(row_event.RowEvent):
    table = None
    events = tuple()

    def __init__(self):
        self.event_name = self.__class__.__name__
        super(BaseEvent, self).__init__(self.events, self.table, None)

    @abc.abstractmethod
    def match_fn(self, event, row, old=None):
        """Define match criteria other than table/event"""

    def matches(self, event, row, old=None):
        if row._table.name != self.table or event not in self.events:
            return False
        if not self.match_fn(event, row, old):
            return False
        LOG.debug("%s : Matched %s, %s, %s %s", self.event_name, self.table,
                  event, self.conditions, self.old_conditions)
        return True


class ChassisEvent(row_event.RowEvent):
    """Chassis create update delete event."""

    def __init__(self, driver):
        self.driver = driver
        self.l3_plugin = directory.get_plugin(constants.L3)
        table = 'Chassis'
        events = (self.ROW_CREATE, self.ROW_UPDATE, self.ROW_DELETE)
        super(ChassisEvent, self).__init__(events, table, None)
        self.event_name = 'ChassisEvent'

    def _get_ha_chassis_groups_within_azs(self, az_hints):
        """Find all HA Chassis groups that are within the given AZs.

        :param az_hints: A list of availability zones hints
        :returns: A set with the HA Chassis Groups objects
        """
        ha_chassis_list = []
        for hcg in self.driver.nb_ovn.db_list_rows(
                'HA_Chassis_Group').execute(check_error=True):
            if not hcg.name.startswith(ovn_const.OVN_NAME_PREFIX):
                continue
            # The filter() is to get rid of the empty string in
            # the list that is returned because of split()
            azs = {az for az in
                   hcg.external_ids.get(
                       ovn_const.OVN_AZ_HINTS_EXT_ID_KEY, '').split(',') if az}
            # Find which Ha Chassis Group that is included in the
            # Availability Zone hints
            if az_hints.intersection(azs):
                ha_chassis_list.append(hcg)
            # If the Availability Zone hints is empty return a list
            # of HA Chassis Groups that does not belong to any AZ
            elif not az_hints and not azs:
                ha_chassis_list.append(hcg)
        return ha_chassis_list

    def _get_min_priority_in_hcg(self, ha_chassis_group):
        """Find the next lowest priority number within a HA Chassis Group."""
        min_priority = min(
            [ch.priority for ch in ha_chassis_group.ha_chassis],
            default=ovn_const.HA_CHASSIS_GROUP_HIGHEST_PRIORITY)
        return min_priority - 1

    def handle_ha_chassis_group_changes(self, event, row, old):
        """Handle HA Chassis Group changes.

        This method handles the inclusion and removal of Chassis to/from
        the default HA Chassis Group.
        """
        if not self.driver._ovn_client.is_external_ports_supported():
            return

        is_gw_chassis = utils.is_gateway_chassis(row)
        # If the Chassis being created is not a gateway, ignore it
        if not is_gw_chassis and event == self.ROW_CREATE:
            return

        azs = utils.get_chassis_availability_zones(row)

        if event == self.ROW_UPDATE:
            is_old_gw = utils.is_gateway_chassis(old)
            if is_gw_chassis and is_old_gw:
                old_azs = utils.get_chassis_availability_zones(old)
                # If there are no differences in the AZs, return
                if azs == old_azs:
                    return
                # Find out the HA Chassis Groups that were affected by
                # the update (to add and/or remove the updated Chassis)
                ha_ch_add = self._get_ha_chassis_groups_within_azs(
                    azs - old_azs)
                ha_ch_del = self._get_ha_chassis_groups_within_azs(
                    old_azs - azs)
                with self.driver.nb_ovn.transaction(check_error=True) as txn:
                    for hcg in ha_ch_add:
                        min_priority = self._get_min_priority_in_hcg(hcg)
                        txn.add(
                            self.driver.nb_ovn.ha_chassis_group_add_chassis(
                                hcg.name, row.name, priority=min_priority))
                    for hcg in ha_ch_del:
                        txn.add(
                            self.driver.nb_ovn.ha_chassis_group_del_chassis(
                                hcg.name, row.name, if_exists=True))
                return
            elif not is_gw_chassis and is_old_gw:
                # Chassis is not a gateway anymore, treat it as deletion
                event = self.ROW_DELETE
            elif is_gw_chassis and not is_old_gw:
                # Chassis is now a gateway, treat it as creation
                event = self.ROW_CREATE

        if event == self.ROW_CREATE:
            ha_chassis_list = self._get_ha_chassis_groups_within_azs(azs)
            with self.driver.nb_ovn.transaction(check_error=True) as txn:
                for hcg in ha_chassis_list:
                    min_priority = self._get_min_priority_in_hcg(hcg)
                    txn.add(self.driver.nb_ovn.ha_chassis_group_add_chassis(
                        hcg.name, row.name, priority=min_priority))

        elif event == self.ROW_DELETE:
            ha_chassis_list = self._get_ha_chassis_groups_within_azs(azs)
            with self.driver.nb_ovn.transaction(check_error=True) as txn:
                for hcg in ha_chassis_list:
                    txn.add(self.driver.nb_ovn.ha_chassis_group_del_chassis(
                        hcg.name, row.name, if_exists=True))

    def match_fn(self, event, row, old):
        if event != self.ROW_UPDATE:
            return True
        # NOTE(lucasgomes): If the external_ids column wasn't updated
        # (meaning, Chassis "gateway" status didn't change) just returns
        if not hasattr(old, 'external_ids') and event == self.ROW_UPDATE:
            return False
        if (old.external_ids.get('ovn-bridge-mappings') !=
                row.external_ids.get('ovn-bridge-mappings')):
            return True
        # Check if either the Gateway status or Availability Zones has
        # changed in the Chassis
        is_gw = utils.is_gateway_chassis(row)
        is_gw_old = utils.is_gateway_chassis(old)
        azs = utils.get_chassis_availability_zones(row)
        old_azs = utils.get_chassis_availability_zones(old)
        if is_gw != is_gw_old or azs != old_azs:
            return True
        return False

    def run(self, event, row, old):
        host = row.hostname
        phy_nets = []
        if event != self.ROW_DELETE:
            bridge_mappings = row.external_ids.get('ovn-bridge-mappings', '')
            mapping_dict = helpers.parse_mappings(bridge_mappings.split(','))
            phy_nets = list(mapping_dict)

        self.driver.update_segment_host_mapping(host, phy_nets)

        if utils.is_ovn_l3(self.l3_plugin):
            # If chassis lost physnet or has been
            # deleted we can limit the scope and
            # reschedule only ports from this chassis.
            # In other cases we need to reschedule all gw ports.
            kwargs = {'event_from_chassis': None}
            if event == self.ROW_DELETE:
                kwargs['event_from_chassis'] = row.name
            elif event == self.ROW_UPDATE:
                old_mappings = old.external_ids.get('ovn-bridge-mappings',
                                                    set()) or set()
                new_mappings = row.external_ids.get('ovn-bridge-mappings',
                                                    set()) or set()
                if old_mappings:
                    old_mappings = set(old_mappings.split(','))
                if new_mappings:
                    new_mappings = set(new_mappings.split(','))

                mappings_removed = old_mappings - new_mappings
                mappings_added = new_mappings - old_mappings
                if mappings_removed and not mappings_added:
                    # Mapping has been only removed. So we can
                    # limit scope of rescheduling only to impacted
                    # gateway chassis.
                    kwargs['event_from_chassis'] = row.name
            self.l3_plugin.schedule_unhosted_gateways(**kwargs)

        self.handle_ha_chassis_group_changes(event, row, old)


class ChassisAgentEvent(BaseEvent):
    GLOBAL = True

    # NOTE (twilson) Do not run new transactions out of a GLOBAL Event since
    # it will be running on every single process, and you almost certainly
    # don't want to insert/update/delete something a bajillion times.
    def __init__(self, driver):
        self.driver = driver
        super().__init__()

    @property
    def table(self):
        # It probably doesn't matter, but since agent_chassis_table changes
        # in post_fork_initialize(), resolve this at runtime
        return self.driver.agent_chassis_table

    @table.setter
    def table(self, value):
        pass


class ChassisAgentDownEvent(ChassisAgentEvent):
    events = (BaseEvent.ROW_DELETE,)

    def run(self, event, row, old):
        for agent in n_agent.AgentCache().agents_by_chassis_private(row):
            agent.set_down = True

    def match_fn(self, event, row, old=None):
        return True


class ChassisAgentDeleteEvent(ChassisAgentEvent):
    events = (BaseEvent.ROW_UPDATE,)
    table = 'SB_Global'

    def match_fn(self, event, row, old=None):
        try:
            return (old.external_ids.get('delete_agent') !=
                    row.external_ids['delete_agent'])
        except (AttributeError, KeyError):
            return False

    def run(self, event, row, old):
        del n_agent.AgentCache()[row.external_ids['delete_agent']]


class ChassisAgentWriteEvent(ChassisAgentEvent):
    events = (BaseEvent.ROW_CREATE, BaseEvent.ROW_UPDATE)

    def match_fn(self, event, row, old=None):
        # On updates to Chassis_Private because the Chassis has been deleted,
        # don't update the AgentCache. We use chassis_private.chassis to return
        # data about the agent.
        return event == self.ROW_CREATE or (
            getattr(old, 'nb_cfg', False) and not
            (self.table == 'Chassis_Private' and not row.chassis))

    def run(self, event, row, old):
        n_agent.AgentCache().update(ovn_const.OVN_CONTROLLER_AGENT, row,
                                    clear_down=event == self.ROW_CREATE)


class ChassisAgentTypeChangeEvent(ChassisEvent):
    """Chassis Agent class change event"""
    GLOBAL = True
    events = (BaseEvent.ROW_UPDATE,)

    def match_fn(self, event, row, old=None):
        if not getattr(old, 'external_ids', False):
            return False
        agent_type_change = n_agent.NeutronAgent.chassis_from_private(
                row).external_ids.get('ovn-cms-options', []) != (
                        old.external_ids.get('ovn-cms-options', []))
        return agent_type_change

    def run(self, event, row, old):
        n_agent.AgentCache().update(ovn_const.OVN_CONTROLLER_AGENT, row,
                                    clear_down=event == self.ROW_CREATE)


class ChassisMetadataAgentWriteEvent(ChassisAgentEvent):
    events = (BaseEvent.ROW_CREATE, BaseEvent.ROW_UPDATE)

    @staticmethod
    def _metadata_nb_cfg(row):
        return int(
            row.external_ids.get(ovn_const.OVN_AGENT_METADATA_SB_CFG_KEY, -1))

    @staticmethod
    def agent_id(row):
        return row.external_ids.get(ovn_const.OVN_AGENT_METADATA_ID_KEY)

    def match_fn(self, event, row, old=None):
        if not self.agent_id(row):
            # Don't create a cached object with an agent_id of 'None'
            return False
        if event == self.ROW_CREATE:
            return True
        try:
            # On updates to Chassis_Private because the Chassis has been
            # deleted, don't update the AgentCache. We use
            # chassis_private.chassis to return data about the agent.
            if self.table == 'Chassis_Private' and not row.chassis:
                return False
            return self._metadata_nb_cfg(row) != self._metadata_nb_cfg(old)
        except (AttributeError, KeyError):
            return False

    def run(self, event, row, old):
        n_agent.AgentCache().update(ovn_const.OVN_METADATA_AGENT, row,
                                    clear_down=True)


class PortBindingChassisEvent(row_event.RowEvent):
    """Port_Binding update event - set chassis for chassisredirect port.

    When a chassisredirect port is updated with chassis, this event get
    generated. We will update corresponding router's gateway port with
    the chassis's host_id. Later, users can check router's gateway port
    host_id to find the location of primary HA router.
    """

    def __init__(self, driver):
        self.driver = driver
        self.l3_plugin = directory.get_plugin(constants.L3)
        table = 'Port_Binding'
        events = (self.ROW_UPDATE,)
        super(PortBindingChassisEvent, self).__init__(
            events, table, (('type', '=', ovn_const.OVN_CHASSIS_REDIRECT),))
        self.event_name = 'PortBindingChassisEvent'

    def run(self, event, row, old):
        if not utils.is_ovn_l3(self.l3_plugin):
            return
        router = host = None
        chassis = getattr(row, 'chassis', None)
        if chassis:
            router = row.datapath.external_ids.get('name', '').replace(
                'neutron-', '')
            host = chassis[0].hostname
            LOG.info("Router %(router)s is bound to host %(host)s",
                     {'router': router, 'host': host})
        self.l3_plugin.update_router_gateway_port_bindings(
            router, host)


class PortBindingCreateUpEvent(row_event.RowEvent):
    """Row create event - Port_Binding 'up' = True.

    On connection, we get a dump of all ports, so if there is a neutron
    port that is down that has since been activated, we'll catch it here.
    This event will not be generated for new ports getting created.
    """

    def __init__(self, driver):
        self.driver = driver
        table = 'Port_Binding'
        events = (self.ROW_CREATE,)
        super().__init__(events, table, None)
        self.event_name = 'PortBindingCreateUpEvent'

    def match_fn(self, event, row, old):
        if row.type in (ovn_const.PB_TYPE_VIRTUAL,
                        ovn_const.OVN_CHASSIS_REDIRECT):
            # NOTE(ltomasbo): Skipping virtual ports as they are not being
            # set to ACTIVE
            # NOTE(ltomasbo): No need to handle cr ports
            return False
        if row.type == ovn_const.PB_TYPE_PATCH:
            # NOTE(ltomasbo): Only handle the logical_switch_port side,
            # not the router side.
            if (row.logical_port.startswith('lrp-') or
                    row.logical_port.startswith('cr-lrp')):
                return False
            return True
        # TODO(ltomasbo): Remove the checkings for 'up' column once minimal
        # ovn version has it (v21.03.0). The match_fn can be then replaced
        # by different init method above:
        # super().__init__(
        #     events, table, (('up', '=', True), ('type', '=', ''),))
        if hasattr(row, 'up'):
            # NOTE(ltomasbo): Due to bug in core ovn not setting the up field
            # to DOWN in some cases (for example subports detachment from
            # trunks), we need to also check the chassis is set to claim the
            # port as ACTIVE
            return row.chassis and bool(row.up[0])
        elif row.chassis:
            return True
        return False

    def run(self, event, row, old):
        self.driver.set_port_status_up(row.logical_port)


class PortBindingCreateDownEvent(row_event.RowEvent):
    """Row create event - Port_Binding 'up' = False

    On connection, we get a dump of all ports, so if there is a neutron
    port that is up that has since been deactivated, we'll catch it here.
    This event will not be generated for new ports getting created.
    """

    def __init__(self, driver):
        self.driver = driver
        table = 'Port_Binding'
        events = (self.ROW_CREATE,)
        super().__init__(events, table, None)
        self.event_name = 'PortBindingCreateDownEvent'

    def match_fn(self, event, row, old):
        if row.type in [ovn_const.PB_TYPE_VIRTUAL, ovn_const.PB_TYPE_PATCH,
                        ovn_const.OVN_CHASSIS_REDIRECT]:
            # NOTE(ltomasbo): Skipping as virtual ports are not being set to
            # ACTIVE
            # Patch ports are set to UP on creation, no need to update
            # No need to handle cr ports
            return False

        # TODO(ltomasbo): Remove the checkings for 'up' column once minimal
        # ovn version has it (v21.03.0). The match_fn can be then replaced
        # by different init method above:
        # super().__init__(
        #     events, table, (('up', '=', False), ('type', '=', ''),))
        if hasattr(row, 'up'):
            # NOTE(ltomasbo): Due to bug in core ovn not setting the up field
            # to DOWN in some cases (for example subports detachment from
            # trunks), we need to also check if the chassis is unset to set
            # the port as DOWN
            return not row.chassis or not bool(row.up[0])
        elif not row.chassis:
            return True
        return False

    def run(self, event, row, old):
        self.driver.set_port_status_down(row.logical_port)


class PortBindingUpdateUpEvent(row_event.RowEvent):
    """Row update event - Port_Binding 'up' going from False to True

    This happens when the VM goes up.
    New value of Port_Binding 'up' will be True and the old value will
    be False. Or if that column does not exists, the chassis will be set
    and the old chassis value will be empty.
    """

    def __init__(self, driver):
        self.driver = driver
        table = 'Port_Binding'
        events = (self.ROW_UPDATE,)
        super().__init__(events, table, None)
        self.event_name = 'PortBindingUpdateUpEvent'

    def match_fn(self, event, row, old):
        if row.type in (ovn_const.PB_TYPE_VIRTUAL,
                        ovn_const.OVN_CHASSIS_REDIRECT):
            # NOTE(ltomasbo): Skipping virtual ports as they are not being
            # set to ACTIVE
            # NOTE(ltomasbo): No need to handle cr ports
            return False
        if row.type == ovn_const.PB_TYPE_PATCH:
            # NOTE(ltomasbo): Only handle the logical_switch_port side,
            # not the router side.
            if (row.logical_port.startswith('lrp-') or
                    row.logical_port.startswith('cr-lrp')):
                return False
            try:
                if old.mac:
                    # NOTE(ltomasbo): only execute it once (the first update
                    # event for this port), as you don't need to set it to
                    # active several time
                    return True
            except AttributeError:
                return False
            return False
        # TODO(ltomasbo): Remove the checkings for 'up' column once minimal
        # ovn version has it (v21.03.0). The match_fn can be then replaced
        # by different init method above:
        # super().__init__(
        #     events, table, (('up', '=', True), ('type', '=', '')),
        #     old_conditions=(('up', '=', False),))
        try:
            if hasattr(row, 'up'):
                # NOTE(ltomasbo): Due to bug in core ovn not setting the up
                # field to DOWN in some cases (for example subports detachment
                # from trunks), we need to also check the chassis is set to
                # claim the port as ACTIVE
                return (bool(row.up[0]) and not bool(old.up[0]) and
                        row.chassis)
            elif row.chassis and not old.chassis:
                return True
        except AttributeError:
            # NOTE(ltomasbo): do not process if there is no old up/chassis
            # information
            return False
        return False

    def run(self, event, row, old):
        self.driver.set_port_status_up(row.logical_port)


class PortBindingUpdateDownEvent(row_event.RowEvent):
    """Row update event - Port_Binding 'up' going from True to False

    This happens when the VM goes down.
    New value of Port_Binding 'up' will be False and the old value will
    be True. Or if that column does not exists, the chassis will be unset
    and the old chassis will be set.
    """

    def __init__(self, driver):
        self.driver = driver
        table = 'Port_Binding'
        events = (self.ROW_UPDATE,)
        super().__init__(events, table, None)
        self.event_name = 'PortBindingUpdateDownEvent'

    def match_fn(self, event, row, old):
        if row.type in [ovn_const.PB_TYPE_VIRTUAL, ovn_const.PB_TYPE_PATCH,
                        ovn_const.OVN_CHASSIS_REDIRECT]:
            # NOTE(ltomasbo): Skipping as virtual ports are not being set to
            # ACTIVE
            # Patch ports are meant to be always UP, after creation, no need
            # to update
            # No need to handle cr ports
            return False
        # TODO(ltomasbo): Remove the checkings for 'up' column once minimal
        # ovn version has it (v21.03.0). The match_fn can be then replaced
        # by different init method above:
        # super().__init__(
        #     events, table, (('up', '=', False), ('type', '=', '')),
        #     old_conditions=(('up', '=', True),))
        try:
            if hasattr(row, 'up'):
                # NOTE(ltomasbo): Due to bug in core ovn not setting the up
                # field to DOWN in some cases (for example subports detachment
                # from trunks), we need to also check if the chassis is being
                # unset to set the port as DOWN
                return ((not bool(row.up[0]) and bool(old.up[0])) or
                        (not row.chassis and old.chassis))
            elif not row.chassis and old.chassis:
                return True
        except AttributeError:
            # NOTE(ltomasbo): do not process if there is no old up/chassis
            # information
            return False
        return False

    def run(self, event, row, old):
        self.driver.set_port_status_down(row.logical_port)


class PortBindingUpdateVirtualPortsEvent(row_event.RowEvent):
    """Row update event - Port_Binding for virtual ports

    The goal of this event is to catch the events of the virtual ports and
    update the hostname in the related "portbinding" register.
    """
    def __init__(self, driver):
        self.driver = driver
        table = 'Port_Binding'
        events = (self.ROW_UPDATE, )
        super().__init__(events, table, None)
        self.event_name = 'PortBindingUpdateVirtualPortsEvent'

    def match_fn(self, event, row, old):
        # This event should catch only those events from ports that are
        # "virtual" or have been "virtual". The second happens when all virtual
        # parent are disassociated; in the same transaction the
        # "virtual-parents" list is removed from "options" and the type is set
        # to "".
        if (row.type != ovn_const.PB_TYPE_VIRTUAL and
                getattr(old, 'type', None) != ovn_const.PB_TYPE_VIRTUAL):
            return False

        virtual_parents = (row.options or {}).get(
            ovn_const.LSP_OPTIONS_VIRTUAL_PARENTS_KEY)
        old_virtual_parents = getattr(old, 'options', {}).get(
            ovn_const.LSP_OPTIONS_VIRTUAL_PARENTS_KEY)
        chassis = row.chassis
        old_chassis = getattr(old, 'chassis', [])

        if virtual_parents and chassis != old_chassis:
            # That happens when the chassis is assigned (VIP is first detected
            # in a port) or changed (the VIP changes of assigned port and
            # host).
            return True

        if not virtual_parents and old_virtual_parents:
            # All virtual parent ports are removed, the VIP is unbound.
            return True
        return False

    def run(self, event, row, old):
        virtual_parents = (row.options or {}).get(
            ovn_const.LSP_OPTIONS_VIRTUAL_PARENTS_KEY)
        chassis_uuid = (row.chassis[0].uuid if
                        row.chassis and virtual_parents else None)
        self.driver.update_virtual_port_host(row.logical_port, chassis_uuid)


class FIPAddDeleteEvent(row_event.RowEvent):
    """Row event - NAT 'dnat_and_snat' entry added or deleted

    This happens when a FIP is created or removed.
    """
    def __init__(self, driver):
        self.driver = driver
        table = 'NAT'
        events = (self.ROW_CREATE, self.ROW_DELETE)
        super(FIPAddDeleteEvent, self).__init__(
            events, table, (('type', '=', 'dnat_and_snat'),))
        self.event_name = 'FIPAddDeleteEvent'

    def run(self, event, row, old):
        # When a FIP is added or deleted, we will delete all entries in the
        # MAC_Binding table of SB OVSDB corresponding to that IP Address.
        # TODO(dalvarez): Remove this workaround once fixed in core OVN:
        # https://mail.openvswitch.org/pipermail/ovs-discuss/2018-October/047604.html
        self.driver.delete_mac_binding_entries(row.external_ip)


class NeutronPgDropPortGroupCreated(row_event.WaitEvent):
    """WaitEvent for neutron_pg_drop Create event."""
    def __init__(self, timeout=None):
        table = 'Port_Group'
        events = (self.ROW_CREATE,)
        conditions = (('name', '=', ovn_const.OVN_DROP_PORT_GROUP_NAME),)
        super(NeutronPgDropPortGroupCreated, self).__init__(
            events, table, conditions, timeout=timeout)
        self.event_name = 'PortGroupCreated'


class OvnDbNotifyHandler(row_event.RowEventHandler):
    def __init__(self, driver):
        self.driver = driver
        super(OvnDbNotifyHandler, self).__init__()
        try:
            self._lock = self._RowEventHandler__lock
            self._watched_events = self._RowEventHandler__watched_events
        except AttributeError:
            pass

    def notify(self, event, row, updates=None, global_=False):
        row = idlutils.frozen_row(row)
        matching = self.matching_events(event, row, updates, global_)
        for match in matching:
            self.notifications.put((match, event, row, updates))

    def matching_events(self, event, row, updates, global_=False):
        with self._lock:
            return tuple(t for t in self._watched_events
                         if getattr(t, 'GLOBAL', False) == global_ and
                         self.match(t, event, row, updates))


class Ml2OvnIdlBase(connection.OvsdbIdl):
    def __init__(self, remote, schema, probe_interval=(), **kwargs):
        if probe_interval == ():  # None is a valid value to pass
            probe_interval = ovn_conf.get_ovn_ovsdb_probe_interval()
        super(Ml2OvnIdlBase, self).__init__(
            remote, schema, probe_interval=probe_interval, **kwargs)

    def set_table_condition(self, table_name, condition):
        # Prior to ovs commit 46d44cf3be0, self.cond_change() doesn't work here
        # but after that commit, setting table.condtion doesn't work.
        if hasattr(ovs_idl_mod, 'ConditionState'):
            self.cond_change(table_name, condition)
        else:
            # Can be removed after the minimum ovs version >= 2.17.0
            self.tables[table_name].condition = condition


class BaseOvnIdl(Ml2OvnIdlBase):
    def __init__(self, remote, schema, **kwargs):
        self.notify_handler = row_event.RowEventHandler()
        super(BaseOvnIdl, self).__init__(remote, schema, **kwargs)

    @classmethod
    def from_server(cls, connection_string, helper):
        helper.register_all()
        return cls(connection_string, helper)

    def notify(self, event, row, updates=None):
        self.notify_handler.notify(event, row, updates)


class BaseOvnSbIdl(Ml2OvnIdlBase):
    @classmethod
    def from_server(cls, connection_string, helper):
        helper.register_table('Chassis')
        helper.register_table('Encap')
        helper.register_table('Port_Binding')
        helper.register_table('Datapath_Binding')
        # Used by MaintenanceWorker which can use ovsdb locking
        try:
            return cls(connection_string, helper, leader_only=True)
        except TypeError:
            # TODO(twilson) We can remove this when we require ovs>=2.12.0
            return cls(connection_string, helper)


class OvnIdl(BaseOvnIdl):

    def __init__(self, driver, remote, schema, **kwargs):
        super(OvnIdl, self).__init__(remote, schema, **kwargs)
        self.driver = driver
        self.notify_handler = OvnDbNotifyHandler(driver)

    def notify(self, event, row, updates=None):
        # Do not handle the notification if the event lock is requested,
        # but not granted by the ovsdb-server.
        if self.is_lock_contended:
            return
        self.notify_handler.notify(event, row, updates)

    @abc.abstractmethod
    def post_connect(self):
        """Should be called after the idl has been initialized"""


class OvnIdlDistributedLock(BaseOvnIdl):

    def __init__(self, driver, remote, schema, **kwargs):
        super(OvnIdlDistributedLock, self).__init__(remote, schema, **kwargs)
        self.driver = driver
        self.notify_handler = OvnDbNotifyHandler(driver)
        self._node_uuid = self.driver.node_uuid
        self._hash_ring = hash_ring_manager.HashRingManager(
            self.driver.hash_ring_group)
        self._last_touch = None
        # This is a map of tables that may be new after OVN database is updated
        self._tables_to_register = {
            'OVN_Southbound': ['Chassis_Private'],
        }

    def handle_db_schema_changes(self, event, row):
        if (event == row_event.RowEvent.ROW_CREATE and
                row._table.name == 'Database'):
            try:
                tables = self._tables_to_register[row.name]
            except KeyError:
                return

            self.update_tables(tables, row.schema[0])

            if 'Chassis_Private' == self.driver.agent_chassis_table:
                if 'Chassis_Private' not in self.tables:
                    self.driver.agent_chassis_table = 'Chassis'
            else:
                if 'Chassis_Private' in self.tables:
                    self.driver.agent_chassis_table = 'Chassis_Private'

    def notify(self, event, row, updates=None):
        self.handle_db_schema_changes(event, row)
        self.notify_handler.notify(event, row, updates, global_=True)
        try:
            target_node = self._hash_ring.get_node(str(row.uuid))
        except exceptions.HashRingIsEmpty as e:
            LOG.error('HashRing is empty, error: %s', e)
            return
        if target_node != self._node_uuid:
            return

        # If the worker hasn't been health checked by the maintenance
        # thread (see bug #1834498), indicate that it's alive here
        time_now = timeutils.utcnow()
        touch_timeout = time_now - datetime.timedelta(
            seconds=ovn_const.HASH_RING_TOUCH_INTERVAL)
        if not self._last_touch or touch_timeout >= self._last_touch:
            # NOTE(lucasagomes): Guard the db operation with an exception
            # handler. If heartbeating fails for whatever reason, log
            # the error and continue with processing the event
            try:
                ctx = neutron_context.get_admin_context()
                ovn_hash_ring_db.touch_node(ctx, self._node_uuid)
                self._last_touch = time_now
            except Exception:
                LOG.exception('Hash Ring node %s failed to heartbeat',
                              self._node_uuid)

        LOG.debug('Hash Ring: Node %(node)s (host: %(hostname)s) '
                  'handling event "%(event)s" for row %(row)s '
                  '(table: %(table)s)',
                  {'node': self._node_uuid, 'hostname': CONF.host,
                   'event': event, 'row': row.uuid, 'table': row._table.name})
        self.notify_handler.notify(event, row, updates)

    @abc.abstractmethod
    def post_connect(self):
        """Should be called after the idl has been initialized"""


class OvnNbIdl(OvnIdlDistributedLock):

    def __init__(self, driver, remote, schema):
        super(OvnNbIdl, self).__init__(driver, remote, schema)
        self._fip_create_delete_event = FIPAddDeleteEvent(driver)

        self.notify_handler.watch_events([self._fip_create_delete_event])

    @classmethod
    def from_server(cls, connection_string, helper, driver):

        helper.register_all()
        return cls(driver, connection_string, helper)


class OvnSbIdl(OvnIdlDistributedLock):

    def __init__(self, driver, remote, schema, **kwargs):
        super(OvnSbIdl, self).__init__(driver, remote, schema, **kwargs)

        self._pb_create_up_event = PortBindingCreateUpEvent(driver)
        self._pb_create_down_event = PortBindingCreateDownEvent(driver)

        self.notify_handler.watch_events([
            ChassisAgentDeleteEvent(self.driver),
            ChassisAgentDownEvent(self.driver),
            ChassisAgentWriteEvent(self.driver),
            ChassisAgentTypeChangeEvent(self.driver),
            ChassisMetadataAgentWriteEvent(self.driver),
            self._pb_create_up_event,
            self._pb_create_down_event,
            PortBindingUpdateUpEvent(driver),
            PortBindingUpdateDownEvent(driver),
            PortBindingUpdateVirtualPortsEvent(driver),
        ])

    @classmethod
    def from_server(cls, connection_string, helper, driver):
        if 'Chassis_Private' in helper.schema_json['tables']:
            helper.register_table('Chassis_Private')
        if 'FDB' in helper.schema_json['tables']:
            helper.register_table('FDB')
        helper.register_table('Chassis')
        helper.register_table('Encap')
        helper.register_table('Port_Binding')
        helper.register_table('Datapath_Binding')
        helper.register_table('Connection')
        helper.register_columns('SB_Global', ['external_ids'])
        try:
            return cls(driver, connection_string, helper, leader_only=False)
        except TypeError:
            # TODO(twilson) We can remove this when we require ovs>=2.12.0
            return cls(driver, connection_string, helper)

    def post_connect(self):
        """Watch Chassis events.

        When the ovs idl client connects to the ovsdb-server, it gets
        a dump of all Chassis create event. We don't need to process them
        because there will be sync up at startup. After that, we will watch
        the events to make notify work.
        """
        self._chassis_event = ChassisEvent(self.driver)
        self._portbinding_event = PortBindingChassisEvent(self.driver)
        self.notify_handler.watch_events(
            [self._chassis_event, self._portbinding_event])

        self.unwatch_port_binding_create_events()

    def unwatch_port_binding_create_events(self):
        """Unwatch the port binding create events.

        When the ovs idl client connects to the ovsdb-server, it gets
        a dump of all port binding events and we need to process
        them at start up.
        After the startup, there is no need to watch these events.
        So unwatch these events.
        """
        self.notify_handler.unwatch_events([self._pb_create_up_event,
                                            self._pb_create_down_event])
        self._pb_create_up_event = None
        self._pb_create_down_event = None


class OvnInitPGNbIdl(OvnIdl):
    """Very limited OVN NB IDL.

    This IDL is intended to be used only in initialization phase with short
    living DB connections.
    """

    tables = ['Port_Group', 'Logical_Switch_Port', 'ACL']

    def __init__(self, driver, remote, schema):
        super(OvnInitPGNbIdl, self).__init__(driver, remote, schema)
        self.set_table_condition(
            'Port_Group', [['name', '==', ovn_const.OVN_DROP_PORT_GROUP_NAME]])
        self.neutron_pg_drop_event = NeutronPgDropPortGroupCreated(
                timeout=ovn_conf.get_ovn_ovsdb_timeout())
        self.notify_handler.watch_event(self.neutron_pg_drop_event)

    def notify(self, event, row, updates=None):
        # Go ahead and process events even if the lock is contended so we can
        # know that some other server has created the drop group
        self.notify_handler.notify(event, row, updates)

    @classmethod
    def from_server(cls, connection_string, helper, driver, pg_only=False):
        if pg_only:
            helper.register_table('Port_Group')
        else:
            for table in cls.tables:
                helper.register_table(table)

        return cls(driver, connection_string, helper)


@contextlib.contextmanager
def short_living_ovsdb_api(api_class, idl):
    """Context manager for short living connections to the database.

    :param api_class: Class implementing the database calls
                      (e.g. from the impl_idl module)
    :param idl: An instance of IDL class (e.g. instance of OvnNbIdl)
    """
    conn = connection.Connection(
        idl, timeout=ovn_conf.get_ovn_ovsdb_timeout())
    api = api_class(conn)
    try:
        yield api
    finally:
        api.ovsdb_connection.stop()


def _check_and_set_ssl_files(schema_name):
    if schema_name == 'OVN_Southbound':
        priv_key_file = ovn_conf.get_ovn_sb_private_key()
        cert_file = ovn_conf.get_ovn_sb_certificate()
        ca_cert_file = ovn_conf.get_ovn_sb_ca_cert()
    else:
        priv_key_file = ovn_conf.get_ovn_nb_private_key()
        cert_file = ovn_conf.get_ovn_nb_certificate()
        ca_cert_file = ovn_conf.get_ovn_nb_ca_cert()

    if priv_key_file:
        Stream.ssl_set_private_key_file(priv_key_file)

    if cert_file:
        Stream.ssl_set_certificate_file(cert_file)

    if ca_cert_file:
        Stream.ssl_set_ca_cert_file(ca_cert_file)
