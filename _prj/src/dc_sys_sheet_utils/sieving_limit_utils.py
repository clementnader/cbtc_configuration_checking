#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_sieving_limit_related_buffers"]


def get_sieving_limit_related_buffers():
    sieving_limit_dict = load_sheet(DCSYS.Sieving_Limit)
    signal_dict = load_sheet(DCSYS.Sig)
    for sl_name, sl_value in sieving_limit_dict.items():
        sl_type = get_dc_sys_value(sl_value, DCSYS.Sieving_Limit.Type)
        if sl_type != SievingLimitType.BUFFER:
            continue
        sl_position = get_object_position(DCSYS.Sieving_Limit, sl_name)
        for sig_name, sig_value in signal_dict.items():
            sig_type = get_dc_sys_value(sig_value, DCSYS.Sig.Type)
            if sig_type != SignalType.HEURTOIR:
                continue
            sig_position = get_object_position(DCSYS.Sig, sig_name)
            if sl_position == sig_position:
                print(sl_name, sig_name)
