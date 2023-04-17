#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_sys import *


def cf_zsm_cbtc_10():
    res_dict = get_zsm_limits()
    manage_zsm_limits_on_different_segs(res_dict)
    concatenate_zsm_limits(res_dict)
    print_results(res_dict)
    return res_dict


def initialize_res_dict():
    seg_dict = get_segs_within_cbtc_ter()
    limits_seg_dict = get_limits_cbtc_ter()
    cbtc_ter_lim_cols_name = get_lim_cols_name("cbtc_ter")

    res_dict = {seg: {
        "seg_limits": (0.0, get_len_seg(seg)),
        "list_limits": list(),
        "list_limits_diff": list()
    } for seg in seg_dict if seg is not None}

    for lim in limits_seg_dict:
        seg = lim[cbtc_ter_lim_cols_name[0]]
        x = lim[cbtc_ter_lim_cols_name[1]]
        direction = lim[cbtc_ter_lim_cols_name[2]]
        if direction == "CROISSANT":
            res_dict[seg] = {
                "seg_limits": (x, get_len_seg(seg)),
                "list_limits": list(),
                "list_limits_diff": list()
            }
        if direction == "DECROISSANT":
            res_dict[seg] = {
                "seg_limits": (0, x),
                "list_limits": list(),
                "list_limits_diff": list()
            }
    res_dict = {key: res_dict[key] for key in sorted(res_dict)}
    return res_dict


def get_zsm_limits():
    res_dict = initialize_res_dict()
    zsm_dict = get_zsm_in_cbtc_ter()
    zsm_cols_name = get_cols_name("zsm")

    for zsm_value in zsm_dict.values():
        seg1 = zsm_value[zsm_cols_name['D']]
        x1 = float(zsm_value[zsm_cols_name['E']])
        seg2 = zsm_value[zsm_cols_name['H']]
        x2 = float(zsm_value[zsm_cols_name['I']])

        if seg1 != seg2:  # limits are on different segments
            res_dict[seg1]["list_limits_diff"].append((x1, seg2))
            res_dict[seg2]["list_limits_diff"].append((x2, seg1))
        else:  # limits are on the same segment
            res_dict[seg1]["list_limits"].append((x1, x2) if x1 < x2 else (x2, x1))
    return res_dict


def manage_zsm_limits_on_different_segs(res_dict):
    for seg, seg_value in res_dict.items():
        for x, other_seg in seg_value["list_limits_diff"]:
            len_seg = get_len_seg(seg)

            if is_seg_downstream(seg, other_seg):  # if other_seg is downstream
                linked_segs = get_straight_linked_segs(seg, downstream=True)
                res_dict[seg]["list_limits"].append((x, len_seg))
            elif is_seg_downstream(other_seg, seg):  # if other_seg is upstream
                linked_segs = get_straight_linked_segs(seg, downstream=False)
                res_dict[seg]["list_limits"].append((0, x))
            else:
                print_error(f"other_seg not in downstream_segs or upstream_segs"
                            f"\n{seg=}"
                            f"\n{res_dict[seg]=}"
                            f"\n{other_seg=}\n")
                continue
            for linked_seg in linked_segs:
                if linked_seg == other_seg:
                    break
                # linked_seg is entirely in a zsm
                if not res_dict[linked_seg]["list_limits"]:  # no limits defined yet
                    res_dict[linked_seg]["list_limits"] = [(0, get_len_seg(linked_seg))]


def concatenate_zsm_limits(res_dict):
    for seg, seg_values in res_dict.items():
        if seg_values["list_limits"]:
            res_dict[seg]["list_limits"].sort()
            list_limits = list()
            old_mini = res_dict[seg]["list_limits"][0][0]
            old_maxi = res_dict[seg]["list_limits"][0][0]
            for lim in res_dict[seg]["list_limits"]:
                mini = lim[0]
                maxi = lim[1]
                if old_maxi != mini:
                    list_limits.append((old_mini, old_maxi))
                    old_mini = mini
                    old_maxi = maxi
                else:
                    old_maxi = maxi
            list_limits.append((old_mini, old_maxi))
            res_dict[seg]["list_limits"] = list_limits


