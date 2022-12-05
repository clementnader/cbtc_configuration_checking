#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_sys_pkg import *


def cf_zsm_cbtc_10(tolerance: float = .02):
    zsm_dict = load_sheet("zsm")
    zsm_cols_name = get_cols_name("zsm")

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    res_dict = {seg: {"list_limits": list(), "list_limits_diff": list()} for seg in seg_dict if seg}

    for zsm in zsm_dict:
        seg1 = zsm_dict[zsm][zsm_cols_name['D']]
        x1 = float(zsm_dict[zsm][zsm_cols_name['E']])
        seg2 = zsm_dict[zsm][zsm_cols_name['H']]
        x2 = float(zsm_dict[zsm][zsm_cols_name['I']])

        if seg1 != seg2:  # limits are on different segments
            res_dict[seg1]["list_limits_diff"].append([x1, seg2, x2])
            res_dict[seg2]["list_limits_diff"].append([x2, seg1, x1])
        else:  # limits are on the same segment
            res_dict[seg1]["list_limits"].append([x1, x2] if x1 < x2 else [x2, x1])

    # Manage limits between different segments
    for seg in res_dict:
        if res_dict[seg]["list_limits_diff"]:
            for limits_diff in res_dict[seg]["list_limits_diff"]:
                x = limits_diff[0]
                other_seg = limits_diff[1]
                len_seg = get_len_seg(seg, seg_dict, seg_cols_name)
                downstream_segs = get_straight_linked_segs(seg, seg_dict, seg_cols_name, downstream=True)
                upstream_segs = get_straight_linked_segs(seg, seg_dict, seg_cols_name, downstream=False)

                if other_seg in downstream_segs:
                    res_dict[seg]["list_limits"].append([x, len_seg])
                    for downstream_seg in downstream_segs:
                        if downstream_seg == other_seg:
                            break
                        # downstream_seg is entirely in a zsm
                        if not res_dict[downstream_seg]["list_limits"]:  # no limits defined yet
                            res_dict[downstream_seg]["list_limits"] = \
                                [[0, get_len_seg(downstream_seg, seg_dict, seg_cols_name)]]

                elif other_seg in upstream_segs:
                    res_dict[seg]["list_limits"].append([0, x])
                    for upstream_seg in upstream_segs:
                        if upstream_seg == other_seg:
                            break
                        # upstream_seg is entirely in a zsm
                        if not res_dict[upstream_seg]["list_limits"]:  # no limits defined yet
                            res_dict[upstream_seg]["list_limits"] = \
                                [[0, get_len_seg(upstream_seg, seg_dict, seg_cols_name)]]

                else:
                    print(f"other_seg not in downstream_segs or upstream_segs"
                          f"\n{seg=}"
                          f"\n{res_dict[seg]=}"
                          f"\n{other_seg=}"
                          f"\n{downstream_segs=}"
                          f"\n{upstream_segs=}\n")

    # Concatenate
    for seg in res_dict:
        if res_dict[seg]["list_limits"]:
            res_dict[seg]["list_limits"].sort()
            list_limits = list()
            old_mini = res_dict[seg]["list_limits"][0][0]
            old_maxi = res_dict[seg]["list_limits"][0][0]
            for lim in res_dict[seg]["list_limits"]:
                mini = lim[0]
                maxi = lim[1]
                if old_maxi != mini:
                    list_limits.append([old_mini, old_maxi])
                    old_mini = mini
                    old_maxi = maxi
                else:
                    old_maxi = maxi
            list_limits.append([old_mini, old_maxi])
            res_dict[seg]["list_limits"] = list_limits

    # Clean Up
    for seg in res_dict:
        if res_dict[seg]["list_limits"]:
            res_dict[seg] = res_dict[seg]["list_limits"][0]
        else:
            res_dict[seg] = []

    # Print errors
    # print()
    # print("-"*100)
    # print()
    sw_dict = get_sw_dict()
    sw_cols_name = get_cols_name("sw")
    for seg in res_dict:
        len_seg = get_len_seg(seg, seg_dict, seg_cols_name)
        if not res_dict[seg]:
            print(f"empty list_limits"
                  f"\n{seg=}"
                  f"\n{res_dict[seg]}"
                  f"\nbetween {0.0} and {len_seg}\n")
        else:
            mini = res_dict[seg][0]
            maxi = res_dict[seg][1]
            if abs(mini - 0) > tolerance:
                direction = check_seg_in_sw(seg, sw_dict, sw_cols_name)
                if direction in ["BIDIR", "INCREASING"]:
                    print(f"\t\t\tOK on switch, mini not equal to 0"
                          f"\n\t\t\t{seg=}"
                          f"\n\t\t\t{res_dict[seg]}"
                          f"\n\t\t\tbetween {0.0} and {len_seg}\n")
                else:
                    print(f"{direction=} mini not equal to 0"
                          f"\n{seg=}"
                          f"\n{res_dict[seg]}"
                          f"\nbetween {0.0} and {len_seg}\n")
            if abs(maxi - len_seg) > tolerance:
                direction = check_seg_in_sw(seg, sw_dict, sw_cols_name)
                if direction in ["BIDIR", "DECREASING"]:
                    print(f"\t\t\tOK on switch, maxi not equal to len(seg)"
                          f"\n\t\t\t{seg=}"
                          f"\n\t\t\t{res_dict[seg]}"
                          f"\n\t\t\tbetween {0.0} and {len_seg}\n")
                else:
                    print(f"{direction=} maxi not equal to len(seg)"
                          f"\n{seg=}"
                          f"\n{res_dict[seg]}"
                          f"\nbetween {0.0} and {len_seg}\n")

    return res_dict


