# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
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
import time

import netaddr
from neutron_lib.agent.linux import interface
from neutron_lib import constants
from neutron_lib import exceptions
from oslo_log import log as logging
from oslo_utils import excutils
from pyroute2.netlink import exceptions \
    as pyroute2_exc  # pylint: disable=no-name-in-module

from neutron.agent.common import ovs_lib
from neutron.agent.linux import ip_lib
from neutron.common import utils
from neutron.conf.plugins.ml2.drivers import ovs_conf
from neutron.plugins.ml2.drivers.openvswitch.agent.common \
    import constants as ovs_const
from neutron.privileged.agent.linux import ethtool

LOG = logging.getLogger(__name__)


def _get_veth(name1, name2, namespace2):
    return (ip_lib.IPDevice(name1),
            ip_lib.IPDevice(name2, namespace=namespace2))


class LinuxInterfaceDriver(interface.LinuxInterfaceDriver,
                           metaclass=abc.ABCMeta):

    def __init__(self, conf, **kwargs):
        self.conf = conf
        self._mtu_update_warn_logged = False

    @property
    def use_gateway_ips(self):
        """Whether to use gateway IPs instead of unique IP allocations.

        In each place where the DHCP agent runs, and for each subnet for
        which DHCP is handling out IP addresses, the DHCP port needs -
        at the Linux level - to have an IP address within that subnet.
        Generally this needs to be a unique Neutron-allocated IP
        address, because the subnet's underlying L2 domain is bridged
        across multiple compute hosts and network nodes, and for HA
        there may be multiple DHCP agents running on that same bridged
        L2 domain.

        However, if the DHCP ports - on multiple compute/network nodes
        but for the same network - are _not_ bridged to each other,
        they do not need each to have a unique IP address.  Instead
        they can all share the same address from the relevant subnet.
        This works, without creating any ambiguity, because those
        ports are not all present on the same L2 domain, and because
        no data within the network is ever sent to that address.
        (DHCP requests are broadcast, and it is the network's job to
        ensure that such a broadcast will reach at least one of the
        available DHCP servers.  DHCP responses will be sent _from_
        the DHCP port address.)

        Specifically, for networking backends where it makes sense,
        the DHCP agent allows all DHCP ports to use the subnet's
        gateway IP address, and thereby to completely avoid any unique
        IP address allocation.  This behaviour is selected by running
        the DHCP agent with a configured interface driver whose
        'use_gateway_ips' property is True.

        When an operator deploys Neutron with an interface driver that
        makes use_gateway_ips True, they should also ensure that a
        gateway IP address is defined for each DHCP-enabled subnet,
        and that the gateway IP address doesn't change during the
        subnet's lifetime.
        """
        return False

    def init_l3(self, device_name, ip_cidrs, namespace=None,
                preserve_ips=None, clean_connections=False):
        """Set the L3 settings for the interface using data from the port.

        ip_cidrs: list of 'X.X.X.X/YY' strings
        preserve_ips: list of ip cidrs that should not be removed from device
        clean_connections: Boolean to indicate if we should cleanup connections
          associated to removed ips
        """
        preserve_ips = preserve_ips or []
        device = ip_lib.IPDevice(device_name, namespace=namespace)

        # The LLA generated by the operating system is not known to
        # Neutron, so it would be deleted if we added it to the 'previous'
        # list here
        default_ipv6_lla = ip_lib.get_ipv6_lladdr(device.link.address)

        cidrs = set()
        remove_ips = set()

        # normalize all the IP addresses first
        for ip_cidr in ip_cidrs:
            net = netaddr.IPNetwork(ip_cidr)
            # Convert to compact IPv6 address because the return values of
            # "ip addr list" are compact.
            if net.version == 6:
                ip_cidr = str(net)
            cidrs.add(ip_cidr)

        # Determine the addresses that must be added and removed
        for address in device.addr.list():
            cidr = address['cidr']
            dynamic = address['dynamic']

            # skip the IPv6 link-local
            if cidr == default_ipv6_lla:
                # it's already configured, leave it alone
                cidrs.discard(cidr)
                continue

            if cidr in preserve_ips:
                continue

            # Statically created addresses are OK, dynamically created
            # addresses must be removed and replaced
            if cidr in cidrs and not dynamic:
                cidrs.remove(cidr)
                continue

            remove_ips.add(cidr)

        # Clean up any old addresses.  This must be done first since there
        # could be a dynamic address being replaced with a static one.
        for ip_cidr in remove_ips:
            if clean_connections:
                device.delete_addr_and_conntrack_state(ip_cidr)
            else:
                device.addr.delete(ip_cidr)

        # add any new addresses
        for ip_cidr in cidrs:
            device.addr.add(ip_cidr)

    def init_router_port(self,
                         device_name,
                         ip_cidrs,
                         namespace,
                         preserve_ips=None,
                         extra_subnets=None,
                         clean_connections=False):
        """Set the L3 settings for a router interface using data from the port.

        ip_cidrs: list of 'X.X.X.X/YY' strings
        preserve_ips: list of ip cidrs that should not be removed from device
        clean_connections: Boolean to indicate if we should cleanup connections
          associated to removed ips
        extra_subnets: An iterable of cidrs to add as routes without address
        """
        LOG.debug("init_router_port: device_name(%s), namespace(%s)",
                  device_name, namespace)
        self.init_l3(device_name=device_name,
                     ip_cidrs=ip_cidrs,
                     namespace=namespace,
                     preserve_ips=preserve_ips or [],
                     clean_connections=clean_connections)
        self.set_onlink_routes(device_name, namespace, extra_subnets,
                               preserve_ips)

    def set_onlink_routes(self, device_name, namespace, extra_subnets,
                          preserve_ips=None, is_ipv6=True):
        """Manage on-link routes (routes without an associate address)

        :param device_name: interface name
        :param namespace: namespace name
        :param extra_subnets: subnets attached to this interface without an IP
                              address set in this interface
        :param preserve_ips: IPs or CIDRs not to be deleted from the device
                             on-link route list
        """
        device = ip_lib.IPDevice(device_name, namespace=namespace)
        new_onlink_cidrs = set(s['cidr'] for s in extra_subnets or [])
        preserve_ips = set(preserve_ips if preserve_ips else [])

        onlink = device.route.list_onlink_routes(constants.IP_VERSION_4)
        if is_ipv6:
            onlink += device.route.list_onlink_routes(constants.IP_VERSION_6)
        existing_onlink_cidrs = set(r['cidr'] for r in onlink)

        for route in new_onlink_cidrs - existing_onlink_cidrs:
            LOG.debug('Adding onlink route (%s)', route)
            device.route.add_onlink_route(route)
        for route in existing_onlink_cidrs - new_onlink_cidrs - preserve_ips:
            LOG.debug('Deleting onlink route (%s)', route)
            device.route.delete_onlink_route(route)

    def add_ipv6_addr(self, device_name, v6addr, namespace, scope='global'):
        device = ip_lib.IPDevice(device_name,
                                 namespace=namespace)
        net = netaddr.IPNetwork(v6addr)
        device.addr.add(str(net), scope)

    def delete_ipv6_addr(self, device_name, v6addr, namespace):
        device = ip_lib.IPDevice(device_name,
                                 namespace=namespace)
        device.delete_addr_and_conntrack_state(v6addr)

    def delete_ipv6_addr_with_prefix(self, device_name, prefix, namespace):
        """Delete the first listed IPv6 address that falls within a given
        prefix.
        """
        device = ip_lib.IPDevice(device_name, namespace=namespace)
        net = netaddr.IPNetwork(prefix)
        for address in device.addr.list(scope='global', filters=['permanent']):
            ip_address = netaddr.IPNetwork(address['cidr'])
            if ip_address in net:
                device.delete_addr_and_conntrack_state(address['cidr'])
                break

    def get_ipv6_llas(self, device_name, namespace):
        kwargs = {'family': utils.get_socket_address_family(
                                constants.IP_VERSION_6),
                  'scope': 'link'}
        return ip_lib.get_devices_with_ip(namespace, name=device_name,
                                          **kwargs)

    def check_bridge_exists(self, bridge):
        if not ip_lib.device_exists(bridge):
            raise exceptions.BridgeDoesNotExist(bridge=bridge)

    def get_device_name(self, port):
        return (self.DEV_NAME_PREFIX + port.id)[:self.DEV_NAME_LEN]

    @staticmethod
    def configure_ipv6_ra(namespace, dev_name, value):
        """Configure handling of IPv6 Router Advertisements on an
        interface. See common/constants.py for possible values.
        """
        cmd = ['net.ipv6.conf.%(dev)s.accept_ra=%(value)s' % {'dev': dev_name,
                                                              'value': value}]
        ip_lib.sysctl(cmd, namespace=namespace)

    @staticmethod
    def configure_ipv6_forwarding(namespace, dev_name, enabled):
        """Configure IPv6 forwarding on an interface."""
        cmd = ['net.ipv6.conf.%(dev)s.forwarding=%(enabled)s' %
               {'dev': dev_name, 'enabled': int(enabled)}]
        ip_lib.sysctl(cmd, namespace=namespace)

    def plug(self, network_id, port_id, device_name, mac_address,
             bridge=None, namespace=None, prefix=None, mtu=None, link_up=True):
        if not ip_lib.device_exists(device_name,
                                    namespace=namespace):
            self.plug_new(network_id, port_id, device_name, mac_address,
                          bridge, namespace, prefix, mtu, link_up)
        else:
            LOG.info("Device %s already exists", device_name)
            if mtu:
                self.set_mtu(
                    device_name, mtu, namespace=namespace, prefix=prefix)
            else:
                LOG.warning("No MTU configured for port %s", port_id)

    @property
    def bridged(self):
        """Whether the DHCP port is bridged to the VM TAP interfaces.

        When the DHCP port is bridged to the TAP interfaces for the
        VMs for which it is providing DHCP service - as is the case
        for most Neutron network implementations - the DHCP server
        only needs to listen on the DHCP port, and will still receive
        DHCP requests from all the relevant VMs.

        If the DHCP port is not bridged to the relevant VM TAP
        interfaces, the DHCP server needs to listen explicitly on
        those TAP interfaces, and to treat those as aliases of the
        DHCP port where the IP subnet is defined.
        """
        return True

    def set_mtu(self, device_name, mtu, namespace=None, prefix=None):
        """Set MTU on the interface."""
        if not self._mtu_update_warn_logged:
            LOG.warning("Interface driver cannot update MTU for ports")
            self._mtu_update_warn_logged = True

    def set_link_status(self, device_name, namespace=None, link_up=True):
        ns_dev = ip_lib.IPWrapper(namespace=namespace).device(device_name)
        if not ns_dev.exists():
            LOG.debug("Device %s may concurrently be deleted.", device_name)
            return
        if link_up:
            ns_dev.link.set_up()
        else:
            ns_dev.link.set_down()


