#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .load_xl import *
from .extract_xl import *
from .seg_utils import *


def get_seg_within_cbtc_ter():
    wb = load_wb()
    sh_cbtc_ter = wb.sheet_by_name("CBTC_TER")
    cbtc_ter_dict = get_dict(sh_cbtc_ter, fixed_cols_ref=['B'], lim_first_col='I', nb_max_limits=15,
                             delta_between_limits=3)
    cbtc_ter_cols_name = get_cols_name(sh_cbtc_ter, cols_ref=['B'])
    cbtc_ter_lim_cols_name = get_lim_cols_name(sh_cbtc_ter, col_ref='I', delta_between_limits=3)

    sh_seg = wb.sheet_by_name("Seg")
    seg_dict = get_dict(sh_seg, fixed_cols_ref=['G', 'H', 'I', 'J', 'K'])
    seg_cols_name = get_cols_name(sh_seg, cols_ref=['G', 'H', 'I', 'J', 'K'])

    for cbtc_ter in cbtc_ter_dict:
        cbtc_type = cbtc_ter_dict[cbtc_ter][cbtc_ter_cols_name['B']]
        if cbtc_type == "EN_CBTC":
            start_cbtc_limits = [lim for lim in cbtc_ter_dict[cbtc_ter]["limits"]
                                 if lim[cbtc_ter_lim_cols_name[2]] == "CROISSANT"]
            end_cbtc_limits = [lim for lim in cbtc_ter_dict[cbtc_ter]["limits"]
                               if lim[cbtc_ter_lim_cols_name[2]] == "DECROISSANT"]
            for lim in start_cbtc_limits:
                lim_seg = lim[cbtc_ter_lim_cols_name[0]]
                lim_x = float(lim[cbtc_ter_lim_cols_name[1]])


def get_next_limits(lim_seg, end_cbtc_limits, cbtc_ter_lim_cols_name, seg_dict: dict,
                    seg_cols_name: dict[str, str]):  # check downstream segments

    ref_cols = ['J', 'K']
    linked_segs = list()
    linked_seg = lim_seg
    found = False
    while linked_seg and not found:
        linked_segs.append(linked_seg)
        found = check_limit(linked_seg, end_cbtc_limits, cbtc_ter_lim_cols_name)
        if not found:
            linked_seg = get_linked_segs(seg=linked_seg, seg_dict=seg_dict, seg_cols_name=seg_cols_name, upstream=False)

    if not closest_plt:  # no more linked_seg
        return "End of Track", None

    return closest_plt, linked_segs


def check_limit(linked_seg, end_cbtc_limits, cbtc_ter_lim_cols_name):
    for lim in end_cbtc_limits:
        lim_seg = lim[cbtc_ter_lim_cols_name[0]]
        if lim_seg == linked_seg:
            return True
    return False
