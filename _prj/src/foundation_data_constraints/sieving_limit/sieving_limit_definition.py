#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_get_zones import get_oriented_limits_of_object


__all__ = ["check_sieving_limit_definition"]


def check_sieving_limit_definition():
    print_title("Verification of Sieving Limits Definition", color=Color.mint_green)
    no_ko = True
    sl_dict = load_sheet(DCSYS.Sieving_Limit)
    for sl_name, sl_value in sl_dict.items():
        sl_position = get_object_position(DCSYS.Sieving_Limit, sl_name)
        sl_type = get_dc_sys_value(sl_value, DCSYS.Sieving_Limit.Type)
        related_block = get_dc_sys_value(sl_value, DCSYS.Sieving_Limit.RelatedBlock)
        if sl_type == SievingLimitType.BUFFER:
            if related_block is not None:
                print_error(f"Sieving Limit {Color.orange}{sl_name}{Color.reset} of type {Color.beige}{sl_type}"
                            f"{Color.reset} has a defined [Related Block] {related_block} while it should be empty.")
                no_ko = False
            matching_buffer = _sl_position_matches_a_buffer(sl_name, sl_type, sl_position)
            if matching_buffer is None:
                print_error(f"Sieving Limit {Color.orange}{sl_name}{Color.reset} of type {Color.beige}{sl_type}"
                            f"{Color.reset} matches no buffer.")
                no_ko = False

        elif sl_type == SievingLimitType.BLOCK:
            if _check_sl_matches_related_block(sl_name, sl_type, sl_position, related_block):
                # OK
                continue
            no_ko = False
            matching_block = _sl_position_matches_a_block_limit(sl_position)
            if matching_block is not None:
                print_error(f"Sieving Limit {Color.orange}{sl_name}{Color.reset} of type {Color.beige}{sl_type}"
                            f"{Color.reset} matches limit of block {Color.yellow}{matching_block}{Color.reset} "
                            f"instead of [Related Block] {related_block}.")
            else:
                print_error(f"Sieving Limit {Color.orange}{sl_name}{Color.reset} of type {Color.beige}{sl_type}"
                            f"{Color.reset} matches no block limit {Color.default}([Related Block] {related_block})"
                            f"{Color.reset}.")

        else:
            print_error(f"Unknown Sieving Limit type {Color.beige}{sl_type}{Color.reset} for "
                        f"{Color.orange}{sl_name}{Color.reset}.")
            no_ko = False
    if no_ko:
        print_log("No KO found on the constraint.")


def _sl_position_matches_a_buffer(sl_name: str, sl_type: str, sl_position: tuple[str, float, str]) -> Optional[str]:
    sl_seg, sl_x, sl_direction = sl_position
    sig_dict = load_sheet(DCSYS.Sig)
    for sig_name, sig_value in sig_dict.items():
        sig_type = get_dc_sys_value(sig_value, DCSYS.Sig.Type)
        if sig_type != SignalType.HEURTOIR:
            continue
        buffer_position = get_object_position(DCSYS.Sig, sig_name)
        buffer_seg, buffer_x, buffer_direction = buffer_position
        if are_points_matching(sl_seg, sl_x, buffer_seg, buffer_x):
            if sl_direction == buffer_direction:
                return sig_name
            else:
                print_error(f"Sieving Limit {Color.orange}{sl_name}{Color.reset} of type {Color.beige}{sl_type}"
                            f"{Color.reset} matches {sig_name} but in opposite direction: Sieving Limit Direction "
                            f"should be {Color.yellow}{buffer_direction}{Color.reset}.")
    return None


def _check_sl_matches_related_block(sl_name: str, sl_type: str, sl_position: tuple[str, float, str],
                                    related_block: str) -> bool:
    sl_seg, sl_x, sl_direction = sl_position
    block_oriented_limits = get_oriented_limits_of_object(DCSYS.CDV, related_block)
    for block_oriented_limit in block_oriented_limits:
        joint_seg, joint_x, joint_direction = block_oriented_limit
        if are_points_matching(sl_seg, sl_x, joint_seg, joint_x):
            if sl_direction == joint_direction:
                return True
            else:
                print_error(f"Sieving Limit {Color.orange}{sl_name}{Color.reset} of type {Color.beige}{sl_type}"
                            f"{Color.reset} matches [Related Block] {related_block} limit "
                            f"{(joint_seg, joint_x)} but in opposite direction: Sieving Limit Direction "
                            f"should be {Color.yellow}{joint_direction}{Color.reset}.", end="")
                return False
    print_error(f"Sieving Limit {Color.orange}{sl_name}{Color.reset} of type {Color.beige}{sl_type}{Color.reset} "
                f"does not match any [Related Block] {related_block} limit.")
    return False


def _sl_position_matches_a_block_limit(sl_position: tuple[str, float, str]) -> Optional[str]:
    sl_seg, sl_x, sl_direction = sl_position
    block_list = get_objects_list(DCSYS.CDV)
    for block_name in block_list:
        block_oriented_limits = get_oriented_limits_of_object(DCSYS.CDV, block_name)
        for block_oriented_limit in block_oriented_limits:
            joint_seg, joint_x, joint_direction = block_oriented_limit
            if are_points_matching(sl_seg, sl_x, joint_seg, joint_x):
                if sl_direction == joint_direction:
                    return block_name
    return None
