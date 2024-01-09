#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common_utils import *
from ..xl_pkg import *
from ..subprocess_utils import *
from ..database_location_utils import *
from ..time_utils import *


__all__ = ["update_header_sheet_for_verif_file"]


HEADER_SHEET_NAME = "Header"

AUTHOR_CELL = "C24"
FILES_FIRST_CELL = "D27"


def update_header_sheet_for_verif_file(wb: openpyxl.workbook.Workbook) -> None:
    ws = get_xl_sheet_by_name(wb, HEADER_SHEET_NAME)
    update_author_name(ws)
    date_cell = update_sa_versions(ws)
    update_date(ws, date_cell)


def update_author_name(ws: xl_ws.Worksheet) -> None:
    user_full_name = get_user_full_name()
    if user_full_name == "":
        return
    create_cell(ws, user_full_name, cell=AUTHOR_CELL, center_horizontal=True, bold=True, borders=True)


C_D470 = "C_D470"
C11_D470 = "C11_D470"
C121_D470 = "C121_D470"
DATE = "DATE"


def update_sa_versions(ws: xl_ws.Worksheet) -> Optional[tuple[int, int]]:
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
            return row, info_column
    return None


def update_date(ws: xl_ws.Worksheet, date_cell: Optional[tuple[int, int]]) -> None:
    if date_cell is None:
        return
    date_row, info_column = date_cell
    create_cell(ws, get_today_date(), row=date_row, column=info_column, borders=True)
