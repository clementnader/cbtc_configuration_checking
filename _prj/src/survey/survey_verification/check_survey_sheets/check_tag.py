#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import clean_track_name, clean_object_name
from .common_utils import *


__all__ = ["check_tag"]


# Tag and IATPM_Tag
def check_tag(dc_sys_sheets, res_sheet_name: str, tag_survey_info: dict[str, dict[str, float]],
              set_of_survey_tracks: set[str], dyn_tag_survey_info: dict[str, dict[str, float]],
              version_tag_survey_info: dict[str, dict[str, float]]):
    assert dc_sys_sheets == DCSYS.Bal or dc_sys_sheets == [DCSYS.Bal, DCSYS.IATPM_tags, DCSYS.IATPM_Version_Tags]
    assert res_sheet_name == "Tag"

    if dc_sys_sheets == DCSYS.Bal:
        dc_sys_dict = get_tags_dict([DCSYS.Bal])
    else:
        dc_sys_dict = get_tags_dict(dc_sys_sheets)
        tag_survey_info.update(dyn_tag_survey_info)
        tag_survey_info.update(version_tag_survey_info)
    list_used_object_names = list()
    res_dict = dict()
    for original_object_name, object_value in dc_sys_dict.items():
        dc_sys_sheet = object_value["dc_sys_sheet"]
        other_name = object_value["other_name"]
        original_dc_sys_track = object_value["track"]
        dc_sys_kp = object_value["kp"]
        dc_sys_track = clean_track_name(original_dc_sys_track, set_of_survey_tracks)

        object_name = clean_object_name(original_object_name)
        other_name = clean_object_name(other_name)
        test_names = [object_name, other_name]
        test_names.extend(_get_tags_test_names(object_name))
        survey_name = test_names_in_survey(test_names, dc_sys_track, tag_survey_info,
                                           do_smallest_amount_of_patterns=True)
        survey_object_info = tag_survey_info.get(survey_name)
        if survey_object_info is not None:
            list_used_object_names.append(survey_name)

        res_dict[(original_object_name, dc_sys_track)] = add_info_to_survey(survey_object_info, dc_sys_sheet,
                                                                            dc_sys_track, original_dc_sys_track,
                                                                            dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_object_names, tag_survey_info))

    return res_dict


def _get_tags_test_names(object_name: str) -> list[str]:
    test_names = list()
    if object_name.startswith("TAG_"):
        test_names.append("PTSA_" + object_name.removeprefix("TAG_"))

    # For Chennai project
    if object_name.startswith("B_BTK"):
        test_names.append("B_BT" + object_name.removeprefix("B_BTK"))
    if object_name.startswith("B_BT") and not object_name.startswith("B_BTK"):
        test_names.append("B_BTK" + object_name.removeprefix("B_BT"))
    if object_name.startswith("B_FTK"):
        test_names.append("B_FT" + object_name.removeprefix("B_FTK"))
    if object_name.startswith("B_FT") and not object_name.startswith("B_FTK"):
        test_names.append("B_FTK" + object_name.removeprefix("B_FT"))

    return test_names


def get_tags_dict(dc_sys_sheets: list):
    objs_dict = dict()
    for dc_sys_sheet in dc_sys_sheets:
        object_dict = load_sheet(dc_sys_sheet)
        for object_name, object_value in object_dict.items():
            other_name = get_dc_sys_value(object_value, dc_sys_sheet.BaliseName)
            if "Voie" in get_class_attributes_dict(dc_sys_sheet):
                track, kp = get_dc_sys_values(object_value, dc_sys_sheet.Voie, dc_sys_sheet.Pk)
            else:
                seg, x = get_dc_sys_values(object_value, dc_sys_sheet.Seg, dc_sys_sheet.X)
                track, kp = from_seg_offset_to_track_kp(seg, x)

            objs_dict[object_name] = {
                "dc_sys_sheet": get_sheet_name(dc_sys_sheet),
                "other_name": other_name,
                "track": track,
                "kp": kp,
            }
    return objs_dict
