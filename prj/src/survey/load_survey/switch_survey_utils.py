#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...dc_sys_sheet_utils.switch_utils import (get_corresponding_center_switch_point_track,
                                                get_corresponding_heels_switch_point_track)


__all__ = ["add_switch_center_points", "add_switch_heel_points"]


def add_switch_center_points(sw_survey_info: dict[str, dict[str, Any]], survey_name: str) -> dict[str, dict[str, Any]]:
    res_dict = dict()

    for survey_obj_info in sw_survey_info.values():
        obj_name = survey_obj_info["obj_name"]
        center_point_name, center_point_other_name, center_point_track, corresponding_sw_pos = (
            get_corresponding_center_switch_point_track(obj_name))
        if center_point_name is None:
            continue
        if (f"{center_point_name}__{center_point_track}".upper() in sw_survey_info
                or f"{center_point_other_name}__{center_point_track}".upper() in sw_survey_info):
            continue  # center point already in survey
        heel_point_track = survey_obj_info["survey_track"]
        if heel_point_track.upper() != center_point_track.upper():
            continue

        old_comments = survey_obj_info["comments"]
        new_comments = (f"Center Switch Point {center_point_name} does not exist in survey:\n{survey_name},\n"
                        f"{corresponding_sw_pos.capitalize()} Switch Point {obj_name} is used\n"
                        f"as they are on the same track.")
        comments = _add_comment_for_switch_point(new_comments, old_comments)

        res_dict[f"{center_point_name}__{center_point_track}".upper()] = {
            "survey_type": survey_obj_info["survey_type"],
            "obj_name": obj_name, "survey_track": center_point_track.upper(),
            "survey_original_track": survey_obj_info["survey_original_track"],
            "surveyed_kp": survey_obj_info["surveyed_kp"],
            "surveyed_kp_comment": survey_obj_info["surveyed_kp_comment"], "comments": comments
        }
    return res_dict


def add_switch_heel_points(sw_survey_info: dict[str, dict[str, Any]], survey_name: str) -> dict[str, dict[str, Any]]:
    res_dict = dict()

    for survey_obj_info in sw_survey_info.values():
        obj_name = survey_obj_info["obj_name"]
        heel_point_name, heel_point_other_name, heel_point_track, corresponding_sw_pos = (
            get_corresponding_heels_switch_point_track(obj_name))
        if heel_point_name is None:
            continue
        if (f"{heel_point_name}__{heel_point_track}".upper() in sw_survey_info
                or f"{heel_point_other_name}__{heel_point_track}".upper() in sw_survey_info):
            continue  # center point already in survey
        center_point_track = survey_obj_info["survey_track"]
        if heel_point_track.upper() != center_point_track.upper():
            continue

        old_comments = survey_obj_info["comments"]
        new_comments = (f"{corresponding_sw_pos.capitalize()} Switch Point {heel_point_name} does not exist in survey:"
                        f"\n{survey_name},\n"
                        f"Center Switch Point {obj_name} is used\n"
                        f"as they are on the same track.")
        comments = _add_comment_for_switch_point(new_comments, old_comments)

        res_dict[f"{heel_point_name}__{heel_point_track}".upper()] = {
            "survey_type": survey_obj_info["survey_type"],
            "obj_name": obj_name, "survey_track": heel_point_track.upper(),
            "survey_original_track": survey_obj_info["survey_original_track"],
            "surveyed_kp": survey_obj_info["surveyed_kp"],
            "surveyed_kp_comment": survey_obj_info["surveyed_kp_comment"], "comments": comments
        }
    return res_dict


def _add_comment_for_switch_point(new_comments: Optional[str], old_comments: Optional[str]) -> Optional[str]:
    if new_comments is None:
        return old_comments
    if old_comments is None:
        return new_comments
    return f"{new_comments}\n\n{old_comments}"
