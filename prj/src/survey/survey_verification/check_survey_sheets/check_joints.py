#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ....utils import *
from ....cctool_oo_schema import *
from .get_joints_dict import *
from .common_utils import *


# Block_Joint
def check_joints(dc_sys_sheet, res_sheet_name: str, survey_info: dict[str, dict[str, float]]):
    assert dc_sys_sheet == DCSYS.CDV
    assert res_sheet_name == "Block_Joint"

    joints_dict = get_joints_dict()
    res_dict = dict()
    added_joints_from_survey = list()
    for joint_name, joint_val in joints_dict.items():
        survey_name = _get_joint_names_in_survey(joint_name, joint_val, survey_info, joints_dict)
        survey_obj_info = survey_info.get(survey_name)

        if survey_obj_info is not None:
            added_joints_from_survey.append(survey_name)

        joint_name = survey_obj_info["obj_name"] if survey_obj_info is not None else joint_name
        survey_track = survey_obj_info["track"] if survey_obj_info is not None else None
        surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
        surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
        comments = survey_obj_info["comments"] if survey_obj_info is not None else None

        track, dc_sys_kp = joint_val["position"]
        res_dict[joint_name] = {"track": track, "dc_sys_kp": dc_sys_kp,
                                "survey_track": survey_track, "surveyed_kp": surveyed_kp,
                                "surveyed_kp_comment": surveyed_kp_comment, "comments": comments}

    res_dict.update(add_extra_info_from_survey(added_joints_from_survey, survey_info))
    return res_dict


def _get_joint_names_in_survey(joint_name: str, joint_val: dict[str], survey_info: dict[str],
                               joints_dict: dict[str, dict[str]],
                               second_try: bool = False) -> Optional[str]:
    other_names = joint_val["other_names"]
    track, _ = joint_val["position"]
    for test_name in [joint_name] + other_names:
        if test_name is None:
            continue
        test_name = test_name.upper()
        if second_try:
            test_name = _remove_leading_zeros_and_trailing_letters(test_name)
        exist_flag, survey_name = _is_name_in_survey(test_name, track, survey_info)
        if exist_flag:
            return survey_name

    if second_try:
        return None

    survey_name = _get_joint_names_in_survey(joint_name, joint_val, survey_info, joints_dict, second_try=True)
    if survey_name is not None:
        return survey_name

    survey_name = _test_one_joint_on_track(joint_name, track, joints_dict, survey_info)
    if survey_name is not None:
        return survey_name

    return joint_name


def _test_one_joint_on_track(joint_name: str, track: str, joints_dict: dict[str, dict[str]], survey_info: dict[str]
                             ) -> Optional[str]:
    list_joint_on_track = [joint for joint, joint_val in joints_dict.items()
                           if joint_val["position"][0] == track]
    list_survey_joint_on_track = [survey_name for survey_name, survey_obj_info in survey_info.items()
                                  if survey_obj_info["track"] == track]
    if len(list_joint_on_track) == 1 and len(list_survey_joint_on_track) == 1 and list_joint_on_track[0] == joint_name:
        return list_survey_joint_on_track[0]
    return None


def _remove_leading_zeros_and_trailing_letters(test_name: str) -> str:
    res_name = "_".join(word.removeprefix("0") for word in test_name.split("_"))
    res_name = delete_middle_capture_group(res_name, re.compile("(_[0-9]+)([A-Z]+)(_)"))
    res_name = delete_middle_capture_group(res_name, re.compile("(_[0-9]+)([A-Z]+)($)"))
    return res_name


def _is_name_in_survey(joint_name: str, track, survey_info: dict[str]) -> tuple[bool, Optional[str]]:
    # Trivial case, the name in survey matches directly
    if joint_name in survey_info:
        return True, joint_name

    # We take the names in survey starting with the joint_name, and if it is only one in this case, we take it
    list_matching_joints = _get_matching_joints_in_survey(joint_name, track, survey_info)
    if len(list_matching_joints) == 1:
        return True, list_matching_joints[0]

    # One limit on track
    if joint_name.endswith(f"__on_{track}".upper()):
        clean_name = joint_name.removesuffix(f"__on_{track}".upper())
        list_matching_joints = _get_matching_joints_in_survey(clean_name, track, survey_info)
        if len(list_matching_joints) != 1:
            return False, None
        return True, list_matching_joints[0]

    # For the blocks limit where we have not found another block limit matching
    pattern_one_limit_per_track = re.compile("_TRACK_END$")
    pattern_left = re.compile("_LEFT$")
    pattern_right = re.compile("_RIGHT$")

    # One limit on track
    if pattern_one_limit_per_track.search(joint_name) is not None:
        clean_name = re.sub(pattern_one_limit_per_track, "", joint_name)
        clean_name = clean_name.removesuffix(f"__{track}".upper())
        list_matching_joints = _get_matching_joints_in_survey(clean_name, track, survey_info)
        if len(list_matching_joints) != 1:
            return False, None
        return True, list_matching_joints[0]

    # Two limits on track
    matched_pattern = None
    associated_func = None
    if pattern_left.search(joint_name) is not None:
        matched_pattern = pattern_left
        associated_func = min
    if pattern_right.search(joint_name) is not None:
        matched_pattern = pattern_right
        associated_func = max

    if matched_pattern:
        clean_name = re.sub(matched_pattern, "", joint_name)
        list_matching_joints = _get_matching_joints_in_survey(clean_name, track, survey_info)
        if len(list_matching_joints) != 2:
            return False, None
        matching_joints_kp = [survey_info[matching_joint]["surveyed_kp"] for matching_joint in list_matching_joints]
        matching_joint = [test_joint for test_joint, kp in zip(list_matching_joints, matching_joints_kp)
                          if kp == associated_func(matching_joints_kp)][0]
        return True, matching_joint

    # Default
    return False, None


def _get_matching_joints_in_survey(joint_name: str, track: str, survey_info: dict[str]) -> list[str]:
    list_matching_joints = list()
    for survey_name, survey_obj_info in survey_info.items():
        survey_track = survey_obj_info["track"]
        if track == survey_track and _survey_name_matching(survey_name, joint_name):
            list_matching_joints.append(survey_name)
    return list_matching_joints


def _survey_name_matching(survey_name: str, joint_name: str) -> bool:
    if not survey_name.startswith(joint_name):
        return False
    suffix = survey_name.removeprefix(joint_name)

    suffix = re.sub("_SWP?[A-Z0-9]+_[0-9]+", "", suffix)  # some switches are named SWP and others SW
    suffix = re.sub("_SWP?[A-Z0-9]+", "", suffix)  # some switches are named SWP and others SW
    suffix = suffix.removesuffix("_LEFT").removesuffix("_RIGHT").removesuffix("_DIRECT").removesuffix("_DIVERT")
    if not suffix:
        return True
    return False
