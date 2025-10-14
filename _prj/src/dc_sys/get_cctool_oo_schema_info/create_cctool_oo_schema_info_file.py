#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from .get_cctool_oo_schema_info import *


__all__ = ["create_cctool_oo_schema_info_file", "get_version_of_cctool_oo_schema_python_file"]


RESULT_DIRECTORY_RELATIVE_PATH = os.path.join("..", "..", "cctool_oo_schema")
RESULT_DIRECTORY = get_full_path(__file__, RESULT_DIRECTORY_RELATIVE_PATH)
PY_FILE_NAME = "cctool_oo_schema.py"
RES_PY_FILE_FULL_PATH = os.path.join(RESULT_DIRECTORY, PY_FILE_NAME)


def get_version_of_cctool_oo_schema_python_file() -> str:
    version_lines = list()
    with open(RES_PY_FILE_FULL_PATH, "r") as f:
        nb_sep_lines = 0
        for line in f.readlines():
            if not is_comment_line(line):
                continue
            if is_sep_line(line):
                nb_sep_lines += 1
                continue
            if nb_sep_lines == 2:  # between the second separation line and the third
                version_lines.append(remove_line_comment_characters(line))
    return "\n".join(version_lines)


def is_comment_line(line: str) -> bool:
    line = line.strip()
    return line.startswith("# ") and line.endswith(" #")


def remove_line_comment_characters(line: str) -> str:
    return line.strip().removeprefix("# ").removesuffix(" #").strip()


def is_sep_line(line: str) -> bool:
    if not is_comment_line(line):
        return False
    line = remove_line_comment_characters(line)
    return all(char == "-" for char in line)


def create_cctool_oo_schema_info_file():
    cctool_oo_file = get_corresponding_cctool_oo_schema()
    cctool_oo_schema_dict = load_cctool_oo_schema_info(cctool_oo_file)

    if not cctool_oo_schema_dict:
        print_error(f"The CCTool-OO Schema file has not been parsed, "
                    f"the Python file for the DCSYS class is not created.")
        return

    file_desc = ("Automatically generated Python file defining a DCSYS class containing the column information of "
                 "the sheets and attributes from the CCTool-OO Schema sheet of the CCTool-OO Schema file.")
    text = create_header_for_the_generated_files(cctool_oo_file, file_desc)
    text += "\n__all__ = [\"DCSYS\"]\n"
    text += add_object_attributes(cctool_oo_schema_dict)
    text += add_main_class(cctool_oo_schema_dict)
    text = text.replace("\t", "    ")
    with open(RES_PY_FILE_FULL_PATH, "w") as f:
        f.write(text)


def add_list_attributes(object_name, attribute_title, attribute_value):
    text = f"\n\nclass {object_name}__{attribute_title}:\n"
    for key, list_value in attribute_value.items():
        sub_dict = {"sheet_name": object_name, "attribute_name": attribute_title, "sub_attribute_name": key, "columns": list_value}
        text += f"\t{key} = {sub_dict}\n"
    return text


def add_object_attributes(info_dict: dict[str, dict]):
    text = str()
    for object_name, object_attributes_dict in info_dict.items():
        sub_definition = str()
        for attribute_title, attribute_value in object_attributes_dict.items():
            if isinstance(attribute_value, dict):
                text += add_list_attributes(object_name, attribute_title, attribute_value)
                sub_definition += f"\t{attribute_title} = {object_name}__{attribute_title}()\n"
            else:
                sub_dict = {"sheet_name": object_name, "attribute_name": attribute_title, "column": attribute_value}
                sub_definition += f"\t{attribute_title} = {sub_dict}\n"
        text += f"\n\nclass {object_name}:\n" + sub_definition
    return text


def add_main_class(info_dict: dict[str, dict]):
    class_name = "DCSYS"
    text = f"\n\nclass {class_name}:\n"
    for object_name in info_dict:
        text += f"\t{object_name} = {object_name}()\n"
    return text
