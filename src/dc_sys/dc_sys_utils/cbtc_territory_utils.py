#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .segments_utils import *
from ..load_database.load_sheets import load_sheet, get_cols_name, get_lim_cols_name
from ...colors_pkg import *

CBTC_TER_SEGMENTS = list()
CBTC_TER_LIMITS = list()


def print_in_cbtc(in_cbtc: bool):
    text = Color.dark_cyan
    text += "in CBTC Territory" if in_cbtc else "on the full line"
    text += Color.reset
    return text


def get_segs_within_cbtc_ter():
    global CBTC_TER_SEGMENTS
    if not CBTC_TER_SEGMENTS:
        update_seg_within_cbtc_ter()
    return CBTC_TER_SEGMENTS


def get_all_segs_in_cbtc_ter():
    global CBTC_TER_SEGMENTS, CBTC_TER_LIMITS
    if not CBTC_TER_SEGMENTS or not CBTC_TER_LIMITS:
        update_seg_within_cbtc_ter()
    cbtc_ter_lim_cols_name = get_lim_cols_name("cbtc_ter")
    return CBTC_TER_SEGMENTS + [lim[cbtc_ter_lim_cols_name[0]] for lim in CBTC_TER_LIMITS]


def get_limits_cbtc_ter():
    global CBTC_TER_LIMITS
    if not CBTC_TER_LIMITS:
        update_seg_within_cbtc_ter()
    return CBTC_TER_LIMITS


def update_seg_within_cbtc_ter():
    global CBTC_TER_SEGMENTS
    if CBTC_TER_SEGMENTS:
        return
    cbtc_ter_dict = load_sheet("cbtc_ter")
    cbtc_ter_cols_name = get_cols_name("cbtc_ter")
    cbtc_ter_lim_cols_name = get_lim_cols_name("cbtc_ter")

    for cbtc_ter_values in cbtc_ter_dict.values():
        cbtc_type = cbtc_ter_values[cbtc_ter_cols_name['B']]
        if cbtc_type == "EN_CBTC":
            start_cbtc_limits = [lim for lim in cbtc_ter_values["limits"]
                                 if lim[cbtc_ter_lim_cols_name[2]] == "CROISSANT"]
            end_cbtc_limits = [lim for lim in cbtc_ter_values["limits"]
                               if lim[cbtc_ter_lim_cols_name[2]] == "DECROISSANT"]
            update_list_seg_lim(cbtc_ter_values["limits"])
            for start_lim in start_cbtc_limits:
                start_seg = start_lim[cbtc_ter_lim_cols_name[0]]
                CBTC_TER_SEGMENTS = get_next_segments(start_seg, end_cbtc_limits, CBTC_TER_SEGMENTS,
                                                      cbtc_ter_lim_cols_name)


def get_next_segments(start_seg, end_cbtc_limits, cbtc_ter_segments, cbtc_ter_lim_cols_name):
    # check downstream segments

    def inner_recurs_next_seg(seg):
        nonlocal cbtc_ter_segments
        if is_seg_end_limit(seg, end_cbtc_limits, cbtc_ter_lim_cols_name):
            return cbtc_ter_segments
        cbtc_ter_segments.append(seg)
        for next_seg in get_linked_segs(seg):
            if next_seg not in cbtc_ter_segments:
                inner_recurs_next_seg(next_seg)

    inner_recurs_next_seg(start_seg)
    return cbtc_ter_segments


def is_seg_end_limit(seg, end_cbtc_limits, cbtc_ter_lim_cols_name):
    return seg in (end_lim[cbtc_ter_lim_cols_name[0]] for end_lim in end_cbtc_limits)


def update_list_seg_lim(cbtc_limits):
    global CBTC_TER_LIMITS
    for lim in cbtc_limits:
        CBTC_TER_LIMITS.append(lim)


def is_seg_in_cbtc_ter_limits(seg):
    global CBTC_TER_LIMITS
    cbtc_ter_lim_cols_name = get_lim_cols_name("cbtc_ter")
    if not CBTC_TER_LIMITS:
        update_seg_within_cbtc_ter()
    if seg in [lim[cbtc_ter_lim_cols_name[0]] for lim in CBTC_TER_LIMITS]:
        return True
    return False


def is_seg_strictly_in_cbtc_ter(seg):
    global CBTC_TER_SEGMENTS
    if not CBTC_TER_SEGMENTS:
        update_seg_within_cbtc_ter()
    if seg in CBTC_TER_SEGMENTS:
        return True
    return False


def is_point_in_cbtc_ter(seg, x: float):
    global CBTC_TER_SEGMENTS, CBTC_TER_LIMITS
    x = float(x)
    if not CBTC_TER_SEGMENTS:
        update_seg_within_cbtc_ter()
    if seg in CBTC_TER_SEGMENTS:
        return True
    cbtc_ter_lim_cols_name = get_lim_cols_name("cbtc_ter")
    for lim in CBTC_TER_LIMITS:
        lim_seg = lim[cbtc_ter_lim_cols_name[0]]
        lim_x = float(lim[cbtc_ter_lim_cols_name[1]])
        lim_direction = lim[cbtc_ter_lim_cols_name[2]]
        if seg == lim_seg:
            if x == lim_x:  # limit point
                return None
            if lim_direction == "CROISSANT" and x > lim_x:
                return True
            if lim_direction == "DECROISSANT" and x < lim_x:
                return True
    return False
