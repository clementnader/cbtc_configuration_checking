#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ...cctool_oo_schema import *
from ...dc_sys import *


__all__ = ["find_corresponding_dc_sys_track"]


def find_corresponding_dc_sys_track(survey_track: str) -> str:
    test_survey_track = survey_track.upper()
    track_dict = load_sheet(DCSYS.Voie)
    list_dc_sys_tracks = [track.upper() for track in track_dict]
    if test_survey_track in list_dc_sys_tracks:
        return test_survey_track

    if re.search("^TRACK_[0-9]+$", test_survey_track) is not None:
        track_number = test_survey_track.removeprefix("TRACK_")
        if f"T{track_number}" in list_dc_sys_tracks:
            return f"T{track_number}"
        if f"T{track_number.removeprefix('0')}" in list_dc_sys_tracks:
            return f"T{track_number.removeprefix('0')}"

    if re.search("_[VT]?[0-9]+[A-Z]$", test_survey_track) is not None:
        test_survey_track_without_letter = test_survey_track[:-1]  # without the last letter
        if test_survey_track_without_letter in list_dc_sys_tracks:
            return test_survey_track_without_letter

    return test_survey_track
