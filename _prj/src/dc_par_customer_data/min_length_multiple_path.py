#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_get_cbtc_territory import *
from ..dc_sys_draw_path.dc_sys_path_and_distances import get_downstream_path, get_path_len
from ..dc_sys_sheet_utils.switch_utils import *


__all__ = ["min_length_multiple_path"]


def min_length_multiple_path(in_cbtc: bool = False):
    seg_dict = load_sheet(DCSYS.Seg)
    if in_cbtc:
        segs_within_cbtc_ter = get_segs_within_cbtc_ter()
        limits_cbtc_ter = get_cbtc_ter_limits()
    else:
        segs_within_cbtc_ter = list(seg_dict.keys())
        limits_cbtc_ter = list()
    sw_point_segs = get_all_sw_point_segs(segs_within_cbtc_ter, limits_cbtc_ter)
    nb_sw_point_segs = len(sw_point_segs)

    multiple_path_len_dict = dict()
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (start_seg, start_downstream) in enumerate(sw_point_segs):
        print_log_progress_bar(i, nb_sw_point_segs, f"processing multiple path length from point segment "
                               f"{start_seg}")
        for end_seg, end_downstream in sw_point_segs[i+1:]:
            end_upstream = not end_downstream
            dist, short_path, list_of_paths, _ = get_downstream_path(start_seg, end_seg,
                                                                     start_downstream=start_downstream,
                                                                     max_nb_paths=2, end_upstream=end_upstream)
            if dist is None:
                continue
            if len(list_of_paths) == 2:  # if there are two paths
                dist -= (get_segment_length(start_seg) + get_segment_length(end_seg))
                long_path = [path for direction, path in list_of_paths
                             if (direction, path) != (end_upstream, short_path)][0]
                long_path_length = get_path_len(long_path) - (
                        get_segment_length(start_seg) + get_segment_length(end_seg))
                downstream_str = {True: "downstream", False: "upstream"}[start_downstream]
                upstream_str = {True: "downstream", False: "upstream"}[not end_upstream]
                multiple_path_len_dict[f"{start_seg} {downstream_str} to {end_seg} {upstream_str}"] = {
                    "From": start_seg,
                    "From Direction": downstream_str,
                    "To": end_seg,
                    "End Direction": upstream_str,
                    "Minimal Length": round(dist, 3),
                    "Short Path": short_path,
                    "Short Path Switch": get_switch_on_path(short_path),
                    "Long Path Length": round(long_path_length, 3),
                    "Long Path": long_path,
                    "Long Path Switch": get_switch_on_path(long_path),
                }

    print_log_progress_bar(nb_sw_point_segs, nb_sw_point_segs, "processing length of multiple paths (rhombus "
                           "or trapezoid) finished", end=True)

    multiple_path_len_dict = {x: multiple_path_len_dict[x]
                              for x in sorted(multiple_path_len_dict,
                                              key=lambda x: multiple_path_len_dict[x]["Minimal Length"])}
    min_len = min(path_len["Minimal Length"] for path_len in multiple_path_len_dict.values())
    corresponding_paths = [path for path, path_len in multiple_path_len_dict.items()
                           if path_len["Minimal Length"] == min_len]
    print(f"The minimum length of a multiple path structure (rhombus or trapezoid) is, {print_in_cbtc(in_cbtc)}:"
          f"\n{Color.green}{min_len = } m{Color.reset}"
          f"\n > for: "
          f"{corresponding_paths}\n")
    for path, path_len in multiple_path_len_dict.items():
        if path in corresponding_paths:
            pretty_print_dict(path_len)
            print()

    result_file = "multiple_path_length.csv"
    result_file = f" - {get_current_version()}".join(os.path.splitext(result_file))
    with open(result_file, "w") as f:
        f.write(create_csv_file(multiple_path_len_dict))
        print(f"{Color.white}CSV file with the different multiple-path configurations is available at{Color.reset}"
              f"\n{Color.yellow}{os.path.realpath(result_file)}{Color.reset}")
    return multiple_path_len_dict


def get_all_sw_point_segs(seg_list: Union[set[str], list[str]], limits_cbtc_ter: list[tuple[str, float, bool]]
                          ) -> list[tuple[str, bool]]:
    sw_point_segs = list()
    for seg in seg_list:
        if is_segment_upstream_of_a_switch(seg):
            sw_point_segs.append((seg, True))
        if is_segment_downstream_of_a_switch(seg):
            sw_point_segs.append((seg, False))

    for lim in limits_cbtc_ter:
        seg, _, downstream = lim
        if downstream and is_segment_upstream_of_a_switch(seg):
            sw_point_segs.append((seg, True))
        if not downstream and is_segment_downstream_of_a_switch(seg):
            sw_point_segs.append((seg, False))

    return sw_point_segs


def get_switch_on_path(path: list[str]):
    list_sw = list()
    for seg, next_seg in zip(path[:-1], path[1:]):
        if is_segment_upstream_of_a_switch(seg) or is_segment_downstream_of_a_switch(seg):
            sw_name, sw_pos = get_heel_position(seg, next_seg)
            if sw_name is not None:
                list_sw.append([sw_name, sw_pos])
        if is_segment_upstream_of_a_switch(next_seg) or is_segment_downstream_of_a_switch(next_seg):
            sw_name, sw_pos = get_heel_position(next_seg, seg)
            if sw_name is not None:
                list_sw.append([sw_name, sw_pos])
    return list_sw


def create_csv_file(multiple_path_len_dict: dict[str, dict[str, Any]]):
    csv = "sep=;\n"
    for line in multiple_path_len_dict.values():
        if not csv:
            csv += ";".join([key for key in line]) + "\n"
        csv += ";".join([str(val) for val in line.values()]) + "\n"
    return csv
