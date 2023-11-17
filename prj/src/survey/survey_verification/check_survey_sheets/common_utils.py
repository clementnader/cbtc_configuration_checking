#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["add_info_to_survey", "add_extra_info_from_survey"]


def add_info_to_survey(survey_obj_info: Optional[dict[str]], track: str, dc_sys_kp: float):
    survey_track = survey_obj_info["track"] if survey_obj_info is not None else None
    surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
    surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
    comments = survey_obj_info["comments"] if survey_obj_info is not None else None

    return {"track": track, "dc_sys_kp": dc_sys_kp,
            "survey_track": survey_track, "surveyed_kp": surveyed_kp,
            "surveyed_kp_comment": surveyed_kp_comment, "comments": comments}


def add_extra_info_from_survey(used_objects_from_survey: list[str], survey_info: dict[str, dict[str]]):
    extra_dict = dict()
    for obj_name, obj_val in survey_info.items():
        if obj_name in used_objects_from_survey:
            continue
        obj_name = obj_val["obj_name"]
        extra_dict[(obj_name, obj_val["track"])] = \
            {"track": None, "dc_sys_kp": None, "survey_track": obj_val["track"], "surveyed_kp": obj_val["surveyed_kp"],
             "surveyed_kp_comment": obj_val["surveyed_kp_comment"], "comments": obj_val["comments"]}
    return extra_dict
