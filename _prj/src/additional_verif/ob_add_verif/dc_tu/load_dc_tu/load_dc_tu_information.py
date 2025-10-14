#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
from .....utils import *
from .....database_location import *
from .....cc_param.cc_param_utils import *
from ..dc_tu_utils import *


__all__ = ["load_dc_tu_information"]


DC_TU_LINE_COLUMN = 0
DC_TU_PARAMETER_NAME_COLUMN = 1
DC_TU_PARAMETER_VALUE_COLUMN = 2


def load_dc_tu_information() -> dict[int, dict[int, dict[str, str]]]:
    kit_c11_dir = DATABASE_LOCATION.kit_c11_dir
    dc_tu_dict = dict()
    for train_dir in os.listdir(kit_c11_dir):
        full_path = os.path.join(kit_c11_dir, train_dir)
        if not os.path.isdir(full_path) or not train_dir.startswith(TRAIN_UNIT_PREFIX):
            continue
        num_train_unit = get_num_train(train_dir)
        train_unit_dc_tu_dict = analyze_train_unit(full_path, num_train_unit)
        if train_unit_dc_tu_dict is None:
            continue
        for line_number, sub_dict in train_unit_dc_tu_dict.items():
            if line_number not in dc_tu_dict:
                dc_tu_dict[line_number] = dict()
            dc_tu_dict[line_number].update(sub_dict)
    return re_order_dict(dc_tu_dict)


def re_order_dict(in_dict: dict[int, dict[int, Any]]) -> dict[int, dict[int, Any]]:
    # Sort train units by increasing order
    return {key: {sub_key: in_dict[key][sub_key] for sub_key in sorted(in_dict[key])} for key in sorted(in_dict)}


def analyze_train_unit(train_unit_path: str, num_train_unit: int) -> Optional[dict[int, dict[int, dict[str, str]]]]:
    dc_tu_file = os.path.join(train_unit_path, DC_TU_FILE)
    if not os.path.isfile(dc_tu_file):
        print_error(f"No {DC_TU_FILE} in train unit {num_train_unit} directory ({train_unit_path}).")
        return None
    dc_tu_dict = open_dc_tu_file(dc_tu_file)
    train_unit_id = int(list(dc_tu_dict.values())[0][TRAIN_UNIT_ID])
    if train_unit_id != num_train_unit:
        print_error(f"The Train Unit Number of the directory {TRAIN_UNIT_PREFIX}{num_train_unit} does not correspond "
                    f"to the parameter {TRAIN_UNIT_ID} ({train_unit_id}) inside the {DC_TU_FILE} file.")
    res_dict = {line_number: {num_train_unit: sub_dict} for line_number, sub_dict in dc_tu_dict.items()}
    return res_dict


def open_dc_tu_file(path: str) -> dict[int, dict[str, str]]:
    dc_tu_dict = dict()
    with open(path, "r") as csv_file:
        lines = csv.reader(csv_file, delimiter=";")
        lines.__next__()  # skip the title line
        for current_line in lines:
            line_number = int(current_line[DC_TU_LINE_COLUMN].strip())
            parameter_name = current_line[DC_TU_PARAMETER_NAME_COLUMN].strip().upper()
            parameter_value = current_line[DC_TU_PARAMETER_VALUE_COLUMN].strip()
            if line_number not in dc_tu_dict:
                dc_tu_dict[line_number] = dict()
            dc_tu_dict[line_number][parameter_name] = parameter_value
    return dc_tu_dict
