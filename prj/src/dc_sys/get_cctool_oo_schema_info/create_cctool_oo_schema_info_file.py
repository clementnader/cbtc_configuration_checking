#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from .get_cctool_oo_schema_info import *


__all__ = ["create_cctool_oo_schema_info_file"]


def create_cctool_oo_schema_info_file():
    py_file_name = "cctool_oo_schema.py"
    res_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "cctool_oo_schema")
    res_py_file_full_path = os.path.join(res_directory, py_file_name)
    cctool_oo_schema_dict = load_cctool_oo_schema_info()

    if not cctool_oo_schema_dict:
        print_error(f"The CCTool-OO Schema file has not been parsed, "
                    f"the Python file for the DCSYS class is not created.")
        return

    text = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n"
    text += add_obj_attrs(cctool_oo_schema_dict)
    text += add_main_class(cctool_oo_schema_dict)
    with open(res_py_file_full_path, 'w') as f:
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