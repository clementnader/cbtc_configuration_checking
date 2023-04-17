#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def min_length_multiple_path(in_cbtc: bool = True):
    seg_dict = load_sheet("seg")
    if in_cbtc:
        segs_within_cbtc_ter = get_segs_within_cbtc_ter()
        limits_cbtc_ter = get_limits_cbtc_ter()
    else:
        segs_within_cbtc_ter = list(seg_dict.keys())
        limits_cbtc_ter = list()
    segs_upstream_of_a_switch, segs_downstream_of_a_switch = get_all_point_segs(segs_within_cbtc_ter, limits_cbtc_ter)

    multiple_path_len_dict = dict()
    for upstream_seg in segs_upstream_of_a_switch:
        for downstream_seg in segs_downstream_of_a_switch:
            if is_seg_downstream(upstream_seg, downstream_seg):  # if there is a path between the 2 segs
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

    multiple_path_len_dict = {x: multiple_path_len_dict[x]
                              for x in sorted(multiple_path_len_dict,
                                              key=lambda x: multiple_path_len_dict[x]["Minimal Length"])}
    min_len = min(path_len["Minimal Length"] for path_len in multiple_path_len_dict.values())
    print(f"The minimum length of a multiple path structure (rhombus or trapezoid) is, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_len=} m"
          f"\n > for: "
          f"{[path for path, path_len in multiple_path_len_dict.items() if path_len['Minimal Length'] == min_len]}\n")

    print(create_csv_file(multiple_path_len_dict))
    return multiple_path_len_dict


def get_all_point_segs(segs_within_cbtc_ter, limits_cbtc_ter):
    cbtc_ter_lim_cols_name = get_lim_cols_name("cbtc_ter")
    segs_upstream_of_a_switch = list()
    segs_downstream_of_a_switch = list()

    for seg in segs_within_cbtc_ter:
        if is_seg_upstream_of_a_switch(seg):
            segs_upstream_of_a_switch.append(seg)
        if is_seg_downstream_of_a_switch(seg):
            segs_downstream_of_a_switch.append(seg)

    for lim in limits_cbtc_ter:
        seg = lim[cbtc_ter_lim_cols_name[0]]
        direction = lim[cbtc_ter_lim_cols_name[2]]
        if direction == "CROISSANT" and is_seg_upstream_of_a_switch(seg):
            segs_upstream_of_a_switch.append(seg)
        if direction == "DECROISSANT" and is_seg_downstream_of_a_switch(seg):
            segs_downstream_of_a_switch.append(seg)

    return segs_upstream_of_a_switch, segs_downstream_of_a_switch


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
