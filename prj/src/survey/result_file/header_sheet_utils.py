#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...dc_sys import *


__all__ = ["create_survey_header_sheet"]


TOOL_NAME = "Survey_Checking"

HEADER_SHEET_NAME = "Header"

FIRST_COLUMN = "B"
LAST_COLUMN = "F"

TITLE_CELL_FIRST_ROW = 11
TITLE_CELL_DELTA_ROWS = 7

AUTHOR_COLUMN = "C"
VERIFIER_COLUMN = "D"
APPROVER_COLUMN = "E"

TITLE_COLUMN = "C"
INFO_COLUMN = "D"


def create_survey_header_sheet(wb: openpyxl.workbook.Workbook, tool_version: str,
                               survey_display_info_list: list[str], block_definition_display_info: Optional[str]
                               ) -> None:
    ws = get_xl_sheet_by_name(wb, HEADER_SHEET_NAME)
    # Add title cell
    row = _add_title_cells(ws, title="Correspondence with Site Survey")
    # Add authors cells
    row = _add_authors_cells(ws, row + 2)
    # Add info cells
    _add_info_cells(ws, row + 2, tool_version, survey_display_info_list, block_definition_display_info)


def _add_title_cells(ws: xl_ws.Worksheet, title: str) -> int:
    row = TITLE_CELL_FIRST_ROW
    create_merged_cell(ws, title,
                       start_column=FIRST_COLUMN, end_column=LAST_COLUMN,
                       start_row=row, end_row=row + TITLE_CELL_DELTA_ROWS,
                       borders=True, bold=True, font_size=20, align_horizontal=XlAlign.center)
    row += TITLE_CELL_DELTA_ROWS + 1
    return row


def _add_authors_cells(ws: xl_ws.Worksheet, row: int) -> int:
    create_cell(ws, "Author", row=row, column=AUTHOR_COLUMN, borders=True, bold=True, italic=True,
                align_horizontal=XlAlign.center)
    create_cell(ws, "Verifier", row=row, column=VERIFIER_COLUMN, borders=True, bold=True, italic=True,
                align_horizontal=XlAlign.center)
    create_cell(ws, "Approver", row=row, column=APPROVER_COLUMN, borders=True, bold=True, italic=True,
                align_horizontal=XlAlign.center)
    row += 1
    user_full_name = get_user_full_name()
    create_cell(ws, user_full_name, row=row, column=AUTHOR_COLUMN, borders=True, bold=True,
                align_horizontal=XlAlign.center)
    create_cell(ws, None, row=row, column=VERIFIER_COLUMN, borders=True, bold=True,
                align_horizontal=XlAlign.center)
    create_cell(ws, None, row=row, column=APPROVER_COLUMN, borders=True, bold=True,
                align_horizontal=XlAlign.center)
    row += 1
    return row


def _add_info_cells(ws: xl_ws.Worksheet, row: int, tool_version: str, survey: list[str], block_def: Optional[str]
                    ) -> None:
    # Core CBTC Referential
    create_cell(ws, "Core CBTC Referential:", row=row, column=TITLE_COLUMN, borders=True, bold=True)
    create_cell(ws, None, row=row, column=INFO_COLUMN, borders=True)
    # C_D470
    row += 1
    create_cell(ws, "C_D470:", row=row, column=TITLE_COLUMN, borders=True, bold=True)
    create_cell(ws, get_c_d470_version(), row=row, column=INFO_COLUMN, borders=True)
    # Survey file(s)
    row += 1
    create_cell(ws, f"Survey file{'s' if len(survey) > 1 else ''}:",
                row=row, column=TITLE_COLUMN, borders=True, bold=True)
    survey_info = "\n - ".join(survey)
    if len(survey) > 1:
        survey_info = " - " + survey_info
    create_cell(ws, survey_info,
                row=row, column=INFO_COLUMN, borders=True, line_wrap=True)
    # Block Definition file
    if block_def is not None:
        row += 1
        create_cell(ws, "Block Definition file:", row=row, column=TITLE_COLUMN, borders=True, bold=True)
        create_cell(ws, block_def, row=row, column=INFO_COLUMN, borders=True)
    # Date
    row += 1
    create_cell(ws, "Date:", row=row, column=TITLE_COLUMN, borders=True, bold=True)
    create_cell(ws, get_today_date(), row=row, column=INFO_COLUMN, borders=True)
    # Tool Version
    row += 1
    create_cell(ws, f"{TOOL_NAME} Version:", row=row, column=TITLE_COLUMN, borders=True, bold=True)
    create_cell(ws, tool_version, row=row, column=INFO_COLUMN, borders=True)
