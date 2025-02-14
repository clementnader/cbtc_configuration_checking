#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...database_location import *
from ..survey_types import *
from .track_survey_utils import *


__all__ = ["load_survey"]


def load_survey() -> tuple[dict[str, dict[str, dict[str, Any]]], list[str]]:
    survey_info = dict()
    survey_loc_info = list(get_survey_loc_info())
    display_info_list = _get_survey_files_display_info(survey_loc_info)
    if not display_info_list:
        survey_info = {type_name: dict() for type_name in SURVEY_TYPES_DICT}
        return survey_info, display_info_list
    nb_of_survey = len(display_info_list)
    for i, (survey_addr, survey_sheet, all_sheets, start_row,
            ref_col, type_col, track_col, survey_kp_col) in enumerate(survey_loc_info, start=1):
        missing_types = list()
        if all_sheets:
            print(f"\n {i}/{nb_of_survey} - "
                  f"{Color.white}{Color.underline}Loading {Color.blue}all sheets{Color.white} of "
                  f"survey file{Color.no_underline}{NBSP}\n{' '*len(f' {i}/{nb_of_survey} - ')}"
                  f"{Color.underline}{Color.cyan}{survey_addr}{Color.white}...{Color.reset}{NBSP}")
        else:
            print(f"\n {i}/{nb_of_survey} - "
                  f"{Color.white}{Color.underline}Loading sheet {Color.blue}\"{survey_sheet}\"{Color.white} of "
                  f"survey file{Color.no_underline}{NBSP}\n{' '*len(f' {i}/{nb_of_survey} - ')}"
                  f"{Color.underline}{Color.cyan}{survey_addr}{Color.white}...{Color.reset}{NBSP}")
        wb = load_xl_file(survey_addr)
        if all_sheets:
            sheet_names = get_xl_sheet_names(wb)
        else:
            sheet_names = [survey_sheet]

        for sheet_name in sheet_names:
            survey_ws = get_xl_sheet_by_name(wb, sheet_name)
            survey_info.update(
                get_survey(survey_info, survey_ws, start_row, ref_col, type_col, track_col, survey_kp_col,
                           os.path.split(survey_addr)[-1], missing_types))
        if missing_types:
            print(f"\t> The following type{'s' if len(missing_types) > 1 else ''} in the survey "
                  f"{'are' if len(missing_types) > 1 else 'is'} not loaded: "
                  f"{Color.yellow}{', '.join(missing_types)}{Color.reset}.")
    return survey_info, display_info_list


def _get_survey_files_display_info(survey_loc_info: list[tuple[Union[str, bool], ...]]) -> list[str]:
    def _display_sheet(all_sheets: bool, survey_sheet: str):
        return 'all sheets' if all_sheets else 'sheet "' + survey_sheet + '"'

    display_info_list = [(f"{os.path.split(survey_addr)[-1]} "
                          f"({_display_sheet(all_sheets, survey_sheet)})")
                         for (survey_addr, survey_sheet, all_sheets, start_row,
                              ref_col, type_col, track_col, survey_kp_col) in survey_loc_info]
    return display_info_list


def get_survey_loc_info():
    survey_addr = (DATABASE_LOC.survey_loc.survey_addr if isinstance(DATABASE_LOC.survey_loc.survey_addr, list)
                   else [DATABASE_LOC.survey_loc.survey_addr])
    survey_sheet = (DATABASE_LOC.survey_loc.survey_sheet if isinstance(DATABASE_LOC.survey_loc.survey_sheet, list)
                    else [DATABASE_LOC.survey_loc.survey_sheet])
    all_sheets = (DATABASE_LOC.survey_loc.all_sheets if isinstance(DATABASE_LOC.survey_loc.all_sheets, list)
                  else [DATABASE_LOC.survey_loc.all_sheets])
    start_row = (DATABASE_LOC.survey_loc.start_row if isinstance(DATABASE_LOC.survey_loc.start_row, list)
                 else [DATABASE_LOC.survey_loc.start_row])
    ref_col = (DATABASE_LOC.survey_loc.ref_col if isinstance(DATABASE_LOC.survey_loc.ref_col, list)
               else [DATABASE_LOC.survey_loc.ref_col])
    type_col = (DATABASE_LOC.survey_loc.type_col if isinstance(DATABASE_LOC.survey_loc.type_col, list)
                else [DATABASE_LOC.survey_loc.type_col])
    track_col = (DATABASE_LOC.survey_loc.track_col if isinstance(DATABASE_LOC.survey_loc.track_col, list)
                 else [DATABASE_LOC.survey_loc.track_col])
    survey_kp_col = (DATABASE_LOC.survey_loc.survey_kp_col if isinstance(DATABASE_LOC.survey_loc.survey_kp_col, list)
                     else [DATABASE_LOC.survey_loc.survey_kp_col])
    return zip(survey_addr, survey_sheet, all_sheets, start_row, ref_col, type_col, track_col, survey_kp_col)


