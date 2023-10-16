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
    with open(RES_PY_FILE_FULL_PATH, 'r') as f:
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
    text += add_obj_attrs(cctool_oo_schema_dict)
    text += add_main_class(cctool_oo_schema_dict)
    text = text.replace("\t", "    ")
    with open(RES_PY_FILE_FULL_PATH, 'w') as f:
        f.write(text)


def add_list_attrs(obj_name, attr_title, attr_val):
    text = f"\n\nclass {obj_name}__{attr_title}:\n"
    for key, list_val in attr_val.items():
        sub_dict = {"sh_name": obj_name, "attr_name": attr_title, "sub_attr_name": key, "cols": list_val}
        text += f"\t{key} = {sub_dict}\n"
    return text


def add_obj_attrs(info_dict: dict[str, dict]):
    text = str()
    for obj_name, obj_attrs_dict in info_dict.items():
        sub_definition = str()
        for attr_title, attr_val in obj_attrs_dict.items():
            if isinstance(attr_val, dict):
                text += add_list_attrs(obj_name, attr_title, attr_val)
                sub_definition += f"\t{attr_title} = {obj_name}__{attr_title}()\n"
            else:
                sub_dict = {"sh_name": obj_name, "attr_name": attr_title, "col": attr_val}
                sub_definition += f"\t{attr_title} = {sub_dict}\n"
        text += f"\n\nclass {obj_name}:\n" + sub_definition
    return text


def add_main_class(info_dict: dict[str, dict]):
    class_name = "DCSYS"
    text = f"\n\nclass {class_name}:\n"
    for obj_name in info_dict:
        text += f"\t{obj_name} = {obj_name}()\n"
    return text
