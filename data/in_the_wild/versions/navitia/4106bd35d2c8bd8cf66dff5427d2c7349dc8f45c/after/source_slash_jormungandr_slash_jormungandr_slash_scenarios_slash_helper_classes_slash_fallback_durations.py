# Copyright (c) 2001-2017, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# channel `#navitia` on riot https://riot.im/app/#/room/#navitia:matrix.org
# https://groups.google.com/d/forum/navitia
# www.navitia.io

from __future__ import absolute_import

import jormungandr.street_network.utils
from navitiacommon import response_pb2
from collections import namedtuple, defaultdict
from math import sqrt
from .helper_utils import get_max_fallback_duration
from jormungandr.street_network.street_network import StreetNetworkPathType
from jormungandr import new_relic
from jormungandr.fallback_modes import FallbackModes
import logging
from .helper_utils import timed_logger
import six
from navitiacommon import type_pb2

# The basic element stored in fallback_durations.
# in DurationElement. can be found:
#  - duration(int): time needed to get to the underlying stop point
#  - status(response_pb2.RoutingStatus): is the stop point reached? unreached?
#  - car_park(PtObject): the stop point reached via a car park
#  - car_park_crowfly_duration(int): how long it would take to get to the stop point from the car park
#  - via_access_point(PtObject):  the stop point reached via an access point

# use dataclass when python3.7 is available
DurationElement = namedtuple(
    'DurationElement', ['duration', 'status', 'car_park', 'car_park_crowfly_duration', 'via_access_point']
)


