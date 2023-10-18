#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *


__all__ = ["get_joints_dict"]


def get_joints_dict() -> dict[str, dict[str]]:
    joints_dict = dict()
    block_dict = load_sheet(DCSYS.CDV)
    for block_name, block_val in block_dict.items():
        matching_blocks = _find_associated_blocks(block_name, block_val)
        for limit_position, matching_block_name in matching_blocks.items():
            joint_name, joint_name2, list_matching_ivb = _get_corresponding_ivb_joint(matching_block_name,
                                                                                      limit_position)
            joint_name, joint_name2 = _get_new_joint_names(joints_dict, joint_name, joint_name2, limit_position)
            if joint_name is not None:
                tc_joint_name, tc_joint_name2 = _get_corresponding_tc_joint(block_name, matching_block_name)
                ivb_other_name, ivb_other_name2 = _get_ivb_other_names_limit_of_track(limit_position, list_matching_ivb)
                tc_other_name, tc_other_name2 = _get_tc_other_names_limit_of_track(limit_position, block_name,
                                                                                   tc_joint_name2)
                joints_dict[joint_name] = {"other_names": [joint_name2, tc_joint_name, tc_joint_name2,
                                                           ivb_other_name, ivb_other_name2,
                                                           tc_other_name, tc_other_name2],
                                           "position": limit_position}
    return joints_dict


def _get_new_joint_names(joints_dict: dict[str, dict[str]], joint_name: str, joint_name2: Optional[str],
                         limit_position: tuple[str, float]) -> tuple[Optional[str], Optional[str]]:
    new_joint_name = joint_name
    new_joint_name2 = joint_name2
    track = limit_position[0]
    if joint_name in joints_dict:
        if limit_position != joints_dict[joint_name]["position"]:
            old_track = joints_dict[joint_name]["position"][0]
            if old_track == track:
                print_warning(f"Joint {joint_name} is already in the dictionary of joints.")
                print(f"Old position: {joints_dict[joint_name]['position']}")
                print(f"New position: {limit_position}")
                new_joint_name = joint_name + "_2"
                new_joint_name2 = joint_name2 + "_2" if joint_name2 is not None else None
            else:
                joints_dict[f"{joint_name}__on_{old_track}"] = joints_dict[joint_name]
                del joints_dict[joint_name]
                new_joint_name = f"{joint_name}__on_{track}"
                new_joint_name2 = f"{joint_name2}__on_{track}"
        else:
            new_joint_name = None
            new_joint_name2 = None
    if joint_name2 is not None and joint_name2 in joints_dict:
        if limit_position != joints_dict[joint_name2]["position"]:
            old_track = joints_dict[joint_name2]["position"][0]
            if old_track == track:
                print_warning(f"Joint {joint_name2} is already in the dictionary of joints.")
                print(f"Old position: {joints_dict[joint_name2]['position']}")
                print(f"New position: {limit_position}")
                new_joint_name = joint_name2 + "_2"
                new_joint_name2 = joint_name + "_2"
            else:
                joints_dict[f"{joint_name2}__on_{old_track}"] = joints_dict[joint_name]
                del joints_dict[joint_name2]
                new_joint_name = f"{joint_name2}__on_{track}"
                new_joint_name2 = f"{joint_name}__on_{track}"
        else:
            new_joint_name = None
            new_joint_name2 = None
    return new_joint_name, new_joint_name2


def _get_corresponding_ivb_joint(matching_block_name: str, limit_position: tuple[str, float]
                                 ) -> tuple[str, Optional[str], list[str]]:
    list_matching_ivb = _get_ivb_matching_limit(limit_position)
    if not list_matching_ivb:
        print_warning(f"No IVB has been found matching this limit {limit_position} of block {matching_block_name}.")
    if matching_block_name.startswith("_"):
        ivb_name = list_matching_ivb[0]
        joint_name = "JOI_" + ivb_name.removeprefix("IVB_") + matching_block_name
        joint_name2 = None
    else:
        ivb_name = list_matching_ivb[0]
        ivb_name2 = list_matching_ivb[1]
        joint_name = _get_joint_name(ivb_name, ivb_name2)
        joint_name2 = _get_joint_name(ivb_name2, ivb_name)
    return joint_name, joint_name2, list_matching_ivb


def _get_ivb_matching_limit(limit_position: tuple[str, float]) -> list[str]:
    list_matching_ivb = list()
    ivb_dict = load_sheet(DCSYS.IVB)
    for ivb_name, ivb_val in ivb_dict.items():
        ivb_limits = list(get_dc_sys_zip_values(ivb_val, DCSYS.IVB.Limit.Track, DCSYS.IVB.Limit.Kp))
        if any(ivb == limit_position for ivb in ivb_limits):
            list_matching_ivb.append(ivb_name)
    return list_matching_ivb


def _get_corresponding_tc_joint(block_name: str, matching_block_name: str) -> tuple[str, Optional[str]]:
    if matching_block_name.startswith("_"):
        joint_name = "JOI_" + block_name.removeprefix("TC_") + matching_block_name
        joint_name2 = None
    else:
        joint_name = _get_joint_name(matching_block_name, block_name)
        joint_name2 = _get_joint_name(block_name, matching_block_name)
    return joint_name, joint_name2


