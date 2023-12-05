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

    obj_dict = _get_dc_sys_platform_dict(survey_info)
    list_used_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in obj_dict.items():
        track, dc_sys_kp = obj_val
        track = track.upper()

        survey_name = f"{obj_name}__{track}".upper()
        survey_obj_info = survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        obj_name = survey_obj_info["obj_name"] if survey_obj_info is not None else obj_name

        res_dict[(obj_name, track)] = add_info_to_survey(survey_obj_info, track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict


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
    survey_obj_ends = _get_survey_obj_ends(obj_name, track_smaller_kp, track_larger_kp, survey_info)
    if not survey_obj_ends:  # platform not surveyed
        return "left_and_right", True  # default order
    if len(survey_obj_ends) != 2:
        print_log(
            f"{'Only one platform end has' if len(survey_obj_ends) == 1 else 'More than two platform ends have'}"
            f" been found in survey for {obj_name}:\n{survey_obj_ends}\n")
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
                         ) -> list[str]:
    obj_ends = list()
    for survey_name in survey_info.keys():
        ordering_type, obj_end_type = _get_corresponding_prefix(survey_name)
        if ordering_type is None or obj_end_type is None:
            continue
        if (survey_name.endswith(f"{obj_name}__{track_smaller_kp}".upper())
                or survey_name.endswith(f"{obj_name}__{track_larger_kp}".upper())):
            obj_ends.append(survey_name)
    return obj_ends


def _get_corresponding_prefix(survey_name: str) -> tuple[Optional[str], Optional[str]]:
    for ordering_type, sub_dict in PLT_PREFIX.items():
        for obj_end_type, obj_prefix in sub_dict.items():
            if survey_name.startswith(obj_prefix.upper()):
                return ordering_type, obj_end_type
    return None, None
