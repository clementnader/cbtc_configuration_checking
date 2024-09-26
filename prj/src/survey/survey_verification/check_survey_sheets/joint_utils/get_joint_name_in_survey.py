#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from .....utils import *
from ..common_utils import *
from .joint_names_utils import *


__all__ = ["get_joint_name_in_survey"]


def get_joint_name_in_survey(tc1: str, tc2: Optional[str], track: str, survey_info:  dict[str, Any],
                             limit_position: tuple[str, float],
                             end_of_track_suffix: str = "", block_def_limit_name: str = None,
                             buffer_survey_info: dict[str, dict[str, float]] = None,
                             other_limit_position: Optional[tuple[str, float]] = None
                             ) -> tuple[str, Optional[str], bool]:

    list_test_names = _get_list_of_joint_test_names_multiple_prefixes(tc1, tc2, limit_position)
    obj_name = list_test_names[0] + end_of_track_suffix

    survey_name = None
    use_buffer = False
    if block_def_limit_name is not None:
        survey_name, use_buffer = _find_survey_name_using_block_def(block_def_limit_name, track, survey_info,
                                                                    buffer_survey_info)

    if survey_name is None:
        if end_of_track_suffix and other_limit_position is not None:
            survey_names = _try_to_find_name_in_survey(obj_name, list_test_names, track, survey_info,
                                                       two_corresponding=True)
            if survey_names is not None:
                survey_name = _get_corresponding_two_limits_in_survey(limit_position, other_limit_position,
                                                                      survey_names, survey_info)
        else:
            survey_name = _try_to_find_name_in_survey(obj_name, list_test_names, track, survey_info)

    return obj_name, survey_name, use_buffer


def _get_corresponding_two_limits_in_survey(limit_position: tuple[str, float], other_limit_position: tuple[str, float],
                                            survey_names: list[str], survey_info:  dict[str, Any]):
    dc_sys_limits = [limit_position, other_limit_position]
    associated_survey_dict = {(lim_track, lim_kp): None for (lim_track, lim_kp)
                              in dc_sys_limits}

    associated_survey_dict = get_corresponding_survey_two_limits_on_track(
        dc_sys_limits, associated_survey_dict, survey_names, survey_info)

    return associated_survey_dict[limit_position]


def _find_survey_name_using_block_def(block_def_limit_name: str, track: str, survey_info:  dict[str, Any],
                                      buffer_survey_info: dict[str, dict[str, float]]
                                      ) -> tuple[Optional[str], bool]:
    if f"{block_def_limit_name.upper()}__{track}" in survey_info:
        return f"{block_def_limit_name.upper()}__{track}", False

    elif f"{block_def_limit_name.upper()}__{track}" in buffer_survey_info:
        return f"{block_def_limit_name.upper()}__{track}", True

    return None, False


def _try_to_find_name_in_survey(obj_name: str, list_test_names: list[str], track: str, survey_info: dict[str, Any],
                                two_corresponding: bool = False,
                                second_try: bool = False, third_try: bool = False, fourth_try: bool = False
                                ) -> Union[None, str, list[str]]:
    for test_name in list_test_names:
        test_name = test_name.upper()
        if second_try:
            test_name = _remove_leading_zeros_and_trailing_letters(test_name)
        elif third_try:
            test_name = _remove_specific_patterns(test_name)
        elif fourth_try:
            test_name = _remove_trigrams(test_name)
        exist_flag, survey_name = _is_name_in_survey(obj_name, test_name, track, survey_info,
                                                     remove_trigrams=fourth_try,
                                                     two_corresponding=two_corresponding)
        if exist_flag:
            return survey_name

    if fourth_try:
        return None

    if third_try:
        survey_name = _try_to_find_name_in_survey(obj_name, list_test_names, track, survey_info,
                                                  two_corresponding=two_corresponding, fourth_try=True)
        if survey_name is not None:
            return survey_name
        return None

    if second_try:
        survey_name = _try_to_find_name_in_survey(obj_name, list_test_names, track, survey_info,
                                                  two_corresponding=two_corresponding, third_try=True)
        if survey_name is not None:
            return survey_name
        return None

    survey_name = _try_to_find_name_in_survey(obj_name, list_test_names, track, survey_info,
                                                  two_corresponding=two_corresponding, second_try=True)
    if survey_name is not None:
        return survey_name

    return None


