#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *


__all__ = ["from_seg_offset_to_kp", "from_kp_to_seg_offset"]


def from_seg_offset_to_kp(seg: str, x: float) -> tuple[str, float]:
    seg_dict = load_sheet(DCSYS.Seg)
    track = get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Voie)
    orig_kp = float(get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Origine))
    end_kp = float(get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Fin))
    if orig_kp <= end_kp:
        kp = round(orig_kp + float(x), 2)
    else:
        kp = round(orig_kp - float(x), 2)
    return track, kp


def from_kp_to_seg_offset(track: str, kp: float) -> tuple[Optional[str], Optional[float]]:
    seg_dict = load_sheet(DCSYS.Seg)
    for seg_name, seg_value in seg_dict.items():
        seg_track = get_dc_sys_value(seg_value, DCSYS.Seg.Voie)
        seg_orig_kp = float(get_dc_sys_value(seg_value, DCSYS.Seg.Origine))
        seg_end_kp = float(get_dc_sys_value(seg_value, DCSYS.Seg.Fin))
        if seg_orig_kp <= seg_end_kp:
            if seg_track == track and seg_orig_kp <= kp <= seg_end_kp:
                x = kp - seg_orig_kp
                return seg_name, x
        else:
            if seg_track == track and seg_end_kp <= kp <= seg_orig_kp:
                x = seg_orig_kp - kp
                return seg_name, x
    print_error(f"Unable to find a corresponding (segment, offset) for {(track, kp) = })")
    return None, None
