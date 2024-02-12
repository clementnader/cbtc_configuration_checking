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

    # plt_dict = load_sheet(DCSYS.Quai)
    obj_dict = _get_dc_sys_platform_dict(plt_survey_info)
    list_used_obj_names = list()
    res_dict = dict()
    # for plt_name, plt_val in plt_dict.items():
    #     plt_limits = _get_plt_limits(plt_val)
    #     (lim1_track, lim1_kp), (lim2_track, lim2_kp) = plt_limits
    #     objects = [[plt_name + "__Limit_1", lim1_track, lim1_kp],
    #                [plt_name + "__Limit_2", lim2_track, lim2_kp]]

    for obj_name, obj_val in obj_dict.items():
        dc_sys_track, dc_sys_kp = obj_val
        # survey_name = _get_platform_survey_name(obj_name, dc_sys_track, plt_survey_info)
        # survey_obj_info = plt_survey_info.get(survey_name)
        dc_sys_track = dc_sys_track.upper()

        survey_name = _get_platform_survey_name(obj_name, dc_sys_track, plt_survey_info)
        survey_obj_info = plt_survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        obj_name = survey_obj_info["obj_name"] if survey_obj_info is not None else obj_name
        res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, plt_survey_info))

    # Add platform OSP on same sheet
    res_dict.update(check_platform_osp(dc_sys_sheet.PointDArret, res_sheet_name, osp_survey_info))
    return res_dict


def _get_plt_limits(plt_val: dict) -> list[tuple[str, float]]:
    limits = list(get_dc_sys_zip_values(plt_val, DCSYS.Quai.ExtremiteDuQuai.Voie, DCSYS.Quai.ExtremiteDuQuai.Pk))
    return limits


# def _get_corresponding_survey_extremities(plt_name: str, plt_limits: list[tuple[str, float]],
#                                           plt_survey_info: dict[str]):
#     survey_name_dict = {1: None, 2: None}
#     (lim1_track, lim1_kp), (lim2_track, lim2_kp) = plt_limits
#
#     list_survey_limits = _get_survey_limits(plt_name, plt_survey_info)
#     if not list_survey_limits:  # platform not surveyed
#         return survey_name_dict
#     if len(list_survey_limits) != 2:
#         print_log(
#             f"{'Only one platform end has' if len(list_survey_limits) == 1 else 'More than two platform ends have'}"
#             f" been found in survey for {plt_name}:\n{list_survey_limits}\n")
#         return None  # TODO
#
#     (survey_lim1_name, survey_lim1_track), (survey_lim2_name, survey_lim2_track) = list_survey_limits
#     survey_lim1_kp = plt_survey_info[survey_lim1_name]["surveyed_kp"]
#     survey_lim2_kp = plt_survey_info[survey_lim2_name]["surveyed_kp"]
#     if lim1_track == lim2_track and survey_lim1_track == survey_lim2_track:
#         if lim1_track != survey_lim1_track:
#             survey_name_dict
#         return _get_corresponding_survey_same_track(lim1_kp, lim2_kp, survey_lim1_name, survey_lim1_kp,
#                                                     survey_lim2_name, survey_lim2_kp)


# def _get_corresponding_survey_same_track(lim1_kp, lim2_kp, survey_lim1_name, survey_lim1_kp,
#                                          survey_lim2_name, survey_lim2_kp):
#     smaller_dc_sys_kp = min(lim1_kp, lim2_kp)
#     larger_dc_sys_kp = max(lim1_kp, lim2_kp)
#     is_1_smaller = True if lim1_kp == smaller_dc_sys_kp else False
#
#     (smaller_survey_name, smaller_survey_kp), (larger_survey_name, larger_survey_kp) = (
#         sorted([(survey_lim1_name, survey_lim1_kp), (survey_lim2_name, survey_lim2_kp)],
#                key=lambda x: x[1])
#     )
#     reversed_polarity = (check_polarity(smaller_dc_sys_kp, smaller_survey_kp)
#                          and check_polarity(larger_dc_sys_kp, larger_survey_kp))
#
#     return


# def _clean_platform_extremity_name(plt_lim_name: str) -> str:
#     plt_name = plt_lim_name.upper()
#     plt_name = plt_lim_name.removeprefix("LEFT_END_").removeprefix("RIGHT_END_")
#     plt_name = plt_lim_name.removeprefix("BEGIN_").removeprefix("END_")
#     plt_name = plt_lim_name.removeprefix("QUAI1_").removeprefix("QUAI2_")
#     plt_name = plt_lim_name.removesuffix("_START").removeprefix("_END")
#     return plt_name


# def _get_survey_limits(plt_name: str, plt_survey_info: dict[str]) -> list[tuple[str, str]]:
#     list_survey_limits = list()
#     for survey_name in plt_survey_info.keys():
#         survey_plt_lim_name, survey_track = survey_name.split("__", 1)
#         survey_plt_name = _clean_platform_extremity_name(survey_plt_lim_name)
#         if (survey_plt_name == plt_name.upper()
#                 or survey_plt_name.removesuffix("_1") + "_T1" == plt_name.upper()
#                 or survey_plt_name.removesuffix("_2") + "_T2" == plt_name.upper()):
#             list_survey_limits.append((survey_name, survey_track))
#     return list_survey_limits


# to remove

def _get_platform_survey_name(obj_name: str, track: str, survey_info: dict[str]) -> str:
    for test_track in get_test_tracks(track):
        survey_name = f"{obj_name}__{test_track}".upper()
        if survey_name in survey_info:
            return survey_name
        if obj_name.endswith("_1") and f"{obj_name.removesuffix('_1')}_T1__{test_track}".upper() in survey_info:
            return f"{obj_name.removesuffix('_1')}_T1__{test_track}".upper()
        if obj_name.endswith("_2") and f"{obj_name.removesuffix('_2')}_T2__{test_track}".upper() in survey_info:
            return f"{obj_name.removesuffix('_2')}_T2__{test_track}".upper()
    return f"{obj_name}__{track}".upper()


def _get_dc_sys_platform_dict(survey_info: dict[str]):
    res_dict = dict()
    obj_dict = load_sheet(DCSYS.Quai)
    for obj_name, obj_val in obj_dict.items():
        limits = list(get_dc_sys_zip_values(obj_val, DCSYS.Quai.ExtremiteDuQuai.Voie, DCSYS.Quai.ExtremiteDuQuai.Pk))
        left_lim = limits[0] if limits[0][1] <= limits[1][1] else limits[1]  # smaller KP
        right_lim = limits[1] if limits[0][1] <= limits[1][1] else limits[0]  # larger KP
        obj_prefix_1, obj_prefix_2 = get_obj_end_prefixes_order(obj_name, survey_info, left_lim, right_lim)
        res_dict[obj_prefix_1 + obj_name] = left_lim
        res_dict[obj_prefix_2 + obj_name] = right_lim
    return res_dict


def get_obj_end_prefixes_order(obj_name: str, survey_info: dict[str],
                               smaller_kp_lim: tuple[str, float], larger_kp_lim: tuple[str, float]) -> tuple[str, str]:
    track_smaller_kp, smaller_kp = smaller_kp_lim
    track_larger_kp, larger_kp = larger_kp_lim
    ordering_type, order_polarity = _get_survey_obj_order_pattern(obj_name, survey_info, track_smaller_kp, smaller_kp,
                                                                  track_larger_kp, larger_kp)
    info_dict = PLT_PREFIX[ordering_type]
    if order_polarity is False:
        obj_prefix_1, obj_prefix_2 = info_dict["right"], info_dict["left"]
    else:
        obj_prefix_1, obj_prefix_2 = info_dict["left"], info_dict["right"]
    return obj_prefix_1, obj_prefix_2


