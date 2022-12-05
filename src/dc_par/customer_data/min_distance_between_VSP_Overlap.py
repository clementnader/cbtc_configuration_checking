#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys_pkg import *
from dc_sys_checking.src.dc_sys_pkg.seg_utils import *


def get_sig_overlap(sig_dict: dict, sig_cols_name: dict[str, str]) -> list[str]:
    res_list = list()
    for sig in sig_dict:
        if sig_dict[sig][sig_cols_name['S']] == "O" and sig_dict[sig][sig_cols_name['B']] == "MANOEUVRE":
            res_list.append(sig)
    return res_list


def min_distance_between_vsp_overlap(same_dir: bool = False):
    wb = load_wb()
    sh_sig = wb.sheet_by_name("Sig")
    sig_dict = get_dict(sh_sig, fixed_cols_ref=['B', 'C', 'D', 'E', 'I', 'S'])
    sig_cols_name = get_cols_name(sh_sig, cols_ref=['B', 'C', 'D', 'E', 'I', 'S'])
    sig_overlap_dict = get_sig_overlap(sig_dict, sig_cols_name)

    sh_seg = wb.sheet_by_name("Seg")
    seg_dict = get_dict(sh_seg, fixed_cols_ref=['G', 'H', 'I', 'J', 'K'])
    seg_cols_name = get_cols_name(sh_seg, cols_ref=['G', 'H', 'I', 'J', 'K'])

    dict_min_dist = dict()

    delta_vsp_name = sig_cols_name['I']

    for sig_overlap in sig_overlap_dict:
        if delta_vsp_name in sig_dict[sig_overlap]:
            delta_vsp1 = float(sig_dict[sig_overlap][delta_vsp_name])
            vsp1_seg = sig_dict[sig_overlap][sig_cols_name['C']]
            vsp1_x = float(sig_dict[sig_overlap][sig_cols_name['D']]) + delta_vsp1
            sig_dir1 = sig_dict[sig_overlap][sig_cols_name['E']]
            for sig in sig_dict:
                if sig_dict[sig][sig_cols_name['B']] != "HEURTOIR":
                    if delta_vsp_name in sig_dict[sig] \
                            and (not same_dir or sig_dict[sig][sig_cols_name['E']] == sig_dir1):

                        delta_vsp2 = float(sig_dict[sig][delta_vsp_name])
                        vsp2_seg = sig_dict[sig][sig_cols_name['C']]
                        vsp2_x = float(sig_dict[sig][sig_cols_name['D']]) + delta_vsp2

                        d = get_straight_dist(vsp1_seg, vsp1_x, vsp2_seg, vsp2_x, seg_dict, seg_cols_name)
                        if d:
                            dict_min_dist[f"{sig_overlap} to {sig}"] = {"d": d}

    min_dist = min([dict_min_dist[vsps]['d'] for vsps in dict_min_dist])
    print(f"min_dist is {min_dist}"
          f"\nfor: {[vsps for vsps in dict_min_dist if dict_min_dist[vsps]['d'] == min_dist]}")
    return dict_min_dist
