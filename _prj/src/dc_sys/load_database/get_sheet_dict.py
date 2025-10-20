#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


__all__ = ["get_sheet_dict"]


START_ROW = 3
DEFAULT_NAME_COLUMN = 1


def get_sheet_dict(ws: xlrd.sheet.Sheet, columns_dict: dict[str, Any],
                   generic_object_name: dict[str, Any]) -> dict[str, dict]:
    sheet_dict = dict()
    if generic_object_name is not None:
        return _get_generic_sheet_dict(ws, columns_dict, generic_object_name)
    for row in range(START_ROW, ws.nrows + 1):
        object_name = get_xlrd_value(ws, row, DEFAULT_NAME_COLUMN)
        if object_name is None:
            continue
        if object_name in sheet_dict:
            print_error(f"Two objects have the same name {Color.beige}{object_name}{Color.reset} at {Color.orange}rows "
                        f"{sheet_dict[object_name]['ws_row']} and {row}{Color.reset} "
                        f"in sheet {Color.blue}{ws.name}{Color.reset}.")
            continue  # keep the first value
        sheet_dict[object_name] = get_info_for_object(ws, row, columns_dict)
    return sheet_dict


def _get_generic_sheet_dict(ws: xlrd.sheet.Sheet, columns_dict: dict[str, Any],
                            generic_object_name: dict[str, Any]) -> dict[str, dict[str, Any]]:
    temp_dict = dict()
    columns: list = generic_object_name["columns"]
    for row in range(START_ROW, ws.nrows + 1):
        object_name = get_xlrd_value(ws, row, DEFAULT_NAME_COLUMN)
        if object_name is not None:
            info_for_object = get_info_for_object(ws, row, columns_dict)
            key = _get_generic_sheet_object_key(columns, info_for_object)
            temp_dict[key] = info_for_object
    # temp_dict = {key: temp_dict[key] for key in sorted(temp_dict.keys())}
    sheet_dict = {f"{ws.name}_row{val['ws_row']}": val for val in temp_dict.values()}
    return sheet_dict


def _get_generic_sheet_object_key(columns: list, info_for_object):
    keys = list()
    for column in columns:
        column_attr = column["attribute"]
        column_type = column["type"]
        if "column" in column_attr:
            try:
                key = column_type(info_for_object[column_attr["attribute_name"]])
            except (ValueError, TypeError):
                key = info_for_object[column_attr["attribute_name"]]
        else:
            try:
                key = column_type(info_for_object[column_attr["attribute_name"]][column_attr["sub_attribute_name"]][0])
            except (ValueError, TypeError):
                key = info_for_object[column_attr["attribute_name"]]
        keys.append(key)
    return tuple(keys)


def get_info_for_object(ws: xlrd.sheet.Sheet, row: int, columns_dict: dict[str, Any]):
    info_dict = dict()
    info_dict["ws_row"] = row
    for key, column in columns_dict.items():
        if isinstance(column, int):
            value = get_xlrd_float_value(ws, row, column)
            check_value_has_spaces(ws.name, value, row, column, key)
            if isinstance(value, str):
                value = value.strip()
            info_dict[key] = value
        else:
            info_dict[key] = _get_sub_attribute_list_info(ws, row, column)
    return info_dict


def _get_sub_attribute_list_info(ws: xlrd.sheet.Sheet, row: int, sub_dict: dict[str, list[int]]):
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


G_LIST_OF_VALUES_WITH_LEADING_SPACES = list()
G_LIST_OF_VALUES_WITH_TRAILING_SPACES = list()


def check_value_has_spaces(sheet_name, value, row, column, key):
    global G_LIST_OF_VALUES_WITH_LEADING_SPACES, G_LIST_OF_VALUES_WITH_TRAILING_SPACES
    if isinstance(value, str) and not value.replace(" ", ""):
        # Only spaces in the cell
        if not any(value.startswith(old_value) for old_value in G_LIST_OF_VALUES_WITH_LEADING_SPACES):
            print_warning(f"There is a cell containing only space in sheet {Color.yellow}{sheet_name}{Color.reset} "
                          f"at cell {Color.blue}{get_xl_column_letter(column)}{row}{Color.reset}:\n\t"
                          f"key column name: {Color.beige}\"{key}\"{Color.reset}, "
                          f"value: {Color.white}\"{value}\"{Color.reset}")
            # G_LIST_OF_VALUES_WITH_LEADING_SPACES.append(value)
        return

    if isinstance(value, str) and value.startswith(" "):
        # Leading space in the cell
        if not any(value.startswith(old_value) for old_value in G_LIST_OF_VALUES_WITH_LEADING_SPACES):
            print_warning(f"There is a leading space in sheet {Color.yellow}{sheet_name}{Color.reset} "
                          f"at cell {Color.blue}{get_xl_column_letter(column)}{row}{Color.reset}:\n\t"
                          f"key column name: {Color.beige}\"{key}\"{Color.reset}, "
                          f"value: {Color.white}\"{value}\"{Color.reset}")
            # G_LIST_OF_VALUES_WITH_LEADING_SPACES.append(value)

    if isinstance(value, str) and value.endswith(" "):
        # Trailing space in the cell
        if not any(value.startswith(old_value) for old_value in G_LIST_OF_VALUES_WITH_LEADING_SPACES):
            print_warning(f"There is a trailing space in sheet {Color.yellow}{sheet_name}{Color.reset} "
                          f"at cell {Color.blue}{get_xl_column_letter(column)}{row}{Color.reset}:\n\t"
                          f"key column name: {Color.beige}\"{key}\"{Color.reset}, "
                          f"value: {Color.white}\"{value}\"{Color.reset}")
            # G_LIST_OF_VALUES_WITH_LEADING_SPACES.append(value)

    if ((sheet_name, key) in [("Quai", "Nom"), ("Quai", "Abreviation"),
                              ("Bal", "TypePose"),
                              ("Driving_Modes", "Name"),
                              ("Wayside_Eqpt", "Location"),
                              ("Flux_PAS_MES", "ClasseObjet"),
                              ("Flux_MES_PAS", "ClasseObjet"),]
            or "Comment" in key):
        return  # Some cells can have space inside in a standard way.
    if isinstance(value, str) and " " in value[1:-1]:
        # Space in the cell, some information can contain spaces
        if not any(value.endswith(old_value) for old_value in G_LIST_OF_VALUES_WITH_TRAILING_SPACES):
            print_warning(f"There is a space inside the word in sheet {Color.yellow}{sheet_name}{Color.reset} "
                          f"at cell {Color.blue}{get_xl_column_letter(column)}{row}{Color.reset}:\n\t"
                          f"key column name: {Color.beige}\"{key}\"{Color.reset}, "
                          f"value: {Color.white}\"{value}\"{Color.reset}")
            # G_LIST_OF_VALUES_WITH_TRAILING_SPACES.append(value)
