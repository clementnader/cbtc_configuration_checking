#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_len_seg(seg: str, seg_dict: dict, seg_cols_name: dict[str, str]) -> float:
    return float(seg_dict[seg][seg_cols_name['G']])


def get_linked_segs(seg: str, seg_dict: dict, seg_cols_name: dict[str, str], downstream: bool = True) -> list[str]:
    ref_col_1 = 'J' if downstream else 'H'
    ref_col_2 = 'K' if downstream else 'I'
    linked_segs = list()

    linked_seg_1 = seg_dict[seg][seg_cols_name[ref_col_1]] if seg_cols_name[ref_col_1] in seg_dict[seg] else ""
    linked_seg_2 = seg_dict[seg][seg_cols_name[ref_col_2]] if seg_cols_name[ref_col_2] in seg_dict[seg] else ""
    if linked_seg_1:
        linked_segs.append(linked_seg_1)
    if linked_seg_2:
        linked_segs.append(linked_seg_2)

    return linked_segs


def is_seg_downstream(start_seg, end_seg, seg_dict: dict, seg_cols_name: dict[str, str]) -> (float, list[str]):

    def inner_recurs_next_seg(seg):
        if seg == end_seg:
            return True
        for next_seg in get_linked_segs(seg, seg_dict=seg_dict, seg_cols_name=seg_cols_name):
            if next_seg:
                return inner_recurs_next_seg(next_seg)
        return False

    return inner_recurs_next_seg(start_seg)


def get_straight_linked_segs(seg: str, seg_dict: dict, seg_cols_name: dict[str, str], downstream: bool = True,
                             depth: int = 10) -> list[str]:
    ref_col = 'J' if downstream else 'H'
    linked_segs = list()
    linked_seg = seg_dict[seg][seg_cols_name[ref_col]] if seg_cols_name[ref_col] in seg_dict[seg] else ""
    cnt = 0
    while linked_seg and cnt < depth:
        cnt += 1
        linked_segs.append(linked_seg)
        linked_seg = seg_dict[linked_seg][seg_cols_name[ref_col]] if seg_cols_name[ref_col] in seg_dict[linked_seg] \
            else ""
    return linked_segs

#
# def get_correct_seg_offset(seg, x, seg_dict, seg_cols_name):
#     len_seg = get_len_seg(seg, seg_dict, seg_cols_name)
#     downstream_segs = get_straight_linked_segs(seg, seg_dict, seg_cols_name, downstream=True)
#     upstream_segs = get_straight_linked_segs(seg, seg_dict, seg_cols_name, downstream=False)
#
#     while x > len_seg:
#         x -= len_seg
#         seg = downstream_segs.pop(0)
#         len_seg = get_len_seg(seg, seg_dict, seg_cols_name)
#
#     while x < 0:
#         seg = upstream_segs.pop(0)
#         len_seg = get_len_seg(seg, seg_dict, seg_cols_name)
#         x += len_seg
#
#     return seg, x
