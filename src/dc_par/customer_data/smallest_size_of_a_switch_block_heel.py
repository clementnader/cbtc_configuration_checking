#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *


def get_segs_in_vb(vb_limits, seg_dict: dict, seg_cols_name: dict[str, str]):
    """ Return the list of segments in a VB. """
    list_segs = list()
    if len(vb_limits) == 3:
        lim1 = give_point_seg_vb(vb_limits, seg_dict, seg_cols_name)
    else:
        lim1 = vb_limits[0]
    seg1 = lim1["Seg"]
    for lim2 in vb_limits:
        if lim2 != lim1:
            seg2 = lim2["Seg"]
            list_paths = get_list_of_paths(seg1, seg2, seg_dict, seg_cols_name)
            for path in list_paths:
                for seg in path:
                    if seg not in list_segs:
                        list_segs.append(seg)
    return list_segs


def is_seg_in_vb(vb_limits, seg, seg_dict: dict, seg_cols_name: dict[str, str]):
    """ Return True if a segment is in a VB else False. """
    return seg in get_segs_in_vb(vb_limits, seg_dict, seg_cols_name)


def get_vb_associated_to_sw(sw, vb_dict, sw_cols_name, seg_dict: dict, seg_cols_name: dict[str, str]):
    """ Get the VB associated to a switch. """
    for vb in vb_dict:
        vb_limits = vb_dict[vb]["limits"]
        if len(vb_limits) == 3:
            if sorted([vb_lim["Seg"] for vb_lim in vb_limits]) == sorted(sw):
                return vb
            if all([is_seg_in_vb(vb_limits, sw[sw_cols_name[j]], seg_dict, seg_cols_name)
                    for j in ['B', 'C', 'D']]):
                return vb
    print(f"Unable to find VB associated to SW: {sw}")
    return None


def smallest_size_of_a_switch_block_heel(tolerance=.0):
    sw_dict = load_sheet("sw")
    sw_cols_name = get_cols_name("sw")

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    vb_dict = load_sheet("vb")

    dict_min_heel = dict()

    for sw in sw_dict:
        point_vb = get_vb_associated_to_sw(sw_dict[sw], vb_dict, sw_cols_name, seg_dict, seg_cols_name)
        point_seg = give_point_seg_vb(vb_dict[point_vb]["limits"], seg_dict, seg_cols_name)["Seg"]
        point_limits = vb_dict[point_vb]["limits"]
        dict_min_heel[sw] = {"point_vb": point_vb, "heels": dict()}
        for vb in vb_dict:
            if vb != point_vb:
                limits = vb_dict[vb]["limits"]
                for lim in limits:
                    seg = lim["Seg"]
                    x = float(lim["x"])
                    for point_lim in point_limits:
                        if point_lim["Seg"] != point_seg:
                            if seg == point_lim["Seg"] \
                                    and abs(x-float(point_lim["x"])) <= tolerance:
                                dict_min_heel[sw]["heels"][vb] = {"len": 0}

    for sw in dict_min_heel:
        for heel_vb in dict_min_heel[sw]["heels"]:
            len_vb = get_len_vb(vb_dict[heel_vb]["limits"], seg_dict, seg_cols_name)
            if not len_vb:
                print(f"Unable to calculate this {heel_vb=} length")
            else:
                dict_min_heel[sw]["heels"][heel_vb]["len"] = len_vb

    min_heel = min([min([dict_min_heel[sw]["heels"][heel_vb]["len"] for heel_vb in dict_min_heel[sw]["heels"]])
                   for sw in dict_min_heel])
    min_heel_sws = [sw for sw in dict_min_heel
                    if min([dict_min_heel[sw]["heels"][heel_vb]["len"]
                            for heel_vb in dict_min_heel[sw]["heels"]]) == min_heel]

    min_heels = [[f"for sw={min_heel_sw}", f"{dict_min_heel[min_heel_sw]}"] for min_heel_sw in min_heel_sws]
    text = '\nand '.join([' -> '.join(heel) for heel in min_heels])
    print(f"The minimum heel length is {min_heel=}"
          f"\n{text}")

    return dict_min_heel
