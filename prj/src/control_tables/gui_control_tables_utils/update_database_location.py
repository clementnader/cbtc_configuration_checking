#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...database_location import *
from ...dc_sys import *
from ...dc_bop import *
from ..control_tables_utils import *


__all__ = ["update_database_loc", "update_control_table_database_loc"]


def update_database_loc(dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                        dc_bop_directory: tkinter.StringVar, dc_bop_file_name: tkinter.StringVar,
                        control_tables_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                        control_table_type: tkinter.StringVar):
    print_section_title(f"Setting user inputs...")

    clean_loaded_dc_sys()
    DATABASE_LOC.dc_sys_addr = os.path.join(dc_sys_directory.get(), dc_sys_file_name.get()
                                            ).replace("/", os.path.sep)

    erase_dc_bop()
    DATABASE_LOC.dc_bop_addr = os.path.join(dc_bop_directory.get(), dc_bop_file_name.get()
                                            ).replace("/", os.path.sep)

    update_control_table_database_loc(control_tables_loc_dict, control_table_type, main=False)

    print_log(f"It is all set. Launching the verification...")


def update_control_table_database_loc(control_tables_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                                      control_table_type: tkinter.StringVar, main: bool = True):
    if main:
        print_section_title(f"Setting user inputs...")

    if control_table_type.get() == CONTROL_TABLE_TYPE.route:
        DATABASE_LOC.control_tables_route.control_tables_addr = list()
        DATABASE_LOC.control_tables_route.all_pages = list()
        DATABASE_LOC.control_tables_route.specific_pages = list()

        for control_table_name, control_table_info in control_tables_loc_dict.items():
            print_log(f"\tSetting information entered for {control_table_name}...")
            DATABASE_LOC.control_tables_route.control_tables_addr.append(
                os.path.join(control_table_info["control_table_directory"].get(),
                             control_table_info["control_table_file_name"].get()).replace("/", os.path.sep))

            page_selection = control_table_info["page_selection"].get()
            if page_selection == 0:  # all pages
                DATABASE_LOC.control_tables_route.all_pages.append(True)
                DATABASE_LOC.control_tables_route.specific_pages.append(None)
            elif page_selection == 1:  # pages range selection
                DATABASE_LOC.control_tables_route.all_pages.append(False)
                DATABASE_LOC.control_tables_route.specific_pages.append(
                    (int(control_table_info["specific_range_inf"].get()),
                     int(control_table_info["specific_range_sup"].get())))
            elif page_selection == 2:  # one-page selection
                DATABASE_LOC.control_tables_route.all_pages.append(False)
                DATABASE_LOC.control_tables_route.specific_pages.append(
                    int(control_table_info["specific_page"].get()))
    else:
        DATABASE_LOC.control_tables_overlap.control_tables_addr = list()
        DATABASE_LOC.control_tables_overlap.all_pages = list()
        DATABASE_LOC.control_tables_overlap.specific_pages = list()

        for control_table_name, control_table_info in control_tables_loc_dict.items():
            print_log(f"\tSetting information entered for {control_table_name}...")
            DATABASE_LOC.control_tables_overlap.control_tables_addr.append(
                os.path.join(control_table_info["control_table_directory"].get(),
                             control_table_info["control_table_file_name"].get()).replace("/", os.path.sep))

            page_selection = control_table_info["page_selection"].get()
            if page_selection == 0:  # all pages
                DATABASE_LOC.control_tables_overlap.all_pages.append(True)
                DATABASE_LOC.control_tables_overlap.specific_pages.append("")
            elif page_selection == 1:  # pages range selection
                DATABASE_LOC.control_tables_overlap.all_pages.append(False)
                DATABASE_LOC.control_tables_overlap.specific_pages.append(
                    (control_table_info["specific_range_inf"].get(), control_table_info["specific_range_sup"].get()))
            elif page_selection == 2:  # one-page selection
                DATABASE_LOC.control_tables_overlap.all_pages.append(False)
                DATABASE_LOC.control_tables_overlap.specific_pages.append(control_table_info["specific_page"].get())

    if main:
        print_log(f"It is all set. Launching the verification...")


def get_col(val: str):
    try:
        val = int(val)
    except ValueError:
        val = get_xl_column_number(val)
    return val
