#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..utils import *
from .pdf_extract_tables import pdf_reader_extract_tables, CONTROL_TABLE_TYPE


CONTROL_TABLES_ROUTE = os.path.join(r"C:\Users\naderc\Downloads",
                                    r"CR-ASTS-045007-10.00 ATC Line Control Tables Routes.pdf")
CONTROL_TABLES_ROUTE_CMC = os.path.join(r"C:\Users\naderc\Downloads",
                                        r"CR-ASTS-045017-11.00 ATC CMC Control Tables Routes.pdf")
# CONTROL_TABLES_ROUTE = os.path.join(r"C:\Users\naderc\Downloads",
#                                     r"M4-ST00PGRE-55129_00.01_Allegato_1.pdf")
# CONTROL_TABLES_ROUTE_CMC = ""


CONTROL_TABLES_OVERLAP = os.path.join(r"C:\Users\naderc\Downloads",
                                      r"CR-ASTS-045009-06.00 ATC Line Control Tables Overlap.pdf")
CONTROL_TABLES_OVERLAP_CMC = os.path.join(r"C:\Users\naderc\Downloads",
                                          r"CR-ASTS-045019-09.00 ATC CMC Control Tables Overlap.pdf")


def parse_control_tables(table_type: str, use_csv_file: bool = False) -> dict:
    if table_type == CONTROL_TABLE_TYPE.route:
        control_tables_path = CONTROL_TABLES_ROUTE
        control_tables_cmc_path = CONTROL_TABLES_ROUTE_CMC
    elif table_type == CONTROL_TABLE_TYPE.overlap:
        control_tables_path = CONTROL_TABLES_OVERLAP
        control_tables_cmc_path = CONTROL_TABLES_OVERLAP_CMC
    else:
        print(f"Unknown table type: {table_type}, it should be \"{CONTROL_TABLE_TYPE.route}\" or "
              f"\"{CONTROL_TABLE_TYPE.overlap}\".")
        return {}
    result_file = os.path.splitext(control_tables_path)[0] + ".csv"
    result_file_cmc = os.path.splitext(control_tables_cmc_path)[0] + ".csv"

    if use_csv_file is False or not os.path.exists(result_file):
        res_dict = parse_pdf_control_table(table_type)
        create_csv_file_control_table(res_dict, result_file)
    else:
        res_dict = analyze_csv_file_control_table(result_file)

    control_tables_cmc = True if control_tables_cmc_path else False  # test_tack and depot are split to another file
    if control_tables_cmc:
        if use_csv_file is False or not os.path.exists(result_file_cmc):
            res_dict_cmc = parse_pdf_control_table(table_type, cmc=True)
            create_csv_file_control_table(res_dict_cmc, result_file_cmc)
        else:
            res_dict_cmc = analyze_csv_file_control_table(result_file_cmc)
        res_dict.update(res_dict_cmc)

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
    _create_csv(csv, result_file)
    print_success(f"The result file can be accessed at \"{result_file}\".")


def parse_pdf_control_table(table_type: str, cmc: bool = False) -> dict:
    if table_type == CONTROL_TABLE_TYPE.route:
        control_tables_path = CONTROL_TABLES_ROUTE if not cmc else CONTROL_TABLES_ROUTE_CMC
    elif table_type == CONTROL_TABLE_TYPE.overlap:
        control_tables_path = CONTROL_TABLES_OVERLAP if not cmc else CONTROL_TABLES_OVERLAP_CMC
    else:
        return {}

    return pdf_reader_extract_tables(control_tables_path, table_type, cmc)


def _create_csv(csv: str, result_file: str):
    if not csv.strip():
        return
    try:
        with open(result_file, "w") as f:
            f.write(csv)
    except PermissionError:
        print_error(f"Permission denied to write at {result_file=}."
                    f"\nYou have to close it if you want it to be overwritten.")
        if input(f"Do you want to retry? (Y/N) ").upper() in ["Y", "YES"]:
            with open(result_file, "w") as f:
                f.write(csv)
