#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..dc_sys import *
from ..dc_sys_get_cbtc_territory import *
from ..dc_sys_sheet_utils.block_utils import get_block_associated_to_sw, find_upstream_n_downstream_limits
from ..dc_sys_sheet_utils.slope_utils import *
from ..dc_sys_draw_path.dc_sys_path_and_distances import get_dist
from ..dc_par import *
from ..cctool_oo_schema import *


def r_cdv_5(print_ok: bool = False):
    sw_dict = get_objects_in_cbtc_ter(DCSYS.Aig)

    error_counts = [0, 0]
    for sw_name, sw_value in sw_dict.items():
        is_sw_upstream = is_sw_point_seg_upstream(sw_value)
        sw_block, sw_block_value = get_block_associated_to_sw(sw_value)
        upstream_limits, downstream_limits = find_upstream_n_downstream_limits(sw_block_value)
        # TODO it is not working fine, to rework

        error_counts[0] += test_sw_danger_point(sw_name, sw_value, sw_block, is_sw_upstream,
                                                upstream_limits, downstream_limits, print_ok)
        # error_counts[1] += test_fouling_point_danger_point(sw_name, sw_block, is_sw_upstream,
        #                                                    upstream_limits, downstream_limits, print_ok)
    if error_counts[0] > 0:
        print(f"{Color.blue}There was {Color.light_blue}{error_counts[0]}{Color.blue} "
              f"error{'s' if error_counts[0] >= 2 else ''} on R_CDV_5 "
              f"with the switch danger point.\n"
              f"{Color.reset}")
    if error_counts[1] > 0:
        print(f"{Color.blue}There was {Color.light_blue}{error_counts[1]}{Color.blue} "
              f"error{'s' if error_counts[1] >= 2 else ''} on R_CDV_5 "
              f"with the fouling points danger points."
              f"{Color.reset}\n")
    if sum(error_counts) == 0:
        print_success(f"\nThere was no error on R_CDV_5.")
    return sum(error_counts) == 0


def test_sw_danger_point(sw_name, sw_value, sw_block, is_sw_upstream, upstream_limits, downstream_limits,
                         print_ok: bool):
    relative_limits = upstream_limits if is_sw_upstream else downstream_limits
    sw_seg, sw_x = give_sw_pos(sw_value)
    error_count = 0
    for seg, x in relative_limits:
        dist = get_dist(sw_seg, sw_x, seg, x)
        if dist is None:
            continue
        min_slope, max_slope = get_min_and_max_slopes_on_virtual_seg(sw_seg, sw_x, seg, x)
        local_slope = -min_slope if is_sw_upstream else max_slope
        final_value, final_value_str, variables, all_sub_variables = get_min_dist(local_slope,
                                                                                  is_danger_point_a_switch=True)
        test = (dist >= final_value)
        if not test:
            print_error(f"Block {Color.yellow}{sw_block}{Color.reset} does not respect R_CDV_5:")
            print(f" · with danger point: the {Color.turquoise}switch{Color.reset} "
                  f"{Color.turquoise}{sw_name}{Color.reset} {(sw_seg, sw_x)},"  # from_seg_offset_to_kp()
                  f"\n\twith block limit {(seg, x)},"  # from_seg_offset_to_kp()
                  f"\n\tthe local slope is {Color.green}{local_slope:.3%}{Color.reset}"
                  f"\n\tthe distance to the danger point is {Color.green}{dist}{Color.reset}")
            print_sub_variables(all_sub_variables)
            print_variables(variables)
            print_final_value(final_value_str)
            error_count += 1
        elif print_ok:
            print_success(f"Block {Color.yellow}{sw_block}{Color.reset} respects R_CDV_5:")
            print(f" · with danger point: the {Color.turquoise}switch{Color.reset} "
                  f"{Color.turquoise}{sw_name}{Color.reset} {(sw_seg, sw_x)},"  # from_seg_offset_to_kp()
                  f"\n\twith block limit {(seg, x)},"  # from_seg_offset_to_kp()
                  f"\n\tthe local slope is {Color.green}{local_slope:.3%}{Color.reset}"
                  f"\n\tthe distance to the danger point is {Color.green}{dist}{Color.reset}")
            print_sub_variables(all_sub_variables)
            print_variables(variables)
            print_final_value(final_value_str)
    return error_count


