#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import DCSYS
from ..load_database import *


def from_seg_offset_to_kp(seg, x):
    seg_dict = load_sheet(DCSYS.Seg)
    track = get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Voie)
    orig_kp = float(get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Origine))
    kp = round(orig_kp + float(x), 2)
    return track, kp


def from_kp_to_seg_offset(track, kp):
    seg_dict = load_sheet(DCSYS.Seg)
    for seg_name, seg_value in seg_dict.items():
        seg_track = get_dc_sys_value(seg_value, DCSYS.Seg.Voie)
        seg_orig_kp = float(get_dc_sys_value(seg_value, DCSYS.Seg.Origine))
        seg_end_kp = float(get_dc_sys_value(seg_value, DCSYS.Seg.Fin))
        if seg_track == track and seg_orig_kp <= kp <= seg_end_kp:
            x = kp - seg_orig_kp
            return seg_name, x
