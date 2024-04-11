#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_cbtc_direction_zone_related_signals"]


def get_cbtc_direction_zone_related_signals() -> list[tuple[str, str]]:
    zsm_dict = load_sheet(DCSYS.ZSM_CBTC)
    list_zsm_sigs = list()
    for zsm_name, zsm_val in zsm_dict.items():
        zsm_related_sigs = get_dc_sys_value(zsm_val, DCSYS.ZSM_CBTC.SignauxZsm.Sigman)
        for sig in zsm_related_sigs:
            list_zsm_sigs.append((sig, zsm_name))
    return list_zsm_sigs
