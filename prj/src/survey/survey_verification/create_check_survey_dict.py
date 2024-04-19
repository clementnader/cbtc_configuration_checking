#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..survey_types import *


__all__ = ["create_check_survey_dict"]


def create_check_survey_dict(survey_info, block_def_dict: Optional[dict[str, dict[tuple[str, float], str]]]):
    survey_verif_dict = dict()
    for survey_type, survey_type_value in SURVEY_TYPES_DICT.items():
        if survey_type in ["OSP", "VERSION TAG"]:
            continue
        res_sheet = survey_type_value["res_sheet"]
        dcsys_sh = survey_type_value["dcsys_sh"]
        func = survey_type_value["func"]
        if survey_type == "PLATFORM":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dcsys_sh, res_sheet, survey_info.get("PLATFORM"), survey_info.get("OSP")))
        elif survey_type == "TAG":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dcsys_sh, res_sheet, survey_info.get("TAG"), survey_info.get("VERSION TAG")))
        elif survey_type == "TC":
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dcsys_sh, res_sheet, survey_info.get("TC"), block_def_dict, survey_info.get("SIGNAL_BUFFER")))
        else:
            survey_verif_dict[res_sheet] = _order_survey_verif_dict(
                func(dcsys_sh, res_sheet, survey_info.get(survey_type)))
    return survey_verif_dict


def _order_survey_verif_dict(verif_dict: dict):
    """ Order by track then KP """
    verif_dict = {key: verif_dict[key] for key in sorted(verif_dict.keys(),
                  key=lambda x: (_get_track_to_order_dict(x, verif_dict), _get_kp_to_order_dict(x, verif_dict)))}
    return verif_dict


def _get_track_to_order_dict(x, verif_dict):
    """ Get track name inside the verif dict dictionary, according to which one exists. """
    return (order_track(verif_dict[x]["dc_sys_track"]) if verif_dict[x]["dc_sys_track"] is not None
            else order_track(verif_dict[x]["survey_track"]))


def order_track(track: str) -> tuple[Union[str, int], ...]:
    if track.isalpha():
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
    """ Get KP value inside the verif dict dictionary, with the different KP values according to which one exists.
        If none, put a dummy large value, for the object to be at the end of the order. """
    return (verif_dict[x]["dc_sys_kp"] if verif_dict[x]["dc_sys_kp"] is not None
            else verif_dict[x]["surveyed_kp"])
