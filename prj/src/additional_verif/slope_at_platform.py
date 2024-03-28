#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_get_cbtc_territory import *
from ..dc_sys_sheet_utils import *


__all__ = ["get_slope_at_plt"]


def get_slope_at_plt(in_cbtc: bool = True):
    if in_cbtc:
        plt_dict = get_objects_in_cbtc_ter(DCSYS.Quai)
    else:
        plt_dict = load_sheet(DCSYS.Quai)

    dict_plt_slopes = dict()
    for plt_name, plt_value in plt_dict.items():
        min_slope, max_slope = get_slope_plt(plt_value)
        dict_plt_slopes[plt_name] = {"min_slope": min_slope, "max_slope": max_slope}

    min_slope = min(plt_slope["min_slope"] for plt_slope in dict_plt_slopes.values())
    max_slope = max(plt_slope["max_slope"] for plt_slope in dict_plt_slopes.values())
    print(f"\nThe maximum slopes in platforms both positive and negative are, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_slope=:.4%}"
          f"\n > for {[plt for plt, plt_value in dict_plt_slopes.items() if plt_value['min_slope'] == min_slope]}"
          f"\n{max_slope=:.4%}"
          f"\n > for {[plt for plt, plt_value in dict_plt_slopes.items() if plt_value['max_slope'] == max_slope]}\n")
    dict_plt_slopes = {key: dict_plt_slopes[key] for key in sorted(dict_plt_slopes.keys(),
                       key=lambda x: max(abs(dict_plt_slopes[x]["min_slope"]), dict_plt_slopes[x]["max_slope"]),
                       reverse=True)}
    return dict_plt_slopes


def get_slope_plt(plt: dict) -> tuple[float, float]:
    seg_lim1, seg_lim2 = get_dc_sys_value(plt, DCSYS.Quai.ExtremiteDuQuai.Seg)
    x_lim1, x_lim2 = get_dc_sys_value(plt, DCSYS.Quai.ExtremiteDuQuai.X)
    return get_min_and_max_slopes_on_virtual_seg(seg_lim1, x_lim1, seg_lim2, x_lim2)
