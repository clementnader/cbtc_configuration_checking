#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_cbtc_direction_zone_related_signals"]


def get_cbtc_direction_zone_related_signals() -> dict[str, list[str]]:
    zsm_dict = load_sheet(DCSYS.ZSM_CBTC)
    zsm_signals_dict = dict()
    for zsm_name, zsm_value in zsm_dict.items():
        zsm_related_signals = get_dc_sys_value(zsm_value, DCSYS.ZSM_CBTC.SignauxZsm.Sigman)
        for sig in zsm_related_signals:
            if sig in zsm_signals_dict:
                zsm_signals_dict[sig].append(zsm_name)
            else:
                zsm_signals_dict[sig] = [zsm_name]
    return zsm_signals_dict