class NullDriver(LinuxInterfaceDriver):
    def plug_new(self, network_id, port_id, device_name, mac_address,
                 bridge=None, namespace=None, prefix=None, mtu=None,
                 link_up=True):
        pass

    def unplug(self, device_name, bridge=None, namespace=None, prefix=None):
        pass


class OVSInterfaceDriver(LinuxInterfaceDriver):
    """Driver for creating an internal interface on an OVS bridge."""

    DEV_NAME_PREFIX = constants.TAP_DEVICE_PREFIX

    def __init__(self, conf, **kwargs):
        super(OVSInterfaceDriver, self).__init__(conf, **kwargs)
        ovs_conf.register_ovs_agent_opts(self.conf)
        if self.conf.ovs_use_veth:
            self.DEV_NAME_PREFIX = 'ns-'

    def _get_tap_name(self, dev_name, prefix=None):
        if self.conf.ovs_use_veth:
            dev_name = dev_name.replace(prefix or self.DEV_NAME_PREFIX,
                                        constants.TAP_DEVICE_PREFIX)
        return dev_name

    def _ovs_add_port(self, bridge, device_name, port_id, mac_address,
                      internal=True):
        attrs = [('external_ids', {'iface-id': port_id,
                                   'iface-status': 'active',
                                   'attached-mac': mac_address})]
        if internal:
            attrs.insert(0, ('type', 'internal'))

        ovs = ovs_lib.OVSBridge(bridge)
        ovs.replace_port(device_name, *attrs)

    def _set_device_address(self, device, mac_address):
        for i in range(9):
            # workaround for the OVS shy port syndrome. ports sometimes
            # hide for a bit right after they are first created.
            # see bug/1618987
            try:
                device.link.set_address(mac_address)
                break
            except RuntimeError as e:
                LOG.warning("Got error trying to set mac, retrying: %s",
                            str(e))
                time.sleep(1)
        else:
            # didn't break, we give it one last shot without catching
            device.link.set_address(mac_address)

    def _add_device_to_namespace(self, ip_wrapper, device, namespace):
        namespace_obj = ip_wrapper.ensure_namespace(namespace)
        for i in range(9):
            try:
                namespace_obj.add_device_to_namespace(device)
                break
            except ip_lib.NetworkInterfaceNotFound:
                # NOTE(slaweq): if the exception was NetworkInterfaceNotFound
                # then lets try again, otherwise lets simply raise it as this
                # is some different issue than retry tries to workaround
                LOG.warning("Failed to set interface %s into namespace %s. "
                            "Interface not found, attempt: %s, retrying.",
                            device, namespace, i + 1)
                time.sleep(1)
            except utils.WaitTimeout:
                # NOTE(slaweq): if the exception was WaitTimeout then it means
                # that probably device wasn't found in the desired namespace
                # for 5 seconds, so lets try again too
                LOG.warning("Failed to set interface %s into namespace %s. "
                            "Interface not found in namespace, attempt: %s, "
                            "retrying.", device, namespace, i + 1)
                time.sleep(1)
        else:
            # didn't break, we give it one last shot without catching
            namespace_obj.add_device_to_namespace(device)

    def plug_new(self, network_id, port_id, device_name, mac_address,
                 bridge=None, namespace=None, prefix=None, mtu=None,
                 link_up=True):
        """Plug in the interface."""
        if not bridge:
            bridge = self.conf.OVS.integration_bridge

        self.check_bridge_exists(bridge)

        ip = ip_lib.IPWrapper()
        tap_name = self._get_tap_name(device_name, prefix)

        if self.conf.ovs_use_veth:
            # Create ns_dev in a namespace if one is configured.
            root_dev, ns_dev = ip.add_veth(tap_name,
                                           device_name,
                                           namespace2=namespace)
            root_dev.disable_ipv6()
        else:
            ns_dev = ip.device(device_name)

        internal = not self.conf.ovs_use_veth
        self._ovs_add_port(bridge, tap_name, port_id, mac_address,
                           internal=internal)
        try:
            self._set_device_address(ns_dev, mac_address)
        except Exception:
            LOG.warning("Failed to set mac for interface %s", ns_dev)
            with excutils.save_and_reraise_exception():
                ovs = ovs_lib.OVSBridge(bridge)
                ovs.delete_port(tap_name)

        # Add an interface created by ovs to the namespace.
        if not self.conf.ovs_use_veth and namespace:
            try:
                self._add_device_to_namespace(ip, ns_dev, namespace)
            except (pyroute2_exc.NetlinkError, OSError, RuntimeError):
                # To prevent the namespace failure from blasting OVS, the OVS
                # port creation should be reverted. Possible exceptions:
                # - NetlinkError in case of duplicated interface
                # - OSError in case of corrupted namespace
                # - RuntimeError in case of any issue with interface, like e.g.
                #   Interface not found
                LOG.warning("Failed to plug interface %s into bridge %s, "
                            "cleaning up", device_name, bridge)
                with excutils.save_and_reraise_exception():
                    ovs = ovs_lib.OVSBridge(bridge)
                    ovs.delete_port(tap_name)

        # NOTE(ihrachys): the order here is significant: we must set MTU after
        # the device is moved into a namespace, otherwise OVS bridge does not
        # allow to set MTU that is higher than the least of all device MTUs on
        # the bridge
        if mtu:
            self.set_mtu(device_name, mtu, namespace=namespace, prefix=prefix)
        else:
            LOG.warning("No MTU configured for port %s", port_id)

        if link_up:
            ns_dev.link.set_up()
        if self.conf.ovs_use_veth:
            # ovs-dpdk does not do checksum calculations for veth interface
            # (bug 1832021)
            if self.conf.OVS.datapath_type == ovs_const.OVS_DATAPATH_NETDEV:
                ethtool.offload(ns_dev.name, rx=False, tx=False,
                                namespace=namespace)
            root_dev.link.set_up()

    def unplug(self, device_name, bridge=None, namespace=None, prefix=None):
        """Unplug the interface."""
        if not bridge:
            bridge = self.conf.OVS.integration_bridge

        tap_name = self._get_tap_name(device_name, prefix)
        self.check_bridge_exists(bridge)
        ovs = ovs_lib.OVSBridge(bridge)

        try:
            ovs.delete_port(tap_name)
            if self.conf.ovs_use_veth:
                device = ip_lib.IPDevice(device_name, namespace=namespace)
                device.link.delete()
                LOG.debug("Unplugged interface '%s'", device_name)
        except RuntimeError:
            LOG.error("Failed unplugging interface '%s'",
                      device_name)

    def set_mtu(self, device_name, mtu, namespace=None, prefix=None):
        if self.conf.ovs_use_veth:
            tap_name = self._get_tap_name(device_name, prefix)
            root_dev, ns_dev = _get_veth(
                tap_name, device_name, namespace2=namespace)
            root_dev.link.set_mtu(mtu)
        else:
            ns_dev = ip_lib.IPWrapper(namespace=namespace).device(device_name)
        ns_dev.link.set_mtu(mtu)


