#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dist_utils import get_dist


def get_len_block(block, block_lim_cols_name, seg_dict: dict, seg_cols_name: dict[str, str]):
    list_dist = list()
    for i, lim1 in enumerate(block["limits"]):
        seg1 = lim1[block_lim_cols_name[0]]
        x1 = lim1[block_lim_cols_name[1]]
        for lim2 in block["limits"][i+1:]:
            seg2 = lim2[block_lim_cols_name[0]]
            x2 = lim2[block_lim_cols_name[1]]
            list_dist.append(get_dist(seg1, x1, seg2, x2, seg_dict, seg_cols_name, verbose=False))
    return max(list_dist)
