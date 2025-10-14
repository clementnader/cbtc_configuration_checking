#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...database_location import *
from ...dc_sys import *


__all__ = ["update_database_loc"]


def update_database_loc(dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                        survey_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                        automatic_names: tkinter.BooleanVar,
                        block_def_directory: tkinter.StringVar, block_def_file_name: tkinter.StringVar):
    print_section_title(f"Setting user inputs...")

    clean_loaded_dc_sys()
    DATABASE_LOCATION.dc_sys_addr = os.path.join(dc_sys_directory.get(), dc_sys_file_name.get()
                                                 ).replace("/", os.path.sep)
    print_log(f"DC_SYS file is {Color.default}\"{DATABASE_LOCATION.dc_sys_addr}\"{Color.reset}.")

    if automatic_names.get():
        DATABASE_LOCATION.block_def = None
    else:
        DATABASE_LOCATION.block_def = os.path.join(block_def_directory.get(), block_def_file_name.get()
                                              ).replace("/", os.path.sep)
        print_log(f"Block Definition file is {Color.default}\"{DATABASE_LOCATION.block_def}\"{Color.reset}.")

    DATABASE_LOCATION.survey_loc.survey_addr = list()
    DATABASE_LOCATION.survey_loc.survey_sheet = list()
    DATABASE_LOCATION.survey_loc.all_sheets = list()
    DATABASE_LOCATION.survey_loc.start_row = list()
    DATABASE_LOCATION.survey_loc.ref_col = list()
    DATABASE_LOCATION.survey_loc.type_col = list()
    DATABASE_LOCATION.survey_loc.track_col = list()
    DATABASE_LOCATION.survey_loc.survey_kp_col = list()

    for survey_name, survey_info in survey_loc_dict.items():
        print_log(f"Setting information entered for {Color.default}{survey_name}{Color.reset}...")

        survey_file = os.path.join(survey_info["survey_directory"].get(),
                                   survey_info["survey_file_name"].get()
                                   ).replace("/", os.path.sep)  # Survey File
        if not survey_file:
            print_log(f"\tNo Survey.")
            continue
        print_log(f"\tSurvey File is {Color.default}\"{survey_file}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.survey_addr.append(survey_file)

        survey_sheet = survey_info["survey_sheet"].get()  # Survey Sheet
        all_sheets = survey_info["all_sheets"].get()  # All Sheets flag
        print_log(f"\tCorresponding Survey Sheet is {Color.default}"
                  f"\"{'all sheets' if all_sheets else survey_sheet}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.survey_sheet.append(survey_sheet)
        DATABASE_LOCATION.survey_loc.all_sheets.append(all_sheets)

        start_row = int(survey_info["start_row"].get())  # First Data Row
        print_log(f"\tCorresponding First Data Row is {Color.default}\"{start_row}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.start_row.append(start_row)

        ref_col = get_xl_column_from_number_or_letter(survey_info["ref_col"].get())  # Reference Column
        print_log(f"\tCorresponding Reference Column is {Color.default}\"{ref_col}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.ref_col.append(ref_col)

        type_col = get_xl_column_from_number_or_letter(survey_info["type_col"].get())  # Type Column
        print_log(f"\tCorresponding Type Column is {Color.default}\"{type_col}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.type_col.append(type_col)

        track_col = get_xl_column_from_number_or_letter(survey_info["track_col"].get())  # Track Column
        print_log(f"\tCorresponding Track Column is {Color.default}\"{track_col}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.track_col.append(track_col)

        survey_kp_col = get_xl_column_from_number_or_letter(survey_info["survey_kp_col"].get())  # Surveyed KP Column
        print_log(f"\tCorresponding Surveyed KP Column is {Color.default}\"{survey_kp_col}\"{Color.reset}.")
        DATABASE_LOCATION.survey_loc.survey_kp_col.append(survey_kp_col)

    print_log(f"\nIt is all set. Launching the verification...")
