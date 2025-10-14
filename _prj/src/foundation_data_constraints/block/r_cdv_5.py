#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_get_cbtc_territory import *
from ...dc_sys_sheet_utils.ivb_utils import get_ivb_associated_to_sw
from ...dc_sys_sheet_utils.block_utils import get_block_associated_to_sw
from ...dc_sys_sheet_utils.slope_utils import *
from ...dc_sys_draw_path.dc_sys_path_and_distances import (is_seg_downstream,
                                                           get_all_positions_at_a_distance_from_a_point)
from ...dc_sys_draw_path.dc_sys_get_zones import (get_oriented_limits_of_object, get_dist_downstream_within_zone_limits,
                                                  is_point_in_zone_limits)
from ...dc_par import *
from ...dc_par_add_on_parameters import get_at_rollback_dist
from ...fouling_points_utils import *


__all__ = ["r_cdv_5", "r_ivb_1"]


def r_ivb_1(print_ok: bool = False):
    return r_cdv_5(ivb=True, print_ok=print_ok)


def r_cdv_5(ivb: bool = False, print_ok: bool = False):
    sw_dict = get_objects_in_cbtc_ter(DCSYS.Aig)
    fp_dict = load_fouling_point_info()
    if not fp_dict:
        print_warning("No Fouling Point information, the results will be only given for the switch as danger point.")

    error_counts = [0, 0]
    for sw_name in sw_dict:
        is_sw_upstream = is_switch_point_upstream_heels(sw_name)
        sw_block_list = _get_block_locking_area(sw_name, ivb)
        oriented_limits = _get_block_zone_limits(sw_block_list, ivb)

        error_counts[0] += test_sw_danger_point(sw_name, sw_block_list, is_sw_upstream,
                                                oriented_limits, ivb, print_ok)
        if fp_dict:
            error_counts[1] += test_fouling_point_danger_point(sw_name, sw_block_list, is_sw_upstream,
                                                               oriented_limits, ivb, fp_dict, print_ok)

    print()
    if error_counts[0] > 0:
        print(f"{Color.blue}There {'are' if error_counts[0] >= 2 else 'is'} "
              f"{Color.light_blue}{error_counts[0]}{Color.blue} "
              f"error{'s' if error_counts[0] >= 2 else ''} on {'R_CDV_5' if not ivb else 'R_IVB_1'} "
              f"with the switch danger point.\n"
              f"{Color.reset}")
    if error_counts[1] > 0:
        print(f"{Color.blue}There {'are' if error_counts[1] >= 2 else 'is'} "
              f"{Color.light_blue}{error_counts[1]}{Color.blue} "
              f"error{'s' if error_counts[1] >= 2 else ''} on {'R_CDV_5' if not ivb else 'R_IVB_1'} "
              f"with the fouling points danger points."
              f"{Color.reset}\n")
    if sum(error_counts) == 0:
        print_success(f"There is no error on {'R_CDV_5' if not ivb else 'R_IVB_1'}.")
    return sum(error_counts) == 0


