#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys import *


# Tag, Signal and Buffer
def check_object(dc_sys_sheet, res_sheet_name: str, survey_info: dict[str, dict[str, float]]):
    assert dc_sys_sheet == DCSYS.Bal or dc_sys_sheet == DCSYS.Sig
    assert res_sheet_name == "Tag" or res_sheet_name == "Signal" or res_sheet_name == "Buffer"

    dc_sys_dict = load_sheet(dc_sys_sheet)
    res_dict = dict()
    for obj_name, obj_val in dc_sys_dict.items():
        if not obj_condition(res_sheet_name, obj_val):
            continue
        survey_obj_info = survey_info.get(obj_name)
        survey_track = survey_obj_info["track"] if survey_obj_info is not None else None
        surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
        surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
        comments = survey_obj_info["comments"] if survey_obj_info is not None else None

        res_dict[obj_name] = _add_dc_sys_info(dc_sys_sheet, obj_val)
        res_dict[obj_name].update({"survey_track": survey_track, "surveyed_kp": surveyed_kp})
        res_dict[obj_name].update({"surveyed_kp_comment": surveyed_kp_comment, "comments": comments})

    res_dict.update(_add_extra_info_from_survey(list(dc_sys_dict.keys()), survey_info))
    return res_dict


def obj_condition(res_sheet, obj_val):
    if res_sheet == "Signal":
        buffer = False
    elif res_sheet == "Buffer":
        buffer = True
    else:
        return True
    sig_type = get_dc_sys_value(obj_val, DCSYS.Sig.Type)
    is_sig_buffer = sig_type == SignalType.HEURTOIR
    return is_sig_buffer == buffer


def _add_dc_sys_info(dc_sys_sheet, obj_val):
    track_attr = dc_sys_sheet.Voie
    kp_attr = dc_sys_sheet.Pk
    return {"track": get_dc_sys_value(obj_val, track_attr), "dc_sys_kp": get_dc_sys_value(obj_val, kp_attr)}


def _add_extra_info_from_survey(list_obj_names: list[str], survey_info: dict[str, dict[str]]):
    extra_dict = dict()
    for obj_name, obj_val in survey_info.items():
        if obj_name in list_obj_names:
            continue
        extra_dict[obj_name] = {"track": None, "dc_sys_kp": None}
        extra_dict[obj_name].update({"survey_track": obj_val["track"], "surveyed_kp": obj_val["surveyed_kp"]})
        extra_dict[obj_name].update({"surveyed_kp_comment": obj_val["surveyed_kp_comment"],
                                     "comments": obj_val["comments"]})
    return extra_dict
