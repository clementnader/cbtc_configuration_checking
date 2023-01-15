#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .segments_utils import *
from .links_utils import is_seg_downstream
from .cbtc_territory_utils import is_point_in_cbtc_ter  # , is_seg_in_cbtc_ter_limits
from ..load_database.load_sheets import load_sheet, get_cols_name
from ...colors_pkg import *


def get_sws_in_cbtc_ter():
    sw_dict = load_sheet("sw")
    sw_cols_name = get_cols_name("sw")

    within_cbtc_sw_dict = dict()
    for sw_name, sw_values in sw_dict.items():
        seg, x = give_sw_pos(sw_values, sw_cols_name)
        if is_point_in_cbtc_ter(seg, x) is not False:
            within_cbtc_sw_dict[sw_name] = sw_values
        if is_point_in_cbtc_ter(seg, x) is None:
            print_warning(f"Switch {sw_name} is on a limit of CBTC Territory. "
                          f"It is still taken into account.")
        # if any(is_seg_in_cbtc_ter_limits(sw_values[sw_cols_name[col]]) for col in ('B', 'C', 'D')):
        #     print_warning(f"Switch {sw_name} has its segments on a limit of CBTC Territory. "
        #                   f"It is still taken into account.")
    return within_cbtc_sw_dict


def is_sw_point_seg_upstream(sw, sw_cols_name):
    """Returns True if the point segment of the switch is upstream of the two heels segments,
    returns False if it is downstream,
    raises an error if it is neither the first nor the second."""
    point_seg = sw[sw_cols_name['B']]
    right_heel = sw[sw_cols_name['C']]
    left_heel = sw[sw_cols_name['D']]
    other_segs_are_downstream = (is_seg_downstream(point_seg, other_seg) for other_seg in (right_heel, left_heel))
    other_segs_are_upstream = (is_seg_downstream(other_seg, point_seg) for other_seg in (right_heel, left_heel))
    if all(other_segs_are_downstream):
        return True
    if all(other_segs_are_upstream):
        return False
    raise Exception("The point segment is not found upstream or downstream of the heels.")


def give_sw_pos(sw, sw_cols_name):
    """Returns the position of the switch with the seg and offset. """
    point_seg = sw[sw_cols_name['B']]
    upstream = is_sw_point_seg_upstream(sw, sw_cols_name)
    len_seg = get_len_seg(point_seg)
    x = len_seg if upstream else 0
    return point_seg, x


def give_sw_kp_pos(sw, sw_cols_name, seg_dict, seg_cols_name):
    """Returns the position of the switch with the track and the KP value. """
    point_seg = sw[sw_cols_name['B']]
    upstream = is_sw_point_seg_upstream(sw, sw_cols_name)
    track = seg_dict[point_seg][seg_cols_name['D']]
    kp_col = 'F' if upstream else 'E'
    kp = float(seg_dict[point_seg][seg_cols_name[kp_col]])
    return track, kp
