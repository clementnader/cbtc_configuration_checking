#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_get_cbtc_territory import *


__all__ = ["get_cbtc_protection_zones_in_cbtc_ter"]


def get_cbtc_protection_zones_in_cbtc_ter():
    cbtc_pz_dict = load_sheet(DCSYS.CBTC_Protection_Zone)

    within_cbtc_cbtc_pz_dict = dict()
    for cbtc_pz_name, cbtc_pz_value in cbtc_pz_dict.items():
        limits_in_cbtc_ter = list()
        for seg, x in get_dc_sys_zip_values(cbtc_pz_value, DCSYS.CBTC_Protection_Zone.Limit.Seg,
                                            DCSYS.CBTC_Protection_Zone.Limit.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if (any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter)
                and all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter)):
            within_cbtc_cbtc_pz_dict[cbtc_pz_name] = cbtc_pz_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"cbtc_pz {cbtc_pz_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_cbtc_pz_dict[cbtc_pz_name] = cbtc_pz_value
    return within_cbtc_cbtc_pz_dict
