#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_sys import *


def get_slope_at_plt(in_cbtc: bool = True):
    if in_cbtc:
        plt_dict = get_plts_in_cbtc_ter()
    else:
        plt_dict = load_sheet("plt")
    plt_cols_name = get_cols_name("plt")

    dict_plt_slopes = dict()
    for plt_name, plt_values in plt_dict.items():
        min_slope, max_slope = get_slope_plt(plt_values, plt_cols_name)
        dict_plt_slopes[plt_name] = {"min_slope": min_slope, "max_slope": max_slope}

    min_slope = min(plt_slope["min_slope"] for plt_slope in dict_plt_slopes.values())
    max_slope = max(plt_slope["max_slope"] for plt_slope in dict_plt_slopes.values())
    print(f"The maximum slopes in platforms both positive and negative are, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_slope=:.4%}"
          f"\n > for {[plt for plt, plt_values in dict_plt_slopes.items() if plt_values['min_slope'] == min_slope]}"
          f"\n{max_slope=:.4%}"
          f"\n > for {[plt for plt, plt_values in dict_plt_slopes.items() if plt_values['max_slope'] == max_slope]}")
    return dict_plt_slopes


def get_slope_plt(plt, plt_cols_name):
    seg_lim1 = plt[plt_cols_name['I']]
    x_lim1 = float(plt[plt_cols_name['J']])
    seg_lim2 = plt[plt_cols_name['Q']]
    x_lim2 = float(plt[plt_cols_name['R']])
    return get_min_and_max_slopes_on_virtual_seg(seg_lim1, x_lim1, seg_lim2, x_lim2)