def get_survey(loaded_survey: dict[str, dict[str, Any]], survey_ws, start_row,
               ref_col, type_col, track_col, survey_kp_col,
               survey_name: str, missing_types: list[str]) -> dict[str, dict[str, Any]]:
    intermediate_survey_dict = {type_name: dict() for type_name in SURVEY_TYPES_DICT}

    for row in range(start_row, get_xl_number_of_rows(survey_ws) + 1):
        obj_name = get_xl_cell_value(survey_ws, row=row, column=ref_col)
        if not obj_name:
            continue
        key_name = obj_name.upper()
        key_name = key_name.replace("-", "_")
        key_name = "".join(key_name.split())  # remove all spaces

        type_name = get_xl_cell_value(survey_ws, row=row, column=type_col)
        survey_type = _get_survey_type(type_name, missing_types)
        if survey_type is None:
            continue

        original_track = get_xl_cell_value(survey_ws, row=row, column=track_col)
        track = original_track.strip().upper().replace("-", "_")
        track = find_corresponding_dc_sys_track(track)

        surveyed_kp = get_xl_float_value(survey_ws, row=row, column=survey_kp_col)
        if surveyed_kp is None:
            continue
        if not (isinstance(surveyed_kp, float) or isinstance(surveyed_kp, int)):
            print_log(f"Surveyed KP of {type_name} {Color.yellow}{key_name}{Color.reset} in \"{survey_name}\" is not "
                      f"a number: {Color.beige}\"{surveyed_kp}\"{Color.reset} ({type(surveyed_kp)}). "
                      f"Object is considered not surveyed.")
            continue

        surveyed_kp_comment = f"From {survey_name}"
        if f"{key_name}__{track}" in intermediate_survey_dict[survey_type]:  # two values in the same survey file
            old_surveyed_values = intermediate_survey_dict[survey_type][f"{key_name}__{track}"]["list_surveyed_values"]
            surveyed_values = sorted(old_surveyed_values + [surveyed_kp])
            if all(surveyed_kp == old_value for old_value in old_surveyed_values):
                # object appearing multiple times in same survey but with the same surveyed KP value
                comments = (f"Object appearing {len(surveyed_values)} times "
                            f"with the same surveyed KP value ({round(surveyed_kp, 6)}) "
                            f"on track {original_track} in survey: {survey_name}.")
                to_delete = False
            else:
                comments = (f"Object appearing {len(surveyed_values)} times on track {original_track} "
                            f"in same survey: {survey_name}.\n"
                            f"List of surveyed KPs is: {str(surveyed_values).removeprefix('[').removesuffix(']')}.")
                to_delete = True
                for i, i_surveyed_kp in enumerate(surveyed_values, start=1):
                    intermediate_survey_dict[survey_type][f"{key_name}__{i}__{track}"] = {
                        "survey_type": type_name,
                        "obj_name": obj_name, "survey_track": track, "survey_original_track": original_track,
                        "surveyed_kp": i_surveyed_kp, "surveyed_kp_comment": surveyed_kp_comment, "comments": comments,
                        "list_surveyed_values": surveyed_values
                    }
        else:
            comments = None
            to_delete = False
            surveyed_values = [surveyed_kp]
        intermediate_survey_dict[survey_type][f"{key_name}__{track}"] = {
            "survey_type": type_name,
            "obj_name": obj_name, "survey_track": track, "survey_original_track": original_track,
            "surveyed_kp": surveyed_kp, "surveyed_kp_comment": surveyed_kp_comment, "comments": comments,
            "list_surveyed_values": surveyed_values, "to_delete": to_delete
        }

    loaded_survey = _update_survey_dictionary(loaded_survey, intermediate_survey_dict)

    return loaded_survey


def _update_survey_dictionary(loaded_survey: dict[str, dict[str, Any]],
                              intermediate_survey_dict: dict[str, dict[str, Any]]
                              ) -> dict[str, dict[str, Any]]:
    if not loaded_survey:
        loaded_survey = {type_name: dict() for type_name in SURVEY_TYPES_DICT}

    for survey_type, sub_dict in intermediate_survey_dict.items():
        for key_name, intermediate_survey_value in sub_dict.items():
            if intermediate_survey_value.get("to_delete", False):
                continue
            comments = intermediate_survey_value["comments"]
            if key_name in loaded_survey[survey_type]:  # object already surveyed in another survey file
                old_surveyed_kp = loaded_survey[survey_type][key_name]["surveyed_kp"]
                old_comments = loaded_survey[survey_type][key_name]["comments"]
                if old_comments or round(intermediate_survey_value["surveyed_kp"], 9) != round(old_surveyed_kp, 9):
                    # we use round because sometimes when reading from excel we get like 0.999999999981 instead of 1
                    old_surveyed_comment = loaded_survey[survey_type][key_name]["surveyed_kp_comment"]
                    new_comment = (f"Another surveyed KP value exists in survey "
                                   f"{old_surveyed_comment.removeprefix('From ')}: {old_surveyed_kp}.")
                    if comments is not None:
                        comments += "\n\n" + new_comment
                    else:
                        comments = new_comment
            loaded_survey[survey_type][key_name] = {
                "survey_type": intermediate_survey_value["survey_type"],
                "obj_name": intermediate_survey_value["obj_name"],
                "survey_track": intermediate_survey_value["survey_track"],
                "survey_original_track": intermediate_survey_value["survey_original_track"],
                "surveyed_kp": intermediate_survey_value["surveyed_kp"],
                "surveyed_kp_comment": intermediate_survey_value["surveyed_kp_comment"],
                "comments": comments
            }

    return loaded_survey


def _get_survey_type(name: Optional[str], missing_types: list[str]):
    if name is None:
        return None
    test_name = name.strip().upper()
    for type_name, type_info in SURVEY_TYPES_DICT.items():
        if test_name in type_info["survey_type_names"]:
            return type_name
    if name not in missing_types:
        missing_types.append(name)
    return None
