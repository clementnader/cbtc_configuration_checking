#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ...survey_utils import clean_track_name
from .joint_utils import *
from .common_utils import *


__all__ = ["check_sse"]


# Sous-Section Électrique
def check_sse(dc_sys_sheet, res_sheet_name: str, survey_info: dict[str, dict[str, float]],
              set_of_survey_tracks: set[str]):
    assert dc_sys_sheet == DCSYS.SS
    assert res_sheet_name == "SS"

    sse_limits_dict = _get_sse_limits_dict()
    list_used_object_names = list()
    res_dict = dict()
    for sse_limit, limit_position in sse_limits_dict.items():
        sse1, sse2, sse_limit_track = sse_limit
        original_dc_sys_track, dc_sys_kp = limit_position
        dc_sys_track = clean_track_name(original_dc_sys_track, set_of_survey_tracks)

        end_of_track_suffix = sse_limit_track.removeprefix(original_dc_sys_track)
        # end_of_track_suffix is not null if a single SSE has two end-of-track limits on the same track

        object_name, survey_name = _get_sse_name_in_survey(sse1, sse2, dc_sys_track, survey_info,
                                                           end_of_track_suffix)
        object_name = get_display_name(object_name, sse1, sse2, dc_sys_track, sse_limits_dict)
        survey_object_info = survey_info.get(survey_name)
        if survey_object_info is not None:
            list_used_object_names.append(survey_name)

        res_dict[(object_name, dc_sys_track)] = add_info_to_survey(survey_object_info, get_sheet_name(dc_sys_sheet),
                                                                   dc_sys_track, original_dc_sys_track, dc_sys_kp)

    res_dict.update(add_extra_info_from_survey(list_used_object_names, survey_info))
    return res_dict


def _get_sse_limits_dict() -> dict[tuple[str, Optional[str], str], tuple[str, float]]:
    sse_limits_dict = dict()
    sse_dict = load_sheet(DCSYS.SS)
    for sse_name, sse_value in sse_dict.items():
        matching_sse = find_associated_blocks(sse_name, sse_value, DCSYS.SS,
                                              DCSYS.SS.Extremite.Voie, DCSYS.SS.Extremite.Pk)
        for limit_position, matching_sse_name in matching_sse.items():
            track = limit_position[0]
            sse_limit = (sse_name, matching_sse_name, track)
            sse_limit2 = (matching_sse_name, sse_name, track) if matching_sse_name is not None else None

            if sse_limit not in sse_limits_dict and (sse_limit2 is None or sse_limit2 not in sse_limits_dict):
                sse_limits_dict[sse_limit] = limit_position
                continue

            if sse_limit2 is not None:
                if sse_limit in sse_limits_dict and limit_position != sse_limits_dict[sse_limit]:
                    print_error(f"Found another sse_limit between the same SSEs and on the same track: {sse_limit}\n"
                                f"but at a different position {sse_limits_dict[sse_limit]} vs {limit_position}.")
                if sse_limit2 in sse_limits_dict and limit_position != sse_limits_dict[sse_limit2]:
                    print_error(f"Found another sse_limit between the same SSEs and on the same track: {sse_limit2}\n"
                                f"but at a different position {sse_limits_dict[sse_limit2]} vs {limit_position}.")
            else:
                if sse_limit in sse_limits_dict and limit_position != sse_limits_dict[sse_limit]:
                    # A SSE with two end-of-track limits on the same track
                    sse_limits_dict[(sse_name, matching_sse_name, track + "__1")] = sse_limits_dict[sse_limit]
                    del sse_limits_dict[sse_limit]
                    sse_limits_dict[(sse_name, matching_sse_name, track + "__2")] = limit_position

    return sse_limits_dict


def _get_sse_name_in_survey(sse1: str, sse2: Optional[str], track: str, survey_info: dict[str, Any],
                            end_of_track_suffix: str = "") -> tuple[str, Optional[str]]:

    if sse2 is not None:
        sse_limit_name = f"{sse1}_{sse2}"
        sse_limit_name_2 = f"{sse2}_{sse1}"
    else:
        sse_limit_name = f"{sse1}__end_of_track"
        sse_limit_name_2 = None
    object_name = sse_limit_name + end_of_track_suffix

    if end_of_track_suffix:
        survey_name = None
    else:
        survey_name = _try_to_find_name_in_survey(object_name, [sse_limit_name, sse_limit_name_2],
                                                  track, survey_info)

    return object_name, survey_name


LIST_OBJ_NAME_WITHOUT_ASSOCIATION = list()

def _try_to_find_name_in_survey(object_name: str, test_names: list[str], track: str, survey_info: dict[str, Any]
                                ) -> Union[None, str]:
    global LIST_OBJ_NAME_WITHOUT_ASSOCIATION

    for test_name in test_names:
        if test_name is None:
            continue
        test_name = test_name.upper()
        if f"{test_name}__{track}" in survey_info:
            return f"{test_name}__{track}"

        list_matching_objs = _get_matching_objs_in_survey(test_name, track, survey_info)

        if len(list_matching_objs) == 1:
            return list_matching_objs[0]
        if len(list_matching_objs) > 1:
            if (object_name, track) not in LIST_OBJ_NAME_WITHOUT_ASSOCIATION:
                LIST_OBJ_NAME_WITHOUT_ASSOCIATION.append((object_name, track))
                print_log(f"\nMultiple SSE limits in survey can correspond to {Color.yellow}{object_name}{Color.reset} "
                          f"on {Color.light_yellow}{track}{Color.reset}, unable to associate it:\n{Color.default}"
                          f"{[matching_obj.removesuffix(f'__{track}') for matching_obj in list_matching_objs]}"
                          f"{Color.reset}")
    return None


def _get_matching_objs_in_survey(object_name: str, track: str, survey_info: dict[str, Any]) -> list[str]:
    list_matching_objs = list()
    for survey_name, survey_object_info in survey_info.items():
        # remove the track in the survey_name, tracks are directly tested in this function
        test_name = survey_name.split("__", 1)[0]
        test_name = _clean_survey_sse_limit_name(test_name)
        survey_track = survey_object_info["survey_track"]
        if track == survey_track and object_name == test_name:
            list_matching_objs.append(survey_name)
    return list_matching_objs


def _clean_survey_sse_limit_name(sse_limit_name: str) -> str:
    sse_limit_name = re.sub(r"^(SS[0-9]+)_(SS[0-9]+)_[^_]+$", r"\1_\2", sse_limit_name)
    return sse_limit_name
