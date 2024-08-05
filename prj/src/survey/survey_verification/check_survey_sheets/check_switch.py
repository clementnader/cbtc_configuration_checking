#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys_sheet_utils.switch_utils import get_dc_sys_switch_points_dict
from ...survey_utils import clean_track_name
from .common_utils import *


# Switch
def check_switch(dc_sys_sheet, res_sheet_name: str, survey_info: dict, set_of_survey_tracks: set[str]):
    assert dc_sys_sheet == DCSYS.Aig
    assert res_sheet_name == "Switch"

    obj_dict = get_dc_sys_switch_points_dict()
    list_used_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in obj_dict.items():
        original_dc_sys_track, dc_sys_kp = obj_val["track"], obj_val["kp"]
        dc_sys_track = clean_track_name(original_dc_sys_track, set_of_survey_tracks)

        test_names = [obj_name, obj_val.get("other_name")]
        if obj_name.endswith("_L"):
            test_names.append(obj_name.removesuffix("_L") + "_G")
        if obj_name.endswith("_R"):
            test_names.append(obj_name.removesuffix("_R") + "_D")

        survey_name = test_names_in_survey(test_names, dc_sys_track, survey_info)
        survey_obj_info = survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                dc_sys_track, original_dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict
