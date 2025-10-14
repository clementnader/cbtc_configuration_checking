#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *


__all__ = ["get_all_traffic_stops", "get_traffic_stop_value", "get_traffic_stop_platform_list"]


def get_all_traffic_stops() -> list[str]:
    traffic_stop_dict = load_sheet(DCSYS.Traffic_Stop)
    list_traffic_stop = list()
    for traffic_stop_subset in traffic_stop_dict.values():
        traffic_stop_name = get_database_value(traffic_stop_subset, DCSYS.Traffic_Stop.Name)
        if traffic_stop_name not in list_traffic_stop:
            list_traffic_stop.append(traffic_stop_name)
    return list_traffic_stop


def get_traffic_stop_value(traffic_stop_name: str) -> dict[str, Any]:
    traffic_stop_dict = load_sheet(DCSYS.Traffic_Stop)
    traffic_stop_subset_value = [traffic_stop for traffic_stop in traffic_stop_dict.values()
                                 if get_database_value(traffic_stop, DCSYS.Traffic_Stop.Name) == traffic_stop_name][0]
    # When the Traffic Stop is split between multiple subsets for a matter of maximal number of platforms,
    # the information concerning the Traffic Stop is on the first subset.
    traffic_stop_subset_value[get_dc_sys_attribute_name(DCSYS.Traffic_Stop.PlatformList)][
        get_dc_sys_attribute_name(DCSYS.Traffic_Stop.PlatformList.Name)
    ] = get_traffic_stop_platform_list(traffic_stop_name)
    return traffic_stop_subset_value


def get_traffic_stop_platform_list(traffic_stop_name: str) -> list[str]:
    traffic_stop_dict = load_sheet(DCSYS.Traffic_Stop)
    traffic_stop_subset_value_list = [traffic_stop for traffic_stop in traffic_stop_dict.values()
                                      if get_database_value(traffic_stop, DCSYS.Traffic_Stop.Name) == traffic_stop_name]
    # Return the list of all platforms on all subsets
    return [plt for subset_value in traffic_stop_subset_value_list
            for plt in get_database_value(subset_value, DCSYS.Traffic_Stop.PlatformList.Name)]
