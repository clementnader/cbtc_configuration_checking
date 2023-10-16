#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_common_utils import *


__all__ = ["get_segs_within_cbtc_ter", "get_cbtc_ter_limits", "get_all_segs_in_cbtc_ter",
           "is_point_in_cbtc_ter", "print_in_cbtc"]


CBTC_TER_SEGMENTS: list[(str, bool)] = list()
CBTC_TER_LIMITS: list[tuple[str, float, bool]] = list()


def print_in_cbtc(in_cbtc: bool) -> str:
    text = Color.yellow
    text += "in CBTC Territory" if in_cbtc else "on the full line"
    text += Color.reset
    return text


def get_segs_within_cbtc_ter() -> set[str]:
    global CBTC_TER_SEGMENTS
    if not CBTC_TER_SEGMENTS:
        update_segs_within_cbtc_ter()
    return set([seg for seg, _ in CBTC_TER_SEGMENTS])


def get_all_segs_in_cbtc_ter() -> set[str]:
    cbtc_ter_segments = get_segs_within_cbtc_ter()
    cbtc_ter_limits = get_cbtc_ter_limits()
    return cbtc_ter_segments.union([seg for seg, _, _ in cbtc_ter_limits])


def get_cbtc_ter_limits() -> list[tuple[str, float, bool]]:
    global CBTC_TER_LIMITS
    if not CBTC_TER_LIMITS:
        update_segs_within_cbtc_ter()
    return CBTC_TER_LIMITS


def update_segs_within_cbtc_ter() -> None:
    global CBTC_TER_SEGMENTS
    if CBTC_TER_SEGMENTS:
        return

    cbtc_limits = get_start_and_end_limits_cbtc_ter()

    for start_lim in cbtc_limits:
        start_seg, start_x, start_direction = start_lim
        get_next_segments(start_seg, start_x, start_direction, cbtc_limits)

    update_list_seg_lim(cbtc_limits)


def get_start_and_end_limits_cbtc_ter() -> list[tuple[str, float, bool]]:
    cbtc_ter_dict = load_sheet(DCSYS.CBTC_TER)
    cbtc_limits = list()

    for cbtc_ter_value in cbtc_ter_dict.values():
        cbtc_type = get_dc_sys_value(cbtc_ter_value, DCSYS.CBTC_TER.TypeTerritoireCbtc)
        if cbtc_type == CBTCTerrType.EN_CBTC:
            for seg, x, direction in get_dc_sys_zip_values(cbtc_ter_value, DCSYS.CBTC_TER.Extremite.Seg,
                                                           DCSYS.CBTC_TER.Extremite.X, DCSYS.CBTC_TER.Extremite.Sens):
                cbtc_limits.append((seg, x, (direction == Direction.CROISSANT)))

    return remove_useless_limits(cbtc_limits)


def remove_useless_limits(cbtc_limits: list[tuple[str, float, bool]]) -> list[tuple[str, float, bool]]:
    limits_to_remove = list()
    for seg, x, downstream in cbtc_limits:
        if (seg, x, not downstream) in cbtc_limits:
            limits_to_remove.append((seg, x, downstream))
            limits_to_remove.append((seg, x, not downstream))
    return [lim for lim in cbtc_limits if lim not in limits_to_remove]


def get_next_segments(start_seg: str, start_x: float, downstream: bool,
                      cbtc_limits: list[tuple[str, float, bool]]) -> None:
    global CBTC_TER_SEGMENTS

    if is_first_seg_on_another_limit(start_seg, start_x, downstream, cbtc_limits):
        return

    def inner_recurs_next_seg(seg: str, inner_downstream: bool):
        global CBTC_TER_SEGMENTS
        for next_seg in get_linked_segs(seg, inner_downstream):
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            if is_seg_end_limit(next_seg, next_inner_downstream, cbtc_limits):
                continue
            if (next_seg, next_inner_downstream) in CBTC_TER_SEGMENTS:
                continue
            CBTC_TER_SEGMENTS.append((next_seg, next_inner_downstream))
            inner_recurs_next_seg(next_seg, next_inner_downstream)

    inner_recurs_next_seg(start_seg, downstream)


def is_first_seg_on_another_limit(start_seg: str, start_x: float, downstream: bool,
                                  cbtc_limits: list[tuple[str, float, bool]]) -> bool:
    for limit_seg, limit_x, limit_downstream in cbtc_limits:
        if start_seg == limit_seg:
            if (downstream and start_x < limit_x) or (not downstream and start_x > limit_x):
                if not downstream == limit_downstream:
                    return True
                print_warning("Reach a CBTC Territory limit but with a different direction.")
                print(f"{start_seg = }, {start_x = }, {downstream = }")
                print((limit_seg, limit_x, limit_downstream))
                return True
    return False


def is_seg_end_limit(seg: str, downstream: bool, cbtc_limits: list[tuple[str, float, bool]]) -> bool:
    if (seg, not downstream) in [(limit_seg, limit_downstream) for limit_seg, _, limit_downstream in cbtc_limits]:
        return True
    if seg in [limit_seg for limit_seg, _, _ in cbtc_limits]:
        print_warning("Reach a CBTC Territory limit but with a different direction.")
        print(f"{seg = }, {downstream = }")
        print([(limit_seg, limit_downstream) for limit_seg, _, limit_downstream in cbtc_limits if seg == limit_seg])
        return True
    return False


def update_list_seg_lim(cbtc_limits: list[tuple[str, float, bool]]) -> None:
    global CBTC_TER_SEGMENTS, CBTC_TER_LIMITS
    segs_on_cbtc_limits = set([seg for seg, _, _ in cbtc_limits])
    for current_seg in segs_on_cbtc_limits:
        limits_on_seg = [lim for lim in cbtc_limits if lim[0] == current_seg]
        left_limits_on_seg = [lim for lim in limits_on_seg]
        for seg, x, downstream in limits_on_seg:
            if (seg, x, not downstream) in cbtc_limits:  # a limit between two IN CBTC Territory
                left_limits_on_seg.remove((seg, x, downstream))
            if ((downstream and x == 0 and not get_linked_segs(seg, downstream=False))
                    or (not downstream and x == get_seg_len(seg) and not get_linked_segs(seg, downstream=True))):
                left_limits_on_seg.remove((seg, x, downstream))
        if not left_limits_on_seg:
            CBTC_TER_SEGMENTS.append((current_seg, None))
            continue
        for seg, x, downstream in left_limits_on_seg:
            CBTC_TER_LIMITS.append((seg, x, downstream))


def is_point_in_cbtc_ter(seg: str, x: float, direction: str = None) -> Optional[bool]:
    x = float(x)
    cbtc_ter_segments = get_segs_within_cbtc_ter()
    cbtc_ter_limits = get_cbtc_ter_limits()
    if seg in cbtc_ter_segments:
        return True
    for lim in cbtc_ter_limits:
        lim_seg, lim_x, lim_downstream = lim
        if seg == lim_seg:
            if x == lim_x:  # limit point
                if direction is not None:
                    if lim_downstream == (direction == Direction.CROISSANT):
                        return True
                    else:
                        return False
                return None
            if lim_downstream and x > lim_x:
                return True
            if not lim_downstream and x < lim_x:
                return True
    return False
