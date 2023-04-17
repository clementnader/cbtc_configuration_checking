#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database.load_sheets import load_sheet, get_cols_name


def get_track_limits(track: str) -> tuple[float, float]:
    track_dict = load_sheet("track")
    track_cols_name = get_cols_name("track")
    start_kp = float(track_dict[track][track_cols_name['G']])
    end_kp = float(track_dict[track][track_cols_name['H']])
    return start_kp, end_kp
