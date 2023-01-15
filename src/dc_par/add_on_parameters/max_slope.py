#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def get_max_slope(in_cbtc: bool = True):
    if in_cbtc:
        slope_dict = get_slopes_in_cbtc_ter()
    else:
        slope_dict = load_sheet("slope")
    slope_cols_name = get_cols_name("slope")

    min_slope = min(float(slope_values[slope_cols_name['A']]) for slope_values in slope_dict.values())
    max_slope = max(float(slope_values[slope_cols_name['A']]) for slope_values in slope_dict.values())
    list_min_slopes = [slope_values for slope_values in slope_dict.values()
                       if float(slope_values[slope_cols_name['A']]) == min_slope]
    list_max_slopes = [slope_values for slope_values in slope_dict.values()
                       if float(slope_values[slope_cols_name['A']]) == max_slope]
    print(f"The maximum slopes both positive and negative are, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_slope=:.4%}"
          f"\n > for {list_min_slopes}"
          f"\n{max_slope=:.4%}"
          f"\n > for {list_max_slopes}")
    return slope_dict
