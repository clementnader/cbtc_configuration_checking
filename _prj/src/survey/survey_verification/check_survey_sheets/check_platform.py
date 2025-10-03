#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import clean_track_name
from .common_utils import *
from .check_osp import *


__all__ = ["check_platform"]


# Switch
def check_platform(dc_sys_sheet, res_sheet_name: str, plt_survey_info: dict,
                   set_of_survey_tracks: set[str], osp_survey_info: dict, mid_plt_survey_info: dict):
    assert dc_sys_sheet == DCSYS.Quai
    assert res_sheet_name == "Platform"

    middle_platforms_exist_bool = False

    # Update Middle Platforms dictionary
    plt_survey_info = _add_associated_plt_to_mid(plt_survey_info, set_of_survey_tracks,
                                                 is_mid_plt_survey_info=False)
    mid_plt_survey_info = _add_associated_plt_to_mid(mid_plt_survey_info, set_of_survey_tracks,
                                                     is_mid_plt_survey_info=True)

    plt_dict = load_sheet(DCSYS.Quai)
    list_used_obj_names = list()
    res_dict = dict()
    for plt_name, plt_val in plt_dict.items():
        plt_limits = _get_plt_limits(plt_val)
        associated_survey_dict = get_corresponding_plt_survey_extremities(plt_name, plt_limits, plt_survey_info,
                                                                          set_of_survey_tracks)

        limits_survey_info = [(plt_name + f"__Limit_{n}", lim_track, lim_kp, survey_name)
                              for n, ((lim_track, lim_kp), survey_name)
                              in enumerate(associated_survey_dict.items(), start=1)]

        for obj_name, dc_sys_original_track, dc_sys_kp, survey_name in limits_survey_info:
            dc_sys_track = clean_track_name(dc_sys_original_track, set_of_survey_tracks)
            survey_obj_info = plt_survey_info.get(survey_name)
            if survey_obj_info is not None:
                list_used_obj_names.append(survey_name)
            else:
                survey_obj_info = _associate_plt_extremity_to_survey_mid_plt(
                    obj_name, plt_name, dc_sys_kp, limits_survey_info, plt_survey_info, mid_plt_survey_info)
                if survey_obj_info is not None:  # we made an association with a Middle Platform
                    middle_platforms_exist_bool = True

            res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                    dc_sys_track, dc_sys_original_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, plt_survey_info))

    # Add Middle Platforms from survey and set defined names
    res_dict.update(add_extra_info_from_survey([], mid_plt_survey_info))

    # Add OSP on same sheet
    res_dict.update(
        check_osp([DCSYS.Quai.PointDArret, DCSYS.PtA], res_sheet_name, osp_survey_info, set_of_survey_tracks))
    return res_dict, middle_platforms_exist_bool


def _clean_platform_extremity_name(plt_lim_name: str) -> str:
    plt_lim_name = plt_lim_name.upper()
    plt_name = plt_lim_name.removeprefix("LEFT_END_").removeprefix("RIGHT_END_")
    plt_name = plt_name.removeprefix("PLATFORM_BEGIN_").removeprefix("PLATFORM_START_").removeprefix("PLATFORM_END_")
    plt_name = plt_name.removeprefix("BEGIN_").removeprefix("START_").removeprefix("END_")
    plt_name = plt_name.removeprefix("PLATFORM1_").removeprefix("PLATFORM2_")
    plt_name = plt_name.removeprefix("QUAI1_").removeprefix("QUAI2_")
    plt_name = plt_name.removesuffix("_BEGIN").removesuffix("_START").removesuffix("_END")
    return plt_name


def _clean_platform_middle_name(plt_mid_name: str, is_mid_plt_survey_info: bool) -> Optional[str]:
    plt_mid_name = plt_mid_name.upper()
    if (not is_mid_plt_survey_info  # if type is already Middle Platform, we don't do this check
            and not (plt_mid_name.startswith("MIDDLE_") or plt_mid_name.startswith("MID_")
                     or plt_mid_name.startswith("MID")
                     or plt_mid_name.endswith("_MIDDLE") or plt_mid_name.endswith("_MID")
                     or plt_mid_name.endswith("MID"))):
        return None
    plt_name = plt_mid_name.removeprefix("MIDDLE_").removeprefix("MID_")
    plt_name = plt_name.removeprefix("MID")
    plt_name = plt_name.removesuffix("_MIDDLE").removesuffix("MID_")
    plt_name = plt_name.removesuffix("MID")
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


