#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


__all__ = ["analyze_csv_file_control_table", "create_csv_file_control_table"]


def analyze_csv_file_control_table(result_file: str) -> dict:
    with open(result_file, "r") as f:
        csv = f.readlines()
    for i, line in enumerate(csv):
        csv[i] = line.removesuffix("\n")
    res_dict = dict()
    headers = csv[0].split(";")
    # Line 1 (second line) gives the key names from the PDF file, they are for information only.
    for line in csv[2:]:
        info = line.split(";")
        name = info[0].strip()
        res_dict[name] = dict()
        for key, value in zip(headers, info):
            res_dict[name][key.strip()] = value.strip()
    return res_dict


def create_csv_file_control_table(res_dict: dict, result_file: str) -> dict:
    control_table_info = dict()
    csv = str()
    for name, tables_dict in res_dict.items():
        control_table_info[name] = {val["csv_title"]: val["text"] for val in tables_dict.values()}
        if not csv:
            csv = ";".join([val["csv_title"] for val in tables_dict.values()]) + "\n"
            csv += ";".join([key_name for key_name in tables_dict.keys()]) + "\n"
        csv += ";".join([val["text"] for val in tables_dict.values()]) + "\n"
    if csv.strip():
        result_file = _create_csv(csv, result_file)
        print_success(f"The result CSV file can be accessed at \"{result_file}\".")
    return control_table_info


def _create_csv(csv: str, result_file: str) -> str:
    if not csv.strip():
        return result_file
    try:
        with open(result_file, "w") as f:
            f.write(csv)
    except PermissionError:
        print_error(f"Permission denied to write at {result_file = }."
                    f"\nYou have to close it if you want it to be overwritten.")
        if not ask_question_yes_or_no("Do you want to retry?"):
            print_error("Execution aborted.")
            raise UnableToSaveFileException
        with open(result_file, "w") as f:
            f.write(csv)
    return result_file
