#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .segments_utils import *


__all__ = ["is_sw_point_seg_upstream", "get_sw_pos", "get_point_seg"]


def get_point_seg(sw):
    return get_dc_sys_value(sw, DCSYS.Aig.SegmentPointe)


def is_sw_point_seg_upstream(sw):
    """Returns True if the point segment of the switch is upstream of the two heels segments,
    returns False if it is downstream,
    raises an error if it is neither the first nor the second."""
    point_seg = get_dc_sys_value(sw, DCSYS.Aig.SegmentPointe)
    right_heel = get_dc_sys_value(sw, DCSYS.Aig.SegmentTd)
    left_heel = get_dc_sys_value(sw, DCSYS.Aig.SegmentTg)

    downstream_segs = get_linked_segs(point_seg, downstream=True)
    upstream_segs = get_linked_segs(point_seg, downstream=False)
    other_segs_are_downstream = [other_seg in downstream_segs for other_seg in [right_heel, left_heel]]
    other_segs_are_upstream = [other_seg in upstream_segs for other_seg in [right_heel, left_heel]]

    if all(other_segs_are_downstream):
        return True
    if all(other_segs_are_upstream):
        return False
    raise Exception("The point segment is not found upstream or downstream of the heels.")


def get_sw_pos(sw_val: dict[str, Any]) -> tuple[str, float]:
    """Returns the position of the switch with the seg and offset. """
    point_seg = get_point_seg(sw_val)
    upstream = is_sw_point_seg_upstream(sw_val)
    len_seg = get_seg_len(point_seg)
    x = len_seg if upstream else 0
    return point_seg, x
