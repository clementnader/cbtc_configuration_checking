#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ..load_database import *


__all__ = ["get_track_limits"]


def get_track_limits(track: str) -> tuple[float, float]:
    track_dict = load_sheet(DCSYS.Voie)
    start_kp = float(get_dc_sys_value(track_dict[track], DCSYS.Voie.PkDebut))
    end_kp = float(get_dc_sys_value(track_dict[track], DCSYS.Voie.PkFin))
    return start_kp, end_kp
