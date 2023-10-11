#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


__all__ = ["get_traction_power_zones_in_cbtc_ter"]


def get_traction_power_zones_in_cbtc_ter():
    tpz_dict = load_sheet(DCSYS.SS)

    within_cbtc_tpz_dict = dict()
    for tpz_name, tpz_value in tpz_dict.items():
        limits_in_cbtc_ter = list()
        for seg, x in get_dc_sys_zip_values(tpz_value, DCSYS.SS.Extremite.Seg, DCSYS.SS.Extremite.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter) and \
                all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter):
            within_cbtc_tpz_dict[tpz_name] = tpz_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"Traction Power Zone {tpz_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_tpz_dict[tpz_name] = tpz_value
    return within_cbtc_tpz_dict
