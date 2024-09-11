#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..survey_types import *


__all__ = ["create_verif_survey_dict"]


def create_verif_survey_dict(survey_info, block_def_dict: Optional[dict[str, dict[tuple[str, float], str]]]):
    survey_verif_dict = dict()
    set_of_survey_tracks = {info["survey_track"] for sub_dict in survey_info.values() for info in sub_dict.values()}

    for survey_type, survey_type_value in SURVEY_TYPES_DICT.items():
        if survey_type in ["OSP", "BUFFER", "DYNAMIC_TAG", "VERSION_TAG", "TURNBACK_PLATFORM"]:
            continue

        res_sheet = survey_type_value["res_sheet"]
        dcsys_sh = survey_type_value["dcsys_sh"]
        func = survey_type_value["func"]
        display_name = survey_type_value["display_name"]
        print(f"\n{Color.white}{Color.underline}Analyzing {display_name} positioning...{Color.reset}{NBSP}")

        if survey_type == "PLATFORM":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dcsys_sh, res_sheet, survey_info.get("PLATFORM"),
                     set_of_survey_tracks, survey_info.get("OSP")))

        elif survey_type == "TAG":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dcsys_sh, res_sheet, survey_info.get("TAG"),
                     set_of_survey_tracks, survey_info.get("DYNAMIC_TAG"), survey_info.get("VERSION_TAG")))

        elif survey_type == "BLOCK":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dcsys_sh, res_sheet, survey_info.get("BLOCK"), block_def_dict,
                     set_of_survey_tracks, survey_info.get("BUFFER")))

        elif survey_type == "SIGNAL":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dcsys_sh, res_sheet, survey_info.get("SIGNAL"),
                     set_of_survey_tracks, survey_info.get("BUFFER")))

        elif survey_type == "WALKWAY":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dcsys_sh, res_sheet, survey_info.get("WALKWAY"),
                     set_of_survey_tracks, survey_info.get("PLATFORM")))

        else:
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dcsys_sh, res_sheet, survey_info.get(survey_type),
                     set_of_survey_tracks))

        _print_logs_survey_verif(display_name, survey_type_value, survey_verif_dict[res_sheet])

    return survey_verif_dict


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
    return (_split_track(verif_dict[x]["dc_sys_track"]) if verif_dict[x]["dc_sys_track"] is not None
            else _split_track(verif_dict[x]["survey_track"]))


def _split_track(track: str) -> tuple[Union[str, int], ...]:
    """ Split track into a tuple to separate the numeric and the alphabetic words.
    For example, TRACK_2 and TRACK_11 would become ("TRACK_", 2) and ("TRACK_", 11),
     so that the TRACK_2 would be ordered before the 11. If doing a simple sort, the 11 is taken as a string
     and is ordered before the 2. """
    if all(not c.isnumeric() for c in track):  # no number if the track name
        return (track.lower(),)
    list_words = list()
    pos = 0
    char_type = "num" if track[pos].isnumeric() else "other"
    if char_type == "num":
        list_words.append("")
    current_word = track[pos]
    while pos < len(track) - 1:
        pos += 1
        new_char_type = "num" if track[pos].isnumeric() else "other"
        if new_char_type == char_type:
            current_word += track[pos]
        else:
            if char_type == "num":
                current_word = int(current_word)
            else:
                current_word = current_word.lower()
            list_words.append(current_word)
            current_word = track[pos]
        char_type = new_char_type
    if char_type == "num":
        current_word = int(current_word)
    else:
        current_word = current_word.lower()
    list_words.append(current_word)
    return tuple(list_words)


def _get_kp_to_order_dict(x, verif_dict):
    """ Get KP value inside the verif dict dictionary, from the DC_SYS or survey according to which one exists."""
    return (verif_dict[x]["dc_sys_kp"] if verif_dict[x]["dc_sys_kp"] is not None
            else verif_dict[x]["surveyed_kp"])


def _get_name_to_order_dict(x, verif_dict):
    """ Get object name inside the verif dict dictionary, from the DC_SYS or survey according to which one exists."""
    return (x[0].upper() if verif_dict[x]["dc_sys_track"] is not None
            else verif_dict[x]["survey_name"].upper())
