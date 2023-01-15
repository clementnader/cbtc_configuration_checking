#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database.load_sheets import load_sheet, get_cols_name


def get_len_seg(seg: str) -> float:
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    return float(seg_dict[seg][seg_cols_name['G']])


def get_seg_track(seg: str) -> str:
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    return seg_dict[seg][seg_cols_name['D']]


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


def get_straight_linked_segs(seg: str, downstream: bool = True, depth: int = 10) -> list[str]:
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    ref_col = 'J' if downstream else 'H'
    linked_segs = list()
    linked_seg = seg_dict[seg].get(seg_cols_name[ref_col])
    cnt = 0
    while linked_seg is not None and cnt < depth:
        cnt += 1
        linked_segs.append(linked_seg)
        linked_seg = seg_dict[linked_seg].get(seg_cols_name[ref_col])
    return linked_segs


def get_correct_seg_offset(seg, x):
    len_seg = get_len_seg(seg)
    downstream_segs = get_straight_linked_segs(seg, downstream=True)
    upstream_segs = get_straight_linked_segs(seg, downstream=False)

    while x > len_seg:
        x -= len_seg
        seg = downstream_segs.pop(0)
        len_seg = get_len_seg(seg)

    while x < 0:
        seg = upstream_segs.pop(0)
        len_seg = get_len_seg(seg)
        x += len_seg

    return seg, x
