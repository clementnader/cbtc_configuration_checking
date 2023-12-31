#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_get_cbtc_territory import *


__all__ = ["get_platforms_in_cbtc_ter"]


def get_platforms_in_cbtc_ter():
    plt_dict = load_sheet(DCSYS.Quai)
    within_cbtc_plt_dict = dict()
    for plt_name, plt_value in plt_dict.items():
        limit_in_cbtc = list()
        for limit_seg, limit_x in get_dc_sys_zip_values(plt_value, DCSYS.Quai.ExtremiteDuQuai.Seg,
                                                        DCSYS.Quai.ExtremiteDuQuai.X):
            limit_in_cbtc.append(is_point_in_cbtc_ter(limit_seg, limit_x))

        if (any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limit_in_cbtc)
                and all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limit_in_cbtc)):
            within_cbtc_plt_dict[plt_name] = plt_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limit_in_cbtc):
            print_log(f"Platform {plt_name} is both inside and outside CBTC Territory. "
                      f"It is still taken into account.")
            within_cbtc_plt_dict[plt_name] = plt_value
    return within_cbtc_plt_dict
