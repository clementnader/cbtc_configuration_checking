#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ....utils import *
from ...survey_utils import *


__all__ = ["add_info_to_survey", "add_extra_info_from_survey", "test_names_in_survey",
           "get_corresponding_survey_one_limit_on_track", "get_corresponding_survey_two_limits_on_track",
           "get_smallest_unique_prefix_dict"]


def add_info_to_survey(survey_obj_info: Optional[dict[str, Any]],
                       dc_sys_sheet: str, dc_sys_track: str, dc_sys_original_track: str, dc_sys_kp: float,
                       extra_comment: str = None):
    survey_name = survey_obj_info["obj_name"] if survey_obj_info is not None else None
    survey_type = survey_obj_info["survey_type"] if survey_obj_info is not None else None
    survey_track = survey_obj_info["survey_track"] if survey_obj_info is not None else None
    survey_original_track = survey_obj_info["survey_original_track"] if survey_obj_info is not None else None
    surveyed_kp = survey_obj_info["surveyed_kp"] if survey_obj_info is not None else None
    surveyed_kp_comment = survey_obj_info["surveyed_kp_comment"] if survey_obj_info is not None else None
    comments = survey_obj_info["comments"] if survey_obj_info is not None else None
    if extra_comment is not None:
        if comments is None:
            comments = extra_comment
        else:
            comments += "\n\n" + extra_comment

    return {"dc_sys_sheet": dc_sys_sheet, "dc_sys_track": dc_sys_track,
            "dc_sys_original_track": dc_sys_original_track, "dc_sys_kp": dc_sys_kp,
            "survey_name": survey_name, "survey_type": survey_type,
            "survey_track": survey_track, "survey_original_track": survey_original_track,
            "surveyed_kp": surveyed_kp,
            "surveyed_kp_comment": surveyed_kp_comment, "comments": comments}


def add_extra_info_from_survey(used_objects_from_survey: list[str], survey_info: dict[str, dict[str, Any]]):
    extra_dict = dict()
    for obj_name, obj_val in survey_info.items():
        if obj_name in used_objects_from_survey:
            continue
        extra_dict[(obj_name, obj_val["survey_track"])] = \
            {"dc_sys_sheet": None, "dc_sys_track": None, "dc_sys_original_track": None, "dc_sys_kp": None,
             "survey_name": obj_val["obj_name"], "survey_type": obj_val["survey_type"],
             "survey_track": obj_val["survey_track"], "survey_original_track": obj_val["survey_original_track"],
             "surveyed_kp": obj_val["surveyed_kp"],
             "surveyed_kp_comment": obj_val["surveyed_kp_comment"], "comments": obj_val["comments"]}
    return extra_dict


def test_names_in_survey(test_names: list[str], track: str, survey_info: dict[str, Any],
                         do_print: bool = True,
                         do_smallest_amount_of_patterns: bool = False) -> str:
    # Remove duplicates in the test list
    test_names = _get_unique_list(test_names)
    # Get only survey names on the corresponding track
    survey_test_list = [(survey_name.upper().removesuffix(f"__{track}".upper()), survey_name)
                        for survey_name in survey_info
                        if survey_name.upper().endswith(f"__{track}".upper())]

    for test_name in test_names:
        test_name_in_survey = _test_name_in_survey(test_name, track, survey_info, survey_test_list, do_print)
        if test_name_in_survey is not None:
            return test_name_in_survey
    # Try removing leading zeros
    for test_name in test_names:
        test_name_in_survey = _test_name_in_survey(test_name, track, survey_info, survey_test_list, do_print,
                                                   remove_leading_zeros=True)
        if test_name_in_survey is not None:
            return test_name_in_survey
    # Try removing underscores
    for test_name in test_names:
        test_name_in_survey = _test_name_in_survey(test_name, track, survey_info, survey_test_list, do_print,
                                                   add_underscores=True)
        if test_name_in_survey is not None:
            return test_name_in_survey
    # Try removing duplicate patterns
    for test_name in test_names:
        test_name_in_survey = _test_name_in_survey(test_name, track, survey_info, survey_test_list, do_print,
                                                   test_unique_patterns=True)
        if test_name_in_survey is not None:
            return test_name_in_survey
    # Try with the smallest amount of patterns
    if do_smallest_amount_of_patterns:
        for test_name in test_names:
            test_name_in_survey = _test_name_in_survey(test_name, track, survey_info, survey_test_list, do_print,
                                                       test_smallest_patterns=True)
            if test_name_in_survey is not None:
                return test_name_in_survey

    return f"{test_names[0]}__{track}".upper()  # default


def _get_unique_list(i_list: list[Optional[str]]):
    new_list = list()
    for x in i_list:
        if x is not None and x not in new_list:
            new_list.append(x.upper())
    return new_list


