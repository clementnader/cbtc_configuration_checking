#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_get_cbtc_territory import *


__all__ = ["get_slopes_in_cbtc_ter"]


def get_slopes_in_cbtc_ter():
    slope_dict = load_sheet(DCSYS.Profil)
    within_cbtc_slope_dict = dict()
    for slope, slope_info in slope_dict.items():
        slope_seg = get_dc_sys_value(slope_info, DCSYS.Profil.Seg)
        slope_x = float(get_dc_sys_value(slope_info, DCSYS.Profil.X))
        if is_point_in_cbtc_ter(slope_seg, slope_x) is not False:
            within_cbtc_slope_dict[slope] = slope_info
        if is_point_in_cbtc_ter(slope_seg, slope_x) is None:
            print_warning(f"Slope {slope} is defined on a limit of CBTC Territory. "
                          f"It is still taken into account."
                          f"\n\t{slope_info}")
    return within_cbtc_slope_dict