class FallbackDurations:
    """
    A "fallback durations" is a dict of 'stop_points uri' vs 'access duration' calculated from a given departure place
    to a set of arrival stop_points. Fallback duration are passed to kraken later to compute the public transport
    journeys.

    Ex.

    From the given place: 20 Rue Hector Malot Paris
    We'd like to compute how long it'll take to get to
    Arrival stop_points: stop_point:stopA, stop_point:stopB, stop_point:stopC

    The returned dict will look like {'stop_point:stopA': 360, 'stop_point:stopB': 180, 'stop_point:stopC': 60}
    """

    def __init__(
        self,
        future_manager,
        instance,
        requested_place_obj,
        mode,
        proximities_by_crowfly_pool,
        places_free_access,
        max_duration_to_pt,
        request,
        speed_switcher,
        request_id,
        direct_path_type=StreetNetworkPathType.BEGINNING_FALLBACK,
    ):
        """
        :param future_manager: a module that manages the future pool properly
        :param instance: instance of the coverage, all outside services callings pass through it(street network,
                         auto completion)
        :param requested_place_obj: departure protobuffer obj, returned by kraken
        :param mode: access mode
        :param proximities_by_crowfly_pool: arrival stop_points, precomputed by crowfly
        :param places_free_access: places that access time is zero, they're pre-defined
        :param max_duration_to_pt: to limit the time of research
        :param request: original user request
        :param speed_switcher: default speed of different modes
        """
        self._future_manager = future_manager
        self._instance = instance
        self._requested_place_obj = requested_place_obj
        self._mode = mode
        self._proximities_by_crowfly_pool = proximities_by_crowfly_pool
        self._places_free_access = places_free_access
        self._max_duration_to_pt = max_duration_to_pt
        self._request = request
        self._speed_switcher = speed_switcher
        self._value = None
        self._direct_path_type = direct_path_type
        self._streetnetwork_service = instance.get_street_network(mode, request)
        self._logger = logging.getLogger(__name__)
        self._request_id = request_id
        self._async_request()

    def _get_duration(self, resp, place):
        if resp.routing_status == response_pb2.reached:
            return resp.duration
        return self._get_manhattan_duration(place.distance, self._speed_switcher.get(self._mode))

    def _get_manhattan_duration(self, distance, speed):
        return int((distance * sqrt(2)) / speed)

    @new_relic.distributedEvent("routing_matrix", "street_network")
    def _get_street_network_routing_matrix(self, origins, destinations):
        with timed_logger(self._logger, 'routing_matrix_calling_external_service', self._request_id):
            try:
                return self._streetnetwork_service.get_street_network_routing_matrix(
                    self._instance,
                    origins,
                    destinations,
                    self._mode,
                    self._max_duration_to_pt,
                    self._request,
                    self._request_id,
                    **self._speed_switcher
                )
            except Exception as e:
                self._logger.exception("Exception':{}".format(str(e)))
                return None

    def _retrieve_access_points(self, stop_point, access_points_map, places_isochrone):
        if self._direct_path_type == StreetNetworkPathType.BEGINNING_FALLBACK:
            access_points = (ap for ap in stop_point.access_points if ap.is_entrance)
        else:
            access_points = (ap for ap in stop_point.access_points if ap.is_exit)

        for ap in access_points:
            if ap.uri not in access_points_map:
                # every object in place_isochrone has a type of PtObject. We convert the AccessPoint into PtObject
                places_isochrone.append(
                    type_pb2.PtObject(
                        name=ap.name, uri=ap.uri, embedded_type=type_pb2.ACCESS_POINT, access_point=ap
                    )
                )
            access_points_map[ap.uri].append((stop_point.uri, ap.length, ap.traversal_time))

    def _update_fb_durations(self, fb_durations, stop_point, duration, resp):
        if duration < self._max_duration_to_pt:
            fb_durations[stop_point.uri] = DurationElement(duration, resp.routing_status, None, 0, None)

    def _update_fb_durations_from_access_point(
        self, fb_durations, access_point, duration, resp, access_points_map
    ):
        for sp_uri, length, traversal_time in access_points_map[access_point.uri]:
            current_duration = fb_durations[sp_uri].duration if sp_uri in fb_durations else float('inf')
            if (duration + traversal_time) < min(current_duration, self._max_duration_to_pt):
                fb_durations[sp_uri] = DurationElement(
                    duration + traversal_time, resp.routing_status, None, 0, access_point
                )

    def _update_free_access_with_free_radius(self, free_access, proximities_by_crowfly):
        free_radius_distance = None
        if self._direct_path_type == StreetNetworkPathType.BEGINNING_FALLBACK:
            free_radius_distance = self._request.free_radius_from
        elif self._direct_path_type == StreetNetworkPathType.ENDING_FALLBACK:
            free_radius_distance = self._request.free_radius_to
        if free_radius_distance is not None:
            free_access.free_radius.update(
                p.uri for p in proximities_by_crowfly if p.distance < free_radius_distance
            )

    def _get_all_free_access(self, proximities_by_crowfly):
        free_access = self._places_free_access.wait_and_get()
        self._update_free_access_with_free_radius(free_access, proximities_by_crowfly)
        all_free_access = free_access.crowfly | free_access.odt | free_access.free_radius
        return all_free_access

    def _build_places_isochrone(self, proximities_by_crowfly, all_free_access):
        places_isochrone = []
        access_points_map = defaultdict(list)
        if self._mode == FallbackModes.car.name or self._request['_access_points'] is False:
            # if a place is freely accessible, there is no need to compute it's access duration in isochrone
            places_isochrone.extend(p for p in proximities_by_crowfly if p.uri not in all_free_access)
        else:
            access_points_map = defaultdict(list)
            for p in proximities_by_crowfly:
                # if a place is freely accessible, there is no need to compute it's access duration in isochrone

                if p.uri in all_free_access:
                    continue
                # what we are looking to compute, is not the stop_point, but the entrance and exit of a stop_point
                # if any of them are existent
                if not p.stop_point.access_points:
                    places_isochrone.append(p)
                else:
                    self._retrieve_access_points(p.stop_point, access_points_map, places_isochrone)
        # places isochrone are filtered according to different connector. ex. In geovelo, we select solely stop_points
        # are more significant.
        places_isochrone = self._streetnetwork_service.filter_places_isochrone(places_isochrone)
        return places_isochrone, access_points_map

    def _fill_fallback_durations_with_free_access(self, fallback_durations, all_free_access):
        # Since we have already places that have free access, we add them into the result
        from collections import deque

        deque(
            (
                fallback_durations.update({uri: DurationElement(0, response_pb2.reached, None, 0, None)})
                for uri in all_free_access
            ),
            maxlen=1,
        )

    def _fill_fallback_durations_with_manhattan(self, fallback_durations, places_isochrone):
        for sp in places_isochrone:
            fallback_durations[sp.uri] = DurationElement(
                self._get_manhattan_duration(sp.distance, self._speed_switcher.get(self._mode)),
                response_pb2.reached,
                None,
                0,
                None,
            )

    def _determine_origins_and_destinations(self, center_isochrone, places_isochrone):
        if self._direct_path_type == StreetNetworkPathType.BEGINNING_FALLBACK:
            origins = [center_isochrone]
            destinations = places_isochrone
        else:
            origins = places_isochrone
            destinations = [center_isochrone]

        return origins, destinations

    def _update_fallback_durations_for_car(self, sn_routing_matrix, places_isochrone, fallback_durations):
        routing_response = (
            r for r in sn_routing_matrix.rows[0].routing_response if r.routing_status != response_pb2.unreached
        )
        # the element in routing_response are ranged in the same order of element in places_isochrones
        for pos, r in enumerate(routing_response):
            car_park = places_isochrone[pos]
            duration = self._get_duration(r, car_park)
            # if the mode is car, we need to find where to park the car :)
            for sp_nearby in car_park.stop_points_nearby:
                duration_to_stop_point = self._get_manhattan_duration(
                    sp_nearby.distance, self._speed_switcher.get('walking')
                )
                durations_sum = duration + duration_to_stop_point + self._request.get('_car_park_duration')
                if durations_sum < min(
                    self._max_duration_to_pt,
                    fallback_durations.get(
                        sp_nearby.uri, DurationElement(float('inf'), None, None, None, None)
                    ).duration,
                ):
                    fallback_durations[sp_nearby.uri] = DurationElement(
                        durations_sum, response_pb2.reached, car_park, duration_to_stop_point, None
                    )

    def _update_fallback_durations_for_stop_points_and_access_points(
        self, sn_routing_matrix, places_isochrone, access_points_map, fallback_durations
    ):
        routing_response = (
            r for r in sn_routing_matrix.rows[0].routing_response if r.routing_status != response_pb2.unreached
        )

        def is_stop_point(pt_object):
            return isinstance(pt_object, type_pb2.PtObject) and pt_object.embedded_type == type_pb2.STOP_POINT

        def is_access_point(pt_object):
            return isinstance(pt_object, type_pb2.PtObject) and pt_object.embedded_type == type_pb2.ACCESS_POINT

        for pos, r in enumerate(routing_response):
            duration = self._get_duration(r, places_isochrone[pos])
            pt_object = places_isochrone[pos]
            # in this case, the pt_object can be either a stop point or an access point
            if is_stop_point(pt_object):
                self._update_fb_durations(fallback_durations, pt_object, duration, r)

            elif is_access_point(pt_object):
                self._update_fb_durations_from_access_point(
                    fallback_durations, pt_object, duration, r, access_points_map
                )

    def _do_request(self):
        logger = logging.getLogger(__name__)
        logger.debug("requesting fallback durations from %s by %s", self._requested_place_obj.uri, self._mode)

        # When max_duration_to_pt is 0, there is no need to compute the fallback to pt, except if place is a
        # stop_point or a stop_area
        center_isochrone = self._requested_place_obj
        proximities_by_crowfly = self._proximities_by_crowfly_pool.wait_and_get(self._mode)
        all_free_access = self._get_all_free_access(proximities_by_crowfly)
        places_isochrone, access_points_map = self._build_places_isochrone(
            proximities_by_crowfly, all_free_access
        )

        # the result to be returned, which is a map of stop_points.uri vs DurationElement
        fallback_durations = defaultdict(lambda: DurationElement(float('inf'), None, None, 0, None))

        # Since we have already places that have free access, we add them into the fallback_durations
        self._fill_fallback_durations_with_free_access(fallback_durations, all_free_access)

        # There are two cases that places_isochrone maybe empty:
        # 1. The duration of direct_path is very small that we cannot find any proximities by crowfly
        # 2. All proximities by crowfly are free access
        if not places_isochrone:
            return fallback_durations

        if self._max_duration_to_pt == 0:
            logger.debug("max_duration_to_pt equals to 0")

            # When max_duration_to_pt is 0, we can get on the public transport ONLY if the place is a stop_point
            if self._instance.georef.get_stop_points_from_uri(center_isochrone.uri, self._request_id):
                return {center_isochrone.uri: DurationElement(0, response_pb2.reached, None, 0, None)}
            else:
                return fallback_durations

        # based on the fallback type, we choose the origins and destinations
        # if fallback type is beginning, then the street network service should compute a matrix of "one to many"
        # otherwise, the street network service should compute a matrix of "many to one"
        origins, destinations = self._determine_origins_and_destinations(center_isochrone, places_isochrone)

        # Launch the computation of fall back durations
        sn_routing_matrix = self._get_street_network_routing_matrix(
            self._streetnetwork_service, origins, destinations
        )

        # In case where none of places in isochrone are reachable, we consider that something goes awry in the
        # computation we fill the fallback_duration with manhattan distance for every requested place and return it
        if (
            not sn_routing_matrix
            or not len(sn_routing_matrix.rows)
            or not len(sn_routing_matrix.rows[0].routing_response)
        ):
            logger.debug("no fallback durations found from %s by %s", self._requested_place_obj.uri, self._mode)
            self._fill_fallback_durations_with_manhattan(fallback_durations, places_isochrone)
            return fallback_durations

        if self._mode == FallbackModes.car.name:
            # note that when requested mode is car, the place in the isochrone is a car park
            self._update_fallback_durations_for_car(sn_routing_matrix, places_isochrone, fallback_durations)
        else:
            # otherwise, the place in the isochrone may be either stop_point or access_point
            self._update_fallback_durations_for_stop_points_and_access_points(
                sn_routing_matrix, places_isochrone, access_points_map, fallback_durations
            )

        # We update the fallback duration matrix if the requested origin/destination is also
        # present in the fallback duration matrix, which means from stop_point_1 to itself, it takes 0 second
        # Note that we consider, in this case, the via access_point is the stop_point itself.
        # Ex:
        #                stop_point1   stop_point2  stop_point3
        # stop_point_1         0(s)       ...          ...
        if center_isochrone.uri in fallback_durations:
            fallback_durations[center_isochrone.uri] = DurationElement(0, response_pb2.reached, None, 0, None)

        logger.debug("finish fallback durations from %s by %s", self._requested_place_obj.uri, self._mode)

        return fallback_durations

    def _async_request(self):
        self._value = self._future_manager.create_future(self._do_request)

    def wait_and_get(self):
        with timed_logger(self._logger, 'waiting_for_routing_matrix', self._request_id):
            return self._value.wait_and_get() if self._value else None


