#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_get_cbtc_territory import *


__all__ = ["get_tsr_area_in_cbtc_ter"]


def get_tsr_area_in_cbtc_ter():
    tsr_dict = load_sheet(DCSYS.TSR_Area)

    within_cbtc_tsr_dict = dict()
    for tsr_name, tsr_value in tsr_dict.items():
        limits_in_cbtc_ter = list()
        for seg, x in get_dc_sys_zip_values(tsr_value, DCSYS.TSR_Area.Limit.Seg, DCSYS.TSR_Area.Limit.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if (any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter)
                and all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter)):
            within_cbtc_tsr_dict[tsr_name] = tsr_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"Temporary Speed Restriction Area {tsr_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_tsr_dict[tsr_name] = tsr_value
    return within_cbtc_tsr_dict
