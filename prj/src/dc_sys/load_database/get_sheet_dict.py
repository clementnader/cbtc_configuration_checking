#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


__all__ = ["get_sh_dict"]


START_ROW = 3
DEFAULT_NAME_COLUMN = 1


def get_sh_dict(ws: xlrd.sheet, columns_dict: dict[str, Any], generic_obj_name: dict[str, Any]) -> dict[str, dict]:
    sh_dict = dict()
    if generic_obj_name is not None:
        return get_generic_sh_dict(ws, columns_dict, generic_obj_name)
    for row in range(START_ROW, ws.nrows + 1):
        obj_name = get_xlrd_value(ws, row, DEFAULT_NAME_COLUMN)
        if obj_name is None:
            continue
        if obj_name in sh_dict:
            print_error(f"Two objects have the same name {Color.beige}{obj_name}{Color.reset} "
                        f"in sheet {Color.blue}{ws.name}{Color.reset}.")
        sh_dict[obj_name] = get_info_for_object(ws, row, columns_dict)
    return sh_dict


def get_generic_sh_dict(ws: xlrd.sheet, columns_dict: dict[str, Any], generic_obj_name: dict[str, Any]
                        ) -> dict[str, dict[str, Any]]:
    temp_dict = dict()
    cols: list = generic_obj_name["cols"]
    for row in range(START_ROW, ws.nrows + 1):
        obj_name = get_xlrd_value(ws, row, DEFAULT_NAME_COLUMN)
        if obj_name is not None:
            info_for_object = get_info_for_object(ws, row, columns_dict)
            key = get_generic_sh_object_key(cols, info_for_object)
            temp_dict[key] = info_for_object
    temp_dict = {key: temp_dict[key] for key in sorted(temp_dict.keys())}
    sh_dict = {f"{ws.name}_{row+1}": val for row, val in enumerate(temp_dict.values())}
    return sh_dict


def get_generic_sh_object_key(cols: list, info_for_object):
    keys = list()
    for col in cols:
        col_attr = col["attr"]
        col_type = col["type"]
        if "col" in col_attr:
            key = col_type(info_for_object[col_attr["attr_name"]])
        else:
            key = col_type(info_for_object[col_attr["attr_name"]][col_attr["sub_attr_name"]][0])
        keys.append(key)
    return tuple(keys)


def get_info_for_object(ws: xlrd.sheet, row: int, columns_dict: dict[str, Any]):
    info_dict = dict()
    for key, column in columns_dict.items():
        if isinstance(column, int):
            value = get_xlrd_float_value(ws, row, column)
            check_value_has_spaces(ws.name, value, row, column, key)
            if isinstance(value, str):
                value = value.strip()
            info_dict[key] = value
        else:
            info_dict[key] = get_sub_attr_list_info(ws, row, column)
    return info_dict


def get_sub_attr_list_info(ws: xlrd.sheet, row: int, sub_dict: dict[str, list[int]]):
    info_sub_dict = dict()
    for key, columns in sub_dict.items():
        info_sub_dict[key] = list()
        for column in columns:
            value = get_xlrd_float_value(ws, row, column)
            check_value_has_spaces(ws.name, value, row, column, key)
            if isinstance(value, str):
                value = value.strip()
            info_sub_dict[key].append(value)
    return info_sub_dict


g_list_of_values_with_leading_spaces = list()
g_list_of_values_with_trailing_spaces = list()


def check_value_has_spaces(sh_name, value, row, column, key):
    global g_list_of_values_with_leading_spaces, g_list_of_values_with_trailing_spaces
    if isinstance(value, str) and value.startswith(" "):
        if not any(value.startswith(old_val) for old_val in g_list_of_values_with_leading_spaces):
            print_warning(f"There is a leading space in sheet {Color.yellow}{sh_name}{Color.reset} "
                          f"at cell {Color.blue}{get_xl_column_letter(column)}{row}{Color.reset}:\n\t"
                          f"key column name: {Color.beige}\"{key}\"{Color.reset}, "
                          f"value: {Color.white}\"{value}\"{Color.reset}")
            # g_list_of_values_with_leading_spaces.append(value)
    if isinstance(value, str) and value.endswith(" "):
        if not any(value.endswith(old_val) for old_val in g_list_of_values_with_trailing_spaces):
            print_warning(f"There is a trailing space in sheet {Color.yellow}{sh_name}{Color.reset} "
                          f"at cell {Color.blue}{get_xl_column_letter(column)}{row}{Color.reset}:\n\t"
                          f"key column name: {Color.beige}\"{key}\"{Color.reset}, "
                          f"value: {Color.white}\"{value}\"{Color.reset}")
            # g_list_of_values_with_trailing_spaces.append(value)
