#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .segments_utils import *
from ..load_database.load_sheets import load_sheet, get_cols_name

SEGMENTS_LINKED = dict()


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


def get_all_linked_segs(seg):
    global SEGMENTS_LINKED
    if not SEGMENTS_LINKED:
        update_segments_paths()
    return SEGMENTS_LINKED[seg]


def get_all_upstream_segs(seg):
    global SEGMENTS_LINKED
    if not SEGMENTS_LINKED:
        update_segments_paths()
    return SEGMENTS_LINKED[seg]["upstream"]


def get_all_downstream_segs(seg):
    global SEGMENTS_LINKED
    if not SEGMENTS_LINKED:
        update_segments_paths()
    return SEGMENTS_LINKED[seg]["downstream"]


def get_all_segs_linked():
    global SEGMENTS_LINKED
    if not SEGMENTS_LINKED:
        update_segments_paths()
    return SEGMENTS_LINKED


def update_segments_paths():
    global SEGMENTS_LINKED
    if SEGMENTS_LINKED:
        return
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")
    start_segs, end_segs = get_start_n_end_segs(seg_dict, seg_cols_name)
    upstream_dict = get_accessible_segs_in_one_direction(start_segs, end_segs, downstream=False)
    downstream_dict = get_accessible_segs_in_one_direction(end_segs, start_segs, downstream=True)
    for seg in seg_dict:
        SEGMENTS_LINKED[seg] = {"upstream": upstream_dict[seg], "downstream": downstream_dict[seg]}


def get_accessible_segs_in_one_direction(start_segs, end_segs, downstream: bool = False):

    def inner_recurs_seg(seg):
        nonlocal res_dict
        next_segs = get_linked_segs(seg, downstream=not downstream)
        for next_seg in next_segs:
            previous_segs = get_linked_segs(next_seg, downstream=downstream)
            all_accessible_previous_segs = set()
            for previous_seg in previous_segs:
                all_accessible_previous_segs.add(previous_seg)
                if previous_seg not in res_dict:
                    return
                all_accessible_previous_segs.update(res_dict[previous_seg])
            res_dict[next_seg] = all_accessible_previous_segs
            if next_seg not in end_segs:
                inner_recurs_seg(next_seg)

    res_dict = dict()
    for start_seg in start_segs:
        res_dict[start_seg] = set()
        inner_recurs_seg(start_seg)
    return res_dict


def get_start_n_end_segs(seg_dict: dict[str, dict], seg_cols_name: dict[str, str]):
    start_segs = list()
    end_segs = list()

    upstream_cols = ('H', 'I')
    downstream_cols = ('J', 'K')

    for seg, seg_values in seg_dict.items():
        if all(seg_cols_name[col] not in seg_values for col in upstream_cols):
            start_segs.append(seg)
        if all(seg_cols_name[col] not in seg_values for col in downstream_cols):
            end_segs.append(seg)

    return start_segs, end_segs
