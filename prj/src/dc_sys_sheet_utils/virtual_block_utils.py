#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_draw_path.dc_sys_path_and_distances import is_seg_downstream, get_dist, get_list_of_paths


__all__ = ["give_point_seg_vb", "get_len_vb", "get_segs_in_vb", "is_seg_in_vb", "get_vb_associated_to_sw",
           "get_sw_associated_to_vb"]


def give_point_seg_vb(vb_limits):
    """ Give the point segment corresponding to the switch associated to the VB. """
    for lim1 in vb_limits:
        seg1, _ = lim1
        other_segs_are_downstream = [is_seg_downstream(seg1, seg2, downstream=True)
                                     for seg2, x2 in vb_limits if (seg2, x2) != lim1]
        other_segs_are_upstream = [is_seg_downstream(seg1, seg2, downstream=False)
                                   for seg2, x2 in vb_limits if (seg2, x2) != lim1]
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
    seg1, x1 = lim1
    return max(get_dist(seg1, x1, seg, x) for seg, x in vb_limits if (seg, x) != lim1)


def get_segs_in_vb(vb_limits):
    """ Return the list of segments in a VB. """
    list_segs = list()
    if len(vb_limits) == 3:
        lim1 = give_point_seg_vb(vb_limits)
    else:
        lim1 = vb_limits[0]
    seg1, _ = lim1
    other_limits = [seg for seg, x in vb_limits if (seg, x) != lim1]
    for seg2 in other_limits:
        list_paths = get_list_of_paths(seg1, seg2)
        for _, path in list_paths:
            for seg in path:
                if seg not in list_segs:
                    list_segs.append(seg)
    return list_segs


def is_seg_in_vb(vb_limits, seg: str):
    """ Return True if a segment is in a VB else False. """
    return seg in get_segs_in_vb(vb_limits)


def get_vb_associated_to_sw(sw):
    """ Get the VB associated to a switch. """
    vb_dict = load_sheet(DCSYS.CV)
    sw_segs = sorted(get_dc_sys_values(sw, DCSYS.Aig.SegmentPointe, DCSYS.Aig.SegmentTd, DCSYS.Aig.SegmentTg))
    for vb, vb_value in vb_dict.items():
        vb_limits = list(get_dc_sys_zip_values(vb_value, DCSYS.CV.Extremite.Seg, DCSYS.CV.Extremite.X))
        if len(vb_limits) == 3:
            if sorted([seg for seg, _ in vb_limits]) == sw_segs:
                return vb
            if all(is_seg_in_vb(vb_limits, seg) for seg in sw_segs):
                return vb
    print_error(f"Unable to find VB associated to SW: {sw}")


def get_sw_associated_to_vb(vb_limits):
    assert len(vb_limits) == 3
    sw_dict = load_sheet(DCSYS.Aig)
    lim_segs = sorted([seg for seg, _ in vb_limits])
    for sw_name, sw_val in sw_dict.items():
        sw_segs = sorted(get_dc_sys_values(sw_val, DCSYS.Aig.SegmentPointe, DCSYS.Aig.SegmentTd, DCSYS.Aig.SegmentTg))
        if lim_segs == sw_segs:
            return sw_name
        if all(is_seg_in_vb(vb_limits, seg) for seg in sw_segs):
            return sw_name
    print_error(f"Unable to find switch associated to VB limits: {vb_limits}")
