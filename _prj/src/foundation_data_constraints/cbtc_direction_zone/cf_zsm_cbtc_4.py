#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point, are_zones_intersecting, get_zones_intersecting_zone


__all__ = ["cf_zsm_cbtc_4"]


def cf_zsm_cbtc_4():
    print_title("Verification of CF_ZSM_CBTC_4", color=Color.mint_green)
    ivb_joints_dict = _get_ivb_joints_dict()
    switch_points_dict = _get_switch_points_dict()
    end_of_track_segments_dict = _get_end_of_track_segments_dict()

    print_section_title("Verifying, for the \"BLOCK_DIRECTION_LOCKING\" CDZ, that their limits match an IVB limit. "
                        "In addition, as a CDZ is a linear part of the line, CDZ will be cut in 3 on switches over the "
                        "3 parts of the switch.")
    print("To respect CC_CV_16 (a VB shall be covered at most by a unique CDZ), CDZ on switch heel parts shall not "
          "cover the switch VB (as it is already covered on the point side by the point segment CDZ). And as we "
          "know that the switch VB heel parts are 1cm long (CC_CV_23), the CDZ on the heel parts shall start 1cm "
          "from the switch point on both heels, meaning that the point segment part of the switch is fully covered "
          "by a CDZ until the switch, and then there is a 1cm gap on each heel with no CDZ on, and then a new CDZ "
          "can start on each heel.\n"
          "Besides, CDZ may be extended at end of line and its limit match the last segment end.\n")
    no_ko = True
    cdz_dict = load_sheet(DCSYS.ZSM_CBTC)
    for cdz_name, cdz_value in cdz_dict.items():
        authorized_direction = get_dc_sys_value(cdz_value, DCSYS.ZSM_CBTC.SensAutorise)
        related_ivb = get_dc_sys_value(cdz_value, DCSYS.ZSM_CBTC.InterlockingVirtualBlock)
        if authorized_direction != DirectionZoneType.BLOCK_DIRECTION_LOCKING:
            print(f"CBTC Direction Zone {cdz_name} is not of type \"BLOCK_DIRECTION_LOCKING\" "
                  f"(but {authorized_direction}), it is not managed by the tool.")
            continue
        if not _check_cdz_block_dl(cdz_name, related_ivb, ivb_joints_dict, switch_points_dict,
                                   end_of_track_segments_dict):
            no_ko = False
    if no_ko:
        print_log("No KO found.")

    _check_one_ivb_on_cdz()


def _check_one_ivb_on_cdz():
    print_section_title("Verifying that only 1 IVB covers each CDZ, and that it is the specified related IVB "
                        "of the CDZ.")
    no_ko = True
    cdz_dict = load_sheet(DCSYS.ZSM_CBTC)
    for cdz_name, cdz_value in cdz_dict.items():
        related_ivb = get_dc_sys_value(cdz_value, DCSYS.ZSM_CBTC.InterlockingVirtualBlock)
        ivb_on_cdz = get_zones_intersecting_zone(DCSYS.IVB, DCSYS.ZSM_CBTC, cdz_name)
        if not ivb_on_cdz:
            print_error(f"No IVB covers CBTC Direction Zone {cdz_name}.")
            no_ko = False
            continue
        if len(ivb_on_cdz) > 1:
            print_error(f"Multiple IVBs cover CBTC Direction Zone {cdz_name}:")
            print(ivb_on_cdz)
            no_ko = False
        if related_ivb not in ivb_on_cdz:
            print_error(f"The related IVB of CBTC Direction Zone {cdz_name} ({related_ivb}) is not on the CDZ:")
            print(ivb_on_cdz)
            no_ko = False

    if no_ko:
        print_log("No KO found.")


