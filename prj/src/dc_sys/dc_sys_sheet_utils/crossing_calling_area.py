#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_common_utils import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


__all__ = ["get_crossing_calling_areas_in_cbtc_ter"]


def get_crossing_calling_areas_in_cbtc_ter():
    cross_call_dict = load_sheet(DCSYS.Crossing_Calling_Area)

    within_cbtc_cross_call_dict = dict()
    for cross_call_name, cross_call_value in cross_call_dict.items():
        limits_in_cbtc_ter = list()
        for seg, x in get_obj_position(DCSYS.Crossing_Calling_Area, cross_call_name):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if (any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter)
                and all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter)):
            within_cbtc_cross_call_dict[cross_call_name] = cross_call_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"Crossing Calling Area {cross_call_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_cross_call_dict[cross_call_name] = cross_call_value
    return within_cbtc_cross_call_dict
