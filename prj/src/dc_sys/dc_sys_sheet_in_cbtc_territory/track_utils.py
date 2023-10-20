#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_get_cbtc_territory import *


__all__ = ["get_track_in_cbtc_ter"]


def get_track_in_cbtc_ter() -> list[str]:
    seg_dict = load_sheet(DCSYS.Seg)
    list_tracks = list()
    for seg in get_all_segs_in_cbtc_ter():
        track = get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Voie)
        if track not in list_tracks:
            list_tracks.append(track)
    return sorted(list_tracks)
