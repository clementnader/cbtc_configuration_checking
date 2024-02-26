#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import *
from .common_utils import *


FG_PREFIX = {
    "left": "Begin_FloodGateArea_",
    "right": "End_FloodGateArea_"
}


# FloodGate
def check_flood_gate(dc_sys_sheet, res_sheet_name: str, survey_info: dict):
    assert dc_sys_sheet == DCSYS.Flood_Gate
    assert res_sheet_name == "FloodGate"

    obj_dict = _get_dc_sys_flood_gate_dict(survey_info)
    list_used_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in obj_dict.items():
        dc_sys_track, dc_sys_kp = obj_val
        dc_sys_track = dc_sys_track.upper()

        survey_name = test_names_in_survey([obj_name], dc_sys_track, survey_info)
        survey_obj_info = survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict


def _get_dc_sys_flood_gate_dict(survey_info: dict[str, Any]):
    res_dict = dict()
    obj_dict = load_sheet(DCSYS.Flood_Gate)
    for obj_name, obj_val in obj_dict.items():
        limits = list(get_dc_sys_zip_values(obj_val, DCSYS.Flood_Gate.Limit.Track, DCSYS.Flood_Gate.Limit.Kp))
        if len(limits) == 2:
            left_lim = limits[0] if limits[0][1] <= limits[1][1] else limits[1]
            right_lim = limits[1] if limits[0][1] <= limits[1][1] else limits[0]
            obj_prefix_1, obj_prefix_2 = get_fg_end_prefixes_order(obj_name, survey_info, left_lim, right_lim)
            res_dict[obj_prefix_1 + obj_name] = left_lim
            res_dict[obj_prefix_2 + obj_name] = right_lim
        else:
            for i, lim in enumerate(limits):
                res_dict[f"FloodGateArea_{obj_name}_Limit_{i}"] = lim
    return res_dict


def get_fg_end_prefixes_order(obj_name: str, survey_info: dict[str, Any],
                              smaller_kp_lim: tuple[str, float], larger_kp_lim: tuple[str, float]) -> tuple[str, str]:
    track_smaller_kp, smaller_kp = smaller_kp_lim
    track_larger_kp, larger_kp = larger_kp_lim
    order_polarity = _get_survey_obj_order_pattern(obj_name, survey_info, track_smaller_kp, smaller_kp,
                                                   track_larger_kp, larger_kp)
    if order_polarity is False:
        obj_prefix_1, obj_prefix_2 = FG_PREFIX["right"], FG_PREFIX["left"]
    else:
        obj_prefix_1, obj_prefix_2 = FG_PREFIX["left"], FG_PREFIX["right"]
    return obj_prefix_1, obj_prefix_2


def _get_survey_obj_order_pattern(obj_name: str, survey_info: dict[str, Any],
                                  track_smaller_kp: str, smaller_dc_sys_kp: float,
                                  track_larger_kp: str, larger_dc_sys_kp: float) -> bool:
    survey_obj_ends = _get_survey_obj_ends(obj_name, track_smaller_kp, track_larger_kp, survey_info)
    if not survey_obj_ends:  # flood gate not surveyed
        return True  # default order
    if len(survey_obj_ends) != 2:
        print_warning(f"Different than 2 flood gate ends have been found for {obj_name}:\n{survey_obj_ends}")
        return True  # default order

    survey_name_1, survey_name_2 = survey_obj_ends
    obj_end_type_1 = _get_corresponding_prefix(survey_name_1)
    obj_end_type_2 = _get_corresponding_prefix(survey_name_2)
    surveyed_kp_1 = survey_info[survey_name_1]["surveyed_kp"]
    surveyed_kp_2 = survey_info[survey_name_2]["surveyed_kp"]
    reversed_polarity = (check_polarity(smaller_dc_sys_kp, min(surveyed_kp_1, surveyed_kp_2))
                         and check_polarity(larger_dc_sys_kp, max(surveyed_kp_1, surveyed_kp_2)))

    if obj_end_type_1 == obj_end_type_2:
        print_warning(f"Flood gate end names in survey don't match the expected pattern:\n"
                      f"{survey_name_1 = }, {survey_name_2 = }\n"
                      f"{obj_end_type_1 = }, {obj_end_type_2 = }.")
        return True  # default order

    if obj_end_type_1 == "left" and obj_end_type_2 == "right":
        survey_polarity = surveyed_kp_1 <= surveyed_kp_2
        global_polarity = survey_polarity if not reversed_polarity else not survey_polarity
        return global_polarity
    elif obj_end_type_1 == "right" and obj_end_type_2 == "left":
        survey_polarity = surveyed_kp_1 >= surveyed_kp_2
        global_polarity = survey_polarity if not reversed_polarity else not survey_polarity
        return global_polarity


def _get_survey_obj_ends(obj_name: str, track_smaller_kp: str, track_larger_kp: str, survey_info: dict[str, Any]
                         ) -> list[str]:
    obj_ends = list()
    for survey_name in survey_info.keys():
        obj_end_type = _get_corresponding_prefix(survey_name)
        if obj_end_type is None:
            continue

        test = False
        if survey_name.endswith(f"{obj_name}__{track_smaller_kp}".upper()):
            test = True
        if survey_name.endswith(f"{obj_name}__{track_larger_kp}".upper()):
            test = True
        if test:
            obj_ends.append(survey_name)
    return obj_ends


def _get_corresponding_prefix(survey_name: str) -> Optional[str]:
    for obj_end_type, obj_prefix in FG_PREFIX.items():
        if survey_name.startswith(obj_prefix.upper()):
            return obj_end_type
    return None