def test_sw_danger_point(sw_name: str, sw_block_list: list[str], is_sw_upstream: bool,
                         oriented_limits: list[tuple[str, float, str]], ivb: bool,
                         print_ok: bool) -> int:
    relative_limits = _get_downstream_limits(sw_name, oriented_limits, downstream=not is_sw_upstream)
    sw_seg, sw_x = get_object_position(DCSYS.Aig, sw_name)
    error_count = 0

    if not is_point_in_zone_limits(oriented_limits, sw_seg, sw_x):
        print_error(f"Switch point {add_track_kp_to_position((sw_seg, sw_x))} is not inside "
                    f"Switch Block Locking Area: {sw_block_list} of switch {sw_name}.")
        error_count += 1
        return error_count

    for lim_seg, lim_x, lim_direction in relative_limits:
        dist = get_dist_downstream_within_zone_limits(sw_seg, sw_x, lim_seg, lim_x, downstream=not is_sw_upstream,
                                                      zone_limits=oriented_limits)
        if dist is None:
            continue
        min_slope, max_slope = get_min_and_max_slopes_in_zone_limits(
            [(sw_seg, sw_x, Direction.DECROISSANT if is_sw_upstream else Direction.CROISSANT),
             (lim_seg, lim_x, lim_direction)],
            polarity_ref_seg=sw_seg)
        local_slope = -min_slope if is_sw_upstream else max_slope
        final_value, final_value_str, variables, all_sub_variables = _get_min_dist(local_slope, ivb)
        test = (dist >= final_value)
        if not test:
            print_error(f"Block {Color.yellow}{sw_block_list}{Color.reset} does not respect "
                        f"{'R_CDV_5' if not ivb else 'R_IVB_1'}:")
            print(f" · with danger point: the {Color.cyan}switch{Color.reset} "
                  f"{Color.cyan}{sw_name}{Color.reset} {add_track_kp_to_position((sw_seg, sw_x))},"
                  f"\n\twith block limit {add_track_kp_to_position((lim_seg, lim_x))},"
                  f"\n\tthe local slope is {Color.green}{local_slope:.3%}{Color.reset}"
                  f"\n\tthe distance to the danger point is {Color.green}{dist}{Color.reset}")
            # print_sub_variables(all_sub_variables)
            # print_variables(variables)
            print_final_value(final_value_str)
            error_count += 1
        elif print_ok:
            print_success(f"Block {Color.yellow}{sw_block_list}{Color.reset} respects "
                          f"{'R_CDV_5' if not ivb else 'R_IVB_1'}:", end="")
            print(f" · with danger point: the {Color.cyan}switch{Color.reset} "
                  f"{Color.cyan}{sw_name}{Color.reset} {add_track_kp_to_position((sw_seg, sw_x))},"
                  f"\n\twith block limit {add_track_kp_to_position((lim_seg, lim_x))},"
                  f"\n\tthe local slope is {Color.green}{local_slope:.3%}{Color.reset}"
                  f"\n\tthe distance to the danger point is {Color.green}{dist}{Color.reset}")
            # print_sub_variables(all_sub_variables)
            # print_variables(variables)
            print_final_value(final_value_str)
    return error_count


def test_fouling_point_danger_point(sw_name: str, sw_block_list: list[str], is_sw_upstream: bool,
                                    oriented_limits: list[tuple[str, float, str]], ivb: bool,
                                    fp_dict: dict[str, float], print_ok: bool):
    relative_limits = _get_downstream_limits(sw_name, oriented_limits, downstream=is_sw_upstream)
    sw_seg, sw_x = get_switch_position(sw_name)
    error_count = 0
    fp_dist = fp_dict.get(sw_name)
    if not fp_dist:
        print_error(f"No fouling point information is found about switch {sw_name}.")
        error_count += 1
        return error_count
    list_fp_pos = get_all_positions_at_a_distance_from_a_point(
        sw_seg, sw_x, Direction.CROISSANT if is_sw_upstream else Direction.DECROISSANT, fp_dist)

    for fp_seg, fp_x, fp_direction in list_fp_pos:
        if not is_point_in_zone_limits(oriented_limits, fp_seg, fp_x):
            print_error(f"Fouling point {add_track_kp_to_position((fp_seg, fp_x))} is not inside "
                        f"Switch Block Locking Area: {sw_block_list} of switch {sw_name}.")
            error_count += 1
            continue
        for lim_seg, lim_x, lim_direction in relative_limits:
            dist = get_dist_downstream_within_zone_limits(fp_seg, fp_x, lim_seg, lim_x,
                                                          downstream=fp_direction==Direction.CROISSANT,
                                                          zone_limits=oriented_limits)
            if dist is None:
                continue
            min_slope, max_slope = get_min_and_max_slopes_in_zone_limits(
                [(fp_seg, fp_x, fp_direction),
                 (lim_seg, lim_x, lim_direction)],
                polarity_ref_seg=fp_seg)
            local_slope = max_slope if fp_direction==Direction.CROISSANT else -min_slope
            final_value, final_value_str, variables, all_sub_variables = _get_min_dist(local_slope, ivb)
            test = (dist >= final_value)
            if not test:
                print_error(f"Block {Color.yellow}{sw_block_list}{Color.reset} does not respect "
                            f"{'R_CDV_5' if not ivb else 'R_IVB_1'}:")
                print(f" · with danger point: the {Color.cyan}fouling point{Color.reset} "
                      f"of {Color.cyan}{sw_name}{Color.reset} {add_track_kp_to_position((fp_seg, fp_x, fp_direction))}"
                      f"\n\t(fouling point distance is {fp_dist}),"
                      f"\n\twith block limit {add_track_kp_to_position((lim_seg, lim_x, lim_direction))},"
                      f"\n\tthe local slope is {Color.green}{local_slope:.3%}{Color.reset}"
                      f"\n\tthe distance to the danger point is {Color.green}{dist}{Color.reset}")
                # print_sub_variables(all_sub_variables)
                # print_variables(variables)
                print_final_value(final_value_str)
                error_count += 1
            elif print_ok:
                print_success(f"Block {Color.yellow}{sw_block_list}{Color.reset} respects "
                              f"{'R_CDV_5' if not ivb else 'R_IVB_1'}:", end="")
                print(f" · with danger point: the {Color.cyan}fouling point{Color.reset} "
                      f"of {Color.cyan}{sw_name}{Color.reset} {add_track_kp_to_position((fp_seg, fp_x, fp_direction))}"
                      f"\n\t(fouling point distance is {fp_dist}),"
                      f"\n\twith block limit {add_track_kp_to_position((lim_seg, lim_x, lim_direction))},"
                      f"\n\tthe local slope is {Color.green}{local_slope:.3%}{Color.reset}"
                      f"\n\tthe distance to the danger point is {Color.green}{dist}{Color.reset}")
                # print_sub_variables(all_sub_variables)
                # print_variables(variables)
                print_final_value(final_value_str)
    return error_count