def _get_list_of_joint_test_names_multiple_prefixes(tc1: str, tc2: Optional[str], limit_position: tuple[str, float]
                                                    ) -> list[str]:
    list_test_names = get_joint_possible_names(tc1, tc2, limit_position)
    # In some surveys, joint prefix is "JOINT_" instead of "JOI_"
    other_prefix_list = ["JOINT_" + name.removeprefix("JOI_") for name in list_test_names if name is not None]
    # In some surveys, joint prefix is "TC_JOINT_" instead of "JOI_"
    other_prefix_list_2 = ["TC_JOINT_" + name.removeprefix("JOI_") for name in list_test_names if name is not None]
    # In some surveys, joint prefix is "AXC_" instead of "JOI_"
    other_prefix_list_3 = ["AXC_" + name.removeprefix("JOI_") for name in list_test_names if name is not None]
    return list_test_names + other_prefix_list + other_prefix_list_2 + other_prefix_list_3


def _remove_leading_zeros_and_trailing_letters(test_name: str) -> Optional[str]:
    res_name = "_".join(word.removeprefix("0") for word in test_name.split("_"))
    res_name = re.sub(r"(_[0-9]+)([A-Z]+)(_)", r"\1\3", res_name)
    res_name = re.sub(r"(_[0-9]+)([A-Z]+)($)", r"\1\3", res_name)

    if res_name == test_name:  # work already done with this name with no success
        return None
    return res_name


def _remove_specific_patterns(test_name: str) -> Optional[str]:
    end_of_track = "__END_OF_TRACK" in test_name
    suffix = ""
    if end_of_track:
        test_name, suffix = test_name.split("__END_OF_TRACK", 1)

    res_name = re.sub(r"_[A-Z]{3}_", r"_", test_name)
    res_name = re.sub(r"PL[0-9]+_", r"", res_name)

    if end_of_track:
        res_name += "__END_OF_TRACK" + suffix

    if res_name == test_name:  # work already done with this name with no success
        return None
    return res_name


def _remove_trigrams(test_name: str) -> Optional[str]:
    end_of_track = "__END_OF_TRACK" in test_name
    suffix = ""
    if end_of_track:
        test_name, suffix = test_name.split("__END_OF_TRACK", 1)

    for _ in range(2):
        test_name = re.sub(r"_[A-Z]{3}_", r"_", test_name)
        test_name = re.sub(r"_[A-Z]{2}[0-9]{0,2}_", r"_", test_name)
        test_name = re.sub(r"_S[0-9]{2}_", r"_", test_name)

    if end_of_track:
        test_name += "__END_OF_TRACK" + suffix
    return test_name


LIST_OBJ_NAME_WITHOUT_ASSOCIATION = list()


