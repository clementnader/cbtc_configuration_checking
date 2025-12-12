#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_sys import *
from ..survey_types import *


__all__ = ["create_verif_survey_dict"]


def create_verif_survey_dict(survey_info, block_def_dict: Optional[dict[str, dict[tuple[str, float], str]]]
                             ) -> tuple[dict[str, dict[str, Any]], bool]:
    middle_platforms_exist_bool = False
    survey_verif_dict = dict()
    set_of_survey_tracks = {info["survey_track"] for sub_dict in survey_info.values() for info in sub_dict.values()}

    for survey_type, survey_type_value in SURVEY_TYPES_DICT.items():
        if survey_type_value is None:
            continue
        res_sheet = survey_type_value["res_sheet"]
        if res_sheet is None:
            continue
        dc_sys_sheet = survey_type_value["dc_sys_sheet"]
        func = survey_type_value["func"]
        display_name = survey_type_value["display_name"]
        print(f"\n{Color.white}{Color.underline}Analyzing {display_name} positioning...{Color.reset}{NBSP}")

        if survey_type == "PLATFORM":
            sub_verif_dict, middle_platforms_exist_bool = func(
                dc_sys_sheet, res_sheet, survey_info.get("PLATFORM"),
                set_of_survey_tracks, survey_info.get("OSP"), survey_info.get("MIDDLE_PLATFORM"))
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(sub_verif_dict)

        elif survey_type == "TAG":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dc_sys_sheet, res_sheet, survey_info.get("TAG"),
                     set_of_survey_tracks, survey_info.get("DYNAMIC_TAG"), survey_info.get("VERSION_TAG")))

        elif survey_type == "BLOCK":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dc_sys_sheet, res_sheet, survey_info.get("BLOCK"), block_def_dict,
                     set_of_survey_tracks, survey_info.get("BUFFER"),
                     survey_info.get("SIGNAL"), survey_info.get("PERMANENT_RED")))

        elif survey_type == "SIGNAL":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dc_sys_sheet, res_sheet, survey_info.get("SIGNAL"),
                     set_of_survey_tracks, survey_info.get("PERMANENT_RED"), survey_info.get("BUFFER")))

        elif survey_type == "SWP":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dc_sys_sheet, res_sheet, survey_info.get("SWP"),
                     set_of_survey_tracks, survey_info.get("DERAILER")))

        elif survey_type == "PTA":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dc_sys_sheet, res_sheet, survey_info.get("PTA"),
                     set_of_survey_tracks, survey_info.get("PLAQUES")))

        else:
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dc_sys_sheet, res_sheet, survey_info.get(survey_type),
                     set_of_survey_tracks))

        _print_logs_survey_verif(display_name, survey_type_value, survey_verif_dict[res_sheet])

    return survey_verif_dict, middle_platforms_exist_bool


def _print_logs_survey_verif(display_name: str, survey_type_value: dict[str, Any], verif_dict: dict) -> None:
    dc_sys_display_names = survey_type_value.get("dc_sys_display_names")
    survey_display_names = survey_type_value.get("survey_display_names")

    if not verif_dict:
        print_log(f"\n\t> No {display_name} object in DC_SYS nor survey.")

    elif all(verif_info["dc_sys_sheet"] is None for verif_info in verif_dict.values()):
        print_log(f"\n\t> No {display_name} object in DC_SYS.")

    elif all(verif_info["survey_type"] is None for verif_info in verif_dict.values()):
        print_log(f"\n\t> No {display_name} information in survey.")

    else:
        if dc_sys_display_names is not None:  # multiple objects in DC_SYS analyzed at the same time
            for sheet_names, dc_sys_display_name in dc_sys_display_names:
                sub_dict = {key: info for key, info in verif_dict.items()
                            if info["dc_sys_sheet"] in sheet_names}
                if not sub_dict:
                    print_log(f"\n\t> No {dc_sys_display_name} object in DC_SYS.")

        if survey_display_names is not None:  # multiple objects in Survey analyzed at the same time
            for survey_type_dict_names, survey_display_name in survey_display_names:
                sub_dict = {key: info for key, info in verif_dict.items()
                            if any(info["survey_type"] is not None and info["survey_type"].upper()
                                   in SURVEY_TYPES_DICT[survey_type_dict_name]["survey_type_names"]
                                   for survey_type_dict_name in survey_type_dict_names)}
                if not sub_dict:
                    print_log(f"\n\t> No {survey_display_name} information in survey.")


def _order_survey_verif_dict(verif_dict: dict):
    """ Order by track then KP """
    verif_dict = {key: verif_dict[key] for key in sorted(verif_dict.keys(),
                  key=lambda x: (_get_track_to_order_dict(x, verif_dict), _get_kp_to_order_dict(x, verif_dict),
                                 _get_name_to_order_dict(x, verif_dict)))}
    return verif_dict


def _get_track_to_order_dict(x, verif_dict):
    """ Get track name inside the verif dict dictionary, from the DC_SYS or survey according to which one exists. """
    return (split_track_to_order_them(verif_dict[x]["dc_sys_track"]) if verif_dict[x]["dc_sys_track"] is not None
            else split_track_to_order_them(verif_dict[x]["survey_track"]))


def _get_kp_to_order_dict(x, verif_dict):
    """ Get KP value inside the verif dict dictionary, from the DC_SYS or survey according to which one exists."""
    return (verif_dict[x]["dc_sys_kp"] if verif_dict[x]["dc_sys_kp"] is not None
            else verif_dict[x]["surveyed_kp"])


def _get_name_to_order_dict(x, verif_dict):
    """ Get object name inside the verif dict dictionary, from the DC_SYS or survey according to which one exists."""
    return (x[0].upper() if verif_dict[x]["dc_sys_track"] is not None
            else verif_dict[x]["survey_name"].upper())
