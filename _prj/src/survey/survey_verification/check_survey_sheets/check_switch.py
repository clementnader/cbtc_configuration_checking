#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys_sheet_utils.switch_utils import get_dc_sys_switch_points_dict
from ...survey_utils import clean_track_name
from .common_utils import *


__all__ = ["check_switch"]


# Switch
def check_switch(dc_sys_sheet, res_sheet_name: str, survey_info: dict,
                 set_of_survey_tracks: set[str]):
    assert dc_sys_sheet == DCSYS.Aig
    assert res_sheet_name == "Switch"

    dc_sys_dict = get_dc_sys_switch_points_dict()
    list_used_obj_names = list()
    res_dict = dict()
    for obj_name, obj_val in dc_sys_dict.items():
        original_dc_sys_track, dc_sys_kp = obj_val["track"], obj_val["kp"]
        dc_sys_track = clean_track_name(original_dc_sys_track, set_of_survey_tracks)

        test_names, sw_type = _get_test_names(obj_name)

        survey_name = test_names_in_survey(test_names, dc_sys_track, survey_info,
                                           do_smallest_amount_of_patterns=(sw_type != "center"))
        survey_obj_info = survey_info.get(survey_name)
        if survey_obj_info is not None:
            list_used_obj_names.append(survey_name)

        if sw_type == "center":
            survey_obj_info, extra_comment = _switch_center_point_to_heel(obj_name, survey_obj_info, survey_info,
                                                                          sw_type, dc_sys_track)
        else:
            survey_obj_info, extra_comment = _switch_heel_point_to_center(obj_name, survey_obj_info, survey_info,
                                                                          sw_type, dc_sys_track)

        res_dict[(obj_name, dc_sys_track)] = add_info_to_survey(survey_obj_info, get_sh_name(dc_sys_sheet),
                                                                dc_sys_track, original_dc_sys_track, dc_sys_kp,
                                                                extra_comment)

    res_dict.update(add_extra_info_from_survey(list_used_obj_names, survey_info))
    return res_dict


def _get_test_names(obj_name: str) -> tuple[list[str], str]:
    test_names = [obj_name]
    if obj_name.endswith("_L"):
        # The left heel name in the survey uses sometimes the French "gauche" instead of left heel
        test_names.append(obj_name.removesuffix("_L") + "_G")
        sw_type = "left"
    elif obj_name.endswith("_R"):
        # The right heel name in the survey uses sometimes the French "droite" instead of right
        test_names.append(obj_name.removesuffix("_R") + "_D")
        sw_type = "right"
    else:
        # The center point name in the survey is sometimes the switch name only
        test_names.append(obj_name.removesuffix("_C"))
        sw_type = "center"
    return test_names, sw_type


def _switch_center_point_to_heel(obj_name: str, survey_obj_info: dict[str, Union[str, float]],
                                 survey_info: dict[str, dict[str, Union[str, float]]],
                                 sw_type: str, dc_sys_track: str):
    assert sw_type == "center"
    if survey_obj_info is not None:  # already associated info in survey
        return survey_obj_info, None

    # Try to associate center point to one of its heel if it's on the same track
    left_test_names, _ = _get_test_names(obj_name.removesuffix("_C") + "_L")
    left_survey_name = test_names_in_survey(left_test_names, dc_sys_track, survey_info, do_print=False,
                                            do_smallest_amount_of_patterns=True)
    left_survey_obj_info = survey_info.get(left_survey_name)

    right_test_names, _ = _get_test_names(obj_name.removesuffix("_C") + "_R")
    right_survey_name = test_names_in_survey(right_test_names, dc_sys_track, survey_info, do_print=False,
                                             do_smallest_amount_of_patterns=True)
    right_survey_obj_info = survey_info.get(right_survey_name)

    if left_survey_obj_info is None and right_survey_obj_info is None:
        return None, None
    if left_survey_obj_info is not None and right_survey_obj_info is not None:
        return None, None  # fail-safe, should not be possible to have both heels on the same track

    if left_survey_obj_info is not None:
        survey_obj_info = left_survey_obj_info
        corresponding_sw_pos = "left"
    else:
        survey_obj_info = right_survey_obj_info
        corresponding_sw_pos = "right"

    extra_comment = (f"Center Switch Point does not exist on track {dc_sys_track} in survey, "
                     f"{corresponding_sw_pos.capitalize()} Switch Point is used "
                     f"as they are on the same track.")
    return survey_obj_info, extra_comment


def _switch_heel_point_to_center(obj_name: str, survey_obj_info: dict[str, Union[str, float]],
                                 survey_info: dict[str, dict[str, Union[str, float]]],
                                 sw_type: str, dc_sys_track: str):
    assert sw_type in ["left", "right"]
    if survey_obj_info is not None:  # already associated info in survey
        return survey_obj_info, None

    # Try to associate heel point to center point if it's on the same track
    test_names, _ = _get_test_names(obj_name.removesuffix("_L").removesuffix("_R") + "_C")
    survey_name = test_names_in_survey(test_names, dc_sys_track, survey_info)
    survey_obj_info = survey_info.get(survey_name)

    if survey_obj_info is None:
        return None, None

    extra_comment = (f"{sw_type.capitalize()} Switch Point does not exist on track {dc_sys_track} in survey, "
                     f"Center Switch Point is used as they are on the same track.")
    return survey_obj_info, extra_comment
