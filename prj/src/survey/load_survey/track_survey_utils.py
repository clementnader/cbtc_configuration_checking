#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ...dc_sys import *
from ..survey_utils import clean_track_name


__all__ = ["find_corresponding_dc_sys_track"]


def find_corresponding_dc_sys_track(survey_track: str) -> str:
    track_dict = load_sheet(DCSYS.Voie)
    set_dc_sys_tracks = {track.upper() for track in track_dict}
    return clean_track_name(survey_track, set_dc_sys_tracks)
