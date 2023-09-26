#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ..load_database import *
from .segments_utils import *


__all__ = ["get_all_accessible_segments_from", "get_all_upstream_segments", "get_all_downstream_segments",
           "update_all_accessible_segments"]


DOWNSTREAM_ACCESSIBLE_SEGMENTS = dict()
UPSTREAM_ACCESSIBLE_SEGMENTS = dict()


def get_all_upstream_segments(seg: str) -> set[tuple[str, bool]]:
    global UPSTREAM_ACCESSIBLE_SEGMENTS
    if not UPSTREAM_ACCESSIBLE_SEGMENTS:
        update_all_accessible_segments()
    return UPSTREAM_ACCESSIBLE_SEGMENTS[seg]


def get_all_downstream_segments(seg: str) -> set[tuple[str, bool]]:
    global DOWNSTREAM_ACCESSIBLE_SEGMENTS
    if not DOWNSTREAM_ACCESSIBLE_SEGMENTS:
        update_all_accessible_segments()
    return DOWNSTREAM_ACCESSIBLE_SEGMENTS[seg]


def update_all_accessible_segments() -> None:
    global DOWNSTREAM_ACCESSIBLE_SEGMENTS, UPSTREAM_ACCESSIBLE_SEGMENTS
    if DOWNSTREAM_ACCESSIBLE_SEGMENTS and UPSTREAM_ACCESSIBLE_SEGMENTS:
        return
    seg_dict = load_sheet(DCSYS.Seg)
    for seg in seg_dict.keys():
        DOWNSTREAM_ACCESSIBLE_SEGMENTS[seg] = get_all_accessible_segments_from(seg, downstream=True)
        UPSTREAM_ACCESSIBLE_SEGMENTS[seg] = get_all_accessible_segments_from(seg, downstream=False)


def get_all_accessible_segments_from(start_seg: str, downstream: bool) -> set[tuple[str, bool]]:
    list_segs = set()

    def inner_recurs_next_seg(seg: str, inner_downstream: bool, path: list[str]):
        nonlocal list_segs
        list_segs.add((seg, inner_downstream))
        linked_segs = get_linked_segs(seg, inner_downstream)
        if not linked_segs:
            return
        for next_seg in linked_segs:
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            if next_seg in path or (next_seg, next_inner_downstream) in list_segs:
                # We check if we have made a full turn and reach a segment that we have already run through
                # in the current path,
                # and we check if we have not already made the work for this segment and direction
                continue
            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [next_seg])

    inner_recurs_next_seg(start_seg, downstream, [start_seg])
    return list_segs
