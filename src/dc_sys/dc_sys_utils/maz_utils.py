#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database.load_sheets import load_sheet, get_lim_cols_name
from .cbtc_territory_utils import is_point_in_cbtc_ter


def get_maz_in_cbtc_ter():
    maz_dict = load_sheet("maz")
    maz_lim_cols_name = get_lim_cols_name("maz")
    within_cbtc_maz_dict = dict()
    for maz_name, maz_value in maz_dict.items():
        limits_in_cbtc_ter: list[bool] = list()
        for lim in maz_value["limits"]:
            seg = lim[maz_lim_cols_name[0]]
            x = lim[maz_lim_cols_name[1]]
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter):
            within_cbtc_maz_dict[maz_name] = maz_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"MAZ {maz_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_maz_dict[maz_name] = maz_value
    return within_cbtc_maz_dict
