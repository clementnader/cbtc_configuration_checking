#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import clean_track_name, clean_object_name
from .common_utils import *


__all__ = ["check_signal"]


# Signal and Buffer
def check_signal(dc_sys_sheet, res_sheet_name: str, survey_info: dict[str, dict[str, Union[str, float]]],
                 set_of_survey_tracks: set[str], pr_survey_info: dict[str, dict[str, Union[str, float]]],
                 buffer_survey_info: dict[str, dict[str, Union[str, float]]]):
    assert dc_sys_sheet == DCSYS.Sig
    assert res_sheet_name == "Signal"

    dc_sys_dict = load_sheet(dc_sys_sheet)
    survey_info.update(pr_survey_info)
    survey_info.update(buffer_survey_info)
    list_used_object_names = list()
    res_dict = dict()
    for object_name, object_value in dc_sys_dict.items():
        original_dc_sys_track, dc_sys_kp = _get_dc_sys_position(dc_sys_sheet, object_value)
        dc_sys_track = clean_track_name(original_dc_sys_track, set_of_survey_tracks)

        is_home_sig = (dc_sys_sheet == DCSYS.Sig
                       and get_dc_sys_value(object_value, DCSYS.Sig.Type) == SignalType.MANOEUVRE)
        is_permanently_red_sig = (dc_sys_sheet == DCSYS.Sig
                                  and get_dc_sys_value(object_value, DCSYS.Sig.Type) == SignalType.PERMANENT_ARRET)
        is_buffer = (dc_sys_sheet == DCSYS.Sig
                     and get_dc_sys_value(object_value, DCSYS.Sig.Type) == SignalType.HEURTOIR)

        test_names = _get_test_names(object_name, dc_sys_track, dc_sys_dict,
                                     is_home_sig, is_permanently_red_sig, is_buffer, survey_info)
        survey_name = test_names_in_survey(test_names, dc_sys_track, survey_info,
                                           do_smallest_amount_of_patterns=True)
        survey_object_info = survey_info.get(survey_name)

        if survey_object_info is not None:
            list_used_object_names.append(survey_name)

        dc_sys_sheet_name = (get_sheet_name(dc_sys_sheet) + f"__{get_dc_sys_value(object_value, DCSYS.Sig.Type)}"
                             if dc_sys_sheet == DCSYS.Sig
                             else get_sheet_name(dc_sys_sheet))

        res_dict[(object_name, dc_sys_track)] = add_info_to_survey(survey_object_info, dc_sys_sheet_name,
                                                                   dc_sys_track, original_dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_object_names, survey_info))

    return res_dict


def _get_test_names(object_name: str, dc_sys_track: str, dc_sys_dict: dict[str, dict[str, Any]],
                    is_home_sig: bool, is_permanently_red_sig: bool, is_buffer: bool,
                    survey_info: dict[str, dict[str, Union[str, float]]]):
    object_name = clean_object_name(object_name)
    test_names = [object_name]
    # Permanently Red Signals
    if is_permanently_red_sig:
        if object_name.startswith("STOP_SIG_"):
            other_name = "SIG_" + object_name.removeprefix("STOP_SIG_")
            if other_name not in dc_sys_dict:  # if there is not already a signal called that
                test_names.append(other_name)
    # Home Signals
    elif is_home_sig:
        if object_name.startswith("SIG_") and "_" not in object_name.removeprefix("SIG_"):  # only one block
            main_name = object_name.removeprefix("SIG")
            if not any(other_name.endswith(main_name) for other_name in dc_sys_dict.keys() if other_name != object_name):
                # if there is not another signal name ending by that
                test_name = f"{main_name}__{dc_sys_track}".upper()
                matching_survey_names = [survey_name for survey_name in survey_info.keys()
                                         if survey_name.endswith(test_name)]
                if len(matching_survey_names) == 1:
                    other_name = matching_survey_names[0].removesuffix(f"__{dc_sys_track}".upper())
                    test_names.append(other_name)
    # Buffers
    elif is_buffer:
        if object_name.startswith("SIG_BUF_"):
            other_name = "BUF_" + object_name.removeprefix("SIG_BUF_")
            if other_name not in dc_sys_dict:  # if there is not already a signal called that
                test_names.append(other_name)
        elif object_name.startswith("BUF_"):
            other_name = "SIG_BUF_" + object_name.removeprefix("BUF_")
            if other_name not in dc_sys_dict:  # if there is not already a signal called that
                test_names.append(other_name)
    return test_names


def _get_dc_sys_position(dc_sys_sheet, object_value) -> tuple[str, float]:
    if "Voie" in get_class_attributes_dict(dc_sys_sheet):
        track, kp = get_dc_sys_values(object_value, dc_sys_sheet.Voie, dc_sys_sheet.Pk)
    else:
        seg, x = get_dc_sys_values(object_value, dc_sys_sheet.Seg, dc_sys_sheet.X)
        track, kp = from_seg_offset_to_track_kp(seg, x)
    return track, kp
