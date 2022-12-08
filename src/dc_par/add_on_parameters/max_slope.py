#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys_pkg import *


def get_max_slope_within_cbtc_ter():
    slope_dict = load_sheet("slope")
    slope_cols_name = get_cols_name("slope")

    dict_slopes_in_cbtc_ter = dict()
    for slope in slope_dict:
        slope_seg = slope_dict[slope][slope_cols_name['B']]
        slope_x = float(slope_dict[slope][slope_cols_name['C']])
        if is_segment_in_cbtc_ter(slope_seg, slope_x):
            dict_slopes_in_cbtc_ter[slope] = slope_dict[slope]

    min_slope = min(float(dict_slopes_in_cbtc_ter[slope][slope_cols_name['A']]) for slope in dict_slopes_in_cbtc_ter)
    max_slope = max(float(dict_slopes_in_cbtc_ter[slope][slope_cols_name['A']]) for slope in dict_slopes_in_cbtc_ter)
    list_min_slopes = [dict_slopes_in_cbtc_ter[slope] for slope in dict_slopes_in_cbtc_ter
                       if float(dict_slopes_in_cbtc_ter[slope][slope_cols_name['A']]) == min_slope]
    list_max_slopes = [dict_slopes_in_cbtc_ter[slope] for slope in dict_slopes_in_cbtc_ter
                       if float(dict_slopes_in_cbtc_ter[slope][slope_cols_name['A']]) == max_slope]
    print(f"\nMax slopes in CBTC Territory:"
          f"\n{min_slope=:.4%}"
          f"\nfor {list_min_slopes}"
          f"\n{max_slope=:.4%}"
          f"\nfor {list_max_slopes}")
    return dict_slopes_in_cbtc_ter


def get_max_slope_on_the_full_line():
    slope_dict = load_sheet("slope")
    slope_cols_name = get_cols_name("slope")

    min_slope = min(float(slope_dict[slope][slope_cols_name['A']]) for slope in slope_dict)
    max_slope = max(float(slope_dict[slope][slope_cols_name['A']]) for slope in slope_dict)
    list_min_slopes = [slope_dict[slope] for slope in slope_dict
                       if float(slope_dict[slope][slope_cols_name['A']]) == min_slope]
    list_max_slopes = [slope_dict[slope] for slope in slope_dict
                       if float(slope_dict[slope][slope_cols_name['A']]) == max_slope]
    print(f"\nMax slopes on the full line:"
          f"\n{min_slope=:.4%}"
          f"\nfor {list_min_slopes}"
          f"\n{max_slope=:.4%}"
          f"\nfor {list_max_slopes}")
    return slope_dict



