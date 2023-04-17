#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...fouling_points import fouling_points
from ..dc_sys_utils import *
from ..load_database.load_sheets import load_sheet, get_cols_name


def get_fouling_point_seg_offset(sw_name, fouling_point_kp, heel_direction):
    sw_dict = load_sheet("sw")
    sw_cols_name = get_cols_name("sw")

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    heel_directions = ("left_heel", "right_heel")
    col = 'D' if heel_direction == heel_directions[0] else 'C' if heel_direction == heel_directions[1] else None
    if col is None:
        raise Exception(f"The heel direction given {heel_direction} does not correspond to expected {heel_directions}.")
    heel_seg = sw_dict[sw_name][sw_cols_name[col]]
    seg_origin_kp = seg_dict[heel_seg][seg_cols_name['E']]
    x = fouling_point_kp - seg_origin_kp
    return get_correct_seg_offset(heel_seg, x)


def fouling_points_associated_to_sw(sw_name):
    fp = fouling_points.get(sw_name)
    if fp is None:
        return {}
    heel_directions = ("left_heel", "right_heel")
    fp_dict = dict()
    for heel_direction in heel_directions:
        fp_kp = fp.get(heel_direction)
        if fp_kp is None or fp_kp == 0:
            fp_seg, fp_x = None, None
        else:
            fp_seg, fp_x = get_fouling_point_seg_offset(sw_name, fp_kp, heel_direction)
        fp_dict[heel_direction] = (fp_seg, fp_x)
    return fp_dict