def _get_survey_obj_order_pattern(obj_name: str, survey_info: dict[str],
                                  track_smaller_kp: str, smaller_dc_sys_kp: float,
                                  track_larger_kp: str, larger_dc_sys_kp: float) -> tuple[str, bool]:
    survey_obj_ends, display_obj_ends = _get_survey_obj_ends(obj_name, track_smaller_kp, track_larger_kp, survey_info)
    if not survey_obj_ends:  # platform not surveyed
        return "left_and_right", True  # default order
    if len(survey_obj_ends) != 2:
        print_log(
            f"{'Only one platform end has' if len(survey_obj_ends) == 1 else 'More than two platform ends have'}"
            f" been found in survey for {obj_name}:\n{display_obj_ends}\n")
        return "left_and_right", True  # default order

    survey_name_1, survey_name_2 = survey_obj_ends
    ordering_type_1, obj_end_type_1 = _get_corresponding_prefix(survey_name_1)
    ordering_type_2, obj_end_type_2 = _get_corresponding_prefix(survey_name_2)
    surveyed_kp_1 = survey_info[survey_name_1]["surveyed_kp"]
    surveyed_kp_2 = survey_info[survey_name_2]["surveyed_kp"]
    reversed_polarity = (check_polarity(smaller_dc_sys_kp, min(surveyed_kp_1, surveyed_kp_2))
                         and check_polarity(larger_dc_sys_kp, max(surveyed_kp_1, surveyed_kp_2)))

    if (ordering_type_1 is None or ordering_type_2 is None or ordering_type_1 != ordering_type_2
            or obj_end_type_1 == obj_end_type_2):
        print_warning(f"Platform end names in survey don't match the expected pattern:\n"
                      f"{survey_name_1 = }, {survey_name_2 = }\n"
                      f"{ordering_type_1 = }, {ordering_type_2 = },"
                      f"{obj_end_type_1 = }, {obj_end_type_2 = }.")
        return "left_and_right", True  # default order

    if obj_end_type_1 == "left" and obj_end_type_2 == "right":
        survey_polarity = surveyed_kp_1 <= surveyed_kp_2
        global_polarity = survey_polarity if not reversed_polarity else not survey_polarity
        return ordering_type_1, global_polarity
    elif obj_end_type_1 == "right" and obj_end_type_2 == "left":
        survey_polarity = surveyed_kp_1 >= surveyed_kp_2
        global_polarity = survey_polarity if not reversed_polarity else not survey_polarity
        return ordering_type_1, global_polarity


def _get_survey_obj_ends(obj_name: str, track_smaller_kp: str, track_larger_kp: str, survey_info: dict[str]
                         ) -> tuple[list[str], list[str]]:
    obj_ends = list()
    display_obj_ends = list()
    for survey_name in survey_info.keys():
        ordering_type, obj_end_type = _get_corresponding_prefix(survey_name)
        if ordering_type is None or obj_end_type is None:
            continue

        test = False
        for test_track_smaller_kp in get_test_tracks(track_smaller_kp):
            if (survey_name.endswith(f"{obj_name}__{test_track_smaller_kp}".upper())
                    or survey_name.endswith(f"{obj_name.removesuffix('_1')}_T1__{test_track_smaller_kp}".upper())
                    or survey_name.endswith(f"{obj_name.removesuffix('_2')}_T2__{test_track_smaller_kp}".upper())):
                test = True
        for test_track_larger_kp in get_test_tracks(track_larger_kp):
            if (survey_name.endswith(f"{obj_name}__{test_track_larger_kp}".upper())
                    or survey_name.endswith(f"{obj_name.removesuffix('_1')}_T1__{test_track_larger_kp}".upper())
                    or survey_name.endswith(f"{obj_name.removesuffix('_2')}_T2__{test_track_larger_kp}".upper())):
                test = True
        if test:
            obj_ends.append(survey_name)
            display_name = survey_name
            for test_track_smaller_kp in get_test_tracks(track_smaller_kp):
                survey_name.removesuffix(f"__{test_track_smaller_kp}")
            for test_track_larger_kp in get_test_tracks(track_larger_kp):
                survey_name.removesuffix(f"__{test_track_larger_kp}")
            display_obj_ends.append(survey_name)
    return obj_ends, display_obj_ends


def _get_corresponding_prefix(survey_name: str) -> tuple[Optional[str], Optional[str]]:
    for ordering_type, sub_dict in PLT_PREFIX.items():
        for obj_end_type, obj_prefix in sub_dict.items():
            if survey_name.startswith(obj_prefix.upper()):
                return ordering_type, obj_end_type
    return None, None
