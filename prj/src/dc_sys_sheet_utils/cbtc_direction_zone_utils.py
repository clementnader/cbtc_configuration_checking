#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_cbtc_direction_zone_related_signals"]


def get_cbtc_direction_zone_related_signals() -> dict[str, list[str]]:
    zsm_dict = load_sheet(DCSYS.ZSM_CBTC)
    zsm_sigs_dict = dict()
    for zsm_name, zsm_val in zsm_dict.items():
        zsm_related_sigs = get_dc_sys_value(zsm_val, DCSYS.ZSM_CBTC.SignauxZsm.Sigman)
        for sig in zsm_related_sigs:
            if sig in zsm_sigs_dict:
                zsm_sigs_dict[sig].append(zsm_name)
            else:
                zsm_sigs_dict[sig] = [zsm_name]
    return zsm_sigs_dict