def check_seg_in_sw(seg, sw_dict, sw_cols_name):
    direction = False
    for sw in sw_dict:
        right_seg = sw_dict[sw][sw_cols_name['C']]
        left_seg = sw_dict[sw][sw_cols_name['D']]
        if seg in [left_seg, right_seg]:
            if direction and direction != sw_dict[sw]["Direction"]:
                direction = "BIDIR"
            else:
                direction = sw_dict[sw]["Direction"]
    return direction


def get_sw_dict():
    sw_dict = load_sheet("sw")
    sw_cols_name = get_cols_name("sw")

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    for sw in sw_dict:
        point_seg = sw_dict[sw][sw_cols_name['B']]
        right_heel_seg = sw_dict[sw][sw_cols_name['C']]
        left_heel_seg = sw_dict[sw][sw_cols_name['D']]
        downstream_point_segs = get_linked_segs_switch(point_seg, seg_dict, seg_cols_name, downstream=True)
        upstream_point_segs = get_linked_segs_switch(point_seg, seg_dict, seg_cols_name, downstream=False)
        if right_heel_seg in downstream_point_segs and left_heel_seg in downstream_point_segs:
            sw_dict[sw]["Direction"] = "INCREASING"
        elif right_heel_seg in upstream_point_segs and left_heel_seg in upstream_point_segs:
            sw_dict[sw]["Direction"] = "DECREASING"
        else:
            print(f"No direction found"
                  f"\n{sw=}"
                  f"\n{sw_dict[sw]=}"
                  f"\n{downstream_point_segs=}"
                  f"\n{upstream_point_segs=}")
    return sw_dict


def get_linked_segs_switch(point_seg: str, seg_dict: dict, seg_cols_name: dict[str, str], downstream: bool = True):
    downstream_cols = ['J', 'K']
    upstream_cols = ['H', 'I']
    linked_segs = list()
    for n in range(2):
        j = downstream_cols[n] if downstream else upstream_cols[n]
        linked_seg = seg_dict[point_seg][seg_cols_name[j]] if seg_cols_name[j] in seg_dict[point_seg] \
            else ""
        if linked_seg:
            linked_segs.append(linked_seg)
    return linked_segs