def _get_min_dist(local_slope, ivb: bool):
    at_deshunt_max_dist = get_parameter_value("at_deshunt_max_dist")
    if ivb:
        at_deshunt_max_dist = 0

    all_sub_variables = dict()
    at_rollback_dist_local_slope = get_at_rollback_dist(local_slope, variables=all_sub_variables)
    mtc_rollback_dist_local_slope = get_at_rollback_dist(local_slope, mtc=True, variables=all_sub_variables)
    final_value = round(at_deshunt_max_dist + max(at_rollback_dist_local_slope, mtc_rollback_dist_local_slope), 3)
    variables = {
        "at_deshunt_max_dist": f"{at_deshunt_max_dist} m",
        "at_rollback_dist_local_slope": f"{at_rollback_dist_local_slope} m",
        "mtc_rollback_dist_local_slope": f"{mtc_rollback_dist_local_slope} m",
    }
    if ivb:
        variables.pop("at_deshunt_max_dist")
    final_value_str = {
        f"{'' if ivb else 'at_deshunt_max_dist +'}"
        f"max(at_rollback_dist_local_slope, mtc_rollback_dist_local_slope)": f"{final_value} m"
    }
    return final_value, final_value_str, variables, all_sub_variables


def _get_downstream_limits(sw_name: str, oriented_limits: list[tuple[str, float, str]], downstream: bool
                           ) -> list[tuple[str, float, str]]:
    sw_seg, sw_x = get_object_position(DCSYS.Aig, sw_name)
    limits = list()
    for lim_seg, lim_x, lim_direction in oriented_limits:
        if (is_seg_downstream(sw_seg, lim_seg, sw_x, lim_x, downstream=downstream)
            # limit is downstream the switch point
                and is_seg_downstream(lim_seg, sw_seg, lim_x, sw_x, downstream=lim_direction==Direction.CROISSANT)):
                # and the switch point is correctly accessible from the oriented limit
            limits.append((lim_seg, lim_x, lim_direction))
    return limits


def _get_block_locking_area(sw_name: str, ivb: bool) -> list[str]:
    sw_block_locking_area = get_dc_sys_value(sw_name, DCSYS.Aig.SwitchBlockLockingArea.Ivb)

    if not sw_block_locking_area:
        # Switch Block Locking Area can be empty for MLK technology of IXL
        if not ivb:
            sw_block = get_block_associated_to_sw(sw_name)
        else:
            sw_block = get_ivb_associated_to_sw(sw_name)
        return [sw_block]

    if ivb:
        return sw_block_locking_area

    tc_list = [get_dc_sys_value(ivb_name, DCSYS.IVB.RelatedBlock) for ivb_name in sw_block_locking_area]
    return tc_list


def _get_block_zone_limits(tc_list: list[str], ivb: bool) -> list[tuple[str, float, str]]:
    limits = list()
    for tc_name in tc_list:
        if ivb:
            oriented_limits = get_oriented_limits_of_object(DCSYS.IVB, tc_name)
        else:
            oriented_limits = get_oriented_limits_of_object(DCSYS.CDV, tc_name)
        limits.extend(oriented_limits)
    return remove_common_limits_of_oriented_limits(limits)
