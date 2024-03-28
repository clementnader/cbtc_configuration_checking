#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_get_cbtc_territory import *
from ..dc_sys_sheet_utils.slope_utils import get_min_and_max_slopes_on_virtual_seg
from ..dc_par import *


__all__ = ["get_slope_at_overshoot_recovery_area"]


def get_slope_at_overshoot_recovery_area(in_cbtc: bool = True):
    overshoot_recovery_dist = get_param_value("overshoot_recovery_dist")
    overshoot_recovery_stopping_max_dist = get_param_value("overshoot_recovery_stopping_max_dist")
    overshoot_recovery_max_uncertainty = get_param_value("overshoot_recovery_max_uncertainty")
    overshoot_recovery_area_distance = (overshoot_recovery_dist + overshoot_recovery_stopping_max_dist
                                        + overshoot_recovery_max_uncertainty)
    if in_cbtc:
        plt_dict = get_objects_in_cbtc_ter(DCSYS.Quai)
    else:
        plt_dict = load_sheet(DCSYS.Quai)

    dict_plt_slopes = dict()
    for plt_name, plt_value in plt_dict.items():
        min_slope, max_slope = get_slope_plt_ovsht(plt_value, overshoot_recovery_area_distance)
        dict_plt_slopes[plt_name] = {"min_slope": min_slope, "max_slope": max_slope}

    min_slope = min(plt_slope["min_slope"] for plt_slope in dict_plt_slopes.values())
    max_slope = max(plt_slope["max_slope"] for plt_slope in dict_plt_slopes.values())
    print(f"\nThe maximum slopes in platforms overshoot recovery areas both positive and negative are, "
          f"{print_in_cbtc(in_cbtc)}:"
          f"\n{min_slope=:.4%}"
          f"\n > for {[plt for plt, plt_value in dict_plt_slopes.items() if plt_value['min_slope'] == min_slope]}"
          f"\n{max_slope=:.4%}"
          f"\n > for {[plt for plt, plt_value in dict_plt_slopes.items() if plt_value['max_slope'] == max_slope]}\n")
    dict_plt_slopes = {key: dict_plt_slopes[key] for key in sorted(dict_plt_slopes.keys(),
                       key=lambda x: max(abs(dict_plt_slopes[x]["min_slope"]), dict_plt_slopes[x]["max_slope"]),
                       reverse=True)}
    return dict_plt_slopes


def get_slope_plt_ovsht(plt: dict, overshoot_recovery_area_distance: float) -> tuple[float, float]:
    track_plt_lim1, track_plt_lim2 = get_dc_sys_value(plt, DCSYS.Quai.ExtremiteDuQuai.Voie)
    kp_plt_lim1, kp_plt_lim2 = get_dc_sys_value(plt, DCSYS.Quai.ExtremiteDuQuai.Pk)

    kp_lim1 = kp_plt_lim1 - overshoot_recovery_area_distance
    kp_lim2 = kp_plt_lim2 + overshoot_recovery_area_distance
    seg_lim1, x_lim1 = from_kp_to_seg_offset(track_plt_lim1, kp_lim1)
    seg_lim2, x_lim2 = from_kp_to_seg_offset(track_plt_lim2, kp_lim2)
    min_slope, max_slope = get_min_and_max_slopes_on_virtual_seg(seg_lim1, x_lim1, seg_lim2, x_lim2)

    kp_lim1 = kp_plt_lim1 + overshoot_recovery_area_distance
    kp_lim2 = kp_plt_lim2 - overshoot_recovery_area_distance
    seg_lim1, x_lim1 = from_kp_to_seg_offset(track_plt_lim1, kp_lim1)
    seg_lim2, x_lim2 = from_kp_to_seg_offset(track_plt_lim2, kp_lim2)
    min_slope2, max_slope2 = get_min_and_max_slopes_on_virtual_seg(seg_lim1, x_lim1, seg_lim2, x_lim2)

    return min(min_slope, min_slope2), max(max_slope, max_slope2)
