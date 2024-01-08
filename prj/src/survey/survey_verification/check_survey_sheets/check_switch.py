#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys import *
from .common_utils import *


# Switch
def check_switch(dc_sys_sheet, res_sheet_name: str, survey_info: dict):
    assert dc_sys_sheet == DCSYS.Aig
    assert res_sheet_name == "Switch"

    obj_dict = get_dc_sys_switch_points_dict()
    list_used_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in obj_dict.items():
        track, dc_sys_kp = obj_val["track"], obj_val["dc_sys_kp"]
        track = track.upper()

        survey_name = test_other_track_name([obj_name, obj_val.get("other_name")], track, survey_info)
        survey_obj_info = survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        obj_name = survey_obj_info["obj_name"] if survey_obj_info is not None else obj_name.removesuffix(f"__{track}")

        res_dict[(obj_name, track)] = add_info_to_survey(survey_obj_info, track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict
