#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...fouling_points import fouling_points
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_sheet_utils import *


def get_fouling_point_seg_offset(sw_name, fouling_point_kp, heel_direction):
    sw_dict = load_sheet(DCSYS.Aig)
    seg_dict = load_sheet(DCSYS.Seg)
    heel_directions = ("left_heel", "right_heel")
    attr = DCSYS.Aig.SegmentTg if heel_direction == heel_directions[0] \
        else DCSYS.Aig.SegmentTd if heel_direction == heel_directions[1] \
        else None
    if attr is None:
        raise Exception(f"The heel direction given {heel_direction} does not correspond to expected {heel_directions}.")
    heel_seg = get_dc_sys_value(sw_dict[sw_name], attr)
    seg_origin_kp = get_dc_sys_value(seg_dict[heel_seg], DCSYS.Seg.Origine)
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
