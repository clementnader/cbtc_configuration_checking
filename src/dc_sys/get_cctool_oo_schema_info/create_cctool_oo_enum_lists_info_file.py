#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from .get_cctool_oo_schema_info import *


__all__ = ["create_cctool_oo_enum_lists_info_file"]


def create_cctool_oo_enum_lists_info_file():
    py_file_name = "cctool_oo_enum_lists.py"
    res_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "cctool_oo_schema")
    res_py_file_full_path = os.path.join(res_directory, py_file_name)
    cctool_oo_enum_lists_dict = load_cctool_oo_enum_lists_info()

    if not cctool_oo_enum_lists_dict:
        print_error(f"The CCTool-OO Schema file has not been parsed, "
                    f"the Python file for the Enum List classes is not created.")
        return

    text = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n"
    text += add_obj_attrs(cctool_oo_enum_lists_dict)
    with open(res_py_file_full_path, 'w') as f:
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
    value = value.replace('?', "Question_Mark")  # remove special char
    value = value.replace("->", "_a_")  # remove special chars
    return value
