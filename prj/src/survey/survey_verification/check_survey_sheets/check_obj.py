#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from .common_utils import *


# Signal and Buffer, and Version Tag
def check_object(dc_sys_sheet, res_sheet_name: str, survey_info: dict[str, dict[str, float]]):
    assert dc_sys_sheet in [DCSYS.Sig, DCSYS.IATPM_Version_Tags]
    assert res_sheet_name in ["Signal", "Buffer", "Tag"]

    dc_sys_dict = load_sheet(dc_sys_sheet)
    list_used_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in dc_sys_dict.items():
        if not obj_condition(res_sheet_name, obj_val):
            continue
        dc_sys_track, dc_sys_kp = _get_dc_sys_position(dc_sys_sheet, obj_val)
        dc_sys_track = dc_sys_track.upper()

        test_names = [obj_name]
        if obj_name.startswith("STOP_SIG_"):
            other_name = "SIG_" + obj_name.removeprefix("STOP_SIG_")
            if other_name not in dc_sys_dict:  # if there is not already a signal called that
                test_names.append(other_name)
        survey_name = test_names_in_survey(test_names, dc_sys_track, survey_info)
        survey_obj_info = survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
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


def _get_dc_sys_position(dc_sys_sheet, obj_val) -> tuple[str, float]:
    if "Voie" in get_class_attr_dict(dc_sys_sheet):
        track, kp = get_dc_sys_values(obj_val, dc_sys_sheet.Voie, dc_sys_sheet.Pk)
    else:
        seg, x = get_dc_sys_values(obj_val, dc_sys_sheet.Seg, dc_sys_sheet.X)
        track, kp = from_seg_offset_to_kp(seg, x)
    return track, kp
