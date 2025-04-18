#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["create_empty_verif_sheet",
           "VB_NAME_COL", "ZE_IMPACTED_BY_EB_COL", "ZE_ID_COL", "DIRECTION_COL", "AUTOMATIC_COMMENTS_COL"]


VERIF_SHEET = "CBTC_APZ_Verif"

VB_NAME_COL = "A"
ZE_IMPACTED_BY_EB_COL = "B"
ZE_ID_COL = "C"
DIRECTION_COL = "D"
AUTOMATIC_COMMENTS_COL = "E"


def create_empty_verif_sheet(wb: openpyxl.workbook.Workbook, ws_name: str, first_sheet: bool = False
                             ) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(ws_name)
    ws = wb[ws_name]
    if first_sheet:
        # Set the new sheet as active for the first verif sheet
        wb.active = ws
    # Set properties and display options for the sheet
    _set_columns_width(ws)
    ws.sheet_view.zoomScale = 100  # set zoom level to 100 %
    ws.sheet_view.showGridLines = True  # turn on gridlines display
    # Write columns titles
    row = 1
    _write_columns_title(ws, row)
    # Set filter
    ws.auto_filter.ref = f"A{row}:{DIRECTION_COL}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"B{row}"
    return ws, row


def _set_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[VB_NAME_COL].width = 25
    ws.column_dimensions[ZE_IMPACTED_BY_EB_COL].width = 40
    ws.column_dimensions[ZE_ID_COL].width = 40
    ws.column_dimensions[DIRECTION_COL].width = 40


def _write_columns_title(ws: xl_ws.Worksheet, row: int):
    # VB name
    create_cell(ws, f"CV_ID", row=row, column=VB_NAME_COL, bold=True, borders=True)
    # List of ZE impacted by EB
    create_cell(ws, f"COMPUTED ZE_IMPACTE_FU", row=row, column=ZE_IMPACTED_BY_EB_COL, bold=True, borders=True)
    # List of the corresponding ZE ID
    create_cell(ws, f"COMPUTED NUMERO_ZE_IMPACTE_FU", row=row, column=ZE_ID_COL, bold=True, borders=True)
    # List of the corresponding directions
    create_cell(ws, f"COMPUTED SENS", row=row, column=DIRECTION_COL, bold=True, borders=True)
