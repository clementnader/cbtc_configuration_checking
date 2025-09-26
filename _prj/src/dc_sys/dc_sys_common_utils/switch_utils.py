#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_basic_utils import *
from .segments_utils import *


__all__ = ["is_switch_point_upstream_heels", "get_switch_position", "is_switch_on_diamond_crossing"]


def is_switch_point_upstream_heels(sw_name: str):
    """Returns True if the point segment of the switch is upstream of the two heels segments (divergent switch),
    returns False if it is downstream (convergent switch),
    raises an error if it is neither the first nor the second."""
    point_seg = get_dc_sys_value(sw_name, DCSYS.Aig.SegmentPointe)
    right_heel = get_dc_sys_value(sw_name, DCSYS.Aig.SegmentTd)
    left_heel = get_dc_sys_value(sw_name, DCSYS.Aig.SegmentTg)

    downstream_segs = get_linked_segments(point_seg, downstream=True)
    upstream_segs = get_linked_segments(point_seg, downstream=False)
    other_segs_are_downstream = [other_seg in downstream_segs for other_seg in [right_heel, left_heel]]
    other_segs_are_upstream = [other_seg in upstream_segs for other_seg in [right_heel, left_heel]]

    if all(other_segs_are_downstream):
        return True
    if all(other_segs_are_upstream):
        return False
    raise Exception("The point segment is not found upstream or downstream of the heels.")


def get_switch_position(sw_name: str) -> tuple[str, float]:
    """Returns the position of the switch with the segment and offset. """
    point_seg = get_dc_sys_value(sw_name, DCSYS.Aig.SegmentPointe)
    upstream = is_switch_point_upstream_heels(sw_name)
    len_seg = get_segment_length(point_seg)
    x = len_seg if upstream else 0.
    return point_seg, x


def is_switch_on_diamond_crossing(sw_name: str) -> tuple[bool, list[str]]:
    ivb_dict = load_sheet(DCSYS.IVB)
    for ivb_value in ivb_dict.values():
        diamond_crossing_switches = get_dc_sys_value(ivb_value, DCSYS.IVB.DiamondCrossingSwitches.SwitchName)
        if sw_name in diamond_crossing_switches:
            return True, diamond_crossing_switches
    return False, []
