#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .....utils import *
from .....cctool_oo_schema import *
from .....dc_sys import *


__all__ = ["get_joints_dict"]


def get_joints_dict() -> dict[tuple[str, Optional[str], str], tuple[str, float]]:
    joints_dict = dict()
    block_dict = load_sheet(DCSYS.CDV)
    for block_name, block_val in block_dict.items():
        matching_blocks = _find_associated_blocks(block_name, block_val)
        for limit_position, matching_block_name in matching_blocks.items():
            track = limit_position[0]
            joint = (block_name, matching_block_name, track)
            joint2 = (matching_block_name, block_name, track) if matching_block_name is not None else None

            if joint not in joints_dict and (joint2 is None or joint2 not in joints_dict):
                joints_dict[joint] = limit_position
                continue

            if joint2 is not None:
                if joint in joints_dict and limit_position != joints_dict[joint]:
                    print_error(f"Found another joint between the same blocks and on the same track: {joint}\n"
                                f"but at a different position {joints_dict[joint]} vs {limit_position}.")
                if joint2 in joints_dict and limit_position != joints_dict[joint2]:
                    print_error(f"Found another joint between the same blocks and on the same track: {joint2}\n"
                                f"but at a different position {joints_dict[joint2]} vs {limit_position}.")
            else:
                if joint in joints_dict and limit_position != joints_dict[joint]:
                    # A block with two end-of-track limits on the same track
                    print_log(f"\nBlock {Color.yellow}{block_name}{Color.reset} in DC_SYS possesses 2 end-of-track "
                              f"limits on the same track {Color.light_yellow}{track}{Color.reset} "
                              f"at {Color.default}KP {joints_dict[joint][1]}{Color.reset} "
                              f"and {Color.default}KP {limit_position[1]}{Color.reset}.")
                    joints_dict[(block_name, matching_block_name, track + "__1")] = joints_dict[joint]
                    del joints_dict[joint]
                    joints_dict[(block_name, matching_block_name, track + "__2")] = limit_position

    return joints_dict


def _find_associated_blocks(ref_block_name: str, ref_block_val: dict) -> dict[tuple[str, float], Optional[str]]:
    block_dict = load_sheet(DCSYS.CDV)
    ref_limits = list(get_dc_sys_zip_values(ref_block_val, DCSYS.CDV.Extremite.Voie, DCSYS.CDV.Extremite.Pk))
    matching_blocks = {ref_limit: None for ref_limit in ref_limits}
    for block_name, block_val in block_dict.items():
        if block_name == ref_block_name:
            continue
        limits = list(get_dc_sys_zip_values(block_val, DCSYS.CDV.Extremite.Voie, DCSYS.CDV.Extremite.Pk))
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


def _get_missing_limits_per_track(missing_limits: list[tuple[str, float]]) -> dict[str, list[float]]:
    missing_limits_dict_per_track = dict()
    for missing_lim_track, missing_lim_kp in missing_limits:
        if missing_lim_track not in missing_limits_dict_per_track:
            missing_limits_dict_per_track[missing_lim_track] = list()
        missing_limits_dict_per_track[missing_lim_track].append(missing_lim_kp)
    return missing_limits_dict_per_track
