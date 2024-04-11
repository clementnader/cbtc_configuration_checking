#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_walkways_track_kp_pos"]


def get_walkways_track_kp_pos():
    nb_max_limits = 0
    ww_dict = load_sheet(DCSYS.Walkways_Area)
    csv = str()
    for ww_name, ww in ww_dict.items():
        csv += f"{ww_name};"
        for i, (seg, x, direction) in enumerate(get_dc_sys_zip_values(ww, DCSYS.Walkways_Area.Limit.Seg,
                                                DCSYS.Walkways_Area.Limit.X, DCSYS.Walkways_Area.Limit.Direction),
                                                start=1):
            if i > nb_max_limits:
                nb_max_limits = i
            track, kp = from_seg_offset_to_kp(seg, x)
            csv += f"{track};{kp};{direction};"
        csv += "\n"
    header = "Walkways Area;" + ";".join([f"Limit {i};;" for i in range(1, nb_max_limits+1)])
    header += "\n;" + ";".join(["Track;KP;Direction" for _ in range(1, nb_max_limits+1)])
    csv = header + "\n" + csv
    print(csv)
