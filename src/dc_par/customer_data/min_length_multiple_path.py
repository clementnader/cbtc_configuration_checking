#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...dc_sys import *


def min_length_multiple_path(in_cbtc: bool = False):
    seg_dict = load_sheet("seg")
    if in_cbtc:
        segs_within_cbtc_ter = get_segs_within_cbtc_ter()
        limits_cbtc_ter = get_limits_cbtc_ter()
    else:
        segs_within_cbtc_ter = list(seg_dict.keys())
        limits_cbtc_ter = list()
    sw_point_segs = get_all_point_segs(segs_within_cbtc_ter, limits_cbtc_ter)
    nb_sw_point_segs = len(sw_point_segs)

    multiple_path_len_dict = dict()
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, upstream_seg in enumerate(sw_point_segs):
        print_log(f"\r{progress_bar(i, nb_sw_point_segs)} processing length of multiple path "
                  f"from point segment {upstream_seg}...", end="")
        for downstream_seg in sw_point_segs[i+1:]:
            if are_segs_linked(upstream_seg, downstream_seg):  # if there is a path between the 2 segs
                dist, list_of_paths = get_min_dist_and_list_of_paths(upstream_seg, downstream_seg, max_nb_paths=2)
                if len(list_of_paths) == 2:  # if there are two paths
                    dist -= get_len_seg(upstream_seg) + get_len_seg(downstream_seg)
                    multiple_path_len_dict[f"{upstream_seg} to {downstream_seg}"] = {
                        "From": upstream_seg,
                        "To": downstream_seg,
                        "Minimal Length": round(dist, 3),
                        "Short Path": min(list_of_paths),
                        "Short Path Switch": get_switch_on_path(min(list_of_paths)),
                        "Long Path": max(list_of_paths),
                        "Long Path Switch": get_switch_on_path(max(list_of_paths)),
                    }
    print_log(f"\r{progress_bar(nb_sw_point_segs, nb_sw_point_segs, end=True)} processing length of multiple paths "
              f"(rhombus or trapezoid) finished.\n")

    multiple_path_len_dict = {x: multiple_path_len_dict[x]
                              for x in sorted(multiple_path_len_dict,
                                              key=lambda x: multiple_path_len_dict[x]["Minimal Length"])}
    min_len = min(path_len["Minimal Length"] for path_len in multiple_path_len_dict.values())
    print(f"The minimum length of a multiple path structure (rhombus or trapezoid) is, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_len=} m"
          f"\n > for: "
          f"{[path for path, path_len in multiple_path_len_dict.items() if path_len['Minimal Length'] == min_len]}\n")

    # print(create_csv_file(multiple_path_len_dict))
    return multiple_path_len_dict


def get_all_point_segs(seg_list, limits_cbtc_ter):
    cbtc_ter_lim_cols_name = get_lim_cols_name("cbtc_ter")
    sw_point_segs = list()

    for seg in seg_list:
        if is_seg_upstream_of_a_switch(seg) or is_seg_downstream_of_a_switch(seg):
            sw_point_segs.append(seg)

    for lim in limits_cbtc_ter:
        seg = lim[cbtc_ter_lim_cols_name[0]]
        direction = lim[cbtc_ter_lim_cols_name[2]]
        if direction == "CROISSANT" and is_seg_upstream_of_a_switch(seg):
            sw_point_segs.append(seg)
        if direction == "DECROISSANT" and is_seg_downstream_of_a_switch(seg):
            sw_point_segs.append(seg)

    return sw_point_segs


def get_switch_on_path(path: list[str]):
    list_sw = list()
    for seg, next_seg in zip(path[:-1], path[1:]):
        if is_seg_upstream_of_a_switch(seg):
            sw_name, sw_pos = get_heel_position(seg, next_seg)
            list_sw.append([sw_name, sw_pos])
        if is_seg_downstream_of_a_switch(next_seg):
            sw_name, sw_pos = get_heel_position(next_seg, seg)
            list_sw.append([sw_name, sw_pos])
    return list_sw


def create_csv_file(multiple_path_len_dict: dict[str, dict[str]]):
    csv = str()
    for line in multiple_path_len_dict.values():
        if not csv:
            csv += ";".join([key for key in line]) + "\n"
        csv += ";".join([str(val) for val in line.values()]) + "\n"
    return csv
