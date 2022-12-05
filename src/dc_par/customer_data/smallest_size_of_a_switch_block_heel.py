#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys_pkg import *
from dc_sys_checking.src.dc_sys_pkg.seg_utils import *


def is_seg_in_vb(vb, seg, seg_dict, seg_cols_name):
    if seg in [vb[lim]["Seg"] for lim in vb]:
        return True
    for lim1 in vb:
        seg1 = vb[lim1]["Seg"]
        for lim2 in vb:
            seg2 = vb[lim2]["Seg"]
            if seg2 != seg1:
                upstream_segs_1 = get_straight_linked_segs(seg1, seg_dict, seg_cols_name, upstream=True)
                downstream_segs_1 = get_straight_linked_segs(seg1, seg_dict, seg_cols_name, upstream=False)
                if seg2 in upstream_segs_1:
                    for upstream_seg in upstream_segs_1:
                        if upstream_seg == seg2:
                            break
                        if seg == upstream_seg:
                            return True
                elif seg2 in downstream_segs_1:
                    for downstream_seg in downstream_segs_1:
                        if downstream_seg == seg2:
                            break
                        if seg == downstream_seg:
                            return True
    return False


def get_sw_point_vb(sw, vb_dict, sw_cols_name, seg_dict, seg_cols_name):
    for vb in vb_dict:
        if len(vb_dict[vb]) == 3:
            if sorted(vb_dict[vb]) == sorted(sw):
                return vb
            if all([is_seg_in_vb(vb_dict[vb], sw[sw_cols_name[j]], seg_dict, seg_cols_name) for j in ['B', 'C', 'D']]):
                return vb
    print(f"Unable to find VB associated to SW: {sw}")
    return None


def list_elem_all_different(list_elem):
    for i, elem in enumerate(list_elem):
        if elem in list_elem[i+1:]:
            return False
    return True


def give_point_seg_vb(vb, seg_dict, seg_cols_name):
    assert len(vb) == 3 and list_elem_all_different([vb[lim]["Seg"] for lim in vb])
    up_or_down = [[None for _ in range(3)] for _ in range(3)]
    for i, lim1 in enumerate(vb):
        seg1 = vb[lim1]["Seg"]
        for j, lim2 in enumerate(vb):
            seg2 = vb[lim2]["Seg"]
            if seg2 == seg1:
                up_or_down[i][j] = "bidir"
            else:
                upstream_segs_1 = get_straight_linked_segs(seg1, seg_dict, seg_cols_name, upstream=True)
                downstream_segs_1 = get_straight_linked_segs(seg1, seg_dict, seg_cols_name, upstream=False)
                if seg2 in upstream_segs_1:
                    up_or_down[i][j] = "up"
                elif seg2 in downstream_segs_1:
                    up_or_down[i][j] = "down"
    for i in range(3):
        for j in range(3):
            if up_or_down[j][i] == "bidir":
                up_or_down[i][j] = "bidir"
            elif up_or_down[j][i] == "up":
                up_or_down[i][j] = "down"
            elif up_or_down[j][i] == "down":
                up_or_down[i][j] = "up"
    for i in range(3):
        if all([up_or_down[i][j] in ["bidir", "up"] for j in range(3)])\
                or all([up_or_down[i][j] in ["bidir", "down"] for j in range(3)]):
            return vb[list(vb.keys())[i]]["Seg"]
    print(f"Unable to found point segment for VB: {vb}")
    return None


def get_len_vb(vb, seg_dict: dict, seg_cols_name: dict[str, str]):
    limits = list(vb.values())
    if len(limits) == 3:
        point_seg = give_point_seg_vb(vb, seg_dict, seg_cols_name)
        for i, lim in enumerate(limits):
            if len(limits) == 3 and lim["Seg"] != point_seg:  # remove either heel segment
                limits.pop(i)
    if len(limits) == 3:
        print(f"Unable to find a limit to remove to calculate the length of this {vb=}")
        return 0
    seg1 = limits[0]["Seg"]
    x1 = limits[0]["x"]
    seg2 = limits[1]["Seg"]
    x2 = limits[1]["x"]
    d = get_dist(seg1, x1, seg2, x2, seg_dict, seg_cols_name)
    return d


def smallest_size_of_a_switch_block_heel(tolerance=.0):
    wb = load_wb()
    sh_sw = wb.sheet_by_name("Aig")
    sw_dict = get_dict(sh_sw, fixed_cols_ref=['B', 'C', 'D'])
    sw_cols_name = get_cols_name(sh_sw, cols_ref=['B', 'C', 'D'])

    sh_seg = wb.sheet_by_name("Seg")
    seg_dict = get_dict(sh_seg, fixed_cols_ref=['G', 'H', 'I', 'J', 'K'])
    seg_cols_name = get_cols_name(sh_seg, cols_ref=['G', 'H', 'I', 'J', 'K'])

    sh_vb = wb.sheet_by_name("CV")
    vb_dict = get_limits_dict(sh_vb, line_ref=3, col_ref='B', nb_max_limits=3, delta_between_limits=2,
                              possible_same_seg=True)

    dict_min_heel = dict()

    for sw in sw_dict:
        point_vb = get_sw_point_vb(sw_dict[sw], vb_dict, sw_cols_name, seg_dict, seg_cols_name)
        point_seg = give_point_seg_vb(vb_dict[point_vb], seg_dict, seg_cols_name)
        point_limits = vb_dict[point_vb]
        dict_min_heel[sw] = {"point_vb": point_vb, "heels": dict()}
        for vb in vb_dict:
            if vb != point_vb:
                limits = vb_dict[vb]
                for lim in limits:
                    seg = limits[lim]["Seg"]
                    x = float(limits[lim]["x"])
                    for point_lim in point_limits:
                        if point_limits[point_lim]["Seg"] != point_seg:
                            if seg == point_limits[point_lim]["Seg"] \
                                    and abs(x-float(point_limits[point_lim]["x"])) <= tolerance:
                                dict_min_heel[sw]["heels"][vb] = {"len": 0}

    for sw in dict_min_heel:
        for heel_vb in dict_min_heel[sw]["heels"]:
            len_vb = get_len_vb(vb_dict[heel_vb], seg_dict, seg_cols_name)
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