def _test_name_in_survey(original_test_name: str, track: str, survey_info: dict[str, dict[str, Union[str, float]]],
                         survey_test_list: list[tuple[str, str]],
                         do_print: bool,
                         remove_leading_zeros: bool = False,
                         add_underscores: bool = False,
                         test_unique_patterns: bool = False,
                         test_smallest_patterns: bool = False):
    if remove_leading_zeros:
        # apply the same transformation to the name from DC_SYS and the ones from the survey
        test_name = _remove_leading_zeros(original_test_name)
        survey_test_list = [(_remove_leading_zeros(survey_test_name), survey_name)
                            for survey_test_name, survey_name in survey_test_list]

    elif add_underscores:  # apply first the removal of leading zeros, then remove underscores
        test_name = _add_underscores(original_test_name)
        survey_test_list = [(_add_underscores(survey_test_name), survey_name)
                            for survey_test_name, survey_name in survey_test_list]

    elif test_unique_patterns or test_smallest_patterns:
        test_name = _get_unique_patterns(original_test_name)
        survey_test_list = [(_get_unique_patterns(survey_test_name), survey_name)
                            for survey_test_name, survey_name in survey_test_list]

    else:  # default
        test_name = original_test_name

    if test_smallest_patterns:
        corresponding_survey_name_list = _test_smallest_patterns(test_name, survey_test_list)
    else:
        corresponding_survey_name_list = [survey_name for survey_test_name, survey_name in survey_test_list
                                          if test_name == survey_test_name]
    if len(corresponding_survey_name_list) == 1:
        return corresponding_survey_name_list[0]
    if len(corresponding_survey_name_list) > 1 and do_print:
        print_log(f"Multiple objects in survey can correspond to {Color.yellow}{original_test_name}{Color.reset} on "
                  f"{Color.light_yellow}{track}{Color.reset}, unable to associate it:\n{Color.default}"
                  f"{[survey_info[matching_obj]['obj_name'] for matching_obj in corresponding_survey_name_list]}"
                  f"{Color.reset}")
    return None


def _remove_leading_zeros(name: str) -> str:
    name = "_".join(re.sub(r"^0*", r"", x) for x in name.split("_"))
    return name


def _add_underscores(name: str) -> str:
    name = re.sub(r"([A-Z])([0-9])", r"\1_\2", name)
    return _remove_leading_zeros(name)


def _get_unique_patterns(name: str) -> str:
    list_patterns = list()
    for pattern in name.split("_"):
        if pattern not in list_patterns or any(element.isnumeric() for element in pattern):
            list_patterns.append(pattern)
    name = "_".join(pattern for pattern in sorted(list_patterns))
    return name


def _test_smallest_patterns(test_name: str, survey_test_list: list[tuple[str, str]]) -> list[str]:
    test_name_patterns = test_name.split("_")
    list_survey_patterns = [(survey_test_name.split("_"), survey_name)
                            for survey_test_name, survey_name in survey_test_list]
    corresponding_survey_name_list = [survey_name for survey_test_patterns, survey_name in list_survey_patterns
                                      if _test_all_patterns_are_present(test_name_patterns, survey_test_patterns)]
    return corresponding_survey_name_list


def _test_all_patterns_are_present(test_name_patterns: list[str], survey_test_patterns: list[str]) -> bool:
    remaining_test_name_patterns = survey_test_patterns[:]
    for pattern in test_name_patterns:
        if pattern not in remaining_test_name_patterns:
            return False
        remaining_test_name_patterns.remove(pattern)
    return True


def get_corresponding_survey_one_limit_on_track(dc_sys_limits_on_track: list[tuple[str, float]],
                                                associated_survey_dict: dict[tuple[str, float], Optional[str]],
                                                survey_limits_on_track: list[str],
                                                survey_info: dict[str, Any]
                                                ) -> dict[tuple[str, float], Optional[str]]:
    for (lim_track, lim_kp) in dc_sys_limits_on_track:
        if not survey_limits_on_track:  # extremity not surveyed
            associated_survey_dict[(lim_track, lim_kp)] = None
        elif len(survey_limits_on_track) == 1:  # only 1 extremity corresponding,
            # we do the survey comparison with this one
            survey_name = survey_limits_on_track[0]
            associated_survey_dict[(lim_track, lim_kp)] = survey_name
        else:  # multiple extremities corresponding,
            # find for which survey limit the difference is the smallest
            test_differences = list()
            for survey_name in survey_limits_on_track:
                surveyed_kp = survey_info[survey_name]["surveyed_kp"]
                reversed_polarity = check_polarity(lim_kp, surveyed_kp)
                if reversed_polarity:
                    diff = abs(abs(lim_kp) - abs(surveyed_kp))
                else:
                    diff = abs(lim_kp - surveyed_kp)
                test_differences.append((diff, survey_name))
            closest_survey_name = sorted(test_differences, key=lambda x: x[0])[0][1]
            associated_survey_dict[(lim_track, lim_kp)] = closest_survey_name
    return associated_survey_dict


