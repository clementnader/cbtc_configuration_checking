#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ....utils import *
from ...survey_utils import *


__all__ = ["add_info_to_survey", "add_extra_info_from_survey", "test_names_in_survey",
           "get_corresponding_survey_one_limit_on_track", "get_corresponding_survey_two_limits_on_track",
           "get_smallest_unique_prefix_dict"]


def add_info_to_survey(survey_obj_info: Optional[dict[str, Any]],
                       dc_sys_sheet: str, dc_sys_track: str, dc_sys_original_track: str, dc_sys_kp: float):
    survey_name = survey_obj_info["obj_name"] if survey_obj_info is not None else None
    survey_type = survey_obj_info["survey_type"] if survey_obj_info is not None else None
    survey_track = survey_obj_info["survey_track"] if survey_obj_info is not None else None
    survey_original_track = survey_obj_info["survey_original_track"] if survey_obj_info is not None else None
    surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
    surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
    comments = survey_obj_info["comments"] if survey_obj_info is not None else None

    return {"dc_sys_sheet": dc_sys_sheet, "dc_sys_track": dc_sys_track,
            "dc_sys_original_track": dc_sys_original_track, "dc_sys_kp": dc_sys_kp,
            "survey_name": survey_name, "survey_type": survey_type,
            "survey_track": survey_track, "survey_original_track": survey_original_track,
            "surveyed_kp": surveyed_kp,
            "surveyed_kp_comment": surveyed_kp_comment, "comments": comments}


def add_extra_info_from_survey(used_objects_from_survey: list[str], survey_info: dict[str, dict[str, Any]]):
    extra_dict = dict()
    for obj_name, obj_val in survey_info.items():
        if obj_name in used_objects_from_survey:
            continue
        extra_dict[(obj_name, obj_val["survey_track"])] = \
            {"dc_sys_sheet": None, "dc_sys_track": None, "dc_sys_original_track": None, "dc_sys_kp": None,
             "survey_name": obj_val["obj_name"], "survey_type": obj_val["survey_type"],
             "survey_track": obj_val["survey_track"], "survey_original_track": obj_val["survey_original_track"],
             "surveyed_kp": obj_val["surveyed_kp"],
             "surveyed_kp_comment": obj_val["surveyed_kp_comment"], "comments": obj_val["comments"]}
    return extra_dict


def test_names_in_survey(test_names: list[str], track: str, survey_info: dict[str, Any]) -> str:
    test_names = _get_unique_list(test_names)
    for test_name in test_names:
        test_name_in_survey = _test_name_in_survey(test_name, track, survey_info)
        if test_name_in_survey is not None:
            return test_name_in_survey
    # try removing leading zeros
    for test_name in test_names:
        test_name_in_survey = _test_name_in_survey(test_name, track, survey_info, remove_leading_zeros=True)
        if test_name_in_survey is not None:
            return test_name_in_survey
    return f"{test_names[0]}__{track}".upper()  # default


def _get_unique_list(i_list: list[Optional[str]]):
    new_list = list()
    for x in i_list:
        if x is not None and x not in new_list:
            new_list.append(x)
    return new_list


def _test_name_in_survey(test_name: str, track: str, survey_info: dict[str, Any], remove_leading_zeros: bool = False):
    if remove_leading_zeros:
        test_name = "_".join(re.sub(r"^0*", "", x) for x in test_name.split("_"))
        test_list = ["_".join(re.sub(r"^0*", "", x) for x in survey_name.split("_"))
                     for survey_name in survey_info]
    else:
        test_list = survey_info.keys()
    if test_name is not None and f"{test_name}__{track}".upper() in test_list:
        return f"{test_name}__{track}".upper()
    return None


