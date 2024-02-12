#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import *
from .common_utils import *
from .check_platform_osp import *


PLT_PREFIX = {
    "left_and_right": {"left": "LEFT_END_", "right": "RIGHT_END_"},
    "begin_and_end": {"left": "Begin_", "right": "End_"}
}


# Switch
def check_platform(dc_sys_sheet, res_sheet_name: str, plt_survey_info: dict, osp_survey_info: dict):
    assert dc_sys_sheet == DCSYS.Quai
    assert res_sheet_name == "Platform"

    plt_dict = load_sheet(DCSYS.Quai)
    list_used_obj_names = list()
    res_dict = dict()
    for plt_name, plt_val in plt_dict.items():
        plt_limits = _get_plt_limits(plt_val)
        (lim1_track, lim1_kp), (lim2_track, lim2_kp) = plt_limits
        survey_name_dict = _get_corresponding_survey_extremities(plt_name, plt_limits, plt_survey_info)
        limits_survey_info = [[plt_name + "__Limit_1", lim1_track, lim1_kp, survey_name_dict[1]],
                              [plt_name + "__Limit_2", lim2_track, lim2_kp, survey_name_dict[2]]]

        for obj_name, dc_sys_track, dc_sys_kp, survey_name in limits_survey_info:
            survey_obj_info = plt_survey_info.get(survey_name)
            if survey_obj_info is not None:
                list_used_obj_names.append(survey_name)

            res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                    dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, plt_survey_info))

    # Add platform OSP on same sheet
    res_dict.update(check_platform_osp(dc_sys_sheet.PointDArret, res_sheet_name, osp_survey_info))
    return res_dict


def _clean_platform_extremity_name(plt_lim_name: str) -> str:
    plt_name = plt_lim_name.upper()
    plt_name = plt_name.removeprefix("LEFT_END_").removeprefix("RIGHT_END_")
    plt_name = plt_name.removeprefix("BEGIN_").removeprefix("END_")
    plt_name = plt_name.removeprefix("QUAI1_").removeprefix("QUAI2_")
    plt_name = plt_name.removesuffix("_START").removesuffix("_END")
    return plt_name


def _get_plt_limits(plt_val: dict) -> list[tuple[str, float]]:
    limits = list(get_dc_sys_zip_values(plt_val, DCSYS.Quai.ExtremiteDuQuai.Voie, DCSYS.Quai.ExtremiteDuQuai.Pk))
    return limits


def _get_corresponding_survey_extremities(plt_name: str, plt_limits: list[tuple[str, float]],
                                          plt_survey_info: dict[str]) -> dict[int, Optional[str]]:
    survey_name_dict = {1: None, 2: None}
    (lim1_track, lim1_kp), (lim2_track, lim2_kp) = plt_limits
    lim1_track = lim1_track.upper()
    lim2_track = lim2_track.upper()
    limits_on_same_track = lim1_track == lim2_track

    if limits_on_same_track:
        return _get_corresponding_survey_same_track(plt_name, lim1_track, lim1_kp, lim2_track, lim2_kp,
                                                    survey_name_dict, plt_survey_info)
    else:
        return _get_corresponding_survey_different_tracks(plt_name, lim1_track, lim1_kp, lim2_track, lim2_kp,
                                                          survey_name_dict, plt_survey_info)


def _get_corresponding_survey_same_track(plt_name: str, lim1_track: str, lim1_kp: float,
                                         lim2_track: str, lim2_kp: float,
                                         survey_name_dict: dict[int, Optional[str]], plt_survey_info: dict[str]
                                         ) -> dict[int, Optional[str]]:
    assert lim1_track == lim2_track
    list_survey_limits = _get_survey_limits(plt_name, lim1_track, plt_survey_info)
    if not list_survey_limits:  # platform not surveyed
        return survey_name_dict
    elif len(list_survey_limits) == 1:
        print_log(f"Only one platform end has been found in survey for {plt_name}:\n"
                  f"{list_survey_limits[0].removesuffix(f'__{lim1_track}')}\n")
        # Find for which DC_SYS limit the difference is the smallest
        survey_name = list_survey_limits[0]
        surveyed_kp = plt_survey_info[survey_name]["surveyed_kp"]
        test_differences = list()
        for i, lim_kp in enumerate([lim1_kp, lim2_kp], start=1):
            reversed_polarity = check_polarity(lim_kp, surveyed_kp)
            if reversed_polarity:
                test_differences.append((abs(abs(lim_kp) - abs(surveyed_kp)), i))
            else:
                test_differences.append((abs(lim_kp - surveyed_kp), i))
        closest_dc_sys_limit = sorted(test_differences, key=lambda x: x[0])[0][1]
        survey_name_dict[closest_dc_sys_limit] = survey_name
        return survey_name_dict
    else:
        # Find for which DC_SYS limits combination the difference is the smallest
        test_differences = list()
        for survey_name_corresponding_to_1 in list_survey_limits:
            surveyed_kp_1 = plt_survey_info[survey_name_corresponding_to_1]["surveyed_kp"]
            for survey_name_corresponding_to_2 in [survey_name for survey_name in list_survey_limits
                                                   if survey_name != survey_name_corresponding_to_1]:
                surveyed_kp_2 = plt_survey_info[survey_name_corresponding_to_2]["surveyed_kp"]
                reversed_polarity = (check_polarity(lim1_kp, surveyed_kp_1) and check_polarity(lim2_kp, surveyed_kp_2))
                if reversed_polarity:
                    diff1 = abs(abs(lim1_kp) - abs(surveyed_kp_1))
                    diff2 = abs(abs(lim2_kp) - abs(surveyed_kp_2))
                else:
                    diff1 = abs(lim1_kp - surveyed_kp_1)
                    diff2 = abs(lim2_kp - surveyed_kp_2)
                test_differences.append((diff1 + diff2,
                                         [survey_name_corresponding_to_1, survey_name_corresponding_to_2]))
        closest_survey_names = sorted(test_differences, key=lambda x: x[0])[0][1]
        for i, closest_survey_name in enumerate(closest_survey_names, start=1):
            survey_name_dict[i] = closest_survey_name
    return survey_name_dict


def _get_corresponding_survey_different_tracks(plt_name: str, lim1_track: str, lim1_kp: float,
                                               lim2_track: str, lim2_kp: float,
                                               survey_name_dict: dict[int, Optional[str]], plt_survey_info: dict[str]
                                               ) -> dict[int, Optional[str]]:
    assert lim1_track != lim2_track
    i: int
    for i, (lim_track, lim_kp) in enumerate([(lim1_track, lim1_kp), (lim2_track, lim2_kp)], start=1):
        list_survey_limits = _get_survey_limits(plt_name, lim_track, plt_survey_info)
        if not list_survey_limits:  # platform extremity not surveyed
            survey_name_dict[i] = None
        elif len(list_survey_limits) == 1:  # only 1 extremity corresponding, we do the survey comparison with this one
            survey_name = list_survey_limits[0]
            survey_name_dict[i] = survey_name
        else:  # find for which Survey limit the difference is the smallest
            test_differences = list()
            for survey_name in list_survey_limits:
                surveyed_kp = plt_survey_info[survey_name]["surveyed_kp"]
                reversed_polarity = check_polarity(lim_kp, surveyed_kp)
                if reversed_polarity:
                    diff = abs(abs(lim_kp) - abs(surveyed_kp))
                else:
                    diff = abs(lim_kp - surveyed_kp)
                test_differences.append((diff, survey_name))
            closest_survey_name = sorted(test_differences, key=lambda x: x[0])[0][1]
            survey_name_dict[i] = closest_survey_name
    return survey_name_dict


def _get_survey_limits(plt_name: str, track: str, plt_survey_info: dict[str]) -> list[str]:
    list_survey_limits = list()
    for survey_name in plt_survey_info.keys():
        survey_plt_lim_name, survey_track = survey_name.split("__", 1)
        survey_plt_name = _clean_platform_extremity_name(survey_plt_lim_name)
        if survey_track.upper() == track:
            if (survey_plt_name == plt_name.upper()
                    or survey_plt_name == plt_name.upper().removeprefix("PLATFORM_")
                    or survey_plt_name == plt_name.upper().removeprefix("PLT_")
                    or survey_plt_name.removeprefix("PLATFORM_") == plt_name.upper().removeprefix("PLT_")
                    or survey_plt_name.removeprefix("PLT_") == plt_name.upper().removeprefix("PLATFORM_")
                    or survey_plt_name.removesuffix("_1") + "_T1" == plt_name.upper()
                    or survey_plt_name.removesuffix("_2") + "_T2" == plt_name.upper()
                    or survey_plt_name.removesuffix("_T1") + "_1" == plt_name.upper()
                    or survey_plt_name.removesuffix("_T2") + "_2" == plt_name.upper()):
                list_survey_limits.append(survey_name)
    return list_survey_limits
