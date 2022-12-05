#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys_pkg import *
from dc_sys_checking.src.dc_sys_pkg.seg_utils import *


def get_sig_before_cbtc_exit(sig_dict: dict, sig_cols_name: dict[str, str]) -> list[str]:
    res_list = list()
    for sig in sig_dict:
        if sig_dict[sig][sig_cols_name['B']] == "PERMANENT_ARRET":  # \
            #     or sig_dict[sig][sig_cols_name['Z']] == "O":
            res_list.append(sig)
    return res_list


def min_dist_between_two_last_signals_before_cbtc_territory_exit(same_dir: bool = False):
    wb = load_wb()
    sh_sig = wb.sheet_by_name("Sig")
    sig_dict = get_dict(sh_sig, fixed_cols_ref=['B', 'C', 'D', 'E', 'Z'])
    sig_cols_name = get_cols_name(sh_sig, cols_ref=['B', 'C', 'D', 'E', 'Z'])
    sig_before_cbtc_exit = get_sig_before_cbtc_exit(sig_dict, sig_cols_name)

    sh_seg = wb.sheet_by_name("Seg")
    seg_dict = get_dict(sh_seg, fixed_cols_ref=['G', 'H', 'I', 'J', 'K'])
    seg_cols_name = get_cols_name(sh_seg, cols_ref=['G', 'H', 'I', 'J', 'K'])

    dict_min_dist = dict()

    for sig1 in sig_before_cbtc_exit:
        dir1 = sig_dict[sig1][sig_cols_name['E']]
        for sig2 in sig_dict:
            if sig_dict[sig2][sig_cols_name['B']] != "HEURTOIR":
                if not same_dir or sig_dict[sig2][sig_cols_name['E']] == dir1:
                    d = get_sig_dist(sig1, sig2, sig_dict, sig_cols_name, seg_dict, seg_cols_name)
                    if d:
                        dict_min_dist[f"{sig1} to {sig2}"] = {"d": d}

    min_dist = min([dict_min_dist[sigs]['d'] for sigs in dict_min_dist])
    print(f"min_dist is {min_dist}"
          f"\nfor: {[sigs for sigs in dict_min_dist if dict_min_dist[sigs]['d'] == min_dist]}")

    return dict_min_dist
