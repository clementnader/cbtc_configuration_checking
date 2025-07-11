#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_get_cbtc_territory import *
from ..dc_sys_sheet_utils.virtual_block_utils import *


__all__ = ["smallest_size_of_a_switch_block_heel"]


def smallest_size_of_a_switch_block_heel(in_cbtc: bool = False):
    if in_cbtc:
        sw_dict = get_objects_in_cbtc_ter(DCSYS.Aig)
    else:
        sw_dict = load_sheet(DCSYS.Aig)
    nb_sw = len(sw_dict)
    vb_dict = load_sheet(DCSYS.CV)

    dict_min_heel = dict()
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (sw, sw_value) in enumerate(sw_dict.items()):
        print_log_progress_bar(i, nb_sw, f"determining the heel virtual blocks of switch {sw}")
        point_vb = get_vb_associated_to_sw(sw_value)
        point_vb_limits = list(get_dc_sys_zip_values(vb_dict[point_vb], DCSYS.CV.Extremite.Seg, DCSYS.CV.Extremite.X))
        point_seg, _ = give_point_seg_vb(point_vb_limits)
        point_vb_other_limits = [(seg, x) for (seg, x) in point_vb_limits if seg != point_seg]
        dict_min_heel[sw] = {"point_vb": point_vb, "heels": dict()}
        for vb, vb_value in vb_dict.items():
            if vb != point_vb:
                for seg, x in get_dc_sys_zip_values(vb_value, DCSYS.CV.Extremite.Seg, DCSYS.CV.Extremite.X):
                    for point_seg, point_x in point_vb_other_limits:
                        if seg == point_seg and x == point_x:
                            dict_min_heel[sw]["heels"][vb] = dict()
    print_log_progress_bar(nb_sw, nb_sw, "determining switches heels finished", end=True)

    for sw, sw_value in dict_min_heel.items():
        for heel_vb in sw_value["heels"]:
            heel_vb_limits = list(get_dc_sys_zip_values(vb_dict[heel_vb], DCSYS.CV.Extremite.Seg, DCSYS.CV.Extremite.X))
            dict_min_heel[sw]["heels"][heel_vb]["len"] = get_len_vb(heel_vb_limits)
        dict_min_heel[sw]["min_heel_length"] = min(heel_vb_value["len"]
                                                   for heel_vb_value in dict_min_heel[sw]["heels"].values())

    min_heel = min(sw_value["min_heel_length"]
                   for sw_value in dict_min_heel.values())
    min_heel_sws = [sw for sw, sw_value in dict_min_heel.items()
                    if sw_value["min_heel_length"] == min_heel]

    min_heels = ((f"for sw = {min_heel_sw}", f"{dict_min_heel[min_heel_sw]}") for min_heel_sw in min_heel_sws)
    text = "\nand ".join(" -> ".join(heel) for heel in min_heels)
    print(f"The minimum heel (VB) length is, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_heel = }"
          f"\n{text}\n")

    min_sw_block_heel_length_dict = {x: dict_min_heel[x]
                                     for x in sorted(dict_min_heel,
                                                     key=lambda x: dict_min_heel[x]["min_heel_length"])}

    return min_sw_block_heel_length_dict
