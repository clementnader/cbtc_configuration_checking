#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_get_cbtc_territory import *
from ...dc_sys_draw_path.dc_sys_path_and_distances import is_seg_downstream


__all__ = ["cf_zsm_cbtc_10"]


def cf_zsm_cbtc_10():
    res_dict = get_zsm_limits()
    manage_zsm_limits_on_different_segs(res_dict)
    concatenate_zsm_limits(res_dict)
    print_results(res_dict)
    return res_dict


def initialize_res_dict():
    seg_dict = get_segs_within_cbtc_ter()
    limits_seg_dict = get_cbtc_ter_limits()

    res_dict = {seg: {
        "seg_limits": (0.0, get_seg_len(seg)),
        "list_limits": list(),
        "list_limits_diff": list()
    } for seg in seg_dict if seg is not None}

    for seg, x, downstream in limits_seg_dict:
        if downstream:
            res_dict[seg] = {
                "seg_limits": (x, get_seg_len(seg)),
                "list_limits": list(),
                "list_limits_diff": list()
            }
        else:
            res_dict[seg] = {
                "seg_limits": (0, x),
                "list_limits": list(),
                "list_limits_diff": list()
            }
    res_dict = {key: res_dict[key] for key in sorted(res_dict)}
    return res_dict


def get_zsm_limits():
    res_dict = initialize_res_dict()
    zsm_dict = get_objects_in_cbtc_ter(DCSYS.ZSM_CBTC)

    for zsm_value in zsm_dict.values():
        seg1, seg2 = get_dc_sys_value(zsm_value, DCSYS.ZSM_CBTC.ExtZsm.Seg)
        x1, x2 = get_dc_sys_value(zsm_value, DCSYS.ZSM_CBTC.ExtZsm.X)
        if seg1 != seg2:  # limits are on different segments
            res_dict[seg1]["list_limits_diff"].append((x1, seg2))
            res_dict[seg2]["list_limits_diff"].append((x2, seg1))
        else:  # limits are on the same segment
            res_dict[seg1]["list_limits"].append((x1, x2) if x1 < x2 else (x2, x1))
    return res_dict


def manage_zsm_limits_on_different_segs(res_dict):
    for seg, seg_value in res_dict.items():
        for x, other_seg in seg_value["list_limits_diff"]:
            len_seg = get_seg_len(seg)

            if is_seg_downstream(seg, other_seg, downstream=True):  # if other_seg is downstream
                linked_segs = get_straight_linked_segs(seg, downstream=True)
                res_dict[seg]["list_limits"].append((x, len_seg))
            elif is_seg_downstream(seg, other_seg, downstream=False):  # if other_seg is upstream
                linked_segs = get_straight_linked_segs(seg, downstream=False)
                res_dict[seg]["list_limits"].append((0, x))
            else:
                print_error(f"other_seg not in downstream_segs or upstream_segs"
                            f"\n\t{seg = }"
                            f"\n\t{res_dict[seg] = }"
                            f"\n\t{other_seg = }\n")
                continue
            for linked_seg in linked_segs:
                if linked_seg == other_seg:
                    break
                # linked_seg is entirely in a zsm
                if not res_dict[linked_seg]["list_limits"]:  # no limits defined yet
                    res_dict[linked_seg]["list_limits"] = [(0, get_seg_len(linked_seg))]


def concatenate_zsm_limits(res_dict):
    for seg, seg_value in res_dict.items():
        if seg_value["list_limits"]:
            res_dict[seg]["list_limits"] = remove_common_min_max_kp(res_dict[seg]["list_limits"])


def print_results(res_dict):
    print_title(f"Results for CF_ZSM_CBTC_10")
    sw_dict = get_sw_dict()
    for seg, seg_value in res_dict.items():
        zsm_coverage_limits = seg_value["list_limits"][0] if seg_value["list_limits"] else []
        seg_limits = seg_value["seg_limits"]
        if not zsm_coverage_limits:
            print_error(f"ZSM not covering the whole \"within CBTC\" Territory"
                        f"\n\tempty zsm_coverage_limits"
                        f"\n\tfor {seg = }, {zsm_coverage_limits = }, {seg_limits = }")
            continue

        zsm_mini, zsm_maxi = zsm_coverage_limits
        seg_mini, seg_maxi = seg_limits
        if zsm_mini > seg_mini:
            direction = check_seg_in_sw(seg, sw_dict)
            if direction in ["BIDIR", "INCREASING"] and round(zsm_mini - seg_mini, 3) <= .01:
                pass
                # print(f"{Color.green}OK on switch heels{Color.reset}\n"
                #       f"\t{zsm_mini = } not equal to {seg_mini = }"
                #       f"\n\tfor {seg = }, {zsm_coverage_limits = }, {seg_limits = }\n")
            else:
                print_error(f"ZSM not covering the whole \"within CBTC\" Territory"
                            f"\n\t{zsm_mini = } not equal to {seg_mini = }"
                            f"\n\tfor {seg = }, {zsm_coverage_limits = }, {seg_limits = }")
        if zsm_maxi < seg_maxi:
            direction = check_seg_in_sw(seg, sw_dict)
            if direction in ["BIDIR", "DECREASING"] and round(seg_maxi - zsm_maxi, 3) <= .01:
                pass
                # print(f"{Color.green}OK on switch heels{Color.reset}\n"
                #       f"\t{zsm_maxi = } not equal to {seg_maxi = }"
                #       f"\n\tfor {seg = }, {zsm_coverage_limits = }, {seg_limits = }\n")
            else:
                print_error(f"ZSM not covering the whole \"within CBTC\" Territory"
                            f"\n\t{zsm_maxi = } not equal to {seg_maxi = }"
                            f"\n\tfor {seg = }, {zsm_coverage_limits = }, {seg_limits = }")


def check_seg_in_sw(seg, sw_dict):
    direction = False
    for sw_value in sw_dict.values():
        right_seg = get_dc_sys_value(sw_value, DCSYS.Aig.SegmentTd)
        left_seg = get_dc_sys_value(sw_value, DCSYS.Aig.SegmentTg)
        if seg in [left_seg, right_seg]:
            if direction and direction != sw_value["Direction"]:
                direction = "BIDIR"
            else:
                direction = sw_value["Direction"]
    return direction


def get_sw_dict():
    sw_dict = load_sheet(DCSYS.Aig)

    for sw, sw_value in sw_dict.items():
        point_seg = get_dc_sys_value(sw_value, DCSYS.Aig.SegmentPointe)
        right_heel_seg = get_dc_sys_value(sw_value, DCSYS.Aig.SegmentTd)
        left_heel_seg = get_dc_sys_value(sw_value, DCSYS.Aig.SegmentTg)
        downstream_point_segs = get_linked_segs(point_seg, downstream=True)
        upstream_point_segs = get_linked_segs(point_seg, downstream=False)
        if left_heel_seg in downstream_point_segs and right_heel_seg in downstream_point_segs:
            sw_dict[sw]["Direction"] = "INCREASING"
        elif left_heel_seg in upstream_point_segs and right_heel_seg in upstream_point_segs:
            sw_dict[sw]["Direction"] = "DECREASING"
        else:
            print(f"No direction found"
                  f"\n{sw = }"
                  f"\n{sw_dict[sw] = }"
                  f"\n{downstream_point_segs = }"
                  f"\n{upstream_point_segs = }")
    return sw_dict
