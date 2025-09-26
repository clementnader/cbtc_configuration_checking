#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ....dc_sys_sheet_utils.switch_utils import *
from ....dc_sys_draw_path import *
from ....dc_par import *



__all__ = ["extremite_secteur"]


def extremite_secteur():
    # EXTREMITE_SECTEUR
    variables = dict()
    tracking_delocalization_threshold = get_param_value("tracking_delocalization_threshold", variables)
    train_max_length = get_param_value("train_max_length", variables)
    limit_value = tracking_delocalization_threshold + train_max_length
    print_sub_variables(variables)
    print(f"limit is {limit_value}\n")
    i = 1
    zone_limits = get_zone_limits(DCSYS.PAS, "ZC_01")
    for seg1 in get_all_segments_in_zone(DCSYS.PAS, "ZC_01"):
        too_far_away = True
        for lim_seg, lim_x, lim_direction in zone_limits:
            dist_to_lim = get_dist_downstream(lim_seg, lim_x, seg1, None,
                                              downstream=lim_direction == Direction.CROISSANT)
            if dist_to_lim is not None and dist_to_lim < limit_value:
                too_far_away = False
                break
        if too_far_away:
            continue
        for seg2 in get_objects_list(DCSYS.Seg):
            if seg2 in get_segments_within_zone(DCSYS.PAS, "ZC_01"):
                continue
            too_far_away = True
            for lim_seg, lim_x, lim_direction in zone_limits:
                dist_to_lim = get_dist_downstream(lim_seg, lim_x, seg2, None,
                                                  downstream=lim_direction != Direction.CROISSANT)
                if dist_to_lim is not None and dist_to_lim < limit_value:
                    too_far_away = False
                    break
            if too_far_away:
                continue
            # TODO if the part of seg2 out of ZC is out of CBTC Territory, no need to consider this segment
            list_of_paths = get_list_of_paths(seg1, seg2)
            for _, path in list_of_paths:
                path_len = get_path_len(path[1:-1])
                if path_len > limit_value:
                    continue
                sw_on_path = get_switch_on_path(path)
                sw_in_zc_on_path = [(sw, pos) for sw, pos in sw_on_path if
                                    "ZC_01" in get_zones_on_object(DCSYS.PAS, DCSYS.Aig, sw)]
                extra_sw = [sw for sw in sw_on_path if sw not in sw_in_zc_on_path]
                print(i, Color.light_blue, seg1, seg2,
                      f"{Color.red}Too far away!!{Color.reset}" if path_len > limit_value else f"{Color.reset}OK")
                print("\t", ", ".join(path), " -> ", path_len)
                print("\t", sw_in_zc_on_path, f"(switch on path out of ZC_01: {extra_sw})" if extra_sw else "")
                i += 1
