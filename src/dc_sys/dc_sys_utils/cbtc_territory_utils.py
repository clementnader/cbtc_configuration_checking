#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import DCSYS
from ..load_database import *
from .segments_utils import *


CBTC_TER_SEGMENTS = list()
CBTC_TER_LIMITS = list()


def print_in_cbtc(in_cbtc: bool):
    text = Color.yellow
    text += "in CBTC Territory" if in_cbtc else "on the full line"
    text += Color.reset
    return text


def get_segs_within_cbtc_ter():
    global CBTC_TER_SEGMENTS
    if not CBTC_TER_SEGMENTS:
        update_segs_within_cbtc_ter()
    return CBTC_TER_SEGMENTS


def get_all_segs_in_cbtc_ter():
    global CBTC_TER_SEGMENTS, CBTC_TER_LIMITS
    if not CBTC_TER_SEGMENTS or not CBTC_TER_LIMITS:
        update_segs_within_cbtc_ter()
    return CBTC_TER_SEGMENTS + [seg for seg, _, _ in CBTC_TER_LIMITS]


def get_limits_cbtc_ter():
    global CBTC_TER_LIMITS
    if not CBTC_TER_LIMITS:
        update_segs_within_cbtc_ter()
    return CBTC_TER_LIMITS


def update_segs_within_cbtc_ter():
    global CBTC_TER_SEGMENTS
    if CBTC_TER_SEGMENTS:
        return

    start_cbtc_limits, end_cbtc_limits = get_start_and_end_limits_cbtc_ter()

    for start_lim in start_cbtc_limits:
        start_seg, _, _ = start_lim
        get_next_segments(start_seg, end_cbtc_limits, CBTC_TER_SEGMENTS)

    update_list_seg_lim(start_cbtc_limits)
    update_list_seg_lim(end_cbtc_limits)


def get_start_and_end_limits_cbtc_ter():
    cbtc_ter_dict = load_sheet(DCSYS.CBTC_TER)
    start_cbtc_limits = list()
    end_cbtc_limits = list()

    for cbtc_ter_value in cbtc_ter_dict.values():
        cbtc_type = get_dc_sys_value(cbtc_ter_value, DCSYS.CBTC_TER.TypeTerritoireCbtc)
        if cbtc_type == "EN_CBTC":
            for seg, x, direction in get_dc_sys_zip_values(cbtc_ter_value, DCSYS.CBTC_TER.Extremite.Seg,
                                                           DCSYS.CBTC_TER.Extremite.X, DCSYS.CBTC_TER.Extremite.Sens):
                if direction == "CROISSANT":
                    start_cbtc_limits.append((seg, x, direction))
                else:
                    end_cbtc_limits.append((seg, x, direction))

    for start_lim in start_cbtc_limits[:]:
        start_lim_seg, start_lim_x, _ = start_lim
        for end_lim in end_cbtc_limits[:]:
            end_lim_seg, end_lim_x, _ = end_lim
            if (start_lim_seg, start_lim_x) == (end_lim_seg, end_lim_x):  # a limit between two in-CBTC Territories
                start_cbtc_limits.remove(start_lim)
                end_cbtc_limits.remove(end_lim)

    return start_cbtc_limits, end_cbtc_limits


def get_next_segments(start_seg, end_cbtc_limits, cbtc_ter_segments):
    # check downstream segments

    def inner_recurs_next_seg(seg):
        nonlocal cbtc_ter_segments
        if is_seg_end_limit(seg, end_cbtc_limits):
            return cbtc_ter_segments
        cbtc_ter_segments.append(seg)
        for next_seg in get_linked_segs(seg):
            if next_seg not in cbtc_ter_segments:
                inner_recurs_next_seg(next_seg)

    inner_recurs_next_seg(start_seg)


def is_seg_end_limit(seg, end_cbtc_limits):
    return seg in (end_seg for end_seg, _, _ in end_cbtc_limits)


def update_list_seg_lim(cbtc_limits):
    global CBTC_TER_LIMITS
    for lim in cbtc_limits:
        CBTC_TER_LIMITS.append(lim)


def is_seg_in_cbtc_ter_limits(seg):
    global CBTC_TER_LIMITS
    if not CBTC_TER_LIMITS:
        update_segs_within_cbtc_ter()
    if seg in (lim_seg for lim_seg, _, _ in CBTC_TER_LIMITS):
        return True
    return False


def is_seg_strictly_in_cbtc_ter(seg):
    global CBTC_TER_SEGMENTS
    if not CBTC_TER_SEGMENTS:
        update_segs_within_cbtc_ter()
    if seg in CBTC_TER_SEGMENTS:
        return True
    return False


def is_point_in_cbtc_ter(seg, x: float):
    global CBTC_TER_SEGMENTS, CBTC_TER_LIMITS
    x = float(x)
    if not CBTC_TER_SEGMENTS:
        update_segs_within_cbtc_ter()
    if seg in CBTC_TER_SEGMENTS:
        return True
    for lim in CBTC_TER_LIMITS:
        lim_seg, lim_x, lim_direction = lim
        if seg == lim_seg:
            if x == lim_x:  # limit point
                return None
            if lim_direction == "CROISSANT" and x > lim_x:
                return True
            if lim_direction == "DECROISSANT" and x < lim_x:
                return True
    return False
