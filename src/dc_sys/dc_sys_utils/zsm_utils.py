#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database.load_sheets import load_sheet, get_cols_name
from .cbtc_territory_utils import is_point_in_cbtc_ter


def get_zsm_in_cbtc_ter():
    zsm_dict = load_sheet("zsm")
    zsm_cols_name = get_cols_name("zsm")
    within_cbtc_zsm_dict = dict()
    for zsm_name, zsm_value in zsm_dict.items():
        seg1 = zsm_value[zsm_cols_name['D']]
        x1 = zsm_value[zsm_cols_name['E']]
        seg2 = zsm_value[zsm_cols_name['H']]
        x2 = zsm_value[zsm_cols_name['I']]
        limits_in_cbtc_ter = [is_point_in_cbtc_ter(seg, x) for seg, x in ((seg1, x1), (seg2, x2))]

        if all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter):
            within_cbtc_zsm_dict[zsm_name] = zsm_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"{zsm_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_zsm_dict[zsm_name] = zsm_value
    return within_cbtc_zsm_dict
