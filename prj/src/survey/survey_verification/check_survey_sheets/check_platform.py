#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import clean_track_name
from .common_utils import *
from .check_platform_osp import *


# Switch
def check_platform(dc_sys_sheet, res_sheet_name: str, plt_survey_info: dict, osp_survey_info: dict,
                   set_of_survey_tracks: set[str]):
    assert dc_sys_sheet == DCSYS.Quai
    assert res_sheet_name == "Platform"

    plt_dict = load_sheet(DCSYS.Quai)
    list_used_obj_names = list()
    res_dict = dict()
    for plt_name, plt_val in plt_dict.items():
        plt_limits = _get_plt_limits(plt_val)
        associated_survey_dict = get_corresponding_plt_survey_extremities(plt_name, plt_limits, plt_survey_info,
                                                                          set_of_survey_tracks)

        limits_survey_info = [[plt_name + f"__Limit_{n}", lim_track, lim_kp, survey_name]
                              for n, ((lim_track, lim_kp), survey_name)
                              in enumerate(associated_survey_dict.items(), start=1)]

        for obj_name, dc_sys_original_track, dc_sys_kp, survey_name in limits_survey_info:
            dc_sys_track = clean_track_name(dc_sys_original_track, set_of_survey_tracks)
            survey_obj_info = plt_survey_info.get(survey_name)
            if survey_obj_info is not None:
                list_used_obj_names.append(survey_name)

            res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                    dc_sys_track, dc_sys_original_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, plt_survey_info))

    # Add platform OSP on same sheet
    res_dict.update(check_platform_osp(dc_sys_sheet.PointDArret, res_sheet_name, osp_survey_info, set_of_survey_tracks))
    return res_dict


def _clean_platform_extremity_name(plt_lim_name: str) -> str:
    plt_lim_name = plt_lim_name.upper()
    plt_name = plt_lim_name.removeprefix("LEFT_END_").removeprefix("RIGHT_END_")
    plt_name = plt_name.removeprefix("BEGIN_").removeprefix("END_")
    plt_name = plt_name.removeprefix("QUAI1_").removeprefix("QUAI2_")
    plt_name = plt_name.removesuffix("_START").removesuffix("_END")
    return plt_name


def _get_plt_limits(plt_val: dict) -> list[tuple[str, float]]:
    limits = list(get_dc_sys_zip_values(plt_val, DCSYS.Quai.ExtremiteDuQuai.Voie, DCSYS.Quai.ExtremiteDuQuai.Pk))
    return limits


UNIQUE_PREFIX_PLT_NAMES_DICT = None


def _get_unique_prefix_plt_names_dict() -> dict[str, dict[str, str]]:
    global UNIQUE_PREFIX_PLT_NAMES_DICT
    if UNIQUE_PREFIX_PLT_NAMES_DICT is None:
        res_dict = dict()
        plt_dict = load_sheet(DCSYS.Quai)
        set_of_tracks = set([track.upper() for test_plt_info in plt_dict.values()
                             for track in get_dc_sys_value(test_plt_info, DCSYS.Quai.ExtremiteDuQuai.Voie)])
        for track in set_of_tracks:
            plt_names_dict = {test_plt_name: test_plt_name.upper().removeprefix("PLATFORM_").removeprefix("PLT_")
                              for test_plt_name, test_plt_info in plt_dict.items()
                              if track in [plt_lim_track.upper() for plt_lim_track
                                           in get_dc_sys_value(test_plt_info, DCSYS.Quai.ExtremiteDuQuai.Voie)]}
            res_dict[track] = get_smallest_unique_prefix_dict(plt_names_dict)
        UNIQUE_PREFIX_PLT_NAMES_DICT = res_dict
    return UNIQUE_PREFIX_PLT_NAMES_DICT


def _get_survey_limits_on_track(plt_name: str, track: str, plt_survey_info: dict[str, Any]) -> list[str]:
    list_all_survey_limits = list()
    list_survey_limits = list()
    for survey_name in plt_survey_info.keys():
        survey_plt_lim_name, survey_track = survey_name.split("__", 1)
        survey_plt_name = _clean_platform_extremity_name(survey_plt_lim_name)
        if survey_track.upper() == track:
            survey_plt_name = survey_plt_name.removeprefix("PLATFORM_").removeprefix("PLT_")
            clean_plt_name = plt_name.upper().removeprefix("PLATFORM_").removeprefix("PLT_")
            list_all_survey_limits.append((survey_name, survey_plt_name))
            if (survey_plt_name == clean_plt_name
                    or survey_plt_name.removesuffix("_1") + "_T1" == clean_plt_name
                    or survey_plt_name.removesuffix("_2") + "_T2" == clean_plt_name
                    or survey_plt_name.removesuffix("_T1") + "_1" == clean_plt_name
                    or survey_plt_name.removesuffix("_T2") + "_2" == clean_plt_name):
                list_survey_limits.append(survey_name)

    if not list_survey_limits:
        unique_prefix = _get_unique_prefix_plt_names_dict()[track][plt_name]
        for survey_name, survey_plt_name in list_all_survey_limits:
            survey_plt_name = survey_plt_name[:len(unique_prefix)]
            if (survey_plt_name == unique_prefix
                    or survey_plt_name.removesuffix("_1") + "_T1" == unique_prefix
                    or survey_plt_name.removesuffix("_2") + "_T2" == unique_prefix
                    or survey_plt_name.removesuffix("_T1") + "_1" == unique_prefix
                    or survey_plt_name.removesuffix("_T2") + "_2" == unique_prefix):
                list_survey_limits.append(survey_name)

    return list_survey_limits


def get_corresponding_plt_survey_extremities(plt_name: str, plt_limits: list[tuple[str, float]],
                                             plt_survey_info: dict[str, Any], set_of_survey_tracks: set[str]
                                             ) -> dict[tuple[str, float], Optional[str]]:
    associated_survey_dict = {(lim_track, lim_kp): None for (lim_track, lim_kp) in plt_limits}

    dc_sys_limit_tracks = set([clean_track_name(track, set_of_survey_tracks) for (track, _) in plt_limits])
    for test_track in dc_sys_limit_tracks:
        dc_sys_limits_on_track = [(track, dc_sys_kp) for (track, dc_sys_kp) in plt_limits
                                  if clean_track_name(track, set_of_survey_tracks) == test_track]
        survey_limits_on_track = _get_survey_limits_on_track(plt_name, test_track, plt_survey_info)

        if len(dc_sys_limits_on_track) == 1:
            associated_survey_dict = get_corresponding_survey_one_limit_on_track(
                dc_sys_limits_on_track, associated_survey_dict, survey_limits_on_track, plt_survey_info)
        elif len(dc_sys_limits_on_track) == 2:
            associated_survey_dict = get_corresponding_survey_two_limits_on_track(
                dc_sys_limits_on_track, associated_survey_dict, survey_limits_on_track, plt_survey_info)

    return associated_survey_dict
