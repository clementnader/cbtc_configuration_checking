#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


START_LINE = 3
DEFAULT_NAME_COLUMN = 1


def get_sh_dict(sh: xlrd.sheet, columns_dict: dict[str], generic_obj_name: bool) -> dict:
    sh_dict = dict()
    for line in range(START_LINE, sh.nrows + 1):
        obj_name = get_xlrd_float_value(sh, line, DEFAULT_NAME_COLUMN)
        if obj_name is not None:
            if generic_obj_name:
                obj_name = f"{sh.name}_line_{line+1}"
            sh_dict[obj_name] = get_info_for_object(sh, line, columns_dict)
    return sh_dict


def get_info_for_object(sh: xlrd.sheet, line: int, columns_dict: dict[str]):
    info_dict = dict()
    for key, column in columns_dict.items():
        if isinstance(column, int):
            value = get_xlrd_float_value(sh, line, column)
            info_dict[key] = value
        else:
            info_dict[key] = get_sub_attr_list_info(sh, line, column)
    return info_dict


def get_sub_attr_list_info(sh: xlrd.sheet, line: int, sub_dict: dict[str, list[int]]):
    info_sub_dict = dict()
    for key, columns in sub_dict.items():
        info_sub_dict[key] = list()
        for column in columns:
            value = get_xlrd_float_value(sh, line, column)
            info_sub_dict[key].append(value)
    return info_sub_dict
