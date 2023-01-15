#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *
from ...colors_pkg import *


def get_sig_before_cbtc_exit(sig_dict: dict, sig_cols_name: dict[str, str]) -> list[str]:
    res_list = list()
    for sig, sig_values in sig_dict.items():
        if sig_values[sig_cols_name['B']] == "PERMANENT_ARRET":  # \
            #     or sig_values[sig_cols_name['Z']] == "O":
            res_list.append(sig)
    return res_list


def min_dist_between_two_last_signals_before_cbtc_territory_exit(same_dir: bool = True):
    sig_dict = get_sigs_in_cbtc_ter()
    sig_cols_name = get_cols_name("sig")
    sig_before_cbtc_exit = get_sig_before_cbtc_exit(sig_dict, sig_cols_name)
    nb_sig_before_exit = len(sig_before_cbtc_exit)

    dict_min_dist = dict()
    for i, sig1 in enumerate(sig_before_cbtc_exit):
        print_log(f"\t {i/nb_sig_before_exit:.2%} processing distances between {sig1} "
                  f"and previous last signal before CBTC territory exit...")
        dir1 = sig_dict[sig1][sig_cols_name['E']]
        seg1 = sig_dict[sig1][sig_cols_name['C']]
        x1 = float(sig_dict[sig1][sig_cols_name['D']])
        for sig2, sig2_values in sig_dict.items():
            if sig2 != sig1 and sig2_values[sig_cols_name['B']] != "HEURTOIR":
                if not same_dir or sig2_values[sig_cols_name['E']] == dir1:
                    seg2 = sig2_values[sig_cols_name['C']]
                    x2 = float(sig2_values[sig_cols_name['D']])
                    d = get_dist(seg1, x1, seg2, x2)
                    if d is not None:
                        dict_min_dist[f"{sig1} to {sig2}"] = {"d": d}

    min_dist = min(min_dist['d'] for min_dist in dict_min_dist.values())
    print(f"The minimum distance between the two last signals before any CBTC territory exit is"
          f"\n{min_dist=}"
          f"\n > for: {[sigs for sigs, sigs_values in dict_min_dist.items() if sigs_values['d'] == min_dist]}")
    return dict_min_dist
