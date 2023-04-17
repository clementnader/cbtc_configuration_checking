#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import xlrd

CCTOOL_OO_SCHEMA_DIR = r"C:\Users\naderc\Desktop\Bxl"
CCTOOL_OO_SCHEMA_FILE_NAME = r"CCTool-OO Schema.xls"
SHEET_NAME = r"CCTool-OO Schema"
DEFAULT_RES_DIRECTORY = os.path.join(os.getenv("UserProfile"), r"Desktop")
RES_PY_FILE = os.path.join(DEFAULT_RES_DIRECTORY, "cctool_oo_schema_info.py")


def open_file():
    wb = xlrd.open_workbook(os.path.join(CCTOOL_OO_SCHEMA_DIR, CCTOOL_OO_SCHEMA_FILE_NAME))
    return wb


def get_info(wb: xlrd.Book):
    sh = wb.sheet_by_name(SHEET_NAME)
    first_line = get_xlrd_line(2)
    obj_col = get_xlrd_column('F')
    attr_col = get_xlrd_column('G')
    trad_attr_col = get_xlrd_column('C')

    res_dict = dict()
    obj_name = None
    attrs_list = list()
    list_attrs_dict = dict()
    for i in range(first_line, sh.nrows):
        new_obj_name = get_clean_cell(sh, i, obj_col)
        if new_obj_name not in ("", "-"):
            if new_obj_name != obj_name:  # new object, save current attributes
                if attrs_list or list_attrs_dict:
                    res_dict[obj_name] = dict()
                if attrs_list:
                    res_dict[obj_name]["attrs"] = attrs_list
                if list_attrs_dict:
                    res_dict[obj_name]["list_attrs"] = list_attrs_dict
                obj_name = new_obj_name
                attrs_list = list()
                list_attrs_dict = dict()

            attr_name = get_clean_cell(sh, i, attr_col)
            if not attr_name:
                attr_name = get_clean_cell(sh, i, trad_attr_col)
            if attr_name.upper() not in ("", "-", "RESERVED"):
                if "::" in attr_name:  # the attribute is a list
                    list_attr_name, sub_attr_name = attr_name.split("::", 1)
                    sub_attr_name = sub_attr_name.replace("::", "__")
                    if list_attr_name not in list_attrs_dict:
                        list_attrs_dict[list_attr_name] = list()
                    if sub_attr_name not in list_attrs_dict[list_attr_name]:
                        list_attrs_dict[list_attr_name].append(sub_attr_name)
                else:
                    if attr_name not in attrs_list:
                        attrs_list.append(attr_name)
    if obj_name not in ("", "-"):
        if attrs_list or list_attrs_dict:
            res_dict[obj_name] = dict()
        if attrs_list:
            res_dict[obj_name]["attrs"] = attrs_list
        if list_attrs_dict:
            res_dict[obj_name]["list_attrs"] = list_attrs_dict
    return res_dict


def get_clean_cell(sh, i, j):
    cell_str = f"{sh.cell_value(i, j)}".encode("ascii", "ignore").decode().strip()
    cell_str = cell_str.title().replace(' ', '')  # camelcase
    cell_str = cell_str.replace('/', '')
    return cell_str


def create_cctool_oo_schema_info_file():
    cctool_oo_schema_dict = get_info(open_file())
    text = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n"
    text += add_obj_attrs(cctool_oo_schema_dict)
    text += add_main_class(cctool_oo_schema_dict)
    with open(RES_PY_FILE, 'w') as f:
        f.write(text)


def add_list_attrs(obj_name, list_attrs: dict[str, list[str]]):
    text = str()
    for key, list_vals in list_attrs.items():
        text += f"\n\nclass {obj_name}__{key}:\n"
        for i, val in enumerate(list_vals):
            text += f"\t{val} = {i}\n"
    return text


def add_obj_attrs(info_dict: dict[str, dict]):
    text = str()
    for obj_name, obj_attrs_dict in info_dict.items():
        attrs_list = obj_attrs_dict.get("attrs", list())
        list_attrs_dict = obj_attrs_dict.get("list_attrs", dict())
        if list_attrs_dict:
            text += add_list_attrs(obj_name, obj_attrs_dict["list_attrs"])
        text += f"\n\nclass {obj_name}:\n"
        for i, val in enumerate(attrs_list):
            text += f"\t{val} = {i}\n"
        for key in list_attrs_dict:
            text += f"\t{key} = {obj_name}__{key}()\n"
    return text


def add_main_class(info_dict: dict[str, dict]):
    class_name = "DCSYS"
    text = f"\n\nclass {class_name}:\n"
    for obj_name in info_dict:
        text += f"\t{obj_name} = {obj_name}()\n"
    return text
