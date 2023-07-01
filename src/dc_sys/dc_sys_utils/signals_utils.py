#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import DCSYS
from ..load_database import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


def get_sigs_outside_cbtc_ter():
    sig_dict = load_sheet(DCSYS.Sig)
    outside_cbtc_sig_dict = dict()
    for sig_name, sig_value in sig_dict.items():
        seg = get_dc_sys_value(sig_value, DCSYS.Sig.Seg)
        x = float(get_dc_sys_value(sig_value, DCSYS.Sig.X))
        if is_point_in_cbtc_ter(seg, x) is not True:
            outside_cbtc_sig_dict[sig_name] = sig_value
        if is_point_in_cbtc_ter(seg, x) is None:
            print_warning(f"Signal {sig_name} is on a limit of CBTC Territory. "
                          f"It is still taken into account.")
    return outside_cbtc_sig_dict


def get_sigs_in_cbtc_ter():
    sig_dict = load_sheet(DCSYS.Sig)

    within_cbtc_sig_dict = dict()
    for sig_name, sig_value in sig_dict.items():
        seg = get_dc_sys_value(sig_value, DCSYS.Sig.Seg)
        x = float(get_dc_sys_value(sig_value, DCSYS.Sig.X))
        if is_point_in_cbtc_ter(seg, x) is not False:
            within_cbtc_sig_dict[sig_name] = sig_value
        if is_point_in_cbtc_ter(seg, x) is None:
            print_warning(f"Signal {sig_name} is on a limit of CBTC Territory. "
                          f"It is still taken into account.")
    return within_cbtc_sig_dict
