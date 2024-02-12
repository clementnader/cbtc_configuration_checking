#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from .get_cctool_oo_schema_info import *


__all__ = ["create_cctool_oo_enum_lists_info_file"]


RESULT_DIRECTORY_RELATIVE_PATH = os.path.join("..", "..", "cctool_oo_schema")
RESULT_DIRECTORY = get_full_path(__file__, RESULT_DIRECTORY_RELATIVE_PATH)
PY_FILE_NAME = "cctool_oo_enum_lists.py"
RES_PY_FILE_FULL_PATH = os.path.join(RESULT_DIRECTORY, PY_FILE_NAME)


def create_cctool_oo_enum_lists_info_file():
    cctool_oo_file = get_corresponding_cctool_oo_schema()
    cctool_oo_enum_lists_dict = load_cctool_oo_enum_lists_info(cctool_oo_file)

    if not cctool_oo_enum_lists_dict:
        print_error(f"The CCTool-OO Schema file has not been parsed, "
                    f"the Python file for the Enum List classes is not created.")
        return

    file_desc = ("Automatically generated Python file defining classes for the enumerates from the EnumList sheet "
                 "of the CCTool-OO Schema file.")
    text = create_header_for_the_generated_files(cctool_oo_file, file_desc)
    text += add_obj_attrs(cctool_oo_enum_lists_dict)
    text = text.replace("\t", "    ")
    with open(RES_PY_FILE_FULL_PATH, 'w') as f:
        f.write(text)


def add_obj_attrs(info_dict: dict[str, list[str]]):
    text = str()
    for enum_name, available_values in info_dict.items():
        sub_definition = str()
        for val in available_values:
            sub_definition += f"\t{get_clean_value(val)} = \"{val}\"\n"
        text += f"\n\nclass {enum_name}:\n" + sub_definition
    return text


def get_clean_value(value: str):
    value = value.replace(' ', "_")  # remove special char
    value = value.replace('?', "Question_Mark")  # remove special char
    value = value.replace("->", "_")  # remove special chars
    return value
