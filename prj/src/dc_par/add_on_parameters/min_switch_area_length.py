#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *


def min_switch_area_length(in_cbtc: bool = False):
    if in_cbtc:
        sw_dict = get_switches_in_cbtc_ter()
    else:
        sw_dict = load_sheet(DCSYS.Aig)

    nb_sw = len(sw_dict)
    dict_switch_area_length = dict()
    progress_bar(1, 1, end=True)  # reset progress_bar
    i: int
    for i, (sw, sw_value) in enumerate(sw_dict.items()):
        print_log(f"\r{progress_bar(i, nb_sw)} processing length of switch area of {sw}...", end="")
        dict_switch_area_length[sw] = dict()
        sw_block_name, sw_block_value = get_block_associated_to_sw(sw_value)
        dict_switch_area_length[sw]["len_point_side_dict"] = get_len_point_side(sw_block_value, sw_value)
        dict_switch_area_length[sw]["min_flank_area_length_dict"] = get_min_flank_area_length(sw_value)
        dict_switch_area_length[sw]["switch_area_length"] = (
                dict_switch_area_length[sw]["min_flank_area_length_dict"]["min_flank_area_length"]
                + dict_switch_area_length[sw]["len_point_side_dict"]["len_point_side"])
    print_log(f"\r{progress_bar(nb_sw, nb_sw, end=True)} processing length of switches area finished.\n")

    min_switch_area_len = min(value["switch_area_length"] for sw, value in dict_switch_area_length.items())
    corresponding_sw = [sw for sw, value in dict_switch_area_length.items()
                        if value["switch_area_length"] == min_switch_area_len]
    print(f"The minimum length of a (flank area for a switch in left or right position + "
          f"part of the switch block on the point side only) on the line is, {print_in_cbtc(in_cbtc)}:"
          f"\n{min_switch_area_len = } m"
          f"\n > for: "
          f"{corresponding_sw}\n")
    for sw, value in dict_switch_area_length.items():
        if sw in corresponding_sw:
            pretty_print_dict(value)
            print()

    dict_switch_area_length = {key: dict_switch_area_length[key]
                               for key in sorted(dict_switch_area_length.keys(),
                                                 key=lambda x: dict_switch_area_length[x]["switch_area_length"])}

    return dict_switch_area_length


def get_len_point_side(sw_block, sw_value):
    """ Return the part of the switch block on the point side only """
    point_seg, point_x = give_sw_pos(sw_value)

    list_upstream_limits = list()
    for seg, x in get_dc_sys_zip_values(sw_block, DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X):
        if does_path_exist_within_block(seg, point_seg, sw_block, downstream=True):
            list_upstream_limits.append((seg, x))

    dict_len_point_side = dict()
    for seg, x in list_upstream_limits:
        dist = get_dist(point_seg, point_x, seg, x)
        dict_len_point_side[f"from ({point_seg}, {point_x}) to ({seg}, {x})"] = dist

    dist = min(dict_len_point_side.values())
    associated_key = [key for key, val in dict_len_point_side.items() if val == dist][0]
    return {"len_point_side": dist, "path_len_point_side": associated_key, "dict_len_point_side": dict_len_point_side}


def get_min_flank_area_length(sw: dict) -> dict[str]:
    """ Return the minimal flank area length for a switch in left or right position """
    dict_min_flank_area_len = dict()
    dict_min_flank_area_len.update(get_right_or_left_flank_area_length(sw, right=True))
    dict_min_flank_area_len.update(get_right_or_left_flank_area_length(sw, right=False))

    min_len = min(val["flank_area_len"] for val in dict_min_flank_area_len.values())
    min_side = [key for key, val in dict_min_flank_area_len.items() if val["flank_area_len"] == min_len][0]
    min_path = dict_min_flank_area_len[min_side]["path"]

    return {"min_flank_area_length": min_len, "min_flank_area_side": min_side, "min_flank_area": min_path,
            "dict_min_flank_area_len": dict_min_flank_area_len}


def get_right_or_left_flank_area_length(sw: dict, right: bool) -> dict[str, dict[str, Union[float, str]]]:
    directed_flank = DCSYS.Aig.AreaRightPositionFlank if right else DCSYS.Aig.AreaLeftPositionFlank
    min_flank_area_len = None
    min_pos = None
    min_path = None
    for i, flank_pos in enumerate(get_dc_sys_zip_values(sw, directed_flank.BeginSeg, directed_flank.BeginX,
                                                        directed_flank.EndSeg, directed_flank.EndX), start=1):
        flank_pos_len, path = get_dist_flank_position(flank_pos)
        if flank_pos_len is None:
            continue
        if min_flank_area_len is None or flank_pos_len < min_flank_area_len:
            min_flank_area_len = flank_pos_len
            min_pos = f"{'Right' if right else 'Left'} Area {i}"
            min_path = path
    return {min_pos: {"flank_area_len": min_flank_area_len, "path": min_path}}


def get_dist_flank_position(flank_pos: tuple[str, float, str, float]) -> tuple[Optional[float], Optional[str]]:
    begin_seg, begin_x, end_seg, end_x = flank_pos
    if not begin_seg:
        return None, None

    return (get_dist(begin_seg, begin_x, end_seg, end_x, verbose=True),
            f"between ({begin_seg}, {begin_x}) and ({end_seg}, {end_x})")
