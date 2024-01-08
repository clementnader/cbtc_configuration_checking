#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["add_info_to_survey", "add_extra_info_from_survey", "test_other_track_name", "get_test_tracks"]


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


def test_other_track_name(test_names: list[str], track: str, survey_info: dict[str]) -> str:
    for test_track in get_test_tracks(track):
        for test_name in test_names:
            test_name_in_survey = _test_name_in_survey(test_name, test_track, survey_info)
            if test_name_in_survey is not None:
                return test_name_in_survey
    return f"{test_names[0]}__{track}".upper()  # default


def get_test_tracks(track: str) -> list[str]:
    test_tracks = [track]
    if track == "T1":
        test_tracks.append("TRACK_1")
    elif track == "T2":
        test_tracks.append("TRACK_2")
    # elif track.endswith("_02W"):
    #     test_tracks.append(track.removesuffix("_02W") + "_02")
    return test_tracks


def _test_name_in_survey(test_name: str, track: str, survey_info: dict[str]):
    if test_name is not None and f"{test_name}__{track}".upper() in survey_info:
        return f"{test_name}__{track}".upper()
    return None
