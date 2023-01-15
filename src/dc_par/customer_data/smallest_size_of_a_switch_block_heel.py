#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def smallest_size_of_a_switch_block_heel(in_cbtc: bool = True):
    if in_cbtc:
        sw_dict = get_sws_in_cbtc_ter()
    else:
        sw_dict = load_sheet("sw")
    sw_cols_name = get_cols_name("sw")
    vb_dict = load_sheet("vb")
    vb_lim_cols_name = get_lim_cols_name("vb")

    dict_min_heel = dict()
    for i, (sw, sw_values) in enumerate(sw_dict.items()):
        point_vb = get_vb_associated_to_sw(sw_values, vb_dict, sw_cols_name)
        point_seg = give_point_seg_vb(vb_dict[point_vb]["limits"])[vb_lim_cols_name[0]]
        point_other_limits = [point_lim for point_lim in vb_dict[point_vb]["limits"]
                              if point_lim[vb_lim_cols_name[0]] != point_seg]
        dict_min_heel[sw] = {"point_vb": point_vb, "heels": dict()}
        for vb, vb_values in vb_dict.items():
            if vb != point_vb:
                limits = vb_values["limits"]
                for lim in limits:
                    seg = lim[vb_lim_cols_name[0]]
                    x = float(lim[vb_lim_cols_name[1]])
                    for point_lim in point_other_limits:
                        if seg == point_lim[vb_lim_cols_name[0]] and x == float(point_lim[vb_lim_cols_name[1]]):
                            dict_min_heel[sw]["heels"][vb] = dict()

    for sw, sw_values in dict_min_heel.items():
        for heel_vb in sw_values["heels"]:
            dict_min_heel[sw]["heels"][heel_vb]["len"] = get_len_vb(vb_dict[heel_vb]["limits"])

    min_heel = min(min(heel_vb_values["len"] for heel_vb_values in sw_values["heels"].values())
                   for sw_values in dict_min_heel.values())
    min_heel_sws = [sw for sw, sw_values in dict_min_heel.items()
                    if min(heel_vb_values["len"] for heel_vb_values in sw_values["heels"].values()) == min_heel]

    min_heels = ((f"for sw={min_heel_sw}", f"{dict_min_heel[min_heel_sw]}") for min_heel_sw in min_heel_sws)
    text = '\nand '.join(' -> '.join(heel) for heel in min_heels)
    print(f"The minimum heel (VB) length is, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_heel=}"
          f"\n{text}")

    return dict_min_heel
