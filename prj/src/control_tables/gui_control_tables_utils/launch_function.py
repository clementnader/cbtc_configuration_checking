#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter.ttk
import traceback
import logging
from ...utils import *
from ..control_tables_utils import *
from ..load_control_tables import *
from ..route_overlap_verification import *
from .update_database_location import *


__all__ = ["launch_function", "launch_translation_function"]


def launch_translation_function(window: tkinter.Tk,
                                control_tables_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                                control_table_type: tkinter.StringVar):
    if are_control_tables_ready(control_tables_loc_dict, control_table_type):
        window.withdraw()  # hide window
        try:
            update_control_table_database_loc(control_tables_loc_dict, control_table_type)
            load_control_tables(control_table_type=control_table_type.get(), use_csv_file=False)

        except Exception as error:
            print(error)
            logging.error(traceback.format_exc())
            print_error(f"Error during process, verify your inputs.")
            tkinter.messagebox.showerror(title="Error",
                                        message="Error during process, verify your inputs.\n"
                                                "Check the cmd window for more information.\n"
                                                "Verify that DC_SYS is matching the CCTool-OO Schema version.")
            window.deiconify()  # un-hide window

        window.deiconify()  # un-hide window
        tkinter.messagebox.showinfo(title="Success",
                                     message=f"{control_table_type.get().title()} Control Tables translation "
                                             f"is complete.")
    else:
        tkinter.messagebox.showerror(title="Missing Information", message="Information is missing to launch the tool.")


def launch_function(window: tkinter.Tk, dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                    dc_bop_directory: tkinter.StringVar, dc_bop_file_name: tkinter.StringVar,
                    control_tables_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                    control_table_type: tkinter.StringVar):
    if is_everything_ready(dc_sys_directory, dc_sys_file_name, dc_bop_directory, dc_bop_file_name,
                           control_tables_loc_dict, control_table_type):
        window.withdraw()  # hide window
        try:
            update_database_loc(dc_sys_directory, dc_sys_file_name, dc_bop_directory, dc_bop_file_name,
                                control_tables_loc_dict, control_table_type)
            if control_table_type.get() == CONTROL_TABLE_TYPE.route:
                check_route_control_tables(use_csv_file=True)
            elif control_table_type.get() == CONTROL_TABLE_TYPE.overlap:
                check_overlap_control_tables(use_csv_file=True)

        except Exception as error:
            print(error)
            logging.error(traceback.format_exc())
            print_error(f"Error during process, verify your inputs.")
            tkinter.messagebox.showerror(title="Error",
                                        message="Error during process, verify your inputs.\n"
                                                "Check the cmd window for more information.\n"
                                                "Verify that DC_SYS is matching the CCTool-OO Schema version.")
            window.deiconify()  # un-hide window

        window.deiconify()  # un-hide window
        window.wm_state("iconic")  # minimize window
        tkinter.messagebox.showinfo(title="Success",
                                     message=f"{control_table_type.get().title()} Control Tables verification "
                                             f"is complete.")
    else:
        tkinter.messagebox.showerror(title="Missing Information", message="Information is missing to launch the tool.")


def is_everything_ready(dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                        dc_bop_directory: tkinter.StringVar, dc_bop_file_name: tkinter.StringVar,
                        control_tables_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                        control_table_type: tkinter.StringVar):
    print_section_title(f"Checking if all information is provided...")
    test = True

    if dc_sys_directory.get() == "" or dc_sys_file_name.get() == "":
        print_log(f"DC_SYS is not selected.")
        test = False

    if dc_bop_directory.get() == "" or dc_bop_file_name.get() == "":
        print_log(f"DC_BOP is not selected.")
        test = False

    if not are_control_tables_ready(control_tables_loc_dict, control_table_type, main=False):
        test = False

    if test:
        print_log("OK all information is provided.")
    return test


def are_control_tables_ready(control_tables_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                             control_table_type: tkinter.StringVar, main: bool = True):
    if main:
        print_section_title(f"Checking if all information is provided...")
    test = True

    if control_table_type.get() == "":
        print_log(f"Control Table Type is not selected.")
        test = False

    for control_table_name, control_table_info in control_tables_loc_dict.items():
        if (control_table_info["control_table_directory"].get() == ""
                or control_table_info["control_table_file_name"].get() == ""):
            print_log(f"For {control_table_name}, Control Table is not selected.")
            test = False
            continue
        if (control_table_info["page_selection"].get() == 1  # pages range selection
                and (control_table_info["specific_range_inf"].get() == ""
                     or control_table_info["specific_range_sup"].get() == "")):
            print_log(f"For {control_table_name}, option \"range selection\" is selected "
                      f"but the range is not filled.")
            test = False
        if (control_table_info["page_selection"].get() == 2  # one-page selection
                and control_table_info["specific_page"].get() == ""):
            print_log(f"For {control_table_name}, option \"one-page selection\" is selected "
                      f"but the page is not filled.")
            test = False

    if main and test:
        print_log("OK all information is provided.")
    return test
