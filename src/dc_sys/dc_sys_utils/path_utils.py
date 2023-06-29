#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database.load_sheets import load_sheet, get_cols_name
from .segments_utils import *
from ...utils import *

SEGMENTS_LINKED = dict()


def are_segs_linked(seg1, seg2, x1: float = None, x2: float = None) -> (float, list[str]):
    return is_seg_downstream(seg1, seg2, x1, x2) or is_seg_downstream(seg2, seg1, x2, x1)


def is_seg_downstream(start_seg, end_seg, start_x: float = None, end_x: float = None) -> (float, list[str]):
    if start_x is not None:
        start_x = float(start_x)
    if end_x is not None:
        end_x = float(end_x)

    if start_seg == end_seg:
        if (start_x is None or end_x is None) or start_x <= end_x:
            return True
        else:
            return False

    return end_seg in get_all_downstream_segs(start_seg)


def get_all_upstream_segs(seg):
    all_accessible_segs = get_all_accessible_segs()
    return all_accessible_segs["upstream"][seg]


def get_all_downstream_segs(seg):
    all_accessible_segs = get_all_accessible_segs()
    return all_accessible_segs["downstream"][seg]


DOWNSTREAM_ACCESSIBLE_SEGS = dict()
UPSTREAM_ACCESSIBLE_SEGS = dict()


def get_all_accessible_segs():
    global DOWNSTREAM_ACCESSIBLE_SEGS, UPSTREAM_ACCESSIBLE_SEGS
    if not DOWNSTREAM_ACCESSIBLE_SEGS or not UPSTREAM_ACCESSIBLE_SEGS:
        _update_all_accessible_segs()
    return {"upstream": UPSTREAM_ACCESSIBLE_SEGS,
            "downstream": DOWNSTREAM_ACCESSIBLE_SEGS}


def _update_all_accessible_segs():
    global DOWNSTREAM_ACCESSIBLE_SEGS, UPSTREAM_ACCESSIBLE_SEGS
    if DOWNSTREAM_ACCESSIBLE_SEGS and UPSTREAM_ACCESSIBLE_SEGS:
        return
    seg_dict = load_sheet("seg")
    for seg in seg_dict.keys():
        DOWNSTREAM_ACCESSIBLE_SEGS[seg] = get_all_accessible_segs_from(seg, downstream=True)
        UPSTREAM_ACCESSIBLE_SEGS[seg] = get_all_accessible_segs_from(seg, downstream=False)


def get_all_accessible_segs_from(start_seg, downstream: bool):
    list_segs = list()

    def inner_recurs_next_seg(seg, inner_downstream):
        nonlocal list_segs
        linked_segs = get_linked_segs(seg, inner_downstream)
        if not linked_segs:
            return
        for next_seg in linked_segs:
            if next_seg in list_segs:
                return
            list_segs.append(next_seg)
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            inner_recurs_next_seg(next_seg, next_inner_downstream)

    inner_recurs_next_seg(start_seg, downstream)
    return list_segs


def get_all_paths_from(start_seg, downstream: bool, max_iter: int = None):
    list_paths = list()

    def inner_recurs_next_seg(seg, path, inner_downstream, nb_iter: int = 0):
        nonlocal list_paths
        linked_segs = get_linked_segs(seg, inner_downstream)
        if not linked_segs or (max_iter is not None and nb_iter >= max_iter):
            list_paths.append(path)
            return
        for next_seg in linked_segs:
            if next_seg in path:  # for ring
                list_paths.append(path)
                return
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            inner_recurs_next_seg(next_seg, path + [next_seg], next_inner_downstream, nb_iter=nb_iter + 1)

    inner_recurs_next_seg(start_seg, [start_seg], downstream)
    return list_paths
