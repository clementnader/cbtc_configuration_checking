#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import clean_track_name, clean_object_name
from .common_utils import *


__all__ = ["check_zvr"]


# ZVR
def check_zvr(dc_sys_sheet, res_sheet_name: str, survey_info: dict,
              set_of_survey_tracks: set[str]):
    assert dc_sys_sheet == DCSYS.ZVR
    assert res_sheet_name == "ZVR"

    zvr_dict = load_sheet(DCSYS.ZVR)
    list_used_object_names = list()
    res_dict = dict()
    for zvr_name, zvr_value in zvr_dict.items():
        zvr_limits = _get_zvr_limits(zvr_value)
        associated_survey_dict = _get_corresponding_survey_extremities(zvr_name, zvr_limits, survey_info,
                                                                       set_of_survey_tracks)

        limits_survey_info = [[zvr_name + f"__Limit_{n}", lim_track, lim_kp, survey_name]
                              for n, ((lim_track, lim_kp), survey_name)
                              in enumerate(associated_survey_dict.items(), start=1)]

        for object_name, dc_sys_original_track, dc_sys_kp, survey_name in limits_survey_info:
            dc_sys_track = clean_track_name(dc_sys_original_track, set_of_survey_tracks)
            survey_object_info = survey_info.get(survey_name)
            if survey_object_info is not None:
                list_used_object_names.append(survey_name)

            res_dict[(object_name, dc_sys_track)] = add_info_to_survey(survey_object_info, get_sheet_name(dc_sys_sheet),
                                                                       dc_sys_track, dc_sys_original_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_object_names, survey_info))
    return res_dict


def _clean_zvr_extremity_name(zvr_lim_name: str) -> str:
    zvr_lim_name = clean_object_name(zvr_lim_name)
    zvr_name = re.sub(r"^(ZVR[0-9]+)_[1-9]_.*$", r"\1", zvr_lim_name)
    return zvr_name


def _get_zvr_limits(zvr_value: dict) -> list[tuple[str, float]]:
    limits = list(get_dc_sys_zip_values(zvr_value, DCSYS.ZVR.Extremite.Voie, DCSYS.ZVR.Extremite.Pk))
    return limits


def _get_survey_limits_on_track(zvr_name: str, test_track: str, survey_info: dict[str, Any]) -> list[str]:
    clean_zvr_name = clean_object_name(zvr_name)
    list_survey_limits = list()
    for survey_name in survey_info:
        survey_zvr_lim_name, survey_track = survey_name.split("__", 1)
        if survey_track.upper() != test_track:
            continue
        survey_zvr_name = _clean_zvr_extremity_name(survey_zvr_lim_name)
        if survey_zvr_name == clean_zvr_name:
            list_survey_limits.append(survey_name)
    return list_survey_limits


def _get_corresponding_survey_extremities(zvr_name: str, zvr_limits: list[tuple[str, float]],
                                          survey_info: dict[str, Any], set_of_survey_tracks: set[str]
                                          ) -> dict[tuple[str, float], Optional[str]]:
    associated_survey_dict = {(lim_track, lim_kp): None for (lim_track, lim_kp) in zvr_limits}

    dc_sys_limit_tracks = set([clean_track_name(track, set_of_survey_tracks) for (track, _) in zvr_limits])
    for test_track in dc_sys_limit_tracks:
        dc_sys_limits_on_track = [(track, dc_sys_kp) for (track, dc_sys_kp) in zvr_limits
                                  if clean_track_name(track, set_of_survey_tracks) == test_track]
        survey_limits_on_track = _get_survey_limits_on_track(zvr_name, test_track, survey_info)

        if len(dc_sys_limits_on_track) == 1:
            associated_survey_dict = get_corresponding_survey_one_limit_on_track(
                dc_sys_limits_on_track, associated_survey_dict, survey_limits_on_track, survey_info)
        elif len(dc_sys_limits_on_track) == 2:
            associated_survey_dict = get_corresponding_survey_two_limits_on_track(
                dc_sys_limits_on_track, associated_survey_dict, survey_limits_on_track, survey_info)

    return associated_survey_dict