def _get_survey_limits_on_track(plt_name: str, track: str, dc_sys_track: str, plt_survey_info: dict[str, Any],
                                test_with_mid_plt: bool = False, is_mid_plt_survey_info: bool = False) -> list[str]:
    clean_plt_name = plt_name.upper().removeprefix("PLATFORM_").removeprefix("PLT_")
    # Get survey platform names from the platform extremity (or middle platform) and remove the PLATFORM prefix
    list_survey_plt_names = list()
    for survey_name in plt_survey_info:
        survey_plt_lim_name, survey_track = survey_name.split("__", 1)
        if survey_track.upper() != track:
            continue
        if test_with_mid_plt:
            survey_plt_name = _clean_platform_middle_name(survey_plt_lim_name, is_mid_plt_survey_info)
            if survey_plt_name is None:
                continue
        else:
            survey_plt_name = _clean_platform_extremity_name(survey_plt_lim_name)
        survey_plt_name = survey_plt_name.removeprefix("PLATFORM_").removeprefix("PLT_")
        list_survey_plt_names.append((survey_name, survey_plt_name))

    # Find correspondence of DC_SYS platform name into survey
    list_survey_limits = _correspondence_plt_names(clean_plt_name, list_survey_plt_names)

    if not list_survey_limits:
        # Try using only the unique prefix of the platform for the association
        unique_prefix = _get_unique_prefix_plt_names_dict()[dc_sys_track.upper()][plt_name]
        list_survey_plt_names = [(survey_name, survey_plt_name[:len(unique_prefix)])
                                 for survey_name, survey_plt_name in list_survey_plt_names]
        list_survey_limits = _correspondence_plt_names(unique_prefix, list_survey_plt_names)

    return list_survey_limits


def _correspondence_plt_names(dc_sys_plt_name: str, list_survey_plt_names: list[tuple[str, str]]) -> list[str]:
    list_survey_limits = list()
    for survey_name, survey_plt_name in list_survey_plt_names:
        if survey_plt_name == dc_sys_plt_name:
            list_survey_limits.append(survey_name)
    if list_survey_limits:
        return list_survey_limits

    # Try changing track name
    for survey_name, survey_plt_name in list_survey_plt_names:
        if re.match(r"_([1-9])$", survey_plt_name) is not None:
            survey_plt_name = re.sub(r"_([1-9])$", r"_T\1", survey_plt_name)
        elif re.match(r"_T([1-9])$", survey_plt_name) is not None:
            survey_plt_name = re.sub(r"_T([1-9])$", r"_\1", survey_plt_name)
        if survey_plt_name == dc_sys_plt_name:
            list_survey_limits.append(survey_name)
    if list_survey_limits:
        return list_survey_limits

    # Try adding underscores
    dc_sys_test_plt_name = re.sub(r"([A-Z])([0-9])", r"\1_\2", dc_sys_plt_name)
    dc_sys_test_plt_name = re.sub(r"([0-9])([A-Z])", r"\1_\2", dc_sys_test_plt_name)
    for survey_name, survey_plt_name in list_survey_plt_names:
        survey_plt_name = re.sub(r"([A-Z])([0-9])", r"\1_\2", survey_plt_name)
        survey_plt_name = re.sub(r"([0-9])([A-Z])", r"\1_\2", survey_plt_name)
        if survey_plt_name == dc_sys_test_plt_name:
            list_survey_limits.append(survey_name)
    if list_survey_limits:
        return list_survey_limits

    return list_survey_limits