def _is_name_in_survey(obj_name: str, test_name: Optional[str], track, survey_info: dict[str, Any],
                       remove_trigrams: bool, two_corresponding: bool = False
                       ) -> tuple[bool, Union[Optional[str], Optional[list[str]]]]:
    global LIST_OBJ_NAME_WITHOUT_ASSOCIATION

    if test_name is None:
        return False, None

    # Trivial case, the name in survey matches directly
    if not two_corresponding and f"{test_name}__{track}" in survey_info:
        return True, f"{test_name}__{track}"

    # We take the names in survey starting with the obj_name, and if it is only one in this case, we take it

    # Limit between two blocks
    if not test_name.endswith("__END_OF_TRACK"):
        list_matching_objs = _get_matching_objs_in_survey(test_name, track, survey_info, single=False,
                                                          remove_trigrams=remove_trigrams)

    # Limit at end of track
    else:
        clean_name = test_name.removesuffix("__END_OF_TRACK")
        list_matching_objs = _get_matching_objs_in_survey(clean_name, track, survey_info, single=True,
                                                          remove_trigrams=remove_trigrams)

    if two_corresponding and test_name.endswith("__END_OF_TRACK"):
        if len(list_matching_objs) == 2:
            return True, list_matching_objs
        else:
            return False, None

    if len(list_matching_objs) == 1:
        return True, list_matching_objs[0]
    if len(list_matching_objs) > 1:
        if (obj_name, track) not in LIST_OBJ_NAME_WITHOUT_ASSOCIATION:
            LIST_OBJ_NAME_WITHOUT_ASSOCIATION.append((obj_name, track))
            print_log(f"\nMultiple joints in survey can correspond to {Color.yellow}{obj_name}{Color.reset} on "
                      f"{Color.light_yellow}{track}{Color.reset}, unable to associate it:\n{Color.default}"
                      f"{[matching_obj.removesuffix(f'__{track}') for matching_obj in list_matching_objs]}"
                      f"{Color.reset}")
    return False, None


def _get_matching_objs_in_survey(obj_name: str, track: str, survey_info: dict[str, Any],
                                 single: bool, remove_trigrams: bool) -> list[str]:
    list_matching_objs = list()
    for survey_name, survey_obj_info in survey_info.items():
        # remove the track in the survey_name, tracks are directly tested in this function
        test_name = survey_name.split("__", 1)[0]
        survey_track = survey_obj_info["survey_track"]
        if track == survey_track and _survey_name_matching(test_name, obj_name, single, remove_trigrams):
            list_matching_objs.append(survey_name)
    return list_matching_objs


def _survey_name_matching(survey_name: str, obj_name: str, single: bool, remove_trigrams: bool) -> bool:
    if remove_trigrams:
        survey_name = _remove_trigrams(survey_name)

    survey_name = re.sub(r"_START_", r"_", survey_name)
    survey_name = re.sub(r"_END_", r"_", survey_name)
    survey_name = re.sub(r"_BUFFER_", r"_", survey_name)
    survey_name = re.sub(r"_L_", r"_", survey_name)
    survey_name = re.sub(r"_R_", r"_", survey_name)

    if not survey_name.startswith(obj_name):
        return False
    suffix = survey_name.removeprefix(obj_name)

    # Removing switches in name
    suffix = re.sub(r"_SW[DP]?[A-Z0-9]+_[0-9]+", r"", suffix)  # some switches are named SWP or SW or SWD
    suffix = re.sub(r"_SW[DP]?[A-Z0-9]+", r"", suffix)  # some switches are named SWP or SW or SWD
    suffix = re.sub(r"_[0-9]+AW[0-9]+", r"", suffix)  # some switches are named with AW
    suffix = re.sub(r"_W[0-9]*A*[0-9]+", r"", suffix)  # some switches are named WXXXX or WXAXXX

    if not single:  # Limit between two blocks
        suffix = re.sub(r"_[A-Z0-9]+", r"", suffix)  # suffix when multiple joints with same name
        if not suffix:
            return True
        return False

    else:  # Limit at end of track
        suffix = re.sub(r"_[0-9]{1,2}", r"", suffix)  # suffix when multiple joints with same name
        suffix = re.sub(r"_F[1-9]", r"", suffix)  # end of track suffix
        suffix = re.sub(r"_T[0-9]+", r"", suffix)  # end of track suffix
        suffix = re.sub(r"_[FM]BS[0-9]+", r"", suffix)  # end of track suffix
        suffix = re.sub(r"_LCP[0-9]+", r"", suffix)  # end of track suffix
        suffix = suffix.removesuffix("_DIRECT").removesuffix("_DIVERT")
        suffix = suffix.removesuffix("_LEFT").removesuffix("_RIGHT")
        suffix = suffix.removesuffix("_START").removesuffix("_END").removesuffix("_BUFFER")
        if not suffix:
            return True
        return False