def _get_ivb_other_names_limit_of_track(limit_position: tuple[str, float], list_matching_ivb: list[str]
                                        ) -> tuple[Optional[str], Optional[str]]:
    if len(list_matching_ivb) == 2:
        return None, None
    ivb_name = list_matching_ivb[0]
    ivb_dict = load_sheet(DCSYS.IVB)
    ivb_track_kp_limits = get_dc_sys_zip_values(ivb_dict[ivb_name], DCSYS.IVB.Limit.Track, DCSYS.IVB.Limit.Kp)
    ivb_seg_offset_limits = get_dc_sys_zip_values(ivb_dict[ivb_name], DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X)
    ref_limit_seg, ref_limit_x = [(seg, x) for (seg, x), (track, kp) in zip(ivb_seg_offset_limits, ivb_track_kp_limits)
                                  if (track, kp) == limit_position][0]
    list_matching_ivb_2 = list()
    for test_ivb, test_ivb_value in ivb_dict.items():
        test_limits = get_dc_sys_zip_values(test_ivb_value, DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X)
        if any(are_points_matching(ref_limit_seg, ref_limit_x, test_seg, test_x) for test_seg, test_x in test_limits):
            list_matching_ivb_2.append(test_ivb)

    if len(list_matching_ivb_2) == 1:
        return None, None

    ivb_name = list_matching_ivb_2[0]
    ivb_name2 = list_matching_ivb_2[1]
    joint_name = _get_joint_name(ivb_name, ivb_name2)
    joint_name2 = _get_joint_name(ivb_name2, ivb_name)
    return joint_name, joint_name2


def _get_tc_other_names_limit_of_track(limit_position: tuple[str, float], block_name: str, tc_joint_name2: Optional[str]
                                       ) -> tuple[Optional[str], Optional[str]]:
    if tc_joint_name2 is not None:
        return None, None
    cdv_dict = load_sheet(DCSYS.CDV)
    cdv_track_kp_limits = get_dc_sys_zip_values(cdv_dict[block_name], DCSYS.CDV.Extremite.Voie, DCSYS.CDV.Extremite.Pk)
    cdv_seg_offset_limits = get_dc_sys_zip_values(cdv_dict[block_name], DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X)
    ref_limit_seg, ref_limit_x = [(seg, x) for (seg, x), (track, kp) in zip(cdv_seg_offset_limits, cdv_track_kp_limits)
                                  if (track, kp) == limit_position][0]
    list_matching_cdv_2 = list()
    for test_cdv, test_cdv_value in cdv_dict.items():
        test_limits = get_dc_sys_zip_values(test_cdv_value, DCSYS.CDV.Extremite.Seg, DCSYS.CDV.Extremite.X)
        if any(are_points_matching(ref_limit_seg, ref_limit_x, test_seg, test_x) for test_seg, test_x in test_limits):
            list_matching_cdv_2.append(test_cdv)

    if len(list_matching_cdv_2) == 1:
        return None, None

    cdv_name = list_matching_cdv_2[0]
    cdv_name2 = list_matching_cdv_2[1]
    joint_name = _get_joint_name(cdv_name, cdv_name2)
    joint_name2 = _get_joint_name(cdv_name2, cdv_name)
    return joint_name, joint_name2


def _get_joint_name(block_name: str, matching_block_name: str) -> str:
    return ("JOI_" + block_name.removeprefix("IVB_").removeprefix("TC_")
            + _get_joint_suffix_name(block_name, matching_block_name))


def _find_associated_blocks(ref_block_name: str, ref_block_val: dict) -> dict[tuple[str, float], str]:
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


def _matching_limits(ref_limits: list[tuple[str, float]], limits: list[tuple[str, float]]) -> list[tuple[str, float]]:
    list_matching_limits = list()
    for track1, kp1 in ref_limits:
        for track2, kp2 in limits:
            if track1 == track2 and kp1 == kp2:
                list_matching_limits.append((track1, kp1))
    return list_matching_limits


def _add_none_limits(block_name: str, matching_blocks: dict[tuple[str, float], str]) -> dict[tuple[str, float], str]:
    missing_limits = [lim for lim, matching_block in matching_blocks.items() if matching_block is None]
    if not missing_limits:
        return matching_blocks
    missing_limits_dict_per_track = _get_missing_limits_per_track(missing_limits)
    for missing_lim_track, missing_lim_kp_list in missing_limits_dict_per_track.items():
        nb_of_limits_on_track = len(missing_lim_kp_list)
        if nb_of_limits_on_track == 1:
            matching_blocks[(missing_lim_track, missing_lim_kp_list[0])] = f"__{missing_lim_track}_track_end"
        elif nb_of_limits_on_track == 2:
            min_lim_kp = min(missing_lim_kp_list)
            max_lim_kp = max(missing_lim_kp_list)
            matching_blocks[(missing_lim_track, min_lim_kp)] = "_left"
            matching_blocks[(missing_lim_track, max_lim_kp)] = "_right"
        else:
            print_warning(f"More than 2 extremities on the same track {missing_lim_track} for block {block_name}.")
            for missing_limit_counter, missing_lim_kp in enumerate(missing_lim_kp_list, start=1):
                matching_blocks[(missing_lim_track, missing_lim_kp)] = f"_track_end_{missing_limit_counter}"
    return matching_blocks


def _get_missing_limits_per_track(missing_limits: list[tuple[str, float]]) -> dict[str, list[float]]:
    missing_limits_dict_per_track = dict()
    for missing_lim_track, missing_lim_kp in missing_limits:
        if missing_lim_track not in missing_limits_dict_per_track:
            missing_limits_dict_per_track[missing_lim_track] = list()
        missing_limits_dict_per_track[missing_lim_track].append(missing_lim_kp)
    return missing_limits_dict_per_track


def _get_joint_suffix_name(block1_name: str, block2_name: str) -> str:
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
        split_diff_start = min(len(split1), len(split2)) - 1
    return "_" + "_".join(split2[split_diff_start:])
