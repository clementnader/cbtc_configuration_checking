#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from .load_xl import *
from .process_block_definition import *


__all__ = ["get_block_definition"]


BLOCK_DEF_SHEET = "CDV"
BLOCK_NAME_COLUMN_TITLE = "CDV_ID"
LIMITS_LIST_COLUMN_TITLE = "LISTE EXTREMITES"
SEGMENT_LIMITS_LIST_COLUMN_TITLE = "LISTE SEGMENT_ID"
OFFSET_LIMITS_LIST_COLUMN_TITLE = "LISTE EXT_ABS_SEG"
JOINT_NAME_COLUMN_TITLE_PREFIX = "OBJET EXTREMITE "
START_ROW = 3


def get_block_definition() -> tuple[Optional[dict[str, dict[tuple[str, float], str]]], Optional[str]]:
    block_def_wb, block_def_addr = load_block_def_wb()
    if block_def_wb is None:
        return None, None
    block_def_ws = get_xl_sheet_by_name(block_def_wb, BLOCK_DEF_SHEET)
    block_name_column, segment_limits_list_column, offset_limits_list_column, joint_name_columns_list = (
        _get_columns(block_def_ws))
    if (block_name_column is None or segment_limits_list_column is None or offset_limits_list_column is None
            or not joint_name_columns_list):
        print_error(f"Block Def. file is not formatted as expected. Tool was unable to find title columns: "
                    f"{BLOCK_NAME_COLUMN_TITLE} and/or {LIMITS_LIST_COLUMN_TITLE}"
                    f"::{SEGMENT_LIMITS_LIST_COLUMN_TITLE} and/or {LIMITS_LIST_COLUMN_TITLE}"
                    f"::{OFFSET_LIMITS_LIST_COLUMN_TITLE} and/or {JOINT_NAME_COLUMN_TITLE_PREFIX}N:\n"
                    f"{block_name_column = }\n"
                    f"{segment_limits_list_column = }\n"
                    f"{offset_limits_list_column = }\n"
                    f"{joint_name_columns_list = }")
        return None, None

    block_def_dict = dict()
    for row in range(START_ROW, get_xl_number_of_rows(block_def_ws) + 1):
        block_name = get_xl_cell_value(block_def_ws, row=row, column=block_name_column)
        if block_name is None:
            continue
        limit_objects = list()
        for limit_column in joint_name_columns_list:
            limit_object = get_xl_cell_value(block_def_ws, row=row, column=limit_column)
            if limit_object is not None:
                limit_objects.append(limit_object.strip())

        segment_limits = get_xl_cell_value(block_def_ws, row=row, column=segment_limits_list_column)
        offset_limits = get_xl_cell_value(block_def_ws, row=row, column=offset_limits_list_column)
        if segment_limits is None or offset_limits is None:
            block_def_dict[block_name.strip()] = list(zip([(None, None) for _ in range(len(limit_objects))],
                                                          limit_objects))
            continue

        segment_limits_list = [seg.strip() for seg in segment_limits.split(";")]
        offset_limits_list = [float(offset.strip().replace(",", ".")) for offset in offset_limits.split(";")]
        seg_x_limits_list = list(zip(segment_limits_list, offset_limits_list))

        if len(seg_x_limits_list) != len(limit_objects):
            print_error(f"In Block Def. file, for block {block_name}, limit objects in columns "
                        f"{JOINT_NAME_COLUMN_TITLE_PREFIX}N do not correspond to the "
                        f"{LIMITS_LIST_COLUMN_TITLE}::{SEGMENT_LIMITS_LIST_COLUMN_TITLE}:\n"
                        f"{seg_x_limits_list = }\n"
                        f"{limit_objects = }")
            block_def_dict[block_name.strip()] = list(zip([(None, None) for _ in range(len(limit_objects))],
                                                          limit_objects))

        block_def_dict[block_name.strip()] = list(zip(seg_x_limits_list, limit_objects))

    block_definition_display_info = _get_block_definition_display_info(block_def_addr, BLOCK_DEF_SHEET)
    return associate_block_def_to_dc_sys(block_def_dict), block_definition_display_info


def _get_block_definition_display_info(block_def_addr: str, block_def_sheet: str) -> str:
    display_info = f"{os.path.split(block_def_addr)[-1]} (sheet \"{block_def_sheet}\")"
    return display_info


def _get_columns(block_def_ws: Union[xlrd.sheet.Sheet, xl_ws.Worksheet]
                 ) -> tuple[Optional[int], Optional[int], Optional[int], list[int]]:
    block_name_column = None
    segment_limits_list_column = None
    offset_limits_list_column = None
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
        elif (cell1 == LIMITS_LIST_COLUMN_TITLE
              and cell2 == SEGMENT_LIMITS_LIST_COLUMN_TITLE):
            if segment_limits_list_column is not None:
                print_error(f"Multiple columns have the same title {LIMITS_LIST_COLUMN_TITLE}"
                            f"::{SEGMENT_LIMITS_LIST_COLUMN_TITLE}: "
                            f"columns {segment_limits_list_column} and {column}. The first one is kept.")
            else:
                segment_limits_list_column = column
        elif (cell1 is None
              and cell2 == OFFSET_LIMITS_LIST_COLUMN_TITLE):
            if offset_limits_list_column is not None:
                print_error(f"Multiple columns have the same title {LIMITS_LIST_COLUMN_TITLE}"
                            f"::{OFFSET_LIMITS_LIST_COLUMN_TITLE}: "
                            f"columns {offset_limits_list_column} and {column}. The first one is kept.")
            else:
                offset_limits_list_column = column
        elif (cell1 is not None and cell1.startswith(JOINT_NAME_COLUMN_TITLE_PREFIX)
              or cell2 is not None and cell2.startswith(JOINT_NAME_COLUMN_TITLE_PREFIX)):
            joint_name_columns_list.append(column)
    return block_name_column, segment_limits_list_column, offset_limits_list_column, joint_name_columns_list
