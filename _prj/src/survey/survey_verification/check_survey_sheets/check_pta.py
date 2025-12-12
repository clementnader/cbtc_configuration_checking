#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import clean_track_name, clean_object_name
from .common_utils import *


__all__ = ["check_pta"]


# PtA
def check_pta(dc_sys_sheet, res_sheet_name: str, survey_info: dict,
              set_of_survey_tracks: set[str], plaques_survey_info: dict):
    assert dc_sys_sheet == DCSYS.PtA
    assert res_sheet_name == "PtA"

    dc_sys_dict = load_sheet(DCSYS.PtA)
    survey_info.update(plaques_survey_info)
    list_used_object_names = list()
    res_dict = dict()
    for object_name, object_value in dc_sys_dict.items():
        original_dc_sys_track, dc_sys_kp = _get_dc_sys_position(object_value)
        dc_sys_track = clean_track_name(original_dc_sys_track, set_of_survey_tracks)

        test_names = _get_test_names(object_name)
        survey_name = test_names_in_survey(test_names, dc_sys_track, survey_info,
                                           do_smallest_amount_of_patterns=True)
        survey_object_info = survey_info.get(survey_name)

        if survey_object_info is not None:
            list_used_object_names.append(survey_name)

        res_dict[(object_name, dc_sys_track)] = add_info_to_survey(survey_object_info, get_sheet_name(dc_sys_sheet),
                                                                   dc_sys_track, original_dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_object_names, survey_info))
    return res_dict


def _get_dc_sys_position(object_value) -> tuple[str, float]:
    track, kp = get_dc_sys_values(object_value, DCSYS.PtA.Voie, DCSYS.PtA.Pk)
    return track, kp


def _get_test_names(object_name: str) -> list[str]:
    test_name = clean_object_name(object_name)
    test_names = [test_name]
    if re.match(r"^OSP_[A-Z]{4}_", test_name) is not None:
        test_name = re.sub(r"^OSP_[A-Z]{4}_", r"", test_name)
        test_names.append(test_name)
    if test_name.startswith("PAEHQ_"):
        test_names.append(test_name.removeprefix("PAEHQ_"))
    return test_names
