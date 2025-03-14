#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter.ttk
import traceback
import logging
from ...utils import *
from ...survey import *
from .update_database_location import *


__all__ = ["launch_function", "is_everything_ready"]


def launch_function(window: tkinter.Tk, dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                    survey_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                    automatic_names: tkinter.BooleanVar,
                    block_def_directory: tkinter.StringVar, block_def_file_name: tkinter.StringVar):
    everything_ready, only_survey_missing = is_everything_ready(
        dc_sys_directory, dc_sys_file_name, survey_loc_dict, automatic_names, block_def_directory, block_def_file_name)

    if not everything_ready and only_survey_missing:
        answer = tkinter.messagebox.askquestion(title="Missing Survey Information",
                                                message="No survey specified to launch the tool.\n"
                                                        "Do you want to proceed without survey?",
                                                icon=tkinter.messagebox.WARNING,
                                                type=tkinter.messagebox.YESNO)
        if answer == tkinter.messagebox.YES:
            everything_ready = True

    if everything_ready:
        success = False
        window.withdraw()  # hide window
        try:
            update_database_loc(dc_sys_directory, dc_sys_file_name, survey_loc_dict,
                                automatic_names, block_def_directory, block_def_file_name)
            success = check_survey()
        except Exception as error:
            logging.error(traceback.format_exc())
            if f"{error = }" == "error = UnableToSaveFileException()":
                print_error(f"Unable to save file.")
                tkinter.messagebox.showerror(title="Error",
                                            message="Unable to save file.")
            else:
                print_error(f"Error during process, verify your inputs.")
                tkinter.messagebox.showerror(title="Error",
                                            message="Error during process, verify your inputs.\n"
                                                    "Check the cmd window for more information.\n"
                                                    "Verify that DC_SYS is matching the CCTool-OO Schema version.")
            window.deiconify()  # un-hide window
        if success:
            window.deiconify()  # un-hide window
            window.wm_state("iconic")  # minimize window
            tkinter.messagebox.showinfo(title="Success",
                                         message="\"Correspondence with Site Survey\" verification file is available "
                                                 "in the tool directory and is opening automatically.")
    else:
        tkinter.messagebox.showerror(title="Missing Information",
                                     message="Information is missing to launch the tool.")


def is_everything_ready(dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                        survey_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                        automatic_names: tkinter.BooleanVar,
                        block_def_directory: tkinter.StringVar, block_def_file_name: tkinter.StringVar
                        ) -> tuple[bool, bool]:
    print_section_title(f"Checking if all information is provided...")
    test = True
    only_survey_missing = False

    if dc_sys_directory.get() == "" or dc_sys_file_name.get() == "":
        print_log(f"DC_SYS is not selected.")
        test = False

    if automatic_names.get() is False and (block_def_directory.get() == "" or block_def_file_name.get() == ""):
        print_log(f"Option \"automatic joint names\" is unchecked but Block Def. is not selected.")
        test = False

    for survey_name, survey_info in survey_loc_dict.items():
        if survey_info["survey_directory"].get() == "" or survey_info["survey_file_name"].get() == "":
            print_log(f"For {survey_name}, Survey is not selected.")
            if test is True and len(list(survey_loc_dict.keys())) == 1:  # only one survey
                only_survey_missing = True
            test = False
            continue
        if survey_info["all_sheets"].get() is False and survey_info["survey_sheet"].get() == "":
            print_log(f"For {survey_name}, Survey Sheet is not filled and option \"use all sheets\" is not selected.")
            test = False
        if survey_info["start_row"].get() == "":
            print_log(f"For {survey_name}, First Data Row is not filled.")
            test = False
        if survey_info["ref_col"].get() == "":
            print_log(f"For {survey_name}, Reference Column is not filled.")
            test = False
        if survey_info["type_col"].get() == "":
            print_log(f"For {survey_name}, Type Column is not filled.")
            test = False
        if survey_info["track_col"].get() == "":
            print_log(f"For {survey_name}, Track Column is not filled.")
            test = False
        if survey_info["survey_kp_col"].get() == "":
            print_log(f"For {survey_name}, Surveyed KP Column is not filled.")
            test = False

    if test:
        print_log("OK all information is provided.")
    return test, only_survey_missing
