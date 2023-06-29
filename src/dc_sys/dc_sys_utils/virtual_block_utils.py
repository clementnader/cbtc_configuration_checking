#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dist_utils import get_dist, get_list_of_paths
from .path_utils import is_seg_downstream


def give_point_seg_vb(vb_limits):
    """ Give the point segment corresponding to the switch associated to the VB. """
    for lim1 in vb_limits:
        seg1 = lim1["Seg"]
        other_segs_are_downstream = [is_seg_downstream(seg1, lim2["Seg"]) for lim2 in vb_limits if lim2 != lim1]
        other_segs_are_upstream = [is_seg_downstream(lim2["Seg"], seg1) for lim2 in vb_limits if lim2 != lim1]
        if all(other_segs_are_downstream) or all(other_segs_are_upstream):
            return lim1
    print(f"Unable to find point segment for VB: {vb_limits}")


def get_len_vb(vb_limits):
    """ Return the length of a VB.
    If it is a 3-limit VB, returns the maximum length between the point segment and either heel point. """
    if len(vb_limits) == 3:
        lim1 = give_point_seg_vb(vb_limits)
    else:
        lim1 = vb_limits[0]
    return max(get_dist(lim1["Seg"], lim1["x"], lim["Seg"], lim["x"])
               for lim in vb_limits if lim != lim1)


def get_segs_in_vb(vb_limits):
    """ Return the list of segments in a VB. """
    list_segs = list()
    if len(vb_limits) == 3:
        lim1 = give_point_seg_vb(vb_limits)
    else:
        lim1 = vb_limits[0]
    seg1 = lim1["Seg"]
    other_limits = [lim["Seg"] for lim in vb_limits if lim != lim1]
    for seg2 in other_limits:
        list_paths = get_list_of_paths(seg1, seg2)
        for path in list_paths:
            for seg in path:
                if seg not in list_segs:
                    list_segs.append(seg)
    return list_segs


def is_seg_in_vb(vb_limits, seg: str):
    """ Return True if a segment is in a VB else False. """
    return seg in get_segs_in_vb(vb_limits)


def get_vb_associated_to_sw(sw, vb_dict: dict, sw_cols_name: dict[str, str]):
    """ Get the VB associated to a switch. """
    for vb, vb_values in vb_dict.items():
        vb_limits = vb_values["limits"]
        if len(vb_limits) == 3:
            if sorted([vb_lim["Seg"] for vb_lim in vb_limits]) == sorted(sw.values()):
                return vb
            if all(is_seg_in_vb(vb_limits, sw[sw_cols_name[j]]) for j in ['B', 'C', 'D']):
                return vb
    print(f"Unable to find VB associated to SW: {sw}")
