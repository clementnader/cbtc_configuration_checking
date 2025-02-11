#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_get_cbtc_territory import *
from ..dc_sys_sheet_utils.block_utils import get_list_len_block


__all__ = ["get_block_min_length", "get_block_max_length"]


def get_block_min_length(in_cbtc: bool = False):
    if in_cbtc:
        block_dict = get_objects_in_cbtc_ter(DCSYS.CDV)
    else:
        block_dict = load_sheet(DCSYS.CDV)

    dict_len_block = dict()
    for block, block_value in block_dict.items():
        dict_len_block[block] = min(get_list_len_block(block_value))

    min_block = min(dict_len_block.values())
    list_min_block = [block for block, block_value in dict_len_block.items()
                      if block_value == min_block]
    print(f"The minimum block length is, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_block = }"
          f"\n > for {list_min_block}")
    return sort_dict(dict_len_block)


def get_block_max_length(in_cbtc: bool = False):
    if in_cbtc:
        block_dict = get_objects_in_cbtc_ter(DCSYS.CDV)
    else:
        block_dict = load_sheet(DCSYS.CDV)

    dict_len_block = dict()
    for block, block_value in block_dict.items():
        dict_len_block[block] = max(get_list_len_block(block_value))

    max_block = max(dict_len_block.values())
    list_max_block = [block for block, block_value in dict_len_block.items()
                      if block_value == max_block]
    print(f"The maximum block length is, {print_in_cbtc(in_cbtc)}:"
          f"\n{max_block = }"
          f"\n > for {list_max_block}")
    return sort_dict(dict_len_block, reverse=True)


def sort_dict(dict_len_block, reverse: bool = False):
    keys = sorted(dict_len_block, key=lambda x: dict_len_block[x], reverse=reverse)
    sorted_dict = {x: dict_len_block[x] for x in keys}
    return sorted_dict