def _check_cdz_block_dl(cdz_name: str, related_ivb: str,
                        ivb_joints_dict: dict[tuple[str, float], list[str]],
                        switch_points_dict: dict[tuple[str, float], str],
                        end_of_track_segments_dict: dict[tuple[str, float], str]) -> bool:
    # CBTC Direction Zone of type BLOCK_DIRECTION_LOCKING shall have their limits matching either:
    # an IVB limit,
    # a switch (as it is a linear part of the line, it will be cut in 3 on the 3 parts of the switch),
    # or an end-of-line segment end (CDZ may be extended at end of line).
    # We will compare the CDZ limit positions with the 3 different dictionaries describing these 3 possible types,
    # to check if the limit matches with one of them.
    no_ko = True
    cdz_limits = get_object_position(DCSYS.ZSM_CBTC, cdz_name)
    for cdz_limit in cdz_limits:
        matching_ivb_limit = _is_limit_in_dict(cdz_limit, ivb_joints_dict)
        matching_switch_position = _is_limit_in_dict(cdz_limit, switch_points_dict)
        matching_end_position = _is_limit_in_dict(cdz_limit, end_of_track_segments_dict)

        if matching_ivb_limit is None and matching_switch_position is None:
            if matching_end_position is None:
                print_error(f"Limit {cdz_limit} of CBTC Direction Zone {cdz_name} of type BLOCK_DIRECTION_LOCKING is "
                            f"not found matching an IVB limit or a switch point, and is not extended at end-of-line.")
                no_ko = False
            else:
                end_segment = end_of_track_segments_dict[matching_end_position]
                if not are_zones_intersecting(DCSYS.IVB, related_ivb, DCSYS.Seg, end_segment):
                    print_error(f"Limit {cdz_limit} of CBTC Direction Zone {cdz_name} of type BLOCK_DIRECTION_LOCKING "
                                f"matches line end {matching_end_position} but segment {end_segment} does not "
                                f"intersect the related IVB of the CDZ: {related_ivb}.")
                    no_ko = False
            continue

        if matching_ivb_limit is not None and matching_switch_position is not None:
            print_warning(f"Weird limit {cdz_limit} of CBTC Direction Zone {cdz_name} of type BLOCK_DIRECTION_LOCKING: "
                          f"it is found matching both an IVB limit and a switch point:")
            print(ivb_joints_dict[matching_ivb_limit], switch_points_dict[matching_switch_position])
            no_ko = False

        if matching_ivb_limit is not None:
            limit_ivb = ivb_joints_dict[matching_ivb_limit]
            if related_ivb not in limit_ivb:
                print_error(f"Limit {cdz_limit} of CBTC Direction Zone {cdz_name} of type BLOCK_DIRECTION_LOCKING "
                            f"matches IVB limit {limit_ivb} but it is not coherent with the related "
                            f"IVB of the CDZ: {related_ivb}.")
                no_ko = False

        if matching_switch_position is not None:
            switch_name = switch_points_dict[matching_switch_position]
            ivb_on_switch = get_zones_on_point(DCSYS.IVB, *get_object_position(DCSYS.Aig, switch_name[:-2]))[0]
            if related_ivb != ivb_on_switch:
                print_error(f"Limit {cdz_limit} of CBTC Direction Zone {cdz_name} of type BLOCK_DIRECTION_LOCKING "
                            f"matches switch point {switch_name} but this switch is on IVB {ivb_on_switch}, which is "
                            f"not coherent with the related IVB of the CDZ: {related_ivb}.")
                no_ko = False

    return no_ko


def _is_limit_in_dict(limit: tuple[str, float], test_dict: dict[tuple[str, float], Any]) -> Optional[tuple[str, float]]:
    for test_limit in test_dict:
        if are_points_matching(*limit, *test_limit):
            return test_limit
    return None


def _get_ivb_joints_dict() -> dict[tuple[str, float], list[str]]:
    ivb_joints_dict = dict()
    ivb_list = get_objects_list(DCSYS.IVB)
    for ivb_name in ivb_list:
        ivb_limits = get_object_position(DCSYS.IVB, ivb_name)
        for ivb_limit in ivb_limits:
            limit_already_in_dict = _is_limit_in_dict(ivb_limit, ivb_joints_dict)
            if limit_already_in_dict is None:
                ivb_joints_dict[ivb_limit] = [ivb_name]
            else:
                ivb_joints_dict[limit_already_in_dict].append(ivb_name)
    return ivb_joints_dict


def _get_switch_points_dict() -> dict[tuple[str, float], str]:
    switch_points_dict = dict()
    switch_dict = load_sheet(DCSYS.Aig)
    for switch_name, switch_value in switch_dict.items():
        # Center position
        switch_position = get_object_position(DCSYS.Aig, switch_name)
        switch_points_dict[switch_position] = f"{switch_name}_C"

        # Heels position
        point_segment = get_dc_sys_value(switch_value, DCSYS.Aig.SegmentPointe)
        left_heel_segment = get_dc_sys_value(switch_value, DCSYS.Aig.SegmentTg)
        right_heel_segment = get_dc_sys_value(switch_value, DCSYS.Aig.SegmentTd)

        for heel_segment, heel_type in [(left_heel_segment, "L"), (right_heel_segment, "R")]:
            previous_segments = get_linked_segments(heel_segment, downstream=False)
            next_segments = get_linked_segments(heel_segment, downstream=True)
            # To respect CC_CV_16 (a VB shall be covered at most by a unique CDZ), and as we know the heel parts are
            # of length 1cm (CC_CV_23), CDZ on the heel parts shall not cover the switch VB (as it is already covered
            # by the point segment CDZ) and shall then start 1cm from the switch point on both heels.
            if point_segment in previous_segments:
                # 1 cm shifted from the segment start
                start_offset = .01
                heel_position = (heel_segment, start_offset)
            elif point_segment in next_segments:
                # 1 cm shifted from the segment end
                end_offset = round(get_segment_length(heel_segment) - .01, 2)
                heel_position = (heel_segment, end_offset)
            else:
                continue
            switch_points_dict[heel_position] = f"{switch_name}_{heel_type}"

    return switch_points_dict


def _get_end_of_track_segments_dict() -> dict[tuple[str, float], str]:
    res_dict = dict()
    seg_list = get_objects_list(DCSYS.Seg)
    for seg_name in seg_list:
        previous_segments = get_linked_segments(seg_name, downstream=False)
        next_segments = get_linked_segments(seg_name, downstream=True)
        if not previous_segments:
            res_dict[(seg_name, 0.)] = seg_name
        if not next_segments:
            res_dict[(seg_name, get_segment_length(seg_name))] = seg_name
    return res_dict
