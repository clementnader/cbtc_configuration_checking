#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_get_cbtc_territory import *
from ...fouling_points_utils.load_fouling_point_file import *


__all__ = ["check_switch_flank_protection"]


def check_switch_flank_protection(in_cbtc: bool = False):  # TODO
    if in_cbtc:
        sw_dict = get_objects_in_cbtc_ter(DCSYS.Aig)
    else:
        sw_dict = load_sheet(DCSYS.Aig)

    status = True
    fp_info = load_fouling_point_info()
    for sw_name in sw_dict:
        fp_dist = fp_info.get(sw_name)
        if fp_dist is None:
            print_error(f"No Fouling Point information for {Color.yellow}{sw_name}{Color.reset}.")
            status = False
            continue
        if not _verify_flank(sw_name, fp_dist):
            status = False
    if status:
        print_log("No KO has been raised in the verification of the switch flank areas.")


def _verify_flank(sw_name: str, fp_dist: float) -> bool:
    status = True
    left_flank_area_list = list(get_dc_sys_zip_values(sw_name, DCSYS.Aig.AreaLeftPositionFlank.BeginSeg,
                                                      DCSYS.Aig.AreaLeftPositionFlank.BeginX,
                                                      DCSYS.Aig.AreaLeftPositionFlank.EndSeg,
                                                      DCSYS.Aig.AreaLeftPositionFlank.EndX,
                                                      DCSYS.Aig.AreaLeftPositionFlank.Direction))
    right_flank_area_list = list(get_dc_sys_zip_values(sw_name, DCSYS.Aig.AreaRightPositionFlank.BeginSeg,
                                                       DCSYS.Aig.AreaRightPositionFlank.BeginX,
                                                       DCSYS.Aig.AreaRightPositionFlank.EndSeg,
                                                       DCSYS.Aig.AreaRightPositionFlank.EndX,
                                                       DCSYS.Aig.AreaRightPositionFlank.Direction))
    sw_seg, sw_x = get_switch_position(sw_name)
    is_sw_upstream = is_switch_point_upstream_heels(sw_name)
    left_seg = get_dc_sys_value(sw_name, DCSYS.Aig.SegmentTg)
    right_seg = get_dc_sys_value(sw_name, DCSYS.Aig.SegmentTd)
    diamond_crossing, dc_switches = is_switch_on_diamond_crossing(sw_name)

    if not _verify_direct_flank(sw_name, fp_dist, right_seg, left_flank_area_list, is_sw_upstream, sw_seg, sw_x,
                                left_or_right="left"):
        status = False

    if not _verify_direct_flank(sw_name, fp_dist, left_seg, right_flank_area_list, is_sw_upstream, sw_seg, sw_x,
                                left_or_right="right"):
        status = False
    if diamond_crossing:
        pass

    return status


def _verify_direct_flank(sw_name: str, fp_dist: float, heel_seg: str,
                         corresponding_flank_area_list: list[tuple[str, float, str, float, str]],
                         is_sw_upstream: bool, sw_seg: str, sw_x: float, left_or_right: str) -> bool:
    status = True
    start_x_test_flank = 0 if is_sw_upstream else get_segment_length(heel_seg)
    first_flanks = [(start_seg, start_x, end_seg, end_x, direction)
                    for start_seg, start_x, end_seg, end_x, direction in corresponding_flank_area_list
                    if (start_seg, start_x) == (heel_seg, start_x_test_flank)
                    or (end_seg, end_x) == (heel_seg, start_x_test_flank)]
    if not first_flanks:
        print_error(f"For {Color.yellow}{sw_name}{Color.reset}, {left_or_right} flank area does not start from "
                    f"the switch point, at {(heel_seg, start_x_test_flank)}:")
        print(f"{corresponding_flank_area_list = }")
        status = False
    if len(first_flanks) > 1:
        print_error(f"For {Color.yellow}{sw_name}{Color.reset}, multiple {left_or_right} flank areas cover the same "
                    f"zone, starting from the switch point, at {(heel_seg, start_x_test_flank)}:")
        print(f"{corresponding_flank_area_list = }")
        status = False
    first_flank = first_flanks[0]
    if (first_flank[0], first_flank[1]) == (heel_seg, start_x_test_flank):
        start_seg, start_x = first_flank[0], first_flank[1]
        end_seg, end_x = first_flank[2], first_flank[3]
        direction = first_flank[4]
    else:
        start_seg, start_x = first_flank[2], first_flank[3]
        end_seg, end_x = first_flank[0], first_flank[1]
        direction = get_reverse_direction(first_flank[4])

    if is_sw_upstream != (direction == Direction.CROISSANT):
        print_error(f"For {Color.yellow}{sw_name}{Color.reset}, for {left_or_right} flank area, "
                    f"the direction {direction=} is not what is expected as the switch is "
                    f"{'upstream' if is_sw_upstream else 'downstream'}.")
        print(f"{corresponding_flank_area_list = }")
        status = False

    if start_seg == end_seg:
        if (end_x - start_x) * (1 if is_sw_upstream else -1) < fp_dist:
            print_error(f"For {Color.yellow}{sw_name}{Color.reset}, the {left_or_right} flank area is too short "
                        f"({fp_dist=}).")
            print(f"{corresponding_flank_area_list = }")
            status = False
        else:
            if len(corresponding_flank_area_list) > 1:
                print_warning(f"For {Color.yellow}{sw_name}{Color.reset}, for {left_or_right} flank area, "
                              f"the {first_flank} is enough ({fp_dist=}), extra flank areas can be deleted.")
                print(f"{corresponding_flank_area_list = }")
                status = False
    else:
        pass

    return status
