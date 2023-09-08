#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
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
    print_title(f"Tracing all paths...", color=Color.mint_green)
    seg_dict = load_sheet(DCSYS.Seg)
    nb_segs = len(seg_dict)
    progress_bar(1, 1, end=True)  # reset progress bar
    for i, seg in enumerate(seg_dict.keys()):
        print_log(f"\r{progress_bar(i, nb_segs)} getting all accessible segments from {seg}...", end="")
        DOWNSTREAM_ACCESSIBLE_SEGMENTS[seg] = get_all_accessible_segments_from(seg, downstream=True)
        UPSTREAM_ACCESSIBLE_SEGMENTS[seg] = get_all_accessible_segments_from(seg, downstream=False)
    print_log(f"\r{progress_bar(nb_segs, nb_segs, end=True)} all paths have been traced.\n")


def get_all_accessible_segments_from(start_seg: str, downstream: bool) -> set[tuple[str, bool]]:
    list_segs = set()

    def inner_recurs_next_seg(seg: str, seg_path: list[str], direction_path: list[bool], inner_downstream: bool):
        nonlocal list_segs
        linked_segs = get_linked_segs(seg, inner_downstream)
        if not linked_segs:
            list_segs.update(zip(seg_path, direction_path))
        for next_seg in linked_segs:
            if next_seg in seg_path:
                list_segs.update(zip(seg_path, direction_path))
                continue
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            inner_recurs_next_seg(next_seg, seg_path + [next_seg], direction_path + [next_inner_downstream],
                                  next_inner_downstream)

    inner_recurs_next_seg(start_seg, [start_seg], [downstream], downstream)
    return list_segs
