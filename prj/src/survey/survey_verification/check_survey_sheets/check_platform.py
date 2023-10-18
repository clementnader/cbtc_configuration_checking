#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import *
from .common_utils import *


PLT_PREFIX = {
    "left_and_right": {"left": "LEFT_END_", "right": "RIGHT_END_"},
    "begin_and_end": {"left": "Begin_", "right": "End_"}
}


# Switch
def check_platform(dc_sys_sheet, res_sheet_name: str, survey_info: dict):
    assert dc_sys_sheet == DCSYS.Quai
    assert res_sheet_name == "Platform"

    plt_dict = _get_dc_sys_platform_dict(survey_info)
    list_plt_names = list()
    res_dict = dict()
    for plt_name, plt_val in plt_dict.items():
        survey_obj_info = survey_info.get(plt_name.upper())
        plt_name = survey_obj_info["obj_name"] if survey_obj_info is not None else plt_name
        survey_track = survey_obj_info["track"] if survey_obj_info is not None else None
        surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
        surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
        comments = survey_obj_info["comments"] if survey_obj_info is not None else None

        list_plt_names.append(plt_name)
        track, dc_sys_kp = plt_val
        res_dict[plt_name] = {"track": track, "dc_sys_kp": dc_sys_kp,
                              "survey_track": survey_track, "surveyed_kp": surveyed_kp,
                              "surveyed_kp_comment": surveyed_kp_comment, "comments": comments}

    res_dict.update(add_extra_info_from_survey(list_plt_names, survey_info))
    return res_dict


def _get_dc_sys_platform_dict(survey_info: dict[str]):
    res_dict = dict()
    plt_dict = load_sheet(DCSYS.Quai)
    for plt_name, plt_val in plt_dict.items():
        limits = list(get_dc_sys_zip_values(plt_val, DCSYS.Quai.ExtremiteDuQuai.Voie, DCSYS.Quai.ExtremiteDuQuai.Pk))
        left_lim = limits[0] if limits[0][1] <= limits[1][1] else limits[1]  # smaller KP
        right_lim = limits[1] if limits[0][1] <= limits[1][1] else limits[0]  # larger KP
        plt_prefix_1, plt_prefix_2 = get_plt_end_prefixes_order(plt_name, survey_info, left_lim[1], right_lim[1])
        res_dict[plt_prefix_1 + plt_name] = left_lim
        res_dict[plt_prefix_2 + plt_name] = right_lim
    return res_dict


def get_plt_end_prefixes_order(plt_name: str, survey_info: dict[str],
                               smaller_kp: float, larger_kp: float) -> tuple[str, str]:
    ordering_type, order_polarity = _get_survey_plt_order_pattern(plt_name, survey_info, smaller_kp, larger_kp)
    info_dict = PLT_PREFIX[ordering_type]
    if order_polarity is False:
        plt_prefix_1, plt_prefix_2 = info_dict["right"], info_dict["left"]
    else:
        plt_prefix_1, plt_prefix_2 = info_dict["left"], info_dict["right"]
    return plt_prefix_1, plt_prefix_2


def _get_survey_plt_order_pattern(plt_name: str, survey_info: dict[str],
                                  smaller_dc_sys_kp: float, larger_dc_sys_kp: float) -> tuple[str, bool]:
    survey_plt_ends = _get_survey_plt_ends(plt_name, survey_info)
    if not survey_plt_ends:  # platform not surveyed
        return "left_and_right", True  # default order
    if len(survey_plt_ends) != 2:
        print_log(
            f"{'Only one platform end has' if len(survey_plt_ends) == 1 else 'More than two platform ends have'}"
            f" been found in survey for {plt_name}:\n{survey_plt_ends}\n")
        return "left_and_right", True  # default order

    survey_name_1, survey_name_2 = survey_plt_ends
    ordering_type_1, plt_end_type_1 = _get_corresponding_prefix(survey_name_1)
    ordering_type_2, plt_end_type_2 = _get_corresponding_prefix(survey_name_2)
    surveyed_kp_1 = survey_info[survey_name_1]["surveyed_kp"]
    surveyed_kp_2 = survey_info[survey_name_2]["surveyed_kp"]
    reversed_polarity = (check_polarity(smaller_dc_sys_kp, min(surveyed_kp_1, surveyed_kp_2))
                         and check_polarity(larger_dc_sys_kp, max(surveyed_kp_1, surveyed_kp_2)))

    if (ordering_type_1 is None or ordering_type_2 is None or ordering_type_1 != ordering_type_2
            or plt_end_type_1 == plt_end_type_2):
        print_warning(f"Platform end names in survey don't match the expected pattern:\n"
                      f"{survey_name_1 = }, {survey_name_2 = }\n"
                      f"{ordering_type_1 = }, {ordering_type_2 = },"
                      f"{plt_end_type_1 = }, {plt_end_type_2 = }.")
        return "left_and_right", True  # default order

    if plt_end_type_1 == "left" and plt_end_type_2 == "right":
        survey_polarity = surveyed_kp_1 <= surveyed_kp_2
        global_polarity = survey_polarity if not reversed_polarity else not survey_polarity
        return ordering_type_1, global_polarity
    elif plt_end_type_1 == "right" and plt_end_type_2 == "left":
        survey_polarity = surveyed_kp_1 >= surveyed_kp_2
        global_polarity = survey_polarity if not reversed_polarity else not survey_polarity
        return ordering_type_1, global_polarity


def _get_survey_plt_ends(plt_name: str, survey_info: dict[str]) -> list[str]:
    plt_ends = list()
    for survey_name in survey_info.keys():
        ordering_type, plt_end_type = _get_corresponding_prefix(survey_name)
        if ordering_type is None or plt_end_type is None:
            continue
        if survey_name.endswith(plt_name.upper()):
            plt_ends.append(survey_name)
    return plt_ends


def _get_corresponding_prefix(survey_name: str) -> tuple[Optional[str], Optional[str]]:
    for ordering_type, sub_dict in PLT_PREFIX.items():
        for plt_end_type, plt_prefix in sub_dict.items():
            if survey_name.startswith(plt_prefix.upper()):
                return ordering_type, plt_end_type
    return None, None
