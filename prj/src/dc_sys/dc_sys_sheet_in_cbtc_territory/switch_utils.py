#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_common_utils import *
from ..dc_sys_get_cbtc_territory import *


__all__ = ["get_switches_in_cbtc_ter"]


def get_switches_in_cbtc_ter():
    sw_dict = load_sheet(DCSYS.Aig)
    within_cbtc_sw_dict = dict()
    for sw_name, sw_value in sw_dict.items():
        seg, x = give_sw_pos(sw_value)
        if is_point_in_cbtc_ter(seg, x) is not False:
            within_cbtc_sw_dict[sw_name] = sw_value
        if is_point_in_cbtc_ter(seg, x) is None:
            print_warning(f"Switch {sw_name} is on a limit of CBTC Territory. "
                          f"It is still taken into account.")
    return within_cbtc_sw_dict
