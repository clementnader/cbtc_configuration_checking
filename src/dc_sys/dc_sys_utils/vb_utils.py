#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .seg_utils import *
from .dist_utils import get_dist


def give_point_seg_vb(vb_limits, seg_dict, seg_cols_name):
    """ Give the point segment corresponding to the switch associated to the VB. """
    for lim1 in vb_limits:
        seg1 = lim1["Seg"]
        other_segs_are_downstream = (is_seg_downstream(seg1, lim2["Seg"], seg_dict, seg_cols_name)
                                     for lim2 in vb_limits if lim2 != lim1)
        other_segs_are_upstream = (is_seg_downstream(lim2["Seg"], seg1, seg_dict, seg_cols_name)
                                   for lim2 in vb_limits if lim2 != lim1)
        if all(other_segs_are_downstream) or all(other_segs_are_upstream):
            return lim1
    print(f"Unable to find point segment for VB: {vb_limits}")
    return None


def get_len_vb(vb_limits, seg_dict: dict, seg_cols_name: dict[str, str]):
    """ Return the length of a VB.
    If it is a 3-limit VB, returns the maximum length between the point segment and either heel point. """
    if len(vb_limits) == 3:
        lim1 = give_point_seg_vb(vb_limits, seg_dict, seg_cols_name)
    else:
        lim1 = vb_limits[0]
    return max(get_dist(lim1["Seg"], lim1["x"], lim["Seg"], lim["x"], seg_dict, seg_cols_name)
               for lim in vb_limits if lim != lim1)
