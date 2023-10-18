#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from ..database_location import *
from ..utils import *
from .pdf_extract_tables import *


__all__ = ["CONTROL_TABLE_TYPE", "CONTROL_TABLE_LINE_PART", "parse_control_tables",
           "ROUTE_CONTROL_SIG_CONTROL_TABLE", "ROUTE_SW_CONTROL_TABLE", "ROUTE_PATH_CONTROL_TABLE",
           "ROUTE_APPROACH_AREA_CLEARANCE_CONTROL_TABLE",
           "OVL_DESTINATION_POINT_CONTROL_TABLE", "OVL_PATH_CONTROL_TABLE", "OVL_SW_CONTROL_TABLE"]


ROUTE_CONTROL_SIG_CONTROL_TABLE = ["[1]", "[1a]"]
ROUTE_SW_CONTROL_TABLE = "[9]"
ROUTE_PATH_CONTROL_TABLE = "[10]"
ROUTE_APPROACH_AREA_CLEARANCE_CONTROL_TABLE = "[14]"

OVL_DESTINATION_POINT_CONTROL_TABLE = "[1]"
OVL_PATH_CONTROL_TABLE = "[5]"
OVL_SW_CONTROL_TABLE = "[8]"


class CONTROL_TABLE_LINE_PART:
    line = "Main Line"
    cmc = "Control and Maintenance Center (CMC)"
    cmc2 = "CMC second part"


class ControlTableInfo:
    control_tables_path = str()
    result_file = str()

    def __init__(self, table_type: str, line_part: str):
        if table_type == CONTROL_TABLE_TYPE.route:
            control_tables = DATABASE_LOC.control_tables_route
        elif table_type == CONTROL_TABLE_TYPE.overlap:
            control_tables = DATABASE_LOC.control_tables_overlap
        else:
            print(f"Unknown table type: {table_type}, it should be \"{CONTROL_TABLE_TYPE.route}\" or "
                  f"\"{CONTROL_TABLE_TYPE.overlap}\".")
            return

        if line_part == CONTROL_TABLE_LINE_PART.line:
            self.control_tables_path = control_tables.line
        elif line_part == CONTROL_TABLE_LINE_PART.cmc:
            self.control_tables_path = control_tables.cmc
        elif line_part == CONTROL_TABLE_LINE_PART.cmc2:
            self.control_tables_path = control_tables.cmc2
        else:
            print(f"Unknown part of the line: {line_part}, it should be \"{CONTROL_TABLE_LINE_PART.line}\", "
                  f"\"{CONTROL_TABLE_LINE_PART.cmc}\" or \"{CONTROL_TABLE_LINE_PART.cmc2}\".")
            return

        self.result_file = os.path.splitext(self.control_tables_path)[0] + ".csv"


def parse_control_tables(table_type: str, use_csv_file: bool = False, verbose: bool = False, specific_page: int = None,
                         line_parts: tuple = (CONTROL_TABLE_LINE_PART.line, CONTROL_TABLE_LINE_PART.cmc,
                                              CONTROL_TABLE_LINE_PART.cmc2)) -> dict:
    res_dict = dict()

    for line_part in line_parts:
        control_table_info = ControlTableInfo(table_type, line_part)
        if not control_table_info.control_tables_path:
            continue
        res_dict.update(_get_res_dict_control_table(
            control_table_info.control_tables_path, control_table_info.result_file, table_type, line_part,
            use_csv_file=use_csv_file, verbose=verbose, specific_page=specific_page))
    res_dict = {obj_name.strip(): {key.strip(): val.strip() for key, val in obj_val.items()}
                for obj_name, obj_val in res_dict.items()}
    return res_dict


def _get_res_dict_control_table(control_tables_path: str, result_file: str, table_type: str, line_part: str,
                                use_csv_file: bool = False, verbose: bool = False, specific_page: int = None):
    if use_csv_file is False or not os.path.exists(result_file):
        res_dict = pdf_reader_extract_tables(control_tables_path, table_type, line_part, verbose=verbose,
                                             specific_page=specific_page)
        create_csv_file_control_table(res_dict, result_file)
    else:
        res_dict = analyze_csv_file_control_table(result_file)
    return res_dict


def analyze_csv_file_control_table(result_file: str) -> dict:
    with open(result_file, "r") as f:
        csv = f.readlines()
    for i, line in enumerate(csv):
        csv[i] = line.removesuffix("\n")
    res_dict = dict()
    headers = csv[0].split(";")
    for line in csv[1:]:
        info = line.split(";")
        name = info[0]
        res_dict[name] = dict()
        for key, value in zip(headers, info):
            res_dict[name][key] = value
    return res_dict


def create_csv_file_control_table(res_dict: dict, result_file: str) -> None:
    csv = str()
    for tables_dict in res_dict.values():
        if not csv:
            csv = ";".join(list(tables_dict.keys())) + "\n"
        csv += ";".join(list(tables_dict.values())) + "\n"
    if not csv.strip():
        return
    _create_csv(csv, result_file)
    print_success(f"The result file can be accessed at \"{result_file}\".")


def _create_csv(csv: str, result_file: str):
    if not csv.strip():
        return
    try:
        with open(result_file, "w") as f:
            f.write(csv)
    except PermissionError:
        print_error(f"Permission denied to write at {result_file = }."
                    f"\nYou have to close it if you want it to be overwritten.")
        if not ask_question_yes_or_no("Do you want to retry?"):
            print_error("Execution aborted.")
            sys.exit(1)
        with open(result_file, "w") as f:
            f.write(csv)
