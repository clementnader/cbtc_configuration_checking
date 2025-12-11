#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import clean_track_name, clean_object_name
from .common_utils import *


__all__ = ["check_osp"]


# OSP
def check_osp(dc_sys_sheets, res_sheet_name: str, survey_info: dict[str, dict[str, float]],
              set_of_survey_tracks: set[str]):
    assert dc_sys_sheets == [DCSYS.Quai.PointDArret, DCSYS.PtA]
    assert res_sheet_name == "Platform"
    if "Name" not in get_class_attributes_dict(DCSYS.Quai.PointDArret):
        return dict()

    dc_sys_dict = get_plt_osp_dict()
    dc_sys_dict.update(get_not_plt_osp_dict())
    list_used_object_names = list()
    res_dict = dict()
    for object_name, object_value in dc_sys_dict.items():
        original_dc_sys_track, dc_sys_kp, dc_sys_sheet = object_value
        dc_sys_track = clean_track_name(original_dc_sys_track, set_of_survey_tracks)

        test_names = _get_osp_test_names(object_name)
        survey_name = test_names_in_survey(test_names, dc_sys_track, survey_info,
                                           do_smallest_amount_of_patterns=True)
        survey_object_info = survey_info.get(survey_name)
        if survey_object_info is not None:
            list_used_object_names.append(survey_name)

        res_dict[(object_name, dc_sys_track)] = add_info_to_survey(survey_object_info, get_sheet_name(dc_sys_sheet),
                                                                   dc_sys_track, original_dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_object_names, survey_info))
    return res_dict


def _get_osp_test_names(object_name: str) -> list[str]:
    object_name = clean_object_name(object_name)
    test_names = [object_name]
    if object_name.startswith("PT_ARRET_"):
        test_names.append("PLATFORM_" + object_name.removeprefix("PT_ARRET_"))
        test_names.append("PLT_" + object_name.removeprefix("PT_ARRET_"))
    elif object_name.startswith("OSP_SIG_"):
        test_names.append("OSP_" + object_name.removeprefix("OSP_SIG_"))
    elif object_name.startswith("ATO_SIG_"):
        test_names.append("OSP_" + object_name.removeprefix("ATO_SIG_"))
    return test_names


def get_plt_osp_dict():
    plt_osp_dict = dict()
    plt_dict = load_sheet(DCSYS.Quai)
    for plt_name, plt_value in plt_dict.items():
        for osp_name, osp_track, osp_kp in get_dc_sys_zip_values(plt_value, DCSYS.Quai.PointDArret.Name,
                                                                 DCSYS.Quai.PointDArret.Voie,
                                                                 DCSYS.Quai.PointDArret.Pk):
            plt_osp_dict[osp_name] = (osp_track, osp_kp, DCSYS.Quai.PointDArret)
    return plt_osp_dict


def get_not_plt_osp_dict():
    res_osp_dict = dict()
    osp_dict = load_sheet(DCSYS.PtA)
    for osp_name, osp_value in osp_dict.items():
        osp_track, osp_kp = get_dc_sys_values(osp_value, DCSYS.PtA.Voie, DCSYS.PtA.Pk)
        res_osp_dict[osp_name] = (osp_track, osp_kp, DCSYS.PtA)
    return res_osp_dict
