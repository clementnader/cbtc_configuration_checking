#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *


def min_length_multiple_path(in_cbtc: bool = False):
    seg_dict = load_sheet(DCSYS.Seg)
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
    for i, start_seg in enumerate(sw_point_segs):
        print_log(f"\r{progress_bar(i, nb_sw_point_segs)} processing length of multiple path "
                  f"from point segment {start_seg}...", end="")
        for end_seg in sw_point_segs[i + 1:]:
            # TODO: check if max_nb_paths really useful with the new process
            dist, short_path, list_of_paths, downstream, upstream = \
                get_min_dist_and_list_of_paths(start_seg, end_seg, max_nb_paths=2)
            if dist is None:
                continue
            if len(list_of_paths) == 2:  # if there are two paths
                dist -= (get_len_seg(start_seg) + get_len_seg(end_seg))
                long_path = [path for direction, path in list_of_paths
                             if (direction, path) != (upstream, short_path)][0]
                long_path_length = get_path_len(long_path) - (get_len_seg(start_seg) + get_len_seg(end_seg))
                if downstream:
                    downstream_str = "downstream"
                else:
                    downstream_str = "upstream"
                multiple_path_len_dict[f"{start_seg} to {end_seg} {downstream_str}"] = {
                    "From": start_seg,
                    "To": end_seg,
                    "Minimal Length": round(dist, 3),
                    "Short Path": short_path,
                    "Short Path Switch": get_switch_on_path(short_path),
                    "Long Path Length": round(long_path_length, 3),
                    "Long Path": long_path,
                    "Long Path Switch": get_switch_on_path(long_path),
                }

    print_log(f"\r{progress_bar(nb_sw_point_segs, nb_sw_point_segs, end=True)} processing length of multiple paths "
              f"(rhombus or trapezoid) finished.\n")

    multiple_path_len_dict = {x: multiple_path_len_dict[x]
                              for x in sorted(multiple_path_len_dict,
                                              key=lambda x: multiple_path_len_dict[x]["Minimal Length"])}
    min_len = min(path_len["Minimal Length"] for path_len in multiple_path_len_dict.values())
    corresponding_paths = [path for path, path_len in multiple_path_len_dict.items()
                           if path_len['Minimal Length'] == min_len]
    print(f"The minimum length of a multiple path structure (rhombus or trapezoid) is, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_len = } m"
          f"\n > for: "
          f"{corresponding_paths}\n")
    for path, path_len in multiple_path_len_dict.items():
        if path in corresponding_paths:
            pretty_print_dict(path_len)
            print()

    # print(create_csv_file(multiple_path_len_dict))
    return multiple_path_len_dict


def get_all_point_segs(seg_list, limits_cbtc_ter):
    sw_point_segs = list()
    for seg in seg_list:
        if is_seg_upstream_of_a_switch(seg) or is_seg_downstream_of_a_switch(seg):
            sw_point_segs.append(seg)

    for lim in limits_cbtc_ter:
        seg, _, direction = lim
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
