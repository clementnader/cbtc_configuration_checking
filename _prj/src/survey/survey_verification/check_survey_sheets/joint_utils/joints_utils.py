#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .....dc_sys import *


__all__ = ["find_associated_blocks", "get_display_name"]


def find_associated_blocks(ref_block_name: str, ref_block_value: dict,
                           sheet: Any, track_attribute: Any, kp_attribute: Any) -> dict[tuple[str, float], Optional[str]]:
    block_dict = load_sheet(sheet)
    ref_limits = list(get_dc_sys_zip_values(ref_block_value, track_attribute, kp_attribute))
    matching_blocks = {ref_limit: None for ref_limit in ref_limits}
    for block_name, block_value in block_dict.items():
        if block_name == ref_block_name:
            continue
        limits = list(get_dc_sys_zip_values(block_value, track_attribute, kp_attribute))
        list_matching_limits = _matching_limits(ref_limits, limits)
        for matching_lim in list_matching_limits:
            if matching_blocks[matching_lim] is not None:
                print_error(f"Limit {matching_lim} of block {ref_block_name} is matching with two different blocks:\n"
                            f"{matching_blocks[matching_lim]} and {block_name}.")
            matching_blocks[matching_lim] = block_name
    return matching_blocks


def _matching_limits(ref_limits: list[tuple[str, float]], limits: list[tuple[str, float]]) -> list[tuple[str, float]]:
    list_matching_limits = list()
    for track1, kp1 in ref_limits:
        for track2, kp2 in limits:
            if track1 == track2 and kp1 == kp2:
                list_matching_limits.append((track1, kp1))
    return list_matching_limits


def get_display_name(object_name: str, tc1: str, tc2: Optional[str], track: str,
                     joints_dict: dict[tuple[str, Optional[str], str],
                                       Union[tuple[tuple[str, float], str], tuple[str, float]]]) -> str:
    if tc2 is not None:
        same_name_joints = [(block1, block2) for (block1, block2, _) in joints_dict
                            if (block1, block2) == (tc1, tc2)]
        if len(same_name_joints) < 2:
            return object_name
        # There are multiple joints with this name, we precise in the name the track to get the unicity
        return object_name + f"__on_{track}"

    else:  # tc2 is None
        same_name_joints = [(block1, block2) for (block1, block2, _) in joints_dict
                            if (block1, block2) == (tc1, tc2)]
        if len(same_name_joints) < 2:
            return object_name
        if not object_name.endswith("__end_of_track"):
            return object_name
        # There are multiple joints with this name, we precise in the name the track to get the unicity
        return object_name + f"__on_{track}"
