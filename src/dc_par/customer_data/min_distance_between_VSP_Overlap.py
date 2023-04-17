#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...dc_sys import *


def min_distance_between_vsp_overlap(in_cbtc: bool = True, same_dir: bool = True, verbose: bool = False):
    if in_cbtc:
        sig_dict = get_sigs_in_cbtc_ter()
    else:
        sig_dict = load_sheet("sig")
    sig_cols_name = get_cols_name("sig")
    home_sigs_with_overlap_list = get_home_signals_with_overlap(sig_dict, sig_cols_name)
    nb_home_sigs_with_overlap = len(home_sigs_with_overlap_list)

    dist_vsp_col_name = sig_cols_name['I']

    dict_min_dist = dict()
    for i, home_sig_with_overlap in enumerate(home_sigs_with_overlap_list):
        if dist_vsp_col_name in sig_dict[home_sig_with_overlap]:
            if verbose:
                print_log(f"\t {i/nb_home_sigs_with_overlap:.2%} processing distances between "
                          f"{home_sig_with_overlap} VSP and other signals VSPs...")
            dist_vsp1 = float(sig_dict[home_sig_with_overlap][dist_vsp_col_name])
            vsp1_seg = sig_dict[home_sig_with_overlap][sig_cols_name['C']]
            vsp1_x = float(sig_dict[home_sig_with_overlap][sig_cols_name['D']]) + dist_vsp1
            sig_dir1 = sig_dict[home_sig_with_overlap][sig_cols_name['E']]
            vsp1_seg, vsp1_x = get_correct_seg_offset(vsp1_seg, vsp1_x)

            for sig, sig_values in sig_dict.items():
                if sig != home_sig_with_overlap and sig_values[sig_cols_name['B']] != "HEURTOIR":
                    if dist_vsp_col_name in sig_values \
                            and (not same_dir or sig_values[sig_cols_name['E']] == sig_dir1):

                        dist_vsp2 = float(sig_values[dist_vsp_col_name])
                        vsp2_seg = sig_values[sig_cols_name['C']]
                        vsp2_x = float(sig_values[sig_cols_name['D']]) + dist_vsp2
                        vsp2_seg, vsp2_x = get_correct_seg_offset(vsp2_seg, vsp2_x)

                        d = get_dist(vsp1_seg, vsp1_x, vsp2_seg, vsp2_x)
                        if d is not None:
                            dict_min_dist[f"{home_sig_with_overlap} to {sig}"] = d

    min_dist = min(vsps_values for vsps_values in dict_min_dist.values())
    print(f"The minimum distance between two VSPs, one of whom is related to a Home Signal with Overlap is, "
          f"{print_in_cbtc(in_cbtc)}:"
          f"\n{min_dist=}"
          f"\n > for: {[vsps for vsps, vsps_values in dict_min_dist.items() if vsps_values == min_dist]}\n")
    return dict_min_dist


def get_home_signals_with_overlap(sig_dict: dict, sig_cols_name: dict[str, str]) -> list[str]:
    res_list = list()
    for sig, sig_values in sig_dict.items():
        if sig_values[sig_cols_name['S']] == "O" and sig_values[sig_cols_name['B']] == "MANOEUVRE":
            res_list.append(sig)
    return res_list
