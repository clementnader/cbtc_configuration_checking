#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


__all__ = ["get_zsm_in_cbtc_ter"]


def get_zsm_in_cbtc_ter():
    zsm_dict = load_sheet(DCSYS.ZSM_CBTC)
    within_cbtc_zsm_dict = dict()
    for zsm_name, zsm_value in zsm_dict.items():
        limits_in_cbtc_ter = list()
        for seg, x in get_dc_sys_zip_values(zsm_value, DCSYS.ZSM_CBTC.ExtZsm.Seg, DCSYS.ZSM_CBTC.ExtZsm.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if (any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter)
                and all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter)):
            within_cbtc_zsm_dict[zsm_name] = zsm_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"{zsm_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_zsm_dict[zsm_name] = zsm_value
    return within_cbtc_zsm_dict
