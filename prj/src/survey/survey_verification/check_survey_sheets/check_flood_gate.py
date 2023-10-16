#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import *


FG_PREFIX = {
    "left": "Begin_FloodGateArea_",
    "right": "End_FloodGateArea_"
}


# FloodGate
def check_flood_gate(dc_sys_sheet, res_sheet_name: str, survey_info: dict):
    assert dc_sys_sheet == DCSYS.Flood_Gate
    assert res_sheet_name == "FloodGate"

    fg_dict = _get_dc_sys_flood_gate_dict(survey_info)
    list_fg_names = list()
    res_dict = dict()
    for fg_name, fg_val in fg_dict.items():
        survey_obj_info = survey_info.get(fg_name.upper())
        fg_name = survey_obj_info["obj_name"] if survey_obj_info is not None else fg_name
        survey_track = survey_obj_info["track"] if survey_obj_info is not None else None
        surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
        surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
        comments = survey_obj_info["comments"] if survey_obj_info is not None else None

        list_fg_names.append(fg_name)
        res_dict[fg_name] = {"track": fg_val[0], "dc_sys_kp": fg_val[1]}
        res_dict[fg_name].update({"survey_track": survey_track, "surveyed_kp": surveyed_kp})
        res_dict[fg_name].update({"surveyed_kp_comment": surveyed_kp_comment, "comments": comments})

    res_dict.update(_add_extra_info_from_survey(list_fg_names, survey_info))
    return res_dict


def _get_dc_sys_flood_gate_dict(survey_info: dict[str]):
    res_dict = dict()
    fg_dict = load_sheet(DCSYS.Flood_Gate)
    for fg_name, fg_val in fg_dict.items():
        limits = list(get_dc_sys_zip_values(fg_val, DCSYS.Flood_Gate.Limit.Track, DCSYS.Flood_Gate.Limit.Kp))
        if len(limits) == 2:
            left_lim = limits[0] if limits[0][1] <= limits[1][1] else limits[1]
            right_lim = limits[1] if limits[0][1] <= limits[1][1] else limits[0]
            fg_prefix_1, fg_prefix_2 = get_fg_end_prefixes_order(fg_name, survey_info, left_lim[1], right_lim[1])
            res_dict[fg_prefix_1 + fg_name] = left_lim
            res_dict[fg_prefix_2 + fg_name] = right_lim
        else:
            for i, lim in enumerate(limits):
                res_dict[f"FloodGateArea_{fg_name}_Limit_{i}"] = lim
    return res_dict


def get_fg_end_prefixes_order(fg_name: str, survey_info: dict[str],
                              smaller_kp: float, larger_kp: float) -> tuple[str, str]:
    order_polarity = _get_survey_fg_order_pattern(fg_name, survey_info, smaller_kp, larger_kp)
    if order_polarity is False:
        fg_prefix_1, fg_prefix_2 = FG_PREFIX["right"], FG_PREFIX["left"]
    else:
        fg_prefix_1, fg_prefix_2 = FG_PREFIX["left"], FG_PREFIX["right"]
    return fg_prefix_1, fg_prefix_2


def _get_survey_fg_order_pattern(fg_name: str, survey_info: dict[str],
                                 smaller_dc_sys_kp: float, larger_dc_sys_kp: float) -> bool:
    survey_fg_ends = _get_survey_fg_ends(fg_name, survey_info)
    if not survey_fg_ends:  # flood gate not surveyed
        return True  # default order
    if len(survey_fg_ends) != 2:
        print_warning(f"Different than 2 flood gate ends have been found for {fg_name}:\n{survey_fg_ends}")
        return True  # default order

    survey_name_1, survey_name_2 = survey_fg_ends
    fg_end_type_1 = _get_corresponding_prefix(survey_name_1)
    fg_end_type_2 = _get_corresponding_prefix(survey_name_2)
    surveyed_kp_1 = survey_info[survey_name_1]["surveyed_kp"]
    surveyed_kp_2 = survey_info[survey_name_2]["surveyed_kp"]
    reversed_polarity = (check_polarity(smaller_dc_sys_kp, min(surveyed_kp_1, surveyed_kp_2))
                         and check_polarity(larger_dc_sys_kp, max(surveyed_kp_1, surveyed_kp_2)))

    if fg_end_type_1 == fg_end_type_2:
        print_warning(f"Flood gate end names in survey don't match the expected pattern:\n"
                      f"{survey_name_1 = }, {survey_name_2 = }\n"
                      f"{fg_end_type_1 = }, {fg_end_type_2 = }.")
        return True  # default order

    if fg_end_type_1 == "left" and fg_end_type_2 == "right":
        survey_polarity = surveyed_kp_1 <= surveyed_kp_2
        global_polarity = survey_polarity if not reversed_polarity else not survey_polarity
        return global_polarity
    elif fg_end_type_1 == "right" and fg_end_type_2 == "left":
        survey_polarity = surveyed_kp_1 >= surveyed_kp_2
        global_polarity = survey_polarity if not reversed_polarity else not survey_polarity
        return global_polarity


def _get_survey_fg_ends(fg_name: str, survey_info: dict[str]) -> list[str]:
    fg_ends = list()
    for survey_name in survey_info.keys():
        fg_end_type = _get_corresponding_prefix(survey_name)
        if fg_end_type is None:
            continue
        if survey_name.endswith(fg_name.upper()):
            fg_ends.append(survey_name)
    return fg_ends


def _get_corresponding_prefix(survey_name: str) -> Optional[str]:
    for fg_end_type, fg_prefix in FG_PREFIX.items():
        if survey_name.startswith(fg_prefix.upper()):
            return fg_end_type
    return None


def _add_extra_info_from_survey(list_fg_names: list[str], survey_info: dict[str, dict[str]]):
    extra_dict = dict()
    for fg_val in survey_info.values():
        fg_name = fg_val["obj_name"]
        if fg_name in list_fg_names:
            continue
        extra_dict[fg_name] = {"track": None, "dc_sys_kp": None}
        extra_dict[fg_name].update({"survey_name": fg_val["obj_name"], "survey_track": fg_val["track"],
                                    "surveyed_kp": fg_val["surveyed_kp"]})
        extra_dict[fg_name].update({"surveyed_kp_comment": fg_val["surveyed_kp_comment"],
                                    "comments": fg_val["comments"]})
    return extra_dict
