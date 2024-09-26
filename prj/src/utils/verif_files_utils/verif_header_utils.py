#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..xl_pkg import *
from ..subprocess_utils import *
from ..database_location_utils import *
from ..time_utils import *


__all__ = ["update_header_sheet_for_verif_file"]


HEADER_SHEET_NAME = "Header"

AUTHOR_CELL = "C24"
FILES_FIRST_CELL = "D27"


def update_header_sheet_for_verif_file(wb: openpyxl.workbook.Workbook, tool_name: str = None,
                                       tool_version: str = None, survey: list[str] = None) -> None:
    ws = get_xl_sheet_by_name(wb, HEADER_SHEET_NAME)
    update_author_name(ws)
    update_sa_versions(ws, tool_name, tool_version, survey)


def update_author_name(ws: xl_ws.Worksheet) -> None:
    user_full_name = get_user_full_name()
    if user_full_name == "":
        return
    create_cell(ws, user_full_name, cell=AUTHOR_CELL, align_horizontal=XlAlign.center, bold=True, borders=True)


C_D470 = "C_D470"
C11_D470 = "C11_D470"
C121_D470 = "C121_D470"
DATE = "DATE"


def update_sa_versions(ws: xl_ws.Worksheet, tool_name: str = None, tool_version: str = None,
                       survey: list[str] = None) -> None:
    first_row, info_column = get_row_and_column_from_cell(FILES_FIRST_CELL)
    title_column = info_column - 1

    for row in range(first_row, get_xl_number_of_rows(ws) + 1):
        title = get_xl_cell_value(ws, row=row, column=title_column).upper().strip()

        if title.startswith(C_D470):
            create_cell(ws, get_c_d470_version(), row=row, column=info_column, borders=True)

        elif title.startswith(C11_D470):
            create_cell(ws, get_c11_d470_version(), row=row, column=info_column, borders=True)

        elif title.startswith(C121_D470):
            create_cell(ws, get_c121_d470_version(), row=row, column=info_column, borders=True)

        elif title.startswith(DATE):
            create_cell(ws, get_today_date(), row=row, column=info_column, borders=True)

        elif (tool_name is not None and tool_version is not None
              and title.startswith(f"{tool_name.upper()} VERSION")):
            create_cell(ws, tool_version, row=row, column=info_column, borders=True)

        elif survey and title.startswith("SURVEY"):
            title = f"Survey file{'s' if len(survey) > 1 else ''}:"
            create_cell(ws, title, row=row, column=title_column, borders=True)

            info = "\n - ".join(survey)
            if len(survey) > 1:
                info = " - " + info
            create_cell(ws, info, row=row, column=info_column, borders=True, line_wrap=True)