class BridgeInterfaceDriver(LinuxInterfaceDriver):
    """Driver for creating bridge interfaces."""

    DEV_NAME_PREFIX = 'ns-'

    def plug_new(self, network_id, port_id, device_name, mac_address,
                 bridge=None, namespace=None, prefix=None, mtu=None,
                 link_up=True):
        """Plugin the interface."""
        ip = ip_lib.IPWrapper()

        # Enable agent to define the prefix
        tap_name = device_name.replace(prefix or self.DEV_NAME_PREFIX,
                                       constants.TAP_DEVICE_PREFIX)
        # Create ns_veth in a namespace if one is configured.
        root_veth, ns_veth = ip.add_veth(tap_name, device_name,
                                         namespace2=namespace)
        root_veth.disable_ipv6()
        ns_veth.link.set_address(mac_address)

        if mtu:
            self.set_mtu(device_name, mtu, namespace=namespace, prefix=prefix)
        else:
            LOG.warning("No MTU configured for port %s", port_id)

        root_veth.link.set_up()
        if link_up:
            ns_veth.link.set_up()

    def unplug(self, device_name, bridge=None, namespace=None, prefix=None):
        """Unplug the interface."""
        device = ip_lib.IPDevice(device_name, namespace=namespace)
        try:
            device.link.delete()
            LOG.debug("Unplugged interface '%s'", device_name)
        except RuntimeError:
            LOG.error("Failed unplugging interface '%s'",
                      device_name)

    def set_mtu(self, device_name, mtu, namespace=None, prefix=None):
        tap_name = device_name.replace(prefix or self.DEV_NAME_PREFIX,
                                       constants.TAP_DEVICE_PREFIX)
        root_dev, ns_dev = _get_veth(
            tap_name, device_name, namespace2=namespace)
        root_dev.link.set_mtu(mtu)
        ns_dev.link.set_mtu(mtu)
