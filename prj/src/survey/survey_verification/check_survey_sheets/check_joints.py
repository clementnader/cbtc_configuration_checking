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

    objs_dict = get_joints_dict()
    list_used_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in objs_dict.items():
        track, dc_sys_kp = obj_val["position"]

        survey_name = _get_obj_names_in_survey(obj_name, obj_val, survey_info, objs_dict)
        survey_obj_info = survey_info.get(survey_name)

        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)
        obj_name = survey_obj_info["obj_name"] if survey_obj_info is not None else obj_name

        res_dict[obj_name] = add_info_to_survey(survey_obj_info, track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict


def _get_obj_names_in_survey(obj_name: str, obj_val: dict[str], survey_info: dict[str],
                             objs_dict: dict[str, dict[str]],
                             second_try: bool = False) -> Optional[str]:
    other_names = obj_val["other_names"]
    track, _ = obj_val["position"]
    for test_name in [obj_name] + other_names:
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

    survey_name = _get_obj_names_in_survey(obj_name, obj_val, survey_info, objs_dict, second_try=True)
    if survey_name is not None:
        return survey_name

    survey_name = _test_one_obj_on_track(obj_name, track, objs_dict, survey_info)
    if survey_name is not None:
        return survey_name

    return obj_name


def _test_one_obj_on_track(obj_name: str, track: str, objs_dict: dict[str, dict[str]], survey_info: dict[str]
                           ) -> Optional[str]:
    list_obj_on_track = [obj for obj, obj_val in objs_dict.items()
                         if obj_val["position"][0] == track]
    list_survey_obj_on_track = [survey_name for survey_name, survey_obj_info in survey_info.items()
                                if survey_obj_info["track"] == track]
    if len(list_obj_on_track) == 1 and len(list_survey_obj_on_track) == 1 and list_obj_on_track[0] == obj_name:
        return list_survey_obj_on_track[0]
    return None


def _remove_leading_zeros_and_trailing_letters(test_name: str) -> str:
    res_name = "_".join(word.removeprefix("0") for word in test_name.split("_"))
    res_name = delete_middle_capture_group(res_name, re.compile("(_[0-9]+)([A-Z]+)(_)"))
    res_name = delete_middle_capture_group(res_name, re.compile("(_[0-9]+)([A-Z]+)($)"))
    return res_name


def _is_name_in_survey(obj_name: str, track, survey_info: dict[str]) -> tuple[bool, Optional[str]]:
    # Trivial case, the name in survey matches directly
    if obj_name in survey_info:
        return True, obj_name

    # We take the names in survey starting with the obj_name, and if it is only one in this case, we take it
    list_matching_objs = _get_matching_objs_in_survey(obj_name, track, survey_info)
    if len(list_matching_objs) == 1:
        return True, list_matching_objs[0]

    # One limit on track
    if obj_name.endswith(f"__on_{track}".upper()):
        clean_name = obj_name.removesuffix(f"__on_{track}".upper())
        list_matching_objs = _get_matching_objs_in_survey(clean_name, track, survey_info)
        if len(list_matching_objs) != 1:
            return False, None
        return True, list_matching_objs[0]

    # For the blocks limit where we have not found another block limit matching
    pattern_one_limit_per_track = re.compile("_TRACK_END$")
    pattern_left = re.compile("_LEFT$")
    pattern_right = re.compile("_RIGHT$")

    # One limit on track
    if pattern_one_limit_per_track.search(obj_name) is not None:
        clean_name = re.sub(pattern_one_limit_per_track, "", obj_name)
        clean_name = clean_name.removesuffix(f"__{track}".upper())
        list_matching_objs = _get_matching_objs_in_survey(clean_name, track, survey_info)
        if len(list_matching_objs) != 1:
            return False, None
        return True, list_matching_objs[0]

    # Two limits on track
    matched_pattern = None
    associated_func = None
    if pattern_left.search(obj_name) is not None:
        matched_pattern = pattern_left
        associated_func = min
    if pattern_right.search(obj_name) is not None:
        matched_pattern = pattern_right
        associated_func = max

    if matched_pattern:
        clean_name = re.sub(matched_pattern, "", obj_name)
        list_matching_objs = _get_matching_objs_in_survey(clean_name, track, survey_info)
        if len(list_matching_objs) != 2:
            return False, None
        matching_objs_kp = [survey_info[matching_obj]["surveyed_kp"] for matching_obj in list_matching_objs]
        matching_obj = [test_obj for test_obj, kp in zip(list_matching_objs, matching_objs_kp)
                        if kp == associated_func(matching_objs_kp)][0]
        return True, matching_obj

    # Default
    return False, None


def _get_matching_objs_in_survey(obj_name: str, track: str, survey_info: dict[str]) -> list[str]:
    list_matching_objs = list()
    for survey_name, survey_obj_info in survey_info.items():
        survey_track = survey_obj_info["track"]
        if track == survey_track and _survey_name_matching(survey_name, obj_name):
            list_matching_objs.append(survey_name)
    return list_matching_objs


def _survey_name_matching(survey_name: str, obj_name: str) -> bool:
    if not survey_name.startswith(obj_name):
        return False
    suffix = survey_name.removeprefix(obj_name)

    suffix = re.sub("_SWP?[A-Z0-9]+_[0-9]+", "", suffix)  # some switches are named SWP and others SW
    suffix = re.sub("_SWP?[A-Z0-9]+", "", suffix)  # some switches are named SWP and others SW
    suffix = suffix.removesuffix("_LEFT").removesuffix("_RIGHT").removesuffix("_DIRECT").removesuffix("_DIVERT")
    if not suffix:
        return True
    return False
