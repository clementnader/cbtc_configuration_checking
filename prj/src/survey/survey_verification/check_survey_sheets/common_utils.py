#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["add_extra_info_from_survey"]


def add_extra_info_from_survey(used_objects_from_survey: list[str], survey_info: dict[str, dict[str]]):
    extra_dict = dict()
    for obj_val in survey_info.values():
        obj_name = obj_val["obj_name"]
        if obj_name in used_objects_from_survey:
            continue
        extra_dict[obj_name] = {"track": None, "dc_sys_kp": None,
                                "survey_track": obj_val["track"], "surveyed_kp": obj_val["surveyed_kp"],
                                "surveyed_kp_comment": obj_val["surveyed_kp_comment"], "comments": obj_val["comments"]}
    return extra_dict
