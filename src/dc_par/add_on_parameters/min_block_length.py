#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def get_block_min_length_within_cbtc_ter():
    block_dict = load_sheet("block")
    block_lim_cols_name = get_lim_cols_name("block")

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    dict_min_block_within_cbtc_ter = dict()
    for block in block_dict:
        limits_in_cbtc_ter = list()
        for lim in block_dict[block]["limits"]:
            seg = lim[block_lim_cols_name[0]]
            x = lim[block_lim_cols_name[1]]
            limits_in_cbtc_ter.append(is_segment_in_cbtc_ter(seg, x))

        if all(limits_in_cbtc_ter):
            dict_min_block_within_cbtc_ter[block] = get_block_dist(block_dict[block], block_lim_cols_name,
                                                                   seg_dict, seg_cols_name)

    min_block = min(dict_min_block_within_cbtc_ter.values())
    list_min_block = [block for block in dict_min_block_within_cbtc_ter
                      if dict_min_block_within_cbtc_ter[block] == min_block]
    print(f"\nMin block length in CBTC Territory:"
          f"\n{min_block=}"
          f"\nfor {list_min_block}")
    return dict_min_block_within_cbtc_ter


def get_block_min_length_all_line():
    block_dict = load_sheet("block")
    block_lim_cols_name = get_lim_cols_name("block")

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    dict_min_block_within_cbtc_ter = dict()
    for block in block_dict:
        dict_min_block_within_cbtc_ter[block] = get_block_dist(block_dict[block], block_lim_cols_name,
                                                               seg_dict, seg_cols_name)

    min_block = min(dict_min_block_within_cbtc_ter.values())
    list_min_block = [block for block in dict_min_block_within_cbtc_ter
                      if dict_min_block_within_cbtc_ter[block] == min_block]
    print(f"\nMin block length on the full line:"
          f"\n{min_block=}"
          f"\nfor {list_min_block}")
    return dict_min_block_within_cbtc_ter
