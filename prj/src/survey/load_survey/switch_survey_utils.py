#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...dc_sys import *


__all__ = ["add_switch_center_points"]


def add_switch_center_points(sw_survey_info: dict[str, dict[str]], survey_name: str) -> dict[str, dict[str]]:
    res_dict = dict()

    for survey_obj_info in sw_survey_info.values():
        obj_name = survey_obj_info["obj_name"]
        center_point_name, center_point_other_name, center_point_track, corresponding_sw_pos = (
            get_corresponding_center_switch_point_track(obj_name))
        if center_point_name is None:
            continue
        if center_point_name.upper() in sw_survey_info or center_point_other_name.upper() in sw_survey_info:
            continue  # center point already in survey
        heel_point_track = survey_obj_info["track"]
        if heel_point_track != center_point_track:
            continue

        old_comments = survey_obj_info["comments"]
        new_comments = (f"Center Switch Point {center_point_name} does not exist in survey {survey_name},\n"
                        f"{corresponding_sw_pos.capitalize()} Switch Point {obj_name} is used "
                        f"as they are on the same track.")
        comments = _add_comment_for_switch_point(new_comments, old_comments)

        res_dict[f"{center_point_name}__{center_point_track}".upper()] = {
            "obj_name": center_point_name, "track": center_point_track, "surveyed_kp": survey_obj_info["surveyed_kp"],
            "surveyed_kp_comment": survey_obj_info["surveyed_kp_comment"], "comments": comments
        }
    return res_dict


def _add_comment_for_switch_point(new_comments: Optional[str], old_comments: Optional[str]) -> Optional[str]:
    if new_comments is None:
        return old_comments
    if old_comments is None:
        return new_comments
    return f"{new_comments}\n\n{old_comments}"
