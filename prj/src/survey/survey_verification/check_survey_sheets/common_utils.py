#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["add_info_to_survey", "add_extra_info_from_survey", "test_names_in_survey"]


def add_info_to_survey(survey_obj_info: Optional[dict[str, Any]],
                       dc_sys_sheet: str, dc_sys_track: str, dc_sys_kp: float):
    survey_name = survey_obj_info["obj_name"] if survey_obj_info is not None else None
    survey_type = survey_obj_info["survey_type"] if survey_obj_info is not None else None
    survey_track = survey_obj_info["survey_track"] if survey_obj_info is not None else None
    survey_original_track = survey_obj_info["survey_original_track"] if survey_obj_info is not None else None
    surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
    surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
    comments = survey_obj_info["comments"] if survey_obj_info is not None else None

    return {"dc_sys_sheet": dc_sys_sheet, "dc_sys_track": dc_sys_track, "dc_sys_kp": dc_sys_kp,
            "survey_name": survey_name, "survey_type": survey_type,
            "survey_track": survey_track, "survey_original_track": survey_original_track,
            "surveyed_kp": surveyed_kp,
            "surveyed_kp_comment": surveyed_kp_comment, "comments": comments}


def add_extra_info_from_survey(used_objects_from_survey: list[str], survey_info: dict[str, dict[str, Any]]):
    extra_dict = dict()
    for obj_name, obj_val in survey_info.items():
        if obj_name in used_objects_from_survey:
            continue
        obj_name = obj_val["obj_name"]
        extra_dict[(obj_name, obj_val["survey_track"])] = \
            {"dc_sys_sheet": None, "dc_sys_track": None, "dc_sys_kp": None,
             "survey_name": obj_val["obj_name"], "survey_type": obj_val["survey_type"],
             "survey_track": obj_val["survey_track"], "survey_original_track": obj_val["survey_original_track"],
             "surveyed_kp": obj_val["surveyed_kp"],
             "surveyed_kp_comment": obj_val["surveyed_kp_comment"], "comments": obj_val["comments"]}
    return extra_dict


def test_names_in_survey(test_names: list[str], track: str, survey_info: dict[str, Any]) -> str:
    for test_name in test_names:
        test_name_in_survey = _test_name_in_survey(test_name, track, survey_info)
        if test_name_in_survey is not None:
            return test_name_in_survey
    return f"{test_names[0]}__{track}".upper()  # default


def _test_name_in_survey(test_name: str, track: str, survey_info: dict[str, Any]):
    if test_name is not None and f"{test_name}__{track}".upper() in survey_info:
        return f"{test_name}__{track}".upper()
    return None
