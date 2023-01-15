#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database.load_sheets import load_sheet, get_cols_name
from .cbtc_territory_utils import is_point_in_cbtc_ter
from ...colors_pkg import *


def get_plts_in_cbtc_ter():
    plt_dict = load_sheet("plt")
    plt_cols_name = get_cols_name("plt")
    within_cbtc_plt_dict = dict()
    for plt_name, plt_values in plt_dict.items():
        left_limit_seg = plt_values[plt_cols_name['I']]
        left_limit_x = plt_values[plt_cols_name['J']]
        right_limit_seg = plt_values[plt_cols_name['Q']]
        right_limit_x = plt_values[plt_cols_name['R']]

        left_in_cbtc = is_point_in_cbtc_ter(left_limit_seg, left_limit_x)
        right_in_cbtc = is_point_in_cbtc_ter(right_limit_seg, right_limit_x)
        if all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in (left_in_cbtc, right_in_cbtc)):
            within_cbtc_plt_dict[plt_name] = plt_values
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in (left_in_cbtc, right_in_cbtc)):
            print_warning(f"Platform {plt_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_plt_dict[plt_name] = plt_values
    return within_cbtc_plt_dict