class FallbackDurationsPool(dict):
    """
    A fallback durations pool is set of "fallback durations" grouped by mode.
    """

    def __init__(
        self,
        future_manager,
        instance,
        requested_place_obj,
        modes,
        proximities_by_crowfly_pool,
        places_free_access,
        direct_paths_by_mode,
        request,
        request_id,
        direct_path_type=StreetNetworkPathType.BEGINNING_FALLBACK,
    ):
        super(FallbackDurationsPool, self).__init__()
        self._future_manager = future_manager
        self._instance = instance
        self._requested_place_obj = requested_place_obj
        self._modes = set(modes)
        self._proximities_by_crowfly_pool = proximities_by_crowfly_pool
        self._places_free_access = places_free_access
        self._direct_paths_by_mode = direct_paths_by_mode
        self._request = request
        self._direct_path_type = direct_path_type
        self._speed_switcher = jormungandr.street_network.utils.make_speed_switcher(request)

        self._value = {}
        self._request_id = request_id

        self._overrided_uri_map = defaultdict(dict)
        self._async_request()

    @property
    def _overriding_mode_map(self):
        """
        This map is used to storing the overriding modes of a give mode.
        the function get_overriding_mode may be modified later to implement more complex business logic
        :return:
        """
        res = {}
        if self._direct_path_type == StreetNetworkPathType.BEGINNING_FALLBACK:
            fallback_modes = self._request['origin_mode']
        else:
            fallback_modes = self._request['destination_mode']

        for mode in self._modes:
            overriding_modes = jormungandr.utils.get_overriding_mode(mode, fallback_modes)
            if overriding_modes:
                res[mode] = overriding_modes
        return res

    def _async_request(self):
        for mode in self._modes:
            max_fallback_duration = get_max_fallback_duration(
                self._request, mode, self._direct_paths_by_mode.get(mode)
            )
            fallback_durations = FallbackDurations(
                self._future_manager,
                self._instance,
                self._requested_place_obj,
                mode,
                self._proximities_by_crowfly_pool,
                self._places_free_access,
                max_fallback_duration,
                self._request,
                self._speed_switcher,
                self._request_id,
                self._direct_path_type,
            )
            self._value[mode] = fallback_durations

    def wait_and_get(self, mode):
        f = self._value.get(mode)
        return f.wait_and_get() if f else None

    def is_empty(self):
        return next((False for _, v in self._value.items() if v.wait_and_get()), True)

    def get_best_fallback_durations(self, main_mode):
        main_fb = self.wait_and_get(main_mode)
        res = {}
        overriding_modes = self._overriding_mode_map.get(main_mode, [])
        overriding_fbs = [
            (mode, self.wait_and_get(mode)) for mode in overriding_modes if self.wait_and_get(mode)
        ]

        for uri, duration_item in six.iteritems(main_fb):
            duration = duration_item.duration
            # if the duration of the main_mode is strictly smaller than all other mode, we keep the uri in the final res
            # else the fallback duration is replaced by the smallest duration among all modes.
            mode_durations = [(main_mode, duration)] + [
                (mode, fb.get(uri).duration) for mode, fb in overriding_fbs if fb.get(uri)
            ]
            best_mode, best_duration = min(mode_durations, key=lambda o: o[1])
            if best_mode != main_mode:
                self._overrided_uri_map[main_mode][uri] = best_mode
            res[uri] = best_duration
        return res

    def get_real_mode(self, main_mode, uri):
        return self._overrided_uri_map.get(main_mode, {}).get(uri, None) or main_mode
