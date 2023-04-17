#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database.load_sheets import load_sheet, get_cols_name
from .cbtc_territory_utils import is_point_in_cbtc_ter


def get_sigs_outside_cbtc_ter():
    sig_dict = load_sheet("sig")
    sig_cols_name = get_cols_name("sig")
    outside_cbtc_sig_dict = dict()
    for sig_name, sig_values in sig_dict.items():
        seg = sig_values[sig_cols_name['C']]
        x = float(sig_values[sig_cols_name['D']])
        if is_point_in_cbtc_ter(seg, x) is not True:
            outside_cbtc_sig_dict[sig_name] = sig_values
        if is_point_in_cbtc_ter(seg, x) is None:
            print_warning(f"Signal {sig_name} is on a limit of CBTC Territory. "
                          f"It is still taken into account.")
    return outside_cbtc_sig_dict


def get_sigs_in_cbtc_ter():
    sig_dict = load_sheet("sig")
    sig_cols_name = get_cols_name("sig")

    within_cbtc_sig_dict = dict()
    for sig_name, sig_values in sig_dict.items():
        seg = sig_values[sig_cols_name['C']]
        x = float(sig_values[sig_cols_name['D']])
        if is_point_in_cbtc_ter(seg, x) is not False:
            within_cbtc_sig_dict[sig_name] = sig_values
        if is_point_in_cbtc_ter(seg, x) is None:
            print(f"Warning: Signal {sig_name} is on a limit of CBTC Territory.")
    return within_cbtc_sig_dict
