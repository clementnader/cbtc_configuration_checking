#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .load_xl import *


__all__ = ["get_block_definition"]


BLOCK_DEF_SHEET = "CDV"
BLOCK_NAME_COLUMN_TITLE = "CDV_ID"
JOINT_NAME_COLUMN_TITLE_PREFIX = "OBJET EXTREMITE "
START_ROW = 3


def get_block_definition() -> Optional[dict[str, list[str]]]:
    block_def_wb = load_block_def_wb()
    if block_def_wb is None:
        return None
    block_def_ws = get_xl_sheet_by_name(block_def_wb, BLOCK_DEF_SHEET)
    block_name_column, joint_name_columns_list = _get_columns(block_def_ws)
    if block_name_column is None or not joint_name_columns_list:
        print_error(f"Block Def. file is not formatted as expected. Tool was unable to find title columns: "
                    f"{BLOCK_NAME_COLUMN_TITLE} and/or {JOINT_NAME_COLUMN_TITLE_PREFIX}N.")
        return None

    block_def_dict = dict()
    for row in range(START_ROW, get_xl_number_of_rows(block_def_ws) + 1):
        block_name = get_xl_cell_value(block_def_ws, row=row, column=block_name_column)
        limit_objects = list()
        for limit_column in joint_name_columns_list:
            limit_object = get_xl_cell_value(block_def_ws, row=row, column=limit_column)
            if limit_object is not None:
                limit_objects.append(limit_object)
        block_def_dict[block_name] = limit_objects
    return block_def_dict


def _get_columns(block_def_ws: Union[xlrd.sheet.Sheet, xl_ws.Worksheet]) -> tuple[Optional[int], list[int]]:
    block_name_column = None
    joint_name_columns_list = list()
    for column in range(1, get_xl_number_of_columns(block_def_ws) + 1):
        cell1 = get_xl_cell_value(block_def_ws, row=1, column=column)
        cell2 = get_xl_cell_value(block_def_ws, row=2, column=column)
        if cell1 == BLOCK_NAME_COLUMN_TITLE or cell2 == BLOCK_NAME_COLUMN_TITLE:
            if block_name_column is not None:
                print_error(f"Multiple columns have the same title {BLOCK_NAME_COLUMN_TITLE}: "
                            f"columns {block_name_column} and {column}. The first one is kept.")
            else:
                block_name_column = column
        elif (cell1 is not None and cell1.startswith(JOINT_NAME_COLUMN_TITLE_PREFIX)
              or cell2 is not None and cell2.startswith(JOINT_NAME_COLUMN_TITLE_PREFIX)):
            joint_name_columns_list.append(column)
    return block_name_column, joint_name_columns_list
