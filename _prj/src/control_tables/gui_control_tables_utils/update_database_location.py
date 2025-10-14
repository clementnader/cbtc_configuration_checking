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
                        control_tables_config_ini_file: tkinter.StringVar,
                        control_tables_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                        control_table_type: tkinter.StringVar):
    print_section_title(f"Setting user inputs...")

    clean_loaded_dc_sys()
    DATABASE_LOCATION.dc_sys_addr = os.path.join(dc_sys_directory.get(), dc_sys_file_name.get()
                                                 ).replace("/", os.path.sep)
    print_log(f"DC_SYS file is {Color.default}\"{DATABASE_LOCATION.dc_sys_addr}\"{Color.reset}.")

    erase_dc_bop()
    DATABASE_LOCATION.dc_bop_addr = os.path.join(dc_bop_directory.get(), dc_bop_file_name.get()
                                                 ).replace("/", os.path.sep)
    print_log(f"DC_BOP file is {Color.default}\"{DATABASE_LOCATION.dc_sys_addr}\"{Color.reset}.")

    update_control_table_database_loc(control_tables_config_ini_file,
                                      control_tables_loc_dict, control_table_type, main=False)

    print_log(f"It is all set. Launching the verification...")


def update_control_table_database_loc(control_tables_config_ini_file: tkinter.StringVar,
                                      control_tables_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                                      control_table_type: tkinter.StringVar, main: bool = True):
    if main:
        print_section_title(f"Setting user inputs...")

    DATABASE_LOCATION.control_tables_config_ini_file = control_tables_config_ini_file.get()
    print_log(f"Control Tables Configuration .ini file is {Color.default}"
              f"\"{DATABASE_LOCATION.control_tables_config_ini_file}\"{Color.reset}.")

    if control_table_type.get() == CONTROL_TABLE_TYPE.route:  # ROUTE Control Tables
        DATABASE_LOCATION.control_tables_route.control_tables_addr = list()
        DATABASE_LOCATION.control_tables_route.all_pages = list()
        DATABASE_LOCATION.control_tables_route.specific_pages = list()

        for control_table_name, control_table_info in control_tables_loc_dict.items():
            print_log(f"Setting information entered for {Color.default}{control_table_name}{Color.reset}...")

            control_table_file = os.path.join(control_table_info["control_table_directory"].get(),
                                              control_table_info["control_table_file_name"].get()
                                              ).replace("/", os.path.sep)  # Control Table File
            print_log(f"\tRoute Control Table file is {Color.default}\"{control_table_file}\"{Color.reset}.")
            DATABASE_LOCATION.control_tables_route.control_tables_addr.append(control_table_file)

            page_selection = control_table_info["page_selection"].get()
            if page_selection == 0:  # all pages
                print_log(f"\tCorresponding Route Control Table pages are {Color.default}"
                          f"\"all pages\"{Color.reset}.")
                DATABASE_LOCATION.control_tables_route.all_pages.append(True)
                DATABASE_LOCATION.control_tables_route.specific_pages.append(None)

            elif page_selection == 1:  # pages range selection
                specific_range_inf = int(control_table_info["specific_range_inf"].get())
                specific_range_sup = int(control_table_info["specific_range_sup"].get())
                print_log(f"\tCorresponding Route Control Table pages are {Color.default}"
                          f"\"from page {specific_range_inf} to page {specific_range_sup}\"{Color.reset}.")
                DATABASE_LOCATION.control_tables_route.all_pages.append(False)
                DATABASE_LOCATION.control_tables_route.specific_pages.append((specific_range_inf, specific_range_sup))

            elif page_selection == 2:  # one-page selection
                specific_page = int(control_table_info["specific_page"].get())
                print_log(f"\tCorresponding Route Control Table pages is {Color.default}"
                          f"\"page {specific_page}\"{Color.reset}.")
                DATABASE_LOCATION.control_tables_route.all_pages.append(False)
                DATABASE_LOCATION.control_tables_route.specific_pages.append(specific_page)
    else:  # OVERLAP Control Tables
        DATABASE_LOCATION.control_tables_overlap.control_tables_addr = list()
        DATABASE_LOCATION.control_tables_overlap.all_pages = list()
        DATABASE_LOCATION.control_tables_overlap.specific_pages = list()

        for control_table_name, control_table_info in control_tables_loc_dict.items():
            print_log(f"Setting information entered for {Color.default}{control_table_name}{Color.reset}...")

            control_table_file = os.path.join(control_table_info["control_table_directory"].get(),
                                              control_table_info["control_table_file_name"].get()
                                              ).replace("/", os.path.sep)  # Control Table File
            print_log(f"\tOverlap Control Table file is {Color.default}\"{control_table_file}\"{Color.reset}.")
            DATABASE_LOCATION.control_tables_overlap.control_tables_addr.append(control_table_file)

            page_selection = control_table_info["page_selection"].get()
            if page_selection == 0:  # all pages
                print_log(f"\tCorresponding Overlap Control Table pages are {Color.default}"
                          f"\"all pages\"{Color.reset}.")
                DATABASE_LOCATION.control_tables_overlap.all_pages.append(True)
                DATABASE_LOCATION.control_tables_overlap.specific_pages.append(None)

            elif page_selection == 1:  # pages range selection
                specific_range_inf = int(control_table_info["specific_range_inf"].get())
                specific_range_sup = int(control_table_info["specific_range_sup"].get())
                print_log(f"\tCorresponding Overlap Control Table pages are {Color.default}"
                          f"\"from page {specific_range_inf} to page {specific_range_sup}\"{Color.reset}.")
                DATABASE_LOCATION.control_tables_overlap.all_pages.append(False)
                DATABASE_LOCATION.control_tables_overlap.specific_pages.append((specific_range_inf, specific_range_sup))

            elif page_selection == 2:  # one-page selection
                specific_page = int(control_table_info["specific_page"].get())
                print_log(f"\tCorresponding Overlap Control Table pages is {Color.default}"
                          f"\"page {specific_page}\"{Color.reset}.")
                DATABASE_LOCATION.control_tables_overlap.all_pages.append(False)
                DATABASE_LOCATION.control_tables_overlap.specific_pages.append(specific_page)

    if main:
        print_log(f"It is all set. Launching the verification...")
