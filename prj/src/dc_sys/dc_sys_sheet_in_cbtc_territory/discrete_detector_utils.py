#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_get_cbtc_territory import *


__all__ = ["get_dd_in_cbtc_ter"]


def get_dd_in_cbtc_ter():
    dd_dict = load_sheet(DCSYS.DP)

    within_cbtc_dd_dict = dict()
    for dd_name, dd_value in dd_dict.items():
        seg = get_dc_sys_value(dd_value, DCSYS.DP.Seg)
        x = float(get_dc_sys_value(dd_value, DCSYS.DP.X))
        if is_point_in_cbtc_ter(seg, x) is not False:
            within_cbtc_dd_dict[dd_name] = dd_value
        if is_point_in_cbtc_ter(seg, x) is None:
            print_warning(f"Discrete Detector {dd_name} is on a limit of CBTC Territory. "
                          f"It is still taken into account.")
    return within_cbtc_dd_dict
