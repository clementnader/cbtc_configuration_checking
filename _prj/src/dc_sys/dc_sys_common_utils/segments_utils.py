#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *


__all__ = ["is_seg_upstream_of_a_switch", "is_seg_downstream_of_a_switch",
           "get_seg_len", "are_points_matching", "get_seg_track",
           "is_seg_depolarized", "get_depolarized_segs", "get_associated_depol",
           "get_linked_segs", "get_straight_linked_segs", "get_correct_seg_offset"]


DEPOLARIZED_SEGMENTS = list()


def is_seg_upstream_of_a_switch(seg: str) -> bool:
    if len(get_linked_segs(seg, downstream=True)) == 2:
        return True
    return False


def is_seg_downstream_of_a_switch(seg: str) -> bool:
    if len(get_linked_segs(seg, downstream=False)) == 2:
        return True
    return False


def get_seg_len(seg_name: str) -> float:
    seg_dict = load_sheet(DCSYS.Seg)
    return round(float(get_dc_sys_value(seg_dict[seg_name], DCSYS.Seg.Longueur)), 3)


def are_points_matching(seg1: str, x1: float, seg2: str, x2: float, tolerance: float = .0) -> bool:
    if seg1 == seg2 and round(abs(x1 - x2), 2) <= tolerance:
        return True
    len_seg1 = get_seg_len(seg1)
    len_seg2 = get_seg_len(seg2)
    if x1 == len_seg1 and x2 == 0:
        next_segs = get_linked_segs(seg1, downstream=True)
        if seg2 in next_segs:
            return True
        return False
    if x2 == len_seg2 and x1 == 0:
        next_segs = get_linked_segs(seg2, downstream=True)
        if seg1 in next_segs:
            return True
        return False
    # Manage depolarization points
    if x1 == len_seg1 and x2 == len_seg2:
        next_segs1 = get_linked_segs(seg1, downstream=True)
        next_segs2 = get_linked_segs(seg2, downstream=True)
        if seg2 in next_segs1 and seg1 in next_segs2:
            return True
        return False
    if x1 == 0 and x2 == 0:
        next_segs1 = get_linked_segs(seg1, downstream=False)
        next_segs2 = get_linked_segs(seg2, downstream=False)
        if seg2 in next_segs1 and seg1 in next_segs2:
            return True
        return False
    return False


def get_seg_track(seg: str) -> str:
    seg_dict = load_sheet(DCSYS.Seg)
    return get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Voie)


def is_seg_depolarized(seg: str) -> bool:
    global DEPOLARIZED_SEGMENTS
    if not DEPOLARIZED_SEGMENTS:
        _update_depol_segs()
    return any(seg in sub_list for sub_list in DEPOLARIZED_SEGMENTS)


def get_associated_depol(seg: str) -> Optional[list[str]]:
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


def _update_depol_segs() -> None:
    global DEPOLARIZED_SEGMENTS
    line_dict = load_sheet(DCSYS.Ligne)
    for line_info in line_dict.values():
        for depol_seg in get_dc_sys_value(line_info, DCSYS.Ligne.SegmentsDepolarises.Cell):
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


def get_linked_segs(seg: str, downstream: bool) -> list[str]:
    seg_dict = load_sheet(DCSYS.Seg)
    attr = DCSYS.Seg.SegmentsVoisins.Aval if downstream else DCSYS.Seg.SegmentsVoisins.Amont
    linked_segs = list()
    for linked_seg in get_dc_sys_value(seg_dict[seg], attr):
        if linked_seg is not None:
            linked_segs.append(linked_seg)
    return linked_segs


def get_straight_linked_segs(seg: str, downstream: bool, depth: int = 10, verbose: bool = False
                             ) -> Generator[str, None, None]:
    seg_dict = load_sheet(DCSYS.Seg)
    attr = DCSYS.Seg.SegmentsVoisins.Aval if downstream else DCSYS.Seg.SegmentsVoisins.Amont
    previous_seg = seg
    linked_segs = get_dc_sys_value(seg_dict[previous_seg], attr)
    linked_seg = linked_segs[0] if len(linked_segs) > 0 else None
    linked_seg2 = linked_segs[1] if len(linked_segs) > 1 else None
    cnt = 0
    while linked_seg is not None and cnt < depth:
        if linked_seg2 is not None and verbose:
            print_warning(f"Another segment exists {'downstream' if downstream else 'upstream'}, which is ignored."
                          f"\n(origin_seg={seg}, seg={previous_seg}, {linked_seg = }, {linked_seg2 = })")
        cnt += 1
        yield linked_seg
        previous_seg = linked_seg
        linked_segs = get_dc_sys_value(seg_dict[previous_seg], attr)
        linked_seg = linked_segs[0] if len(linked_segs) > 0 else None
        linked_seg2 = linked_segs[1] if len(linked_segs) > 1 else None


def get_correct_seg_offset(seg: str, x: float) -> tuple[str, float]:
    len_seg = get_seg_len(seg)
    downstream_segs = get_straight_linked_segs(seg, downstream=True, verbose=True)
    upstream_segs = get_straight_linked_segs(seg, downstream=False, verbose=True)

    while x > len_seg:
        x -= len_seg
        seg = downstream_segs.__next__()
        len_seg = get_seg_len(seg)

    while x < 0:
        seg = upstream_segs.__next__()
        len_seg = get_seg_len(seg)
        x += len_seg

    return seg, x
