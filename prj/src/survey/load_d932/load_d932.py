#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...database_location import *
from ..d932_utils import *
from .load_xl import *


__all__ = ["load_survey"]


LOADED_SURVEY = dict()


def load_survey() -> dict:
    global LOADED_SURVEY
    if not LOADED_SURVEY:
        for survey_addr, survey_sheet, start_line, ref_col, type_col, track_col, design_kp_col, survey_kp_col in \
                get_d932_loc_info():
            print(f"Loading sheet \"{survey_sheet}\" of survey {Color.blue}{survey_addr}{Color.reset}.\n")
            wb = load_survey_wb(survey_addr)
            d932_sh = get_xl_sheet_by_name(wb, survey_sheet)
            LOADED_SURVEY.update(get_survey(LOADED_SURVEY, d932_sh,
                                            start_line, ref_col, type_col, track_col, design_kp_col, survey_kp_col,
                                            os.path.split(survey_addr)[-1]))
    return LOADED_SURVEY


def get_d932_loc_info():
    survey_addr = DATABASE_LOC.survey_loc.survey_addr if isinstance(DATABASE_LOC.survey_loc.survey_addr, list) \
        else [DATABASE_LOC.survey_loc.survey_addr]
    survey_sheet = DATABASE_LOC.survey_loc.survey_sheet if isinstance(DATABASE_LOC.survey_loc.survey_sheet, list) \
        else [DATABASE_LOC.survey_loc.survey_sheet]
    start_line = DATABASE_LOC.survey_loc.start_line if isinstance(DATABASE_LOC.survey_loc.start_line, list) \
        else [DATABASE_LOC.survey_loc.start_line]
    ref_col = DATABASE_LOC.survey_loc.ref_col if isinstance(DATABASE_LOC.survey_loc.ref_col, list) \
        else [DATABASE_LOC.survey_loc.ref_col]
    type_col = DATABASE_LOC.survey_loc.type_col if isinstance(DATABASE_LOC.survey_loc.type_col, list) \
        else [DATABASE_LOC.survey_loc.type_col]
    track_col = DATABASE_LOC.survey_loc.track_col if isinstance(DATABASE_LOC.survey_loc.track_col, list) \
        else [DATABASE_LOC.survey_loc.track_col]
    design_kp_col = DATABASE_LOC.survey_loc.design_kp_col if isinstance(DATABASE_LOC.survey_loc.design_kp_col, list) \
        else [DATABASE_LOC.survey_loc.design_kp_col]
    survey_kp_col = DATABASE_LOC.survey_loc.survey_kp_col if isinstance(DATABASE_LOC.survey_loc.survey_kp_col, list) \
        else [DATABASE_LOC.survey_loc.survey_kp_col]
    return zip(survey_addr, survey_sheet, start_line, ref_col, type_col, track_col, design_kp_col, survey_kp_col)


def get_survey(loaded_survey, d932_sh, start_line, ref_col, type_col, track_col, design_kp_col, survey_kp_col,
               survey_name: str) -> dict:
    if not loaded_survey:
        loaded_survey = {type_name: dict() for type_name in SURVEY_TYPES_DICT}

    for line in range(start_line, get_xl_sh_nb_rows(d932_sh) + 1):
        obj_name = get_xl_cell_value(d932_sh, line=line, col=ref_col)
        if not obj_name:
            continue

        obj_comment = f"From {survey_name}"
        type_name = get_xl_cell_value(d932_sh, line=line, col=type_col)
        survey_type = _get_survey_type(type_name)
        if survey_type is None:
            continue

        track = get_xl_cell_value(d932_sh, line=line, col=track_col)
        track_comment = f"From {survey_name}" if track is not None else None
        design_kp = get_xl_float_value(d932_sh, line=line, col=design_kp_col) if design_kp_col is not None else None
        design_kp_comment = f"From {survey_name}" if design_kp is not None else None
        surveyed_kp = get_xl_float_value(d932_sh, line=line, col=survey_kp_col)
        surveyed_kp_comment = f"From {survey_name}" if surveyed_kp is not None else None
        if obj_name in loaded_survey[survey_type]:
            old_surveyed_kp = loaded_survey[survey_type][obj_name]["surveyed_kp"]
            if old_surveyed_kp is not None and surveyed_kp is not None and surveyed_kp != old_surveyed_kp:
                print_warning(f"There are two different surveyed KP for object {Color.blue}{obj_name}{Color.reset}: "
                              f"{Color.beige}{old_surveyed_kp = }{Color.reset} "
                              f"and {Color.beige}{surveyed_kp = }{Color.reset}.\n"
                              f"The new value {Color.beige}{surveyed_kp = }{Color.reset} from {survey_name} is taken.")
            if track is not None:
                loaded_survey[survey_type][obj_name]["track"] = track
                loaded_survey[survey_type][obj_name]["track_comment"] = track_comment
            if design_kp is not None:
                loaded_survey[survey_type][obj_name]["design_kp"] = design_kp
                loaded_survey[survey_type][obj_name]["design_kp_comment"] = design_kp_comment
            if surveyed_kp is not None:
                loaded_survey[survey_type][obj_name]["surveyed_kp"] = surveyed_kp
                loaded_survey[survey_type][obj_name]["surveyed_kp_comment"] = surveyed_kp_comment
        else:
            loaded_survey[survey_type][obj_name] = {"track": track, "surveyed_kp": surveyed_kp, "design_kp": design_kp}
            loaded_survey[survey_type][obj_name].update({"obj_comment": obj_comment,
                                                         "track_comment": track_comment,
                                                         "surveyed_kp_comment": surveyed_kp_comment,
                                                         "design_kp_comment": design_kp_comment})

    return loaded_survey


def _get_survey_type(name):
    name = name.upper()
    for type_name, type_info in SURVEY_TYPES_DICT.items():
        if name == type_name:
            return type_name
        if name in type_info["other_names"]:
            return type_name
    return None
