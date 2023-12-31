#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_get_cbtc_territory import *


__all__ = ["get_maz_in_cbtc_ter"]


def get_maz_in_cbtc_ter():
    maz_dict = load_sheet(DCSYS.Zaum)
    within_cbtc_maz_dict = dict()
    for maz_name, maz_value in maz_dict.items():
        limits_in_cbtc_ter: list[bool] = list()
        for seg, x in get_dc_sys_zip_values(maz_value, DCSYS.Zaum.Extremite.Seg, DCSYS.Zaum.Extremite.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if (any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter)
                and all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter)):
            within_cbtc_maz_dict[maz_name] = maz_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_log(f"MAZ {maz_name} is both inside and outside CBTC Territory. "
                      f"It is still taken into account.")
            within_cbtc_maz_dict[maz_name] = maz_value
    return within_cbtc_maz_dict
