#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ..load_database import *
from .platform_utils import *


__all__ = ["get_traffic_stops_in_cbtc_ter"]


def get_traffic_stops_in_cbtc_ter():
    stop_dict = load_sheet(DCSYS.Traffic_Stop)
    platforms_in_cbtc = get_platforms_in_cbtc_ter()

    within_cbtc_stop_dict = dict()
    for stop_name, stop_value in stop_dict.items():
        rel_plts_in_cbtc_ter = list()
        for rel_plt_name in get_dc_sys_value(stop_value, DCSYS.Traffic_Stop.PlatformList.Name):
            rel_plts_in_cbtc_ter.append(rel_plt_name in platforms_in_cbtc)
        if all(rel_plt_in_cbtc_ter is True for rel_plt_in_cbtc_ter in rel_plts_in_cbtc_ter):
            within_cbtc_stop_dict[stop_name] = stop_value
    return within_cbtc_stop_dict
