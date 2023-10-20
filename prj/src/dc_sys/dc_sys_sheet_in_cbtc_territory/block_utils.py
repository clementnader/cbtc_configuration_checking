#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_get_cbtc_territory import *


__all__ = ["get_blocks_in_cbtc_ter"]


def get_blocks_in_cbtc_ter():
    block_dict = load_sheet(DCSYS.CDV)
    within_cbtc_block_dict = dict()
    for block, block_value in block_dict.items():
        limits_in_cbtc_ter = list()
        for seg, x in get_dc_sys_zip_values(block_value, DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if (any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter)
                and all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter)):
            within_cbtc_block_dict[block] = block_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"Block {block} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_block_dict[block] = block_value
    return within_cbtc_block_dict
