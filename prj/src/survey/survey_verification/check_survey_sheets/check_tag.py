#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys import *
from .common_utils import *
from .check_obj import check_object


# Tag and IATPM_Tag
def check_tag(dc_sys_sheets, res_sheet_name: str, tag_survey_info: dict[str, dict[str, float]],
              version_tag_survey_info: dict[str, dict[str, float]]):
    assert dc_sys_sheets == [DCSYS.Bal, DCSYS.IATPM_tags]
    assert res_sheet_name == "Tag"

    objs_dict = get_tags_dict(dc_sys_sheets)
    list_used_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in objs_dict.items():
        dc_sys_sheet = obj_val["dc_sys_sheet"]
        other_name = obj_val["other_name"]
        original_dc_sys_track = obj_val["track"]
        dc_sys_kp = obj_val["kp"]
        dc_sys_track = original_dc_sys_track.upper()

        test_names = [obj_name, other_name]
        if obj_name.startswith("TAG_"):
            test_names.append("PTSA_" + obj_name.removeprefix("TAG_"))
        survey_name = test_names_in_survey(test_names, dc_sys_track, tag_survey_info)
        survey_obj_info = tag_survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, dc_sys_sheet,
                                                                original_dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, tag_survey_info))

    res_dict.update(check_object(DCSYS.IATPM_Version_Tags, res_sheet_name, version_tag_survey_info))
    return res_dict


def get_tags_dict(dc_sys_sheets: list):
    objs_dict = dict()
    for dc_sys_sheet in dc_sys_sheets:
        obj_dict = load_sheet(dc_sys_sheet)
        objs_dict.update({obj_name: {
            "dc_sys_sheet": get_sh_name(dc_sys_sheet),
            "other_name": get_dc_sys_value(obj_val, dc_sys_sheet.BaliseName),
            "track": get_dc_sys_value(obj_val, dc_sys_sheet.Voie),
            "kp": get_dc_sys_value(obj_val, dc_sys_sheet.Pk),
        } for obj_name, obj_val in obj_dict.items()})
    return objs_dict
