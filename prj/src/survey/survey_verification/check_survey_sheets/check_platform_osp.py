#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....cctool_oo_schema import *
from ....dc_sys import *
from .common_utils import *


__all__ = ["check_platform_osp"]


# Platform OSP
def check_platform_osp(dc_sys_sheet, res_sheet_name: str, survey_info: dict[str, dict[str, float]]):
    assert dc_sys_sheet == DCSYS.Quai.PointDArret
    assert res_sheet_name == "Platform"

    objs_dict = get_plt_osp_dict()
    list_used_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in objs_dict.items():
        dc_sys_track, dc_sys_kp = obj_val
        dc_sys_track = dc_sys_track.upper()

        test_names = [obj_name]
        survey_name = test_names_in_survey(test_names, dc_sys_track, survey_info)
        survey_obj_info = survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict


def get_plt_osp_dict():
    plt_osp_dict = dict()
    plt_dict = load_sheet(DCSYS.Quai)
    for plt_name, plt_val in plt_dict.items():
        for osp_name, osp_track, osp_kp in get_dc_sys_zip_values(plt_val, DCSYS.Quai.PointDArret.Name,
                                                                 DCSYS.Quai.PointDArret.Voie,
                                                                 DCSYS.Quai.PointDArret.Pk):
            plt_osp_dict[osp_name] = (osp_track, osp_kp)
    return plt_osp_dict
