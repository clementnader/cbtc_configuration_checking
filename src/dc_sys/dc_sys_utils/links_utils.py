#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database.load_sheets import load_sheet, get_cols_name
from .segments_utils import *

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
    depol_segs = get_depolarized_segs()

    upstream_dict = get_accessible_segs_in_one_direction(start_segs, end_segs, depol_segs, downstream=False)
    downstream_dict = get_accessible_segs_in_one_direction(end_segs, start_segs, depol_segs, downstream=True)

    upstream_dict, downstream_dict = update_all_accessible_depolarized_segs(upstream_dict, downstream_dict)

    for seg in seg_dict:
        SEGMENTS_LINKED[seg] = {"upstream": upstream_dict.get(seg, []),
                                "downstream": downstream_dict.get(seg, [])}


def update_all_accessible_depolarized_segs(upstream_dict, downstream_dict):
    upstream_dict_segs_to_add = update_accessible_segs_dict_depolarized(upstream_dict, downstream_dict)
    downstream_dict_segs_to_add = update_accessible_segs_dict_depolarized(downstream_dict, upstream_dict,
                                                                          reverse_order=True)
    upstream_dict_crossed_depol = _add_crossed_depol(upstream_dict_segs_to_add, downstream_dict_segs_to_add)
    downstream_dict_crossed_depol = _add_crossed_depol(downstream_dict_segs_to_add, upstream_dict_segs_to_add)
    downstream_dict_segs_to_add.update(upstream_dict_crossed_depol)
    upstream_dict_segs_to_add.update(downstream_dict_crossed_depol)

    for depol_seg, sub_dict in upstream_dict_segs_to_add.items():
        segs_to_add = sub_dict["segs_to_add"]
        concerned_segs = sub_dict["concerned_segs"]
        for seg in concerned_segs:
            upstream_dict[seg].update(segs_to_add)

    for depol_seg, sub_dict in downstream_dict_segs_to_add.items():
        segs_to_add = sub_dict["segs_to_add"]
        concerned_segs = sub_dict["concerned_segs"]
        for seg in concerned_segs:
            downstream_dict[seg].update(segs_to_add)

    return upstream_dict, downstream_dict


def _add_crossed_depol(upstream_dict_segs_to_add, downstream_dict_segs_to_add):
    res_dict = dict()
    for upstream_depol_seg, upstream_sub_dict in upstream_dict_segs_to_add.items():
        upstream_segs_to_add = upstream_sub_dict["segs_to_add"]
        upstream_concerned_segs = upstream_sub_dict["concerned_segs"]
        for seg in upstream_concerned_segs:
            if is_seg_depolarized(seg):
                associated_depol = get_associated_depol(seg)
                for associated_depol_seg in associated_depol:
                    if associated_depol_seg != seg:
                        if f"{upstream_depol_seg}__2" not in res_dict:
                            res_dict[f"{upstream_depol_seg}__2"] = {"segs_to_add": upstream_segs_to_add,
                                                                    "concerned_segs": set()}
                        res_dict[f"{upstream_depol_seg}__2"]["concerned_segs"].add(associated_depol_seg)
        for downstream_depol_seg, downstream_sub_dict in downstream_dict_segs_to_add.items():
            if downstream_depol_seg in upstream_concerned_segs:
                res_dict[f"{upstream_depol_seg}__2"]["concerned_segs"].update(downstream_sub_dict["segs_to_add"])
    return res_dict


def update_accessible_segs_dict_depolarized(upstream_dict: dict[str, set], downstream_dict: dict[str, set],
                                            reverse_order: bool = False):
    dict_segs_to_add = dict()
    for seg, upstream_segs in upstream_dict.items():
        if is_seg_depolarized(seg):
            associated_depol = get_associated_depol(seg)
            for upstream_seg in upstream_segs:
                if upstream_seg in associated_depol:
                    dict_segs_to_add[seg] = _update_all_previous_segs_depol(downstream_dict, reverse_order,
                                                                            seg, upstream_seg)

    return dict_segs_to_add


def _update_all_previous_segs_depol(downstream_dict: dict[str, set], reverse_order: bool,
                                    current_seg: str, upstream_depol_seg: str):
    segs_to_add = downstream_dict[upstream_depol_seg]
    res_dict = {"segs_to_add": segs_to_add, "concerned_segs": [current_seg]}
    for seg in downstream_dict[current_seg]:
        if not is_seg_depolarized(seg):
            res_dict["concerned_segs"].append(seg)
        else:
            upstream_depol = get_linked_segs(seg, downstream=reverse_order)
            if any(upstream_seg_depol in downstream_dict[current_seg] for upstream_seg_depol in upstream_depol):
                res_dict["concerned_segs"].append(seg)

    return res_dict


def get_accessible_segs_in_one_direction(start_segs, end_segs, depol_segs: list[list[str]], downstream: bool = False):

    def inner_recurs_seg(seg):
        nonlocal res_dict
        next_segs = get_linked_segs(seg, downstream=not downstream)
        for next_seg in next_segs:
            if is_seg_depolarized(next_seg) and is_seg_depolarized(seg):
                continue
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
        if start_seg not in res_dict:
            res_dict[start_seg] = set()
            inner_recurs_seg(start_seg)
    if depol_segs:
        for sub_list in depol_segs:
            for depol_seg in sub_list:
                if depol_seg not in res_dict:
                    res_dict[depol_seg] = set()
                    for linked_seg in get_linked_segs(depol_seg, downstream):
                        res_dict[depol_seg].add(linked_seg)
                        if linked_seg in sub_list:
                            continue
                        if linked_seg in res_dict:
                            res_dict[depol_seg].update(res_dict[linked_seg])
                    inner_recurs_seg(depol_seg)
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
