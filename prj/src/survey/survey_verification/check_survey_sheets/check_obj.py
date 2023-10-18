#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys import *
from .common_utils import *


# Tag, Signal and Buffer
def check_object(dc_sys_sheet, res_sheet_name: str, survey_info: dict[str, dict[str, float]]):
    assert dc_sys_sheet in [DCSYS.Bal, DCSYS.Sig]
    assert res_sheet_name in ["Tag", "Signal", "Buffer"]

    dc_sys_dict = load_sheet(dc_sys_sheet)
    list_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in dc_sys_dict.items():
        if not obj_condition(res_sheet_name, obj_val):
            continue
        survey_obj_info = survey_info.get(obj_name.upper())
        obj_name = survey_obj_info["obj_name"] if survey_obj_info is not None else obj_name
        survey_track = survey_obj_info["track"] if survey_obj_info is not None else None
        surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
        surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
        comments = survey_obj_info["comments"] if survey_obj_info is not None else None

        list_obj_names.append(obj_name)
        track, dc_sys_kp = _add_dc_sys_info(dc_sys_sheet, obj_val)
        res_dict[obj_name] = {"track": track, "dc_sys_kp": dc_sys_kp,
                              "survey_track": survey_track, "surveyed_kp": surveyed_kp,
                              "surveyed_kp_comment": surveyed_kp_comment, "comments": comments}

    res_dict.update(add_extra_info_from_survey(list_obj_names, survey_info))
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


def _add_dc_sys_info(dc_sys_sheet, obj_val) -> tuple[str, float]:
    track = get_dc_sys_value(obj_val, dc_sys_sheet.Voie)
    kp = get_dc_sys_value(obj_val, dc_sys_sheet.Pk)
    return track, kp


def _add_extra_info_from_survey(list_obj_names: list[str], survey_info: dict[str, dict[str]]):
    extra_dict = dict()
    for obj_val in survey_info.values():
        obj_name = obj_val["obj_name"]
        if obj_name in list_obj_names:
            continue
        extra_dict[obj_name] = {"track": None, "dc_sys_kp": None}
        extra_dict[obj_name].update({"survey_track": obj_val["track"], "surveyed_kp": obj_val["surveyed_kp"]})
        extra_dict[obj_name].update({"surveyed_kp_comment": obj_val["surveyed_kp_comment"],
                                     "comments": obj_val["comments"]})
    return extra_dict
