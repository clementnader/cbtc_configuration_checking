#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_get_cbtc_territory import *
from ..dc_sys_sheet_utils.platform_utils import *
from ..dc_sys_sheet_utils.slope_utils import *
from ..dc_par import *


__all__ = ["get_min_and_max_slope_at_all_overshoot_recovery_areas", "get_slope_at_plt_ovsht_area"]


def get_min_and_max_slope_at_all_overshoot_recovery_areas(in_cbtc: bool = False):
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
    for plt_name in plt_dict:
        min_slope, max_slope = get_slope_at_plt_ovsht_area(plt_name, overshoot_recovery_area_distance)
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


def get_slope_at_plt_ovsht_area(plt_name: str, overshoot_recovery_area_distance: float) -> tuple[float, float]:
    plt_start_limit, plt_end_limit = get_platform_start_and_end_limits(plt_name)

    plt_start_seg, plt_start_x, plt_start_direction = plt_start_limit  # start limit is in direction CROISSANT
    plt_end_seg, plt_end_x, plt_end_direction = plt_end_limit  # end limit is in direction DECROISSANT

    start_seg, start_x = get_correct_seg_offset(plt_start_seg, plt_start_x - overshoot_recovery_area_distance)
    end_seg, end_x = get_correct_seg_offset(plt_end_seg, plt_end_x + overshoot_recovery_area_distance)

    zone_limits = [(start_seg, start_x, plt_start_direction), (end_seg, end_x, plt_end_direction)]

    min_slope, max_slope = get_min_and_max_slopes_in_zone_limits(zone_limits)

    return min_slope, max_slope
