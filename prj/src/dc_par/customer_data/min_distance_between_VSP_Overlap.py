#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *


__all__ = ["min_distance_between_vsp_overlap"]


def min_distance_between_vsp_overlap(in_cbtc: bool = False, same_dir: bool = True):
    if in_cbtc:
        sig_dict = get_sigs_in_cbtc_ter()
    else:
        sig_dict = load_sheet(DCSYS.Sig)
    home_sigs_with_overlap_list = get_home_signals_with_overlap(sig_dict)
    nb_home_sigs_with_overlap = len(home_sigs_with_overlap_list)

    dict_min_dist = dict()
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, home_sig_with_overlap_name in enumerate(home_sigs_with_overlap_list):
        home_sig_with_overlap = sig_dict[home_sig_with_overlap_name]
        sig1_seg, sig1_x, sig1_dir, dist_vsp1 = get_dc_sys_values(home_sig_with_overlap, DCSYS.Sig.Seg, DCSYS.Sig.X,
                                                                  DCSYS.Sig.Sens, DCSYS.Sig.DistPap)
        if dist_vsp1 is not None:
            print_log(f"\r{progress_bar(i, nb_home_sigs_with_overlap)} processing distances between "
                      f"{home_sig_with_overlap_name} VSP and other signals VSPs...", end="")
            vsp1_seg, vsp1_x = get_correct_seg_offset(sig1_seg, sig1_x + dist_vsp1)
            for sig_name, sig_value in sig_dict.items():
                sig2_seg, sig2_x, sig2_dir, dist_vsp2 = get_dc_sys_values(sig_value, DCSYS.Sig.Seg, DCSYS.Sig.X,
                                                                          DCSYS.Sig.Sens, DCSYS.Sig.DistPap)
                sig2_type = get_dc_sys_value(sig_value, DCSYS.Sig.Type)
                if sig_name != home_sig_with_overlap_name and sig2_type != SignalType.HEURTOIR:
                    if dist_vsp2 is not None and (not same_dir or sig2_dir == sig1_dir):
                        vsp2_seg, vsp2_x = get_correct_seg_offset(sig2_seg, sig2_x + dist_vsp2)
                        d = get_dist(vsp1_seg, vsp1_x, vsp2_seg, vsp2_x)
                        if d is not None:
                            dict_min_dist[f"{home_sig_with_overlap_name} to {sig_name}"] = d
    print_log(f"\r{progress_bar(nb_home_sigs_with_overlap, nb_home_sigs_with_overlap, end=True)} processing distances "
              f"between VSP in Overlap finished.\n")

    min_dist = min(vsps_value for vsps_value in dict_min_dist.values())
    print(f"The minimum distance between two VSPs, one of whom is related to a Home Signal with Overlap is, "
          f"{print_in_cbtc(in_cbtc)}:"
          f"\n{min_dist = }"
          f"\n > for: {[vsps for vsps, vsps_value in dict_min_dist.items() if vsps_value == min_dist]}\n")
    return dict_min_dist


def get_home_signals_with_overlap(sig_dict: dict) -> list[str]:
    res_list = list()
    for sig, sig_value in sig_dict.items():
        sig_type = get_dc_sys_value(sig_value, DCSYS.Sig.Type)
        sig_with_ovl = get_dc_sys_value(sig_value, DCSYS.Sig.Enc_Dep)
        if sig_with_ovl == YesOrNo.O and sig_type == SignalType.MANOEUVRE:
            res_list.append(sig)
    return res_list
