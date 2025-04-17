#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["create_empty_verif_sheet",
           "TRACK_COL", "START_KP_COL", "END_KP_COL", "AUTOMATIC_COMMENTS_COL",
           "VERIFICATION_COL", "COMMENTS_COL"]


TRACK_COL = "A"
START_KP_COL = "B"
END_KP_COL = "C"
AUTOMATIC_COMMENTS_COL = "D"
VERIFICATION_COL = "E"
COMMENTS_COL = "F"


def create_empty_verif_sheet(wb: openpyxl.workbook.Workbook, ws_name: str,
                             dc_sys_sheet_name: str) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(ws_name)
    ws = wb[ws_name]
    # Set the new sheet as active
    wb.active = ws
    # Set properties and display options for the sheet
    ws.sheet_properties.tabColor = "FFCC99"  # orange
    ws.row_dimensions[1].height = 40
    _set_columns_width(ws)
    ws.sheet_view.zoomScale = 100  # set zoom level to 100 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display
    _set_conditional_formatting(ws)
    # Write columns titles
    row = 1
    _write_columns_title(ws, row, dc_sys_sheet_name)
    # Set filter
    row += 1
    ws.auto_filter.ref = f"A{row}:{COMMENTS_COL}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"B{row}"
    return ws, row


def _set_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[TRACK_COL].width = 30
    ws.column_dimensions[START_KP_COL].width = 20
    ws.column_dimensions[END_KP_COL].width = 20
    ws.column_dimensions[AUTOMATIC_COMMENTS_COL].width = 30
    ws.column_dimensions[VERIFICATION_COL].width = 13.5
    ws.column_dimensions[COMMENTS_COL].width = 45


def _set_conditional_formatting(ws: xl_ws.Worksheet):
    status_range = get_cell_range(start_column=VERIFICATION_COL, end_column=VERIFICATION_COL)

    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"OK\"", font_color=XlFontColor.ok, bg_color=XlBgColor.ok)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"KO\"", font_color=XlFontColor.ko, bg_color=XlBgColor.ko)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"NA\"", font_color=XlFontColor.na, bg_color=XlBgColor.na)


def _write_columns_title(ws: xl_ws.Worksheet, row: int, dc_sys_sheet_name: str):
    # Track
    create_merged_cell(ws, f"Track", start_row=row, end_row=row+1,
                       start_column=TRACK_COL, end_column=TRACK_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Start KP
    create_merged_cell(ws, f"{dc_sys_sheet_name}\nLimit 1 KP", start_row=row, end_row=row+1,
                       start_column=START_KP_COL, end_column=START_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # End KP
    create_merged_cell(ws, f"{dc_sys_sheet_name}\nLimit 2 KP", start_row=row, end_row=row+1,
                       start_column=END_KP_COL, end_column=END_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Automatic Comments
    create_merged_cell(ws, "Automatic Comments", start_row=row, end_row=row+1,
                       start_column=AUTOMATIC_COMMENTS_COL, end_column=AUTOMATIC_COMMENTS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
    # Verification
    create_merged_cell(ws, "Verification", start_row=row, end_row=row+1,
                       start_column=VERIFICATION_COL, end_column=VERIFICATION_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
    # Comments
    create_merged_cell(ws, "Comments", start_row=row, end_row=row+1,
                       start_column=COMMENTS_COL, end_column=COMMENTS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
