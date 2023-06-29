#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database.load_sheets import load_sheet, get_cols_name
from .cbtc_territory_utils import get_all_segs_in_cbtc_ter


def get_track_limits(track: str) -> tuple[float, float]:
    track_dict = load_sheet("track")
    track_cols_name = get_cols_name("track")
    start_kp = float(track_dict[track][track_cols_name['G']])
    end_kp = float(track_dict[track][track_cols_name['H']])
    return start_kp, end_kp


def get_track_in_cbtc_ter():
    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")
    list_tracks = list()
    for seg in get_all_segs_in_cbtc_ter():
        track = seg_dict[seg][seg_cols_name['D']]
        if track not in list_tracks:
            list_tracks.append(track)
    return sorted(list_tracks)
