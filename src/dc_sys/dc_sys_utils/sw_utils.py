#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .seg_utils import *


def is_sw_point_seg_upstream(sw, sw_cols_name, seg_dict, seg_cols_name):
    """Returns True if the point segment of the switch is upstream of the two heels segments,
    returns False if it is downstream,
    raises an error if it is neither the first nor the second."""
    point_seg = sw[sw_cols_name['B']]
    right_heel = sw[sw_cols_name['C']]
    left_heel = sw[sw_cols_name['D']]
    other_segs_are_downstream = (is_seg_downstream(point_seg, other_seg, seg_dict, seg_cols_name)
                                 for other_seg in (right_heel, left_heel))
    other_segs_are_upstream = (is_seg_downstream(other_seg, point_seg, seg_dict, seg_cols_name)
                               for other_seg in (right_heel, left_heel))
    if all(other_segs_are_downstream):
        return True
    if all(other_segs_are_upstream):
        return False
    raise Exception("The point segment is not found upstream or downstream of the heels.")


def give_sw_kp_pos(sw, sw_cols_name, seg_dict, seg_cols_name):
    """Returns the position of the switch with the track and the KP value. """
    point_seg = sw[sw_cols_name['B']]
    upstream = is_sw_point_seg_upstream(sw, sw_cols_name, seg_dict, seg_cols_name)
    track = seg_dict[point_seg][seg_cols_name['D']]
    kp_col = 'F' if upstream else 'E'
    kp = float(seg_dict[point_seg][seg_cols_name[kp_col]])
    return track, kp
