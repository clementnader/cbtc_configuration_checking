#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import clean_track_name
from .common_utils import *


# FloodGate
def check_flood_gate(dc_sys_sheet, res_sheet_name: str, survey_info: dict, set_of_survey_tracks: set[str]):
    assert dc_sys_sheet == DCSYS.Flood_Gate
    assert res_sheet_name == "FloodGate"

    fg_dict = load_sheet(DCSYS.Flood_Gate)
    list_used_obj_names = list()
    res_dict = dict()
    for fg_name, fg_val in fg_dict.items():
        fg_limits = _get_fg_limits(fg_val)
        associated_survey_dict = _get_corresponding_survey_extremities(fg_name, fg_limits, survey_info,
                                                                       set_of_survey_tracks)

        limits_survey_info = [[fg_name + f"__Limit_{n}", lim_track, lim_kp, survey_name]
                              for n, ((lim_track, lim_kp), survey_name)
                              in enumerate(associated_survey_dict.items(), start=1)]

        for obj_name, dc_sys_original_track, dc_sys_kp, survey_name in limits_survey_info:
            dc_sys_track = clean_track_name(dc_sys_original_track, set_of_survey_tracks)
            survey_obj_info = survey_info.get(survey_name)
            if survey_obj_info is not None:
                list_used_obj_names.append(survey_name)

            res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                    dc_sys_track, dc_sys_original_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict


def _clean_flood_gate_extremity_name(fg_lim_name: str) -> str:
    fg_lim_name = fg_lim_name.upper()
    fg_name = fg_lim_name.removeprefix("BEGIN_FLOODGATEAREA_").removeprefix("END_FLOODGATEAREA_")
    return fg_name


def _get_fg_limits(fg_val: dict) -> list[tuple[str, float]]:
    limits = list(get_dc_sys_zip_values(fg_val, DCSYS.Flood_Gate.Limit.Track, DCSYS.Flood_Gate.Limit.Kp))
    return limits


def _get_survey_limits_on_track(fg_name: str, test_track: str, survey_info: dict[str, Any]) -> list[str]:
    list_survey_limits = list()
    for survey_name in survey_info.keys():
        survey_fg_lim_name, survey_track = survey_name.split("__", 1)
        survey_fg_name = _clean_flood_gate_extremity_name(survey_fg_lim_name)
        if survey_track.upper() == test_track:
            if survey_fg_name == fg_name.upper():
                list_survey_limits.append(survey_name)
    return list_survey_limits


def _get_corresponding_survey_extremities(fg_name: str, fg_limits: list[tuple[str, float]],
                                          survey_info: dict[str, Any], set_of_survey_tracks: set[str]
                                          ) -> dict[tuple[str, float], Optional[str]]:
    associated_survey_dict = {(lim_track, lim_kp): None for (lim_track, lim_kp) in fg_limits}

    dc_sys_limit_tracks = set([clean_track_name(track, set_of_survey_tracks) for (track, _) in fg_limits])
    for test_track in dc_sys_limit_tracks:
        dc_sys_limits_on_track = [(track, dc_sys_kp) for (track, dc_sys_kp) in fg_limits
                                  if clean_track_name(track, set_of_survey_tracks) == test_track]
        survey_limits_on_track = _get_survey_limits_on_track(fg_name, test_track, survey_info)

        if len(dc_sys_limits_on_track) == 1:
            associated_survey_dict = get_corresponding_survey_one_limit_on_track(
                dc_sys_limits_on_track, associated_survey_dict, survey_limits_on_track, survey_info)
        elif len(dc_sys_limits_on_track) == 2:
            associated_survey_dict = get_corresponding_survey_two_limits_on_track(
                dc_sys_limits_on_track, associated_survey_dict, survey_limits_on_track, survey_info)

    return associated_survey_dict
