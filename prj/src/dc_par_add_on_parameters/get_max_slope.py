#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_get_cbtc_territory import *


__all__ = ["get_max_slope"]


def get_max_slope(in_cbtc: bool = True, verbose: bool = True):
    if in_cbtc:
        slope_dict = get_objects_in_cbtc_ter(DCSYS.Profil)
    else:
        slope_dict = load_sheet(DCSYS.Profil)

    min_slope = min(float(get_dc_sys_value(slope_value, DCSYS.Profil.Pente)) for slope_value in slope_dict.values())
    max_slope = max(float(get_dc_sys_value(slope_value, DCSYS.Profil.Pente)) for slope_value in slope_dict.values())

    if verbose:
        list_min_slopes = [slope_value for slope_value in slope_dict.values()
                           if float(get_dc_sys_value(slope_value, DCSYS.Profil.Pente)) == min_slope]
        list_max_slopes = [slope_value for slope_value in slope_dict.values()
                           if float(get_dc_sys_value(slope_value, DCSYS.Profil.Pente)) == max_slope]
        print(f"The maximum slopes both positive and negative are, {print_in_cbtc(in_cbtc)}:"
              f"\n{min_slope=:.4%}"
              f"\n > for {list_min_slopes}"
              f"\n{max_slope=:.4%}"
              f"\n > for {list_max_slopes}")
    return min_slope, max_slope
