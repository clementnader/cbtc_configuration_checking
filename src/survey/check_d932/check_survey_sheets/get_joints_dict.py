#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *


def get_joints_dict():
    joints_dict = dict()
    block_dict = load_sheet(DCSYS.CDV)
    for block_name, block_val in block_dict.items():
        matching_blocks = _find_associated_blocks(block_name, block_val)
        for limit_position, matching_block_name in matching_blocks.items():
            joint_name, joint_name2 = _get_corresponding_joint(matching_block_name, limit_position)
            joint_name, joint_name2 = _get_new_joint_names(joints_dict, joint_name, joint_name2, limit_position)
            if joint_name is not None:
                joints_dict[joint_name] = {"other_name": joint_name2, "position": limit_position}
    return joints_dict


def _get_new_joint_names(joints_dict, joint_name, joint_name2, limit_position):
    new_joint_name = joint_name
    new_joint_name2 = joint_name2
    if joint_name in joints_dict:
        if limit_position != joints_dict[joint_name]["position"]:
            new_joint_name = joint_name + "_2"
            new_joint_name2 = joint_name2 + "_2" if joint_name2 is not None else None
        else:
            new_joint_name = None
            new_joint_name2 = None
    if joint_name2 is not None and joint_name2 in joints_dict:
        if limit_position != joints_dict[joint_name2]["position"]:
            new_joint_name = joint_name2 + "_2"
            new_joint_name2 = joint_name + "_2"
        else:
            new_joint_name = None
            new_joint_name2 = None
    return new_joint_name, new_joint_name2


def _get_corresponding_joint(matching_block_name: str, limit_position):
    list_matching_ivb = _get_ivb_matching_limit(limit_position)
    if not list_matching_ivb:
        print(matching_block_name, limit_position)
    if matching_block_name.startswith("_"):
        ivb_name = list_matching_ivb[0]
        joint_name = "JOI_" + ivb_name.removeprefix("IVB_") + matching_block_name
        joint_name2 = None
    else:
        ivb_name = list_matching_ivb[0]
        ivb_name2 = list_matching_ivb[1]
        joint_name = _get_joint_name(ivb_name, ivb_name2)
        joint_name2 = _get_joint_name(ivb_name2, ivb_name)
    return joint_name, joint_name2


def _get_ivb_matching_limit(limit_position):
    list_matching_ivb = list()
    ivb_dict = load_sheet(DCSYS.IVB)
    for ivb_name, ivb_val in ivb_dict.items():
        ivb_limits = list(get_dc_sys_zip_values(ivb_val, DCSYS.IVB.Limit.Track, DCSYS.IVB.Limit.Kp))
        if any(ivb == limit_position for ivb in ivb_limits):
            list_matching_ivb.append(ivb_name.upper())
    return list_matching_ivb


def _get_joint_name(block_name: str, matching_block_name: str):
    return "JOI_" + block_name.removeprefix("IVB_") + _get_joint_suffix_name(block_name, matching_block_name)


def _find_associated_blocks(ref_block_name, ref_block_val):
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
    matching_blocks = _add_none_limits(ref_block_name, matching_blocks)
    return matching_blocks


def _matching_limits(limits1, limits2):
    list_matching_limits = list()
    for track1, kp1 in limits1:
        for track2, kp2 in limits2:
            if track1 == track2 and kp1 == kp2:
                list_matching_limits.append((track1, kp1))
    return list_matching_limits


def _add_none_limits(block_name, matching_blocks):
    missing_limits = [lim for lim, matching_block in matching_blocks.items() if matching_block is None]
    if not missing_limits:
        return matching_blocks
    for missing_limit_counter, (missing_lim_track, missing_lim_kp) in enumerate(missing_limits, start=1):
        other_lim_on_same_track = [(track, kp) for track, kp in matching_blocks.keys()
                                   if (track, kp) != (missing_lim_track, missing_lim_kp)
                                   and track == missing_lim_track]
        if other_lim_on_same_track:
            other_lim_kp = float(other_lim_on_same_track[0][1])
            matching_blocks[(missing_lim_track, missing_lim_kp)] = "_right" if float(missing_lim_kp) > other_lim_kp \
                else "_left"
        else:
            matching_blocks[(missing_lim_track, missing_lim_kp)] = _add_switch_in_name(block_name, matching_blocks,
                                                                                       missing_limit_counter)
    return matching_blocks


def _add_switch_in_name(block_name: str, matching_blocks, missing_limit_counter: int):
    if len(matching_blocks.keys()) == 3:
        return _add_switch_in_name_for_divert(block_name)
    return f"_track_end_{missing_limit_counter}"


def _add_switch_in_name_for_divert(block_name: str):
    block_dict = load_sheet(DCSYS.CDV)
    seg_offset_limits = list(get_dc_sys_zip_values(block_dict[block_name], DCSYS.CDV.Extremite.Seg,
                                                   DCSYS.CDV.Extremite.X))
    sw = get_sw_associated_to_vb(seg_offset_limits)
    text = _get_joint_suffix_name(block_name, sw) + "_divert"
    return text


def _get_joint_suffix_name(block1_name: str, block2_name: str):
    split_diff_start = -1
    split1 = block1_name.split("_")[1:]  # remove the TC_
    split2 = block2_name.split("_")[1:]  # remove the TC_
    if not split1 or not split2:
        print_error(f"There is no underscore in block name {block1_name = } or {block2_name = }.")
        return "_" + block2_name
    for i, (t1, t2) in enumerate(zip(split1, split2)):
        if t1 != t2:
            split_diff_start = i
            break
    if split_diff_start == -1:
        print_warning(f"The whole name of {block1_name = } or of {block2_name = } is contained in the other.")
        split_diff_start = min(len(split1), len(split2)) - 1
    return "_" + "_".join(split2[split_diff_start:])
