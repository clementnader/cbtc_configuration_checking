#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...database_location import *


__all__ = ["update_database_loc"]


def update_database_loc(dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                        survey_loc_dict: dict[str, dict[str, tkinter.StringVar]]):

    DATABASE_LOC.dc_sys_addr = os.path.join(dc_sys_directory.get(), dc_sys_file_name.get()).replace("/", os.path.sep)

    DATABASE_LOC.survey_loc.survey_addr = list()
    DATABASE_LOC.survey_loc.survey_sheet = list()
    DATABASE_LOC.survey_loc.all_sheets = list()
    DATABASE_LOC.survey_loc.start_row = list()
    DATABASE_LOC.survey_loc.ref_col = list()
    DATABASE_LOC.survey_loc.type_col = list()
    DATABASE_LOC.survey_loc.track_col = list()
    DATABASE_LOC.survey_loc.survey_kp_col = list()

    for survey_name, survey_info in survey_loc_dict.items():
        DATABASE_LOC.survey_loc.survey_addr.append(os.path.join(survey_info["survey_directory"].get(),
                                                   survey_info["survey_file_name"].get()).replace("/", os.path.sep))
        DATABASE_LOC.survey_loc.survey_sheet.append(survey_info["survey_sheet"].get())
        DATABASE_LOC.survey_loc.all_sheets.append(survey_info["all_sheets"].get())
        DATABASE_LOC.survey_loc.start_row.append(int(survey_info["start_row"].get()))
        DATABASE_LOC.survey_loc.ref_col.append(get_col(survey_info["ref_col"].get()))
        DATABASE_LOC.survey_loc.type_col.append(get_col(survey_info["type_col"].get()))
        DATABASE_LOC.survey_loc.track_col.append(get_col(survey_info["track_col"].get()))
        DATABASE_LOC.survey_loc.survey_kp_col.append(get_col(survey_info["survey_kp_col"].get()))


def get_col(val: str):
    try:
        val = int(val)
    except ValueError:
        val = get_xl_column_number(val)
    return val
