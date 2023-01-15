#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_sys import *
from ..dc_par import *


def r_cdv_5():
    at_rollback_dist = get_param_value("at_rollback_dist")
    mtc_rollback_dist = get_param_value("mtc_rollback_dist")
    at_deshunt_max_dist = get_param_value("at_deshunt_max_dist")

    print(f"{at_rollback_dist=}")
    print(f"{mtc_rollback_dist=}")
    print(f"{at_deshunt_max_dist=}")
    return


def get_fouling_point_seg_offset(sw_name, fouling_point_kp, dir_heel):
    sw_dict = load_sheet("sw")
    sw_cols_name = get_cols_name("sw")

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    col = 'D' if dir_heel == "left_heel" else 'B'
    heel_seg = sw_dict[sw_name][sw_cols_name[col]]
    track = get_seg_track(heel_seg)
    origin_kp = seg_dict[heel_seg][seg_cols_name['E']]
    x = fouling_point_kp - origin_kp
    return track, x