def get_corresponding_plt_survey_extremities(plt_name: str, plt_limits: list[tuple[str, float]],
                                             plt_survey_info: dict[str, Any], set_of_survey_tracks: set[str]
                                             ) -> dict[tuple[str, float], Optional[str]]:
    associated_survey_dict = {(lim_track, lim_kp): None for (lim_track, lim_kp) in plt_limits}

    dc_sys_limit_tracks = set([(track, clean_track_name(track, set_of_survey_tracks)) for (track, _) in plt_limits])
    for dc_sys_track, test_track in dc_sys_limit_tracks:
        dc_sys_limits_on_track = [(track, dc_sys_kp) for (track, dc_sys_kp) in plt_limits
                                  if clean_track_name(track, set_of_survey_tracks) == test_track]
        survey_limits_on_track = _get_survey_limits_on_track(plt_name, test_track, dc_sys_track, plt_survey_info)

        if len(dc_sys_limits_on_track) == 1:
            associated_survey_dict = get_corresponding_survey_one_limit_on_track(
                dc_sys_limits_on_track, associated_survey_dict, survey_limits_on_track, plt_survey_info)
        elif len(dc_sys_limits_on_track) == 2:
            associated_survey_dict = get_corresponding_survey_two_limits_on_track(
                dc_sys_limits_on_track, associated_survey_dict, survey_limits_on_track, plt_survey_info)

    return associated_survey_dict


def _add_associated_plt_to_mid(plt_survey_info: dict, set_of_survey_tracks: set[str],
                               is_mid_plt_survey_info: bool) -> dict:
    plt_dict = load_sheet(DCSYS.Quai)
    for plt_name in plt_dict:
        corresponding_defined_name = f"mid_plt_{plt_name}"
        dc_sys_track = get_dc_sys_value(plt_name, DCSYS.Quai.ExtremiteDuQuai.Voie)[0]
        test_track = clean_track_name(dc_sys_track, set_of_survey_tracks)

        # Update plt_survey_info for PLATFORM objects corresponding to Middle Platforms only
        # to add as defined_name the DC_SYS platform name.
        survey_mid_plt_name = _get_survey_limits_on_track(plt_name, test_track, dc_sys_track, plt_survey_info,
                                                          test_with_mid_plt=True,
                                                          is_mid_plt_survey_info=is_mid_plt_survey_info)
        if not survey_mid_plt_name:
            continue
        if len(survey_mid_plt_name) > 1:
            print_warning(f"There are multiple middle platforms from survey that correspond to {plt_name}:")
            print("", survey_mid_plt_name)
            continue
        survey_mid_plt_name = survey_mid_plt_name[0]

        plt_survey_info[survey_mid_plt_name]["defined_name"] = corresponding_defined_name

        new_comments = "Middle Platform. A defined name is defined on the Surveyed KP cell."
        plt_survey_info[survey_mid_plt_name]["comments"] = (
            new_comments if plt_survey_info[survey_mid_plt_name]["comments"] is None
            else (plt_survey_info[survey_mid_plt_name]["comments"] + "\n\n" + new_comments))

    return plt_survey_info


def _associate_plt_extremity_to_survey_mid_plt(obj_name: str, plt_name: str, dc_sys_kp: float,
                                               limits_survey_info: list[tuple[str, str, float, str]],
                                               plt_survey_info: dict, mid_plt_survey_info: dict
                                               ) -> Optional[dict]:
    corresponding_defined_name = f"mid_plt_{plt_name}"
    all_survey_info = plt_survey_info | mid_plt_survey_info
    list_matching_survey_info = [info for info in all_survey_info.values()
                                 if info.get("defined_name") == corresponding_defined_name]
    if not list_matching_survey_info:
        return None
    if len(list_matching_survey_info) > 1:
        print_warning(f"There are multiple middle platforms from survey that correspond to {plt_name}:")
        print("", list_matching_survey_info)
        return None
    survey_info = list_matching_survey_info[0]

    # Get formula to compute this extremity from middle platform
    other_limit_dc_sys_kp = [kp for lim_name, _, kp, _ in limits_survey_info if lim_name != obj_name][0]
    if dc_sys_kp < other_limit_dc_sys_kp:
        formula_symbol = "-"
    else:
        formula_symbol = "+"

    surveyed_kp_formula = f'= {corresponding_defined_name} {formula_symbol} platform_length/2'
    comments = f"Computed with Middle Platform \"{survey_info['obj_name']}\"."

    survey_obj_info = {
        "obj_name": "Computed",
        "survey_type": None,
        "survey_track": survey_info["survey_track"],
        "survey_original_track": survey_info["survey_original_track"],
        "surveyed_kp": surveyed_kp_formula,
        "surveyed_kp_comment": None,
        "comments": comments,
    }
    return survey_obj_info
