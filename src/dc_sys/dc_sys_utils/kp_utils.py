#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database.load_sheets import load_sheet, get_cols_name


def from_seg_offset_to_kp(seg, x):
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    track = seg_dict[seg][seg_cols_name['D']]
    orig_kp = float(seg_dict[seg][seg_cols_name['E']])
    kp = round(orig_kp + float(x), 2)
    return track, kp


def from_kp_to_seg_offset(track, kp):
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    for seg_name, seg_values in seg_dict.items():
        seg_track = seg_values[seg_cols_name['D']]
        seg_orig_kp = float(seg_values[seg_cols_name['E']])
        seg_end_kp = float(seg_values[seg_cols_name['F']])
        if seg_track == track and seg_orig_kp <= kp <= seg_end_kp:
            x = kp - seg_orig_kp
            return seg_name, x
