#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from .load_psr_inputs import get_psr_definition


__all__ = ["check_psr_41_42", "load_psr_info_tracks_41_42"]


def check_psr_41_42():
    input_psr_dict = get_psr_definition()
    dc_sys_psr_dict = load_psr_info_tracks_41_42()
    pretty_print_dict(input_psr_dict)


def load_psr_info_tracks_41_42():
    psr_dict = load_sheet(DCSYS.ZLPV)
    dc_sys_psr_dict = dict()
    for track_name in ("TRACK_41", "TRACK_42"):
        psr_sub_dict_track = dict()
        for key, val in psr_dict.items():
            if get_dc_sys_value(val, DCSYS.ZLPV.De.Voie) == track_name:
                if get_dc_sys_value(val, DCSYS.ZLPV.A.Voie) != track_name:
                    print_error(f"PSR {key} has different start and end tracks:\n"
                                f"start_track = {get_dc_sys_value(val, DCSYS.ZLPV.De.Voie)}"
                                f"end_track = {get_dc_sys_value(val, DCSYS.ZLPV.A.Voie)}")
                psr_sub_dict_track[key] = {"speed": get_dc_sys_value(val, DCSYS.ZLPV.VitesseZlpv),
                                           "from_kp": get_dc_sys_value(val, DCSYS.ZLPV.De.Pk),
                                           "to_kp": get_dc_sys_value(val, DCSYS.ZLPV.A.Pk)}
        dc_sys_psr_dict[track_name] = psr_sub_dict_track
    return dc_sys_psr_dict
