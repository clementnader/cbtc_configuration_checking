#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


__all__ = ["get_asr_in_cbtc_ter"]


def get_asr_in_cbtc_ter():
    asr_dict = load_sheet(DCSYS.ASR)

    within_cbtc_asr_dict = dict()
    for asr_name, asr_value in asr_dict.items():
        limits_in_cbtc_ter = list()
        for seg, x in get_dc_sys_zip_values(asr_value, DCSYS.ASR.Limit.Seg, DCSYS.ASR.Limit.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if (any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter)
                and all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter)):
            within_cbtc_asr_dict[asr_name] = asr_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"Automatic Speed Restriction {asr_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_asr_dict[asr_name] = asr_value
    return within_cbtc_asr_dict
