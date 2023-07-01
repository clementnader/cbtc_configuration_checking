#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


START_LINE = 3
DEFAULT_NAME_COLUMN = 1


def get_sh_dict(sh: xlrd.sheet, columns_dict: dict[str], generic_obj_name: bool) -> dict:
    xlrd_line_ref = get_xlrd_line(START_LINE)
    xlrd_name_col = get_xlrd_column(DEFAULT_NAME_COLUMN)
    sh_dict = dict()
    for xlrd_line in range(xlrd_line_ref, sh.nrows):
        obj_name = read_cell(sh, xlrd_line, xlrd_name_col)
        if obj_name is not None:
            if generic_obj_name:
                obj_name = f"{sh.name}_line_{xlrd_line+1}"
            sh_dict[obj_name] = get_info_for_object(sh, xlrd_line, columns_dict)
    return sh_dict


def get_info_for_object(sh: xlrd.sheet, xlrd_line: int, columns_dict: dict[str]):
    info_dict = dict()
    for key, column in columns_dict.items():
        if isinstance(column, int):
            xlrd_col = get_xlrd_column(column)
            value = read_cell(sh, xlrd_line, xlrd_col)
            info_dict[key] = value
        else:
            info_dict[key] = get_sub_attr_list_info(sh, xlrd_line, column)
    return info_dict


def get_sub_attr_list_info(sh: xlrd.sheet, xlrd_line: int, sub_dict: dict[str, list[int]]):
    info_sub_dict = dict()
    for key, columns in sub_dict.items():
        info_sub_dict[key] = list()
        for column in columns:
            xlrd_col = get_xlrd_column(column)
            value = read_cell(sh, xlrd_line, xlrd_col)
            info_sub_dict[key].append(value)
    return info_sub_dict
