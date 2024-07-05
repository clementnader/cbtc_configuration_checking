#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from .common_utils import *
from .check_platform import get_corresponding_plt_survey_extremities


# Walkway
def check_walkway(dc_sys_sheet, res_sheet_name: str, survey_info: dict, plt_survey_info: dict):
    assert dc_sys_sheet == DCSYS.Walkways_Area
    assert res_sheet_name == "Walkway"

    ww_dict = load_sheet(DCSYS.Walkways_Area)
    list_used_obj_names = list()
    res_dict = dict()
    for ww_name, ww_val in ww_dict.items():
        ww_limits = _get_ww_limits(ww_val)
        associated_survey_dict = _get_corresponding_ww_survey_extremities(ww_name, ww_limits, survey_info,
                                                                          plt_survey_info)

        limits_survey_info = [[ww_name + f"__Limit_{n}", lim_track, lim_kp, survey_name]
                              for n, ((lim_track, lim_kp), survey_name)
                              in enumerate(associated_survey_dict.items(), start=1)]

        for obj_name, dc_sys_track, dc_sys_kp, survey_name in limits_survey_info:
            survey_obj_info = survey_info.get(survey_name)
            if survey_obj_info is not None:
                list_used_obj_names.append(survey_name)
            else:  # we try to find it among the surveyed platforms
                survey_obj_info = plt_survey_info.get(survey_name)

            res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                    dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict


def _clean_walkway_extremity_name(ww_lim_name: str) -> str:
    ww_lim_name = ww_lim_name.upper()
    ww_name = ww_lim_name.removesuffix("_START").removesuffix("_STOP")
    ww_name = ww_name.removeprefix("LIMIT_")
    ww_name = ww_name.removeprefix("WALKWAY_").removeprefix("WWAY_").removeprefix("WW_")
    return ww_name


def _get_ww_limits(ww_val: dict) -> list[tuple[str, float]]:
    limits = list(get_dc_sys_zip_values(ww_val, DCSYS.Walkways_Area.Limit.Seg, DCSYS.Walkways_Area.Limit.X))
    track_kp_limits = [from_seg_offset_to_kp(seg, x) for seg, x in limits]
    return track_kp_limits


def _get_survey_limits_on_track(ww_name: str, test_track: str, survey_info: dict[str, Any]) -> list[str]:
    list_survey_limits = list()
    for survey_name in survey_info.keys():
        survey_ww_lim_name, survey_track = survey_name.split("__", 1)
        survey_ww_name = _clean_walkway_extremity_name(survey_ww_lim_name)
        if survey_track.upper() == test_track:
            if survey_ww_name == ww_name.upper():
                list_survey_limits.append(survey_name)
    return list_survey_limits


def _get_corresponding_ww_survey_extremities(ww_name: str, ww_limits: list[tuple[str, float]],
                                             survey_info: dict[str, Any], plt_survey_info: dict[str, Any]
                                             ) -> dict[tuple[str, float], Optional[str]]:
    associated_survey_dict = {(lim_track, lim_kp): None for (lim_track, lim_kp) in ww_limits}

    plt_dict = load_sheet(DCSYS.Quai)

    ww_name = ww_name.removeprefix("WALKWAY_").removeprefix("WWAY_").removeprefix("WW_")
    if ww_name in plt_dict:
        return get_corresponding_plt_survey_extremities(ww_name, ww_limits, plt_survey_info)

    dc_sys_limit_tracks = set([track.upper() for (track, _) in ww_limits])
    for test_track in dc_sys_limit_tracks:
        dc_sys_limits_on_track = [(track, dc_sys_kp) for (track, dc_sys_kp) in ww_limits
                                  if track.upper() == test_track]
        survey_limits_on_track = _get_survey_limits_on_track(ww_name, test_track, survey_info)

        if len(dc_sys_limits_on_track) == 1:
            associated_survey_dict = get_corresponding_survey_one_limit_on_track(
                dc_sys_limits_on_track, associated_survey_dict, survey_limits_on_track, survey_info)
        elif len(dc_sys_limits_on_track) == 2:
            associated_survey_dict = get_corresponding_survey_two_limits_on_track(
                dc_sys_limits_on_track, associated_survey_dict, survey_limits_on_track, survey_info)

    return associated_survey_dict
