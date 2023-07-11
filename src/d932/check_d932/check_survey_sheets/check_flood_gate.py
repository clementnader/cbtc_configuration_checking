#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import DCSYS
from ....dc_sys import *


FG_PREFIX = {"left": "Begin_FloodGateArea_",
             "right": "End_FloodGateArea_"}


# FloodGate
def check_flood_gate(dc_sys_sheet, res_sheet_name: str, survey_info: dict):
    assert dc_sys_sheet == DCSYS.Flood_Gate
    assert res_sheet_name == "FloodGate"

    fg_dict = _get_dc_sys_flood_gate_dict()
    res_dict = dict()
    for fg_name, fg_val in fg_dict.items():
        survey_obj_info = survey_info.get(fg_name)
        survey_object_comment = survey_obj_info["obj_comment"] if survey_obj_info is not None else None
        survey_track = survey_obj_info["track"] if survey_obj_info is not None else None
        survey_track_comment = survey_obj_info["track_comment"] if survey_obj_info is not None else None
        surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
        surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
        design_kp = survey_obj_info["design_kp"] if survey_obj_info is not None else None
        design_kp_comment = survey_obj_info["design_kp_comment"] if survey_obj_info is not None else None
        res_dict[fg_name] = {"track": fg_val[0], "dc_sys_kp": fg_val[1]}
        res_dict[fg_name].update({"survey_track": survey_track, "surveyed_kp": surveyed_kp, "design_kp": design_kp})
        res_dict[fg_name].update({"survey_object_comment": survey_object_comment,
                                  "survey_track_comment": survey_track_comment,
                                  "surveyed_kp_comment": surveyed_kp_comment,
                                  "design_kp_comment": design_kp_comment})

    res_dict.update(_add_extra_info_from_survey(list(fg_dict.keys()), survey_info))
    return res_dict


def _get_dc_sys_flood_gate_dict():
    res_dict = dict()
    fg_dict = load_sheet(DCSYS.Flood_Gate)
    for fg_name, fg_val in fg_dict.items():
        limits = list(get_dc_sys_zip_values(fg_val, DCSYS.Flood_Gate.Limit.Track, DCSYS.Flood_Gate.Limit.Kp))
        if len(limits) == 2:
            left_lim = limits[0] if limits[0][1] <= limits[1][1] else limits[1]
            right_lim = limits[1] if limits[0][1] <= limits[1][1] else limits[0]
            res_dict[FG_PREFIX["left"] + fg_name] = left_lim
            res_dict[FG_PREFIX["right"] + fg_name] = right_lim
        else:
            for i, lim in enumerate(limits):
                res_dict[f"FloodGateArea_{fg_name}_Limit_{i}"] = lim
    return res_dict


def _add_extra_info_from_survey(list_fg_names: list[str], survey_info: dict[str, dict[str]]):
    extra_dict = dict()
    for fg_name, fg_val in survey_info.items():
        if fg_name in list_fg_names:
            continue
        extra_dict[fg_name] = {"track": None, "dc_sys_kp": None}
        extra_dict[fg_name].update({"survey_track": fg_val["track"], "surveyed_kp": fg_val["surveyed_kp"],
                                    "design_kp": fg_val["design_kp"]})
        extra_dict[fg_name].update({"survey_object_comment": fg_val["obj_comment"],
                                    "survey_track_comment": fg_val["track_comment"],
                                    "surveyed_kp_comment": fg_val["surveyed_kp_comment"],
                                    "design_kp_comment": fg_val["design_kp_comment"]})
    return extra_dict
