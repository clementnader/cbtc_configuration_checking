#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..utils import *
from ..database_location import *
from .control_tables_utils import *
from .pdf_analysis import *
from .csv_control_tables import *
from .ini_file import *


__all__ = ["load_control_tables"]


def load_control_tables(control_table_type: str, use_csv_file: bool = False,
                        supersede_input_file_number: int = None,
                        supersede_specific_pages: Union[int, tuple[int, int]] = None,
                        debug: bool = False, print_pdf_code: bool = False):

    if control_table_type not in [CONTROL_TABLE_TYPE.route, CONTROL_TABLE_TYPE.overlap]:
        print_error(f"{Color.yellow}{control_table_type = }{Color.reset} is unknown, expected "
                    f"{CONTROL_TABLE_TYPE.route} or {CONTROL_TABLE_TYPE.overlap}.")
        raise UnknownControlTablesType(control_table_type)

    get_control_tables_template_info()  # Read the information from the .ini file, initialize the global dictionaries.

    control_tables_loc_info = list(_get_control_tables_loc_info(control_table_type))
    result_files_name = _get_result_files_name(control_tables_loc_info)

    control_tables_info = dict()
    nb_of_control_tables = len(control_tables_loc_info)

    for i, ((control_table_addr, all_pages, specific_pages), result_file_name) in (
            enumerate(zip(control_tables_loc_info, result_files_name), start=1)):

        if supersede_input_file_number is not None and i != supersede_input_file_number:
            continue

        if use_csv_file is False or not os.path.exists(result_file_name):
            specific_pages = supersede_specific_pages if supersede_specific_pages is not None else specific_pages
            all_pages = False if supersede_specific_pages is not None else all_pages
            control_table_info = _load_control_table_info(control_table_type, control_table_addr, all_pages,
                                                          specific_pages, i, nb_of_control_tables, debug=debug,
                                                          print_pdf_code=print_pdf_code)
            control_table_info = create_csv_file_control_table(control_table_info, result_file_name)

        else:
            control_table_info = analyze_csv_file_control_table(result_file_name)

        control_tables_info.update(control_table_info)

    return control_tables_info


def _load_control_table_info(control_table_type: str, control_table_addr: str, all_pages: bool,
                             specific_pages: Union[int, tuple[int, int]], i: int, nb_of_control_tables: int,
                             debug: bool = False, print_pdf_code: bool = False):
    if all_pages:
        print(f"\n {i}/{nb_of_control_tables} - "
              f"{Color.white}{Color.underline}Conversion of {Color.yellow}{control_table_type.title()}"
              f"{Color.white} Control Tables {Color.no_underline}{NBSP}"
              f"\n{' ' * len(f' {i}/{nb_of_control_tables} - ')}"
              f"{Color.underline}{Color.cyan}{control_table_addr}{Color.white}...{Color.reset}{NBSP}")
    else:
        print(f"\n {i}/{nb_of_control_tables} - "
              f"{Color.white}{Color.underline}Conversion of {Color.blue}page" +
              (f"s {specific_pages[0]} to {specific_pages[1]}" if isinstance(specific_pages, tuple)
               else f" {specific_pages}") +
              f"{Color.white} of {Color.yellow}{control_table_type.title()}"
              f"{Color.white} Control Table file{Color.no_underline}{NBSP}"
              f"\n{' ' * len(f' {i}/{nb_of_control_tables} - ')}"
              f"{Color.underline}{Color.cyan}{control_table_addr}{Color.white}...{Color.reset}{NBSP}")

    if all_pages:
        list_specific_pages = None
    else:
        list_specific_pages = (list(range(specific_pages[0], specific_pages[1] + 1))
                               if isinstance(specific_pages, tuple)
                               else [specific_pages])
    control_table_info = control_tables_pdf_parsing(control_table_type, control_table_addr, list_specific_pages,
                                                    debug=debug, print_pdf_code=print_pdf_code)
    return control_table_info


def _get_control_tables_loc_info(control_table_type: str):
    if control_table_type == CONTROL_TABLE_TYPE.route:
        control_table_addr = DATABASE_LOC.control_tables_route.control_tables_addr
        all_pages = DATABASE_LOC.control_tables_route.all_pages
        specific_pages = DATABASE_LOC.control_tables_route.specific_pages
        return zip(control_table_addr, all_pages, specific_pages)

    elif control_table_type == CONTROL_TABLE_TYPE.overlap:
        control_table_addr = DATABASE_LOC.control_tables_overlap.control_tables_addr
        all_pages = DATABASE_LOC.control_tables_overlap.all_pages
        specific_pages = DATABASE_LOC.control_tables_overlap.specific_pages
        return zip(control_table_addr, all_pages, specific_pages)


def _get_result_files_name(control_tables_loc_info: list[tuple[str, bool, Union[int, tuple[int, int]]]]) -> list[str]:
    result_files_name = list()
    for (control_table_addr, all_pages, specific_pages) in control_tables_loc_info:
        if all_pages:
            result_file_name = os.path.splitext(control_table_addr)[0] + ".csv"
        else:
            if isinstance(specific_pages, int):
                result_file_name = os.path.splitext(control_table_addr)[0] + f"_{specific_pages}" + ".csv"
            else:
                result_file_name = (os.path.splitext(control_table_addr)[0]
                                    + f"_{specific_pages[0]}-{specific_pages[1]}" + ".csv")
        result_files_name.append(result_file_name)
    return result_files_name
