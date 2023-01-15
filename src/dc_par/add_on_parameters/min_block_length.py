#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def get_block_min_length(in_cbtc: bool = True):
    if in_cbtc:
        block_dict = get_blocks_in_cbtc_ter()
    else:
        block_dict = load_sheet("block")

    dict_len_block = dict()
    for block, block_values in block_dict.items():
        dict_len_block[block] = get_len_block(block_values)

    min_block = min(dict_len_block.values())
    list_min_block = [block for block, block_values in dict_len_block.items()
                      if block_values == min_block]
    print(f"The minimum block length is, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_block=}"
          f"\n > for {list_min_block}")
    return dict_len_block
