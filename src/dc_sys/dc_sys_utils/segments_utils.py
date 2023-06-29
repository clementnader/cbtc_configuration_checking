#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database.load_sheets import load_sheet, get_cols_name

DEPOLARIZED_SEGMENTS = list()
__all__ = ["is_seg_upstream_of_a_switch", "is_seg_downstream_of_a_switch",
           "get_len_seg", "get_seg_track", "is_seg_depolarized", "get_depolarized_segs", "get_associated_depol",
           "get_linked_segs", "get_straight_linked_segs", "get_correct_seg_offset"]


def is_seg_upstream_of_a_switch(seg: str) -> bool:
    if len(get_linked_segs(seg, downstream=True)) == 2:
        return True
    return False


def is_seg_downstream_of_a_switch(seg: str) -> bool:
    if len(get_linked_segs(seg, downstream=False)) == 2:
        return True
    return False


def get_len_seg(seg: str) -> float:
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")
    return float(seg_dict[seg][seg_cols_name['G']])


def get_seg_track(seg: str) -> str:
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")
    return seg_dict[seg][seg_cols_name['D']]


def is_seg_depolarized(seg):
    global DEPOLARIZED_SEGMENTS
    if not DEPOLARIZED_SEGMENTS:
        _update_depol_segs()
    return any(seg in sub_list for sub_list in DEPOLARIZED_SEGMENTS)


def get_associated_depol(seg):
    global DEPOLARIZED_SEGMENTS
    if not is_seg_depolarized(seg):
        return None
    for sub_list in DEPOLARIZED_SEGMENTS:
        if seg in sub_list:
            return sub_list


def get_depolarized_segs() -> list[list[str]]:
    global DEPOLARIZED_SEGMENTS
    if not DEPOLARIZED_SEGMENTS:
        _update_depol_segs()
    return DEPOLARIZED_SEGMENTS


def _update_depol_segs():
    global DEPOLARIZED_SEGMENTS
    line_dict = load_sheet("line")
    line_cols_name = get_cols_name("line")
    for line_info in line_dict.values():
        for col in columns_from_to('G', 'N'):  # all depolarized segments
            depol_seg = line_info.get(line_cols_name[col])
            if depol_seg is not None:
                DEPOLARIZED_SEGMENTS.append(_get_second_depol_seg(depol_seg))


def _get_second_depol_seg(depol_seg: str):
    list_depols = [depol_seg]
    downstream_segs = get_linked_segs(depol_seg, downstream=True)
    upstream_segs = get_linked_segs(depol_seg, downstream=False)
    for downstream_seg in downstream_segs:
        if depol_seg in get_linked_segs(downstream_seg, downstream=True):
            # depol_seg is downstream of its downstream seg
            list_depols.append(downstream_seg)
    for upstream_seg in upstream_segs:
        if depol_seg in get_linked_segs(upstream_seg, downstream=False):
            # depol_seg is upstream of its upstream seg
            list_depols.append(upstream_seg)
    return list_depols


def get_linked_segs(seg: str, downstream: bool = True) -> list[str]:
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    ref_col_1 = 'J' if downstream else 'H'
    ref_col_2 = 'K' if downstream else 'I'
    linked_segs = list()

    linked_seg_1 = seg_dict[seg].get(seg_cols_name[ref_col_1])
    linked_seg_2 = seg_dict[seg].get(seg_cols_name[ref_col_2])
    if linked_seg_1 is not None:
        linked_segs.append(linked_seg_1)
    if linked_seg_2 is not None:
        linked_segs.append(linked_seg_2)

    return linked_segs


def get_straight_linked_segs(seg: str, downstream: bool = True, depth: int = 10, verbose: bool = False):
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    ref_col = 'J' if downstream else 'H'
    ref_col2 = 'K' if downstream else 'I'
    previous_seg = seg
    linked_seg = seg_dict[previous_seg].get(seg_cols_name[ref_col])
    linked_seg2 = seg_dict[previous_seg].get(seg_cols_name[ref_col2])
    cnt = 0
    while linked_seg is not None and cnt < depth:
        if linked_seg2 is not None and verbose:
            print_warning(f"Another segment exists {'downstream' if downstream else 'upstream'}, which is ignored."
                          f"\n(origin_seg={seg}, seg={previous_seg}, {linked_seg = }, {linked_seg2 = })")
        cnt += 1
        yield linked_seg
        previous_seg = linked_seg
        linked_seg = seg_dict[previous_seg].get(seg_cols_name[ref_col])
        linked_seg2 = seg_dict[previous_seg].get(seg_cols_name[ref_col2])


def get_correct_seg_offset(seg, x):
    len_seg = get_len_seg(seg)
    downstream_segs = get_straight_linked_segs(seg, downstream=True, verbose=True)
    upstream_segs = get_straight_linked_segs(seg, downstream=False, verbose=True)

    while x > len_seg:
        x -= len_seg
        seg = downstream_segs.__next__()
        len_seg = get_len_seg(seg)

    while x < 0:
        seg = upstream_segs.__next__()
        len_seg = get_len_seg(seg)
        x += len_seg

    return seg, x
