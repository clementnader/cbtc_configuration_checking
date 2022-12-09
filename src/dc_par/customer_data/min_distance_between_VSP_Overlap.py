#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def get_sig_overlap(sig_dict: dict, sig_cols_name: dict[str, str]) -> list[str]:
    res_list = list()
    for sig in sig_dict:
        if sig_dict[sig][sig_cols_name['S']] == "O" and sig_dict[sig][sig_cols_name['B']] == "MANOEUVRE":
            res_list.append(sig)
    return res_list


def min_distance_between_vsp_overlap(same_dir: bool = False):
    sig_dict = load_sheet("sig")
    sig_cols_name = get_cols_name("sig")
    sig_overlap_dict = get_sig_overlap(sig_dict, sig_cols_name)

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    dict_min_dist = dict()

    delta_vsp_name = sig_cols_name['I']

    for sig_overlap in sig_overlap_dict:
        if delta_vsp_name in sig_dict[sig_overlap]:
            delta_vsp1 = float(sig_dict[sig_overlap][delta_vsp_name])
            vsp1_seg = sig_dict[sig_overlap][sig_cols_name['C']]
            vsp1_x = float(sig_dict[sig_overlap][sig_cols_name['D']]) + delta_vsp1
            sig_dir1 = sig_dict[sig_overlap][sig_cols_name['E']]
            vsp1_seg, vsp1_x = get_correct_seg_offset(vsp1_seg, vsp1_x, seg_dict, seg_cols_name)

            for sig in sig_dict:
                if sig_dict[sig][sig_cols_name['B']] != "HEURTOIR":
                    if delta_vsp_name in sig_dict[sig] \
                            and (not same_dir or sig_dict[sig][sig_cols_name['E']] == sig_dir1):

                        delta_vsp2 = float(sig_dict[sig][delta_vsp_name])
                        vsp2_seg = sig_dict[sig][sig_cols_name['C']]
                        vsp2_x = float(sig_dict[sig][sig_cols_name['D']]) + delta_vsp2
                        vsp2_seg, vsp2_x = get_correct_seg_offset(vsp2_seg, vsp2_x, seg_dict, seg_cols_name)

                        d = get_dist(vsp1_seg, vsp1_x, vsp2_seg, vsp2_x, seg_dict, seg_cols_name)
                        if d:
                            dict_min_dist[f"{sig_overlap} to {sig}"] = {"d": d}

    min_dist = min([dict_min_dist[vsps]['d'] for vsps in dict_min_dist])
    print(f"min_dist is {min_dist}"
          f"\nfor: {[vsps for vsps in dict_min_dist if dict_min_dist[vsps]['d'] == min_dist]}")
    return dict_min_dist
