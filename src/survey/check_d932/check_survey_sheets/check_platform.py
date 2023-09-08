#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys import *


PLT_PREFIX = {"left": "LEFT_END_",
              "right": "RIGHT_END_"}


# Switch
def check_platform(dc_sys_sheet, res_sheet_name: str, survey_info: dict):
    assert dc_sys_sheet == DCSYS.Quai
    assert res_sheet_name == "Platform"

    plt_dict = _get_dc_sys_platform_dict()
    res_dict = dict()
    for plt_name, plt_val in plt_dict.items():
        survey_obj_info = survey_info.get(plt_name)
        survey_object_comment = survey_obj_info["obj_comment"] if survey_obj_info is not None else None
        survey_track = survey_obj_info["track"] if survey_obj_info is not None else None
        survey_track_comment = survey_obj_info["track_comment"] if survey_obj_info is not None else None
        surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
        surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
        design_kp = survey_obj_info["design_kp"] if survey_obj_info is not None else None
        design_kp_comment = survey_obj_info["design_kp_comment"] if survey_obj_info is not None else None
        res_dict[plt_name] = {"track": plt_val[0], "dc_sys_kp": plt_val[1]}
        res_dict[plt_name].update({"survey_track": survey_track, "surveyed_kp": surveyed_kp, "design_kp": design_kp})
        res_dict[plt_name].update({"survey_object_comment": survey_object_comment,
                                   "survey_track_comment": survey_track_comment,
                                   "surveyed_kp_comment": surveyed_kp_comment,
                                   "design_kp_comment": design_kp_comment})

    res_dict.update(_add_extra_info_from_survey(list(plt_dict.keys()), survey_info))
    return res_dict


def _get_dc_sys_platform_dict():
    res_dict = dict()
    plt_dict = load_sheet(DCSYS.Quai)
    for plt_name, plt_val in plt_dict.items():
        limits = list(get_dc_sys_zip_values(plt_val, DCSYS.Quai.ExtremiteDuQuai.Voie, DCSYS.Quai.ExtremiteDuQuai.Pk))
        left_lim = limits[0] if limits[0][1] <= limits[1][1] else limits[1]
        right_lim = limits[1] if limits[0][1] <= limits[1][1] else limits[0]
        res_dict[PLT_PREFIX["left"] + plt_name] = left_lim
        res_dict[PLT_PREFIX["right"] + plt_name] = right_lim
    return res_dict


def _add_extra_info_from_survey(list_plt_names: list[str], survey_info: dict[str, dict[str]]):
    extra_dict = dict()
    for plt_name, plt_val in survey_info.items():
        if plt_name in list_plt_names:
            continue
        extra_dict[plt_name] = {"track": None, "dc_sys_kp": None}
        extra_dict[plt_name].update({"survey_track": plt_val["track"], "surveyed_kp": plt_val["surveyed_kp"],
                                     "design_kp": plt_val["design_kp"]})
        extra_dict[plt_name].update({"survey_object_comment": plt_val["obj_comment"],
                                     "survey_track_comment": plt_val["track_comment"],
                                     "surveyed_kp_comment": plt_val["surveyed_kp_comment"],
                                     "design_kp_comment": plt_val["design_kp_comment"]})
    return extra_dict