def get_corresponding_survey_two_limits_on_track(dc_sys_limits_on_track: list[tuple[str, float]],
                                                 survey_name_dict: dict[tuple[str, float], Optional[str]],
                                                 survey_limits_on_track: list[str],
                                                 survey_info: dict[str, Any]
                                                 ) -> dict[tuple[str, float], Optional[str]]:
    if not survey_limits_on_track:  # extremities not surveyed
        pass
    elif len(survey_limits_on_track) == 1:  # only 1 extremity corresponding,
        # find for which DC_SYS limit the difference is the smallest
        survey_name = survey_limits_on_track[0]
        surveyed_kp = survey_info[survey_name]["surveyed_kp"]
        test_differences = list()
        for (lim_track, lim_kp) in dc_sys_limits_on_track:
            reversed_polarity = check_polarity(lim_kp, surveyed_kp)
            if reversed_polarity:
                diff = abs(abs(lim_kp) - abs(surveyed_kp))
            else:
                diff = abs(lim_kp - surveyed_kp)
            test_differences.append((diff, (lim_track, lim_kp)))
        closest_dc_sys_limit = sorted(test_differences, key=lambda x: x[0])[0][1]
        survey_name_dict[closest_dc_sys_limit] = survey_name
    else:  # multiple extremities corresponding,
        # find for which DC_SYS limits combination the difference is the smallest
        (lim1_track, lim1_kp) = dc_sys_limits_on_track[0]
        (lim2_track, lim2_kp) = dc_sys_limits_on_track[1]
        test_differences = list()
        for survey_name_corresponding_to_1 in survey_limits_on_track:
            surveyed_kp_1 = survey_info[survey_name_corresponding_to_1]["surveyed_kp"]
            for survey_name_corresponding_to_2 in [survey_name for survey_name in survey_limits_on_track
                                                   if survey_name != survey_name_corresponding_to_1]:
                surveyed_kp_2 = survey_info[survey_name_corresponding_to_2]["surveyed_kp"]
                reversed_polarity = (check_polarity(lim1_kp, surveyed_kp_1) and check_polarity(lim2_kp, surveyed_kp_2))
                if not reversed_polarity:
                    # First, test if there is an association where in each pair both values are close,
                    # and try to minimize the sum of differences.
                    diff1 = abs(lim1_kp - surveyed_kp_1)
                    diff2 = abs(lim2_kp - surveyed_kp_2)
                    # If the sums of the differences are equal, it means that the survey KPs are both larger
                    # or both smaller than both DC_SYS KPs.
                    # In that case, associate the smallest KP with the smallest and the largest with the largest.
                    # We want a False (0) when they are aligned and a True (1) if not, to work in the sort.
                    second_test = not ((lim1_kp <= lim2_kp) == (surveyed_kp_1 <= surveyed_kp_2))
                else:  # In reverse polarity, we simply work with the absolute values of the KP.
                    diff1 = abs(abs(lim1_kp) - abs(surveyed_kp_1))
                    diff2 = abs(abs(lim2_kp) - abs(surveyed_kp_2))
                    second_test = not ((abs(lim1_kp) <= abs(lim2_kp)) == (abs(surveyed_kp_1) <= abs(surveyed_kp_2)))
                test_differences.append(((diff1 + diff2, second_test),
                                         {(lim1_track, lim1_kp): survey_name_corresponding_to_1,
                                          (lim2_track, lim2_kp): survey_name_corresponding_to_2}))
        closest_combination = sorted(test_differences, key=lambda x: x[0])[0][1]
        survey_name_dict.update(closest_combination)
    return survey_name_dict


def get_smallest_unique_prefix_dict(input_dict: dict[str, str]) -> dict[str, str]:
    res_dict = dict()
    list_of_splits = [value.split("_") for value in input_dict.values()]

    for key, split in zip(input_dict, list_of_splits):
        other_splits = [other_split for other_split in list_of_splits if other_split != split]
        level = 1
        prefix = "_".join(split[:level])

        while level < len(split):
            other_prefixes = ["_".join(other_split[:level]) for other_split in other_splits]
            if prefix not in other_prefixes:  # unique prefix
                break
            level += 1
            prefix = "_".join(split[:level])

        res_dict[key] = prefix
    return res_dict