def print_results(res_dict):
    print(f"{Color.blue}{Color.underline}Results for CF_ZSM_CBTC_10{Color.reset}\n")
    sw_dict = get_sw_dict()
    sw_cols_name = get_cols_name("sw")
    for seg, seg_values in res_dict.items():
        zsm_coverage_limits = seg_values["list_limits"][0] if seg_values["list_limits"] else []
        seg_limits = seg_values["seg_limits"]
        if not zsm_coverage_limits:
            print_error(f"ZSM not covering the whole \"within CBTC\" Territory"
                        f"\nempty zsm_coverage_limits"
                        f"\nfor {seg=}, {zsm_coverage_limits=}, {seg_limits=}")
            continue

        zsm_mini, zsm_maxi = zsm_coverage_limits
        seg_mini, seg_maxi = seg_limits
        if zsm_mini > seg_mini:
            direction = check_seg_in_sw(seg, sw_dict, sw_cols_name)
            if direction in ("BIDIR", "INCREASING") and round(zsm_mini - seg_mini, 3) <= .01:
                print(f"{Color.green}OK on switch heels{Color.reset}\n"
                      f"{Color.dark_yellow}{zsm_mini=} not equal to {seg_mini=}"
                      f"\nfor {seg=}, {zsm_coverage_limits=}, {seg_limits=}{Color.reset}\n")
            else:
                print_error(f"ZSM not covering the whole \"within CBTC\" Territory"
                            f"\n{zsm_mini=} not equal to {seg_mini=}"
                            f"\nfor {seg=}, {zsm_coverage_limits=}, {seg_limits=}")
        if zsm_maxi < seg_maxi:
            direction = check_seg_in_sw(seg, sw_dict, sw_cols_name)
            if direction in ("BIDIR", "DECREASING") and round(seg_maxi - zsm_maxi, 3) <= .01:
                print(f"{Color.green}OK on switch heels{Color.reset}\n"
                      f"{Color.dark_yellow}{zsm_maxi=} not equal to {seg_maxi=}"
                      f"\nfor {seg=}, {zsm_coverage_limits=}, {seg_limits=}{Color.reset}\n")
            else:
                print_error(f"ZSM not covering the whole \"within CBTC\" Territory"
                            f"\n{zsm_maxi=} not equal to {seg_maxi=}"
                            f"\nfor {seg=}, {zsm_coverage_limits=}, {seg_limits=}")


def check_seg_in_sw(seg, sw_dict, sw_cols_name):
    direction = False
    for sw_values in sw_dict.values():
        right_seg = sw_values[sw_cols_name['C']]
        left_seg = sw_values[sw_cols_name['D']]
        if seg in (left_seg, right_seg):
            if direction and direction != sw_values["Direction"]:
                direction = "BIDIR"
            else:
                direction = sw_values["Direction"]
    return direction


def get_sw_dict():
    sw_dict = load_sheet("sw")
    sw_cols_name = get_cols_name("sw")

    for sw, sw_values in sw_dict.items():
        point_seg = sw_values[sw_cols_name['B']]
        left_heel_seg = sw_values[sw_cols_name['D']]
        right_heel_seg = sw_values[sw_cols_name['C']]
        downstream_point_segs = get_linked_segs(point_seg, downstream=True)
        upstream_point_segs = get_linked_segs(point_seg, downstream=False)
        if left_heel_seg in downstream_point_segs and right_heel_seg in downstream_point_segs:
            sw_dict[sw]["Direction"] = "INCREASING"
        elif left_heel_seg in upstream_point_segs and right_heel_seg in upstream_point_segs:
            sw_dict[sw]["Direction"] = "DECREASING"
        else:
            print(f"No direction found"
                  f"\n{sw=}"
                  f"\n{sw_dict[sw]=}"
                  f"\n{downstream_point_segs=}"
                  f"\n{upstream_point_segs=}")
    return sw_dict