def get_min_dist(local_slope, is_danger_point_a_switch: bool = False):
    # 1. If the danger point is a switch point,
    # at_deshunt_max_dist shall not be considered but only tag_accurate_laying_uncertainty
    # 2. If the danger point is a fouling point,
    # and the block not locking the switch is part of the IXL flank protection area, rule is not applicable.
    is_danger_point_a_switch = False  # TODO
    at_deshunt_max_dist = get_param_value("at_deshunt_max_dist")
    tag_accurate_laying_uncertainty = get_param_value("tag_accurate_laying_uncertainty")
    additional_value = at_deshunt_max_dist if not is_danger_point_a_switch else tag_accurate_laying_uncertainty
    additional_value_str = "at_deshunt_max_dist" if not is_danger_point_a_switch else "tag_accurate_laying_uncertainty"

    all_sub_variables = dict()
    at_rollback_dist_local_slope = get_at_rollback_dist(local_slope, variables=all_sub_variables)
    mtc_rollback_dist_local_slope = get_at_rollback_dist(local_slope, mtc=True, variables=all_sub_variables)
    final_value = round(additional_value + max(at_rollback_dist_local_slope, mtc_rollback_dist_local_slope), 3)
    variables = {
        additional_value_str: f"{additional_value} m",
        "at_rollback_dist_local_slope": f"{at_rollback_dist_local_slope} m",
        "mtc_rollback_dist_local_slope": f"{mtc_rollback_dist_local_slope} m",
    }
    final_value_str = {
        f"{additional_value_str} + max(at_rollback_dist_local_slope, mtc_rollback_dist_local_slope)": f"{final_value} m"
    }
    return final_value, final_value_str, variables, all_sub_variables


def test_fouling_point_danger_point(sw_name, sw_block, is_sw_upstream, upstream_limits, downstream_limits,
                                    print_ok: bool):
    relative_limits = downstream_limits if is_sw_upstream else upstream_limits
    fp_dict = fouling_points_associated_to_sw(sw_name)
    error_count = 0
    for heel_direction, (fp_seg, fp_x) in fp_dict.items():
        # if fp_seg is None or fp_x is None:
        #     print(f"Block {Color.yellow}{sw_block}{Color.reset} respects R_CDV_5:"
        #           f" · with danger point: the {Color.turquoise}{heel_direction} fouling point{Color.reset} "
        #           f"of {Color.turquoise}{sw_name}{Color.reset}"
        #           f"\n\tno fouling point is defined.")
        #     continue
        for seg, x in relative_limits:
            if fp_seg is None or fp_x is None:
                min_slope, max_slope = get_min_and_max_slopes_at_point(seg, x)
            else:
                min_slope, max_slope = get_min_and_max_slopes_on_virtual_seg(fp_seg, fp_x, seg, x)
            local_slope = max_slope if is_sw_upstream else -min_slope
            final_value, final_value_str, variables, all_sub_variables = get_min_dist(local_slope)
            dist = get_dist(fp_seg, fp_x, seg, x)
            if dist is None:
                print(f"Block {Color.yellow}{sw_block}{Color.reset} respects R_CDV_5:"
                      f" · with danger point: the {Color.turquoise}{heel_direction} fouling point{Color.reset} "
                      f"of {Color.turquoise}{sw_name}{Color.reset}"
                      f"\n\twith fouling point position {(fp_seg,fp_x)},"  # from_seg_offset_to_kp()
                      f"\n\twith block limit {(seg, x)},"  # from_seg_offset_to_kp()
                      f"\n\tthe local slope is {Color.green}{local_slope:.3%}{Color.reset}"
                      f"\n\tno distance is found.")
                print_final_value(final_value_str)
                continue
            test = (dist >= final_value)
            if not test:
                print_error(f"Block {Color.yellow}{sw_block}{Color.reset} does not respect R_CDV_5:")
                print(f" · with danger point: the {Color.turquoise}{heel_direction} fouling point{Color.reset} "
                      f"of {Color.turquoise}{sw_name}{Color.reset},"
                      f"\n\twith fouling point position {(fp_seg,fp_x)},"  # from_seg_offset_to_kp()
                      f"\n\twith block limit {(seg, x)},"  # from_seg_offset_to_kp()
                      f"\n\tthe local slope is {Color.green}{local_slope:.3%}{Color.reset}"
                      f"\n\tthe distance to the danger point is {Color.green}{dist}{Color.reset}")
                print_sub_variables(all_sub_variables)
                print_variables(variables)
                print_final_value(final_value_str)
                error_count += 1
            elif print_ok:
                print_success(f"Block {Color.yellow}{sw_block}{Color.reset} respects R_CDV_5:")
                print(f" · with danger point: the {Color.turquoise}{heel_direction} fouling point{Color.reset} "
                      f"of {Color.turquoise}{sw_name}{Color.reset},"
                      f"\n\twith fouling point position {(fp_seg,fp_x)},"  # from_seg_offset_to_kp()
                      f"\n\twith block limit {(seg, x)},"  # from_seg_offset_to_kp()
                      f"\n\tthe local slope is {Color.green}{local_slope:.3%}{Color.reset}"
                      f"\n\tthe distance to the danger point is {Color.green}{dist}{Color.reset}")
                # print_sub_variables(all_sub_variables)
                # print_variables(variables)
                print_final_value(final_value_str)
    return error_count