def get_corresponding_survey_one_limit_on_track(dc_sys_limits_on_track: list[tuple[str, float]],
                                                associated_survey_dict: dict[tuple[str, float], Optional[str]],
                                                survey_limits_on_track: list[str],
                                                survey_info: dict[str, Any]
                                                ) -> dict[tuple[str, float], Optional[str]]:
    for (lim_track, lim_kp) in dc_sys_limits_on_track:
        if not survey_limits_on_track:  # extremity not surveyed
            associated_survey_dict[(lim_track, lim_kp)] = None
        elif len(survey_limits_on_track) == 1:  # only 1 extremity corresponding,
            # we do the survey comparison with this one
            survey_name = survey_limits_on_track[0]
            associated_survey_dict[(lim_track, lim_kp)] = survey_name
        else:  # multiple extremities corresponding,
            # find for which survey limit the difference is the smallest
            test_differences = list()
            for survey_name in survey_limits_on_track:
                surveyed_kp = survey_info[survey_name]["surveyed_kp"]
                reversed_polarity = check_polarity(lim_kp, surveyed_kp)
                if reversed_polarity:
                    diff = abs(abs(lim_kp) - abs(surveyed_kp))
                else:
                    diff = abs(lim_kp - surveyed_kp)
                test_differences.append((diff, survey_name))
            closest_survey_name = sorted(test_differences, key=lambda x: x[0])[0][1]
            associated_survey_dict[(lim_track, lim_kp)] = closest_survey_name
    return associated_survey_dict


def get_corresponding_survey_two_limits_on_track(dc_sys_limits_on_track: list[tuple[str, float]],
                                                 survey_name_dict: dict[tuple[str, float], Optional[str]],
                                                 survey_limits_on_track: list[str],
                                                 survey_info: dict[str, Any]
                                                 ) -> dict[tuple[str, float], Optional[str]]:
    if not survey_limits_on_track:  # extremities not surveyed
        pass
    elif len(survey_limits_on_track) == 1:  # only 1 extremity corresponding,
        # find for which DC_SYS limit the difference is the smallest
        survey_name = survey_limits_on_track[0]
        surveyed_kp = survey_info[survey_name]["surveyed_kp"]
        test_differences = list()
        for (lim_track, lim_kp) in dc_sys_limits_on_track:
            reversed_polarity = check_polarity(lim_kp, surveyed_kp)
            if reversed_polarity:
                diff = abs(abs(lim_kp) - abs(surveyed_kp))
            else:
                diff = abs(lim_kp - surveyed_kp)
            test_differences.append((diff, (lim_track, lim_kp)))
        closest_dc_sys_limit = sorted(test_differences, key=lambda x: x[0])[0][1]
        survey_name_dict[closest_dc_sys_limit] = survey_name
    else:  # multiple extremities corresponding,
        # find for which DC_SYS limits combination the difference is the smallest
        (lim1_track, lim1_kp), (lim2_track, lim2_kp) = dc_sys_limits_on_track
        test_differences = list()
        for survey_name_corresponding_to_1 in survey_limits_on_track:
            surveyed_kp_1 = survey_info[survey_name_corresponding_to_1]["surveyed_kp"]
            for survey_name_corresponding_to_2 in [survey_name for survey_name in survey_limits_on_track
                                                   if survey_name != survey_name_corresponding_to_1]:
                surveyed_kp_2 = survey_info[survey_name_corresponding_to_2]["surveyed_kp"]
                reversed_polarity = (check_polarity(lim1_kp, surveyed_kp_1) and check_polarity(lim2_kp, surveyed_kp_2))
                if reversed_polarity:
                    diff1 = abs(abs(lim1_kp) - abs(surveyed_kp_1))
                    diff2 = abs(abs(lim2_kp) - abs(surveyed_kp_2))
                else:
                    diff1 = abs(lim1_kp - surveyed_kp_1)
                    diff2 = abs(lim2_kp - surveyed_kp_2)
                test_differences.append((diff1 + diff2,
                                         {(lim1_track, lim1_kp): survey_name_corresponding_to_1,
                                          (lim2_track, lim2_kp): survey_name_corresponding_to_2}))
        closest_combination = sorted(test_differences, key=lambda x: x[0])[0][1]
        survey_name_dict.update(closest_combination)
    return survey_name_dict


def get_smallest_unique_prefix_dict(input_dict: dict[str, str]) -> dict[str, str]:
    res_dict = dict()
    list_of_splits = [value.split("_") for value in input_dict.values()]

    for key, split in zip(input_dict.keys(), list_of_splits):
        other_splits = [other_split for other_split in list_of_splits if other_split != split]
        level = 1
        prefix = "_".join(split[:level])

        while level < len(split):
            other_prefixes = ["_".join(other_split[:level]) for other_split in other_splits]
            if prefix not in other_prefixes:  # unique prefix
                break
            level += 1
            prefix = "_".join(split[:level])

        res_dict[key] = prefix
    return res_dict
