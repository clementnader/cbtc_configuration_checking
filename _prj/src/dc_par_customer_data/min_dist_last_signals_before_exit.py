#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_get_cbtc_territory import *
from ..dc_sys_draw_path.dc_sys_path_and_distances import get_dist


__all__ = ["min_dist_between_two_last_signals_before_cbtc_territory_exit"]


def get_sig_before_cbtc_exit(sig_dict: dict) -> list[str]:
    res_list = list()
    for sig, sig_value in sig_dict.items():
        if get_dc_sys_value(sig_value, DCSYS.Sig.SortieTerritoireCbtc) == YesOrNo.O:
        # if (get_dc_sys_value(sig_value, DCSYS.Sig.SortieTerritoireCbtc) == YesOrNo.O
        #         or get_dc_sys_value(sig_value, DCSYS.Sig.Type) == SignalType.PERMANENT_ARRET):
            res_list.append(sig)
    return res_list


def min_dist_between_two_last_signals_before_cbtc_territory_exit(same_dir: bool = True):
    sig_dict = get_objects_in_cbtc_ter(DCSYS.Sig)
    sig_before_cbtc_exit = get_sig_before_cbtc_exit(sig_dict)
    nb_sig_before_exit = len(sig_before_cbtc_exit)

    dict_min_dist = dict()
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, sig1 in enumerate(sig_before_cbtc_exit):
        print_log_progress_bar(i, nb_sig_before_exit, f"distance between {sig1} and previous last signal")
        seg1, x1, dir1 = get_dc_sys_values(sig_dict[sig1], DCSYS.Sig.Seg, DCSYS.Sig.X, DCSYS.Sig.Sens)
        for sig2, sig2_value in sig_dict.items():
            seg2, x2, dir2, sig_type2 = get_dc_sys_values(sig_dict[sig2], DCSYS.Sig.Seg, DCSYS.Sig.X, DCSYS.Sig.Sens,
                                                          DCSYS.Sig.Type)
            if sig2 != sig1 and sig_type2 != SignalType.HEURTOIR:
                if not same_dir or dir2 == dir1:
                    d = get_dist(seg1, x1, seg2, x2)
                    if d is not None:
                        dict_min_dist[f"{sig1} to {sig2}"] = {"d": d}
    print_log_progress_bar(nb_sig_before_exit, nb_sig_before_exit, "computation of distances between two last "
                           "signals before CBTC Territory exit finished", end=True)

    min_dist = min(min_dist["d"] for min_dist in dict_min_dist.values())
    print(f"The minimum distance between the two last signals before any CBTC territory exit is"
          f"\n{min_dist = }"
          f"\n > for: {[signals for signals, signals_value in dict_min_dist.items() if signals_value['d'] == min_dist]}\n")
    return dict_min_dist
