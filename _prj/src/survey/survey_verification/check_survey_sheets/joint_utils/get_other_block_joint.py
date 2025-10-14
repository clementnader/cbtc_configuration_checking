#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .....utils import *
from .....cctool_oo_schema import *
from .....dc_sys import *


__all__ = ["get_corresponding_ivb_joint", "get_other_corresponding_tc_joint_on_limit_of_track",
           "get_other_corresponding_ivb_joint_on_limit_of_track"]


def get_corresponding_ivb_joint(tc1: str, tc2: Optional[str], limit_position: tuple[str, float]
                                ) -> tuple[Optional[str], Optional[str]]:
    list_matching_ivb = _get_ivb_matching_limit(limit_position)
    if not list_matching_ivb:
        if tc2 is None:
            pass  # end of track TC joint can be different from IVB joint
        else:
            print_error(f"No IVB has been found matching this limit {limit_position} between {tc1} and {tc2}.")
        return None, None
    if len(list_matching_ivb) > 2:
        print_error(f"More than 2 IVBs are matching this limit {limit_position} between {tc1} and {tc2}.")

    ivb_name = list_matching_ivb[0]
    ivb_name2 = list_matching_ivb[1] if len(list_matching_ivb) > 1 else None
    return ivb_name, ivb_name2


def _get_ivb_matching_limit(limit_position: tuple[str, float]) -> list[str]:
    list_matching_ivb = list()
    ivb_dict = load_sheet(DCSYS.IVB)
    for ivb_name, ivb_value in ivb_dict.items():
        ivb_limits = list(get_dc_sys_zip_values(ivb_value, DCSYS.IVB.Limit.Track, DCSYS.IVB.Limit.Kp))
        if any(ivb == limit_position for ivb in ivb_limits):
            list_matching_ivb.append(ivb_name)
    return list_matching_ivb


def get_other_corresponding_tc_joint_on_limit_of_track(tc1: str, tc2: Optional[str], limit_position: tuple[str, float]
                                                       ) -> tuple[Optional[str], Optional[str]]:
    # Check if there is a common limit with the (segment, offset) rather than (track, kp)
    if tc2 is not None:  # when no common limit was found
        return None, None
    tc_dict = load_sheet(DCSYS.CDV)

    tc_track_kp_limits = get_dc_sys_zip_values(tc_dict[tc1], DCSYS.CDV.Extremite.Voie, DCSYS.CDV.Extremite.Pk)
    tc_seg_offset_limits = get_dc_sys_zip_values(tc_dict[tc1], DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X)
    ref_limit_seg, ref_limit_x = [(seg, x) for (seg, x), (track, kp) in zip(tc_seg_offset_limits, tc_track_kp_limits)
                                  if (track, kp) == limit_position][0]

    list_matching_tc2 = list()
    for test_tc, test_tc_value in tc_dict.items():
        if test_tc == tc1:
            continue
        test_limits = get_dc_sys_zip_values(test_tc_value, DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X)
        if any(are_points_matching(ref_limit_seg, ref_limit_x, test_seg, test_x) for test_seg, test_x in test_limits):
            list_matching_tc2.append(test_tc)

    if not list_matching_tc2:
        return None, None

    if len(list_matching_tc2) > 1:
        print_error(f"More than one other block is matching limit {limit_position} of {tc1}:\n{list_matching_tc2}")

    return tc1, list_matching_tc2[0]


def get_other_corresponding_ivb_joint_on_limit_of_track(ivb1: str, ivb2: str, limit_position: tuple[str, float]
                                                        ) -> tuple[Optional[str], Optional[str]]:
    # Check if there is a common limit with the (segment, offset) rather than (track, kp)
    if ivb2 is not None:  # when no common limit was found
        return None, None
    ivb_dict = load_sheet(DCSYS.IVB)

    ivb_track_kp_limits = get_dc_sys_zip_values(ivb_dict[ivb1], DCSYS.IVB.Limit.Track, DCSYS.IVB.Limit.Kp)
    ivb_seg_offset_limits = get_dc_sys_zip_values(ivb_dict[ivb1], DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X)
    ref_limit_seg, ref_limit_x = [(seg, x) for (seg, x), (track, kp) in zip(ivb_seg_offset_limits, ivb_track_kp_limits)
                                  if (track, kp) == limit_position][0]

    list_matching_ivb2 = list()
    for test_ivb, test_ivb_value in ivb_dict.items():
        if test_ivb == ivb1:
            continue
        test_limits = get_dc_sys_zip_values(test_ivb_value, DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X)
        if any(are_points_matching(ref_limit_seg, ref_limit_x, test_seg, test_x) for test_seg, test_x in test_limits):
            list_matching_ivb2.append(test_ivb)

    if not list_matching_ivb2:
        return None, None

    if len(list_matching_ivb2) > 1:
        print_error(f"More than one other block is matching limit {limit_position} of {ivb1}:\n{list_matching_ivb2}")

    return ivb1, list_matching_ivb2[0]
