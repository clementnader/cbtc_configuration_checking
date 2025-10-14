#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .....utils import *


__all__ = ["create_empty_values_sheet", "NB_PMC",
           "PARAMETER_NAME_COLUMN", "PMC_FIRST_COLUMN", "STATUS_COLUMN", "COMMENTS_COLUMN",
           "IP_ADDRESS_STATUS2_COLUMN", "IP_ADDRESS_COMMENTS2_COLUMN"]


NB_PMC = 3

PARAMETER_NAME_COLUMN = 1
PMC_FIRST_COLUMN = 2
STATUS_COLUMN = 5
COMMENTS_COLUMN = 6
IP_ADDRESS_STATUS2_COLUMN = 7
IP_ADDRESS_COMMENTS2_COLUMN = 8


def create_empty_values_sheet(wb: openpyxl.workbook.Workbook, ws_name: str,
                               column_name: str, extra_column: str = None, set_active: bool = False
                               ) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(ws_name)
    ws = wb[ws_name]
    if set_active:
        # Set the new sheet as active
        wb.active = ws
    # Set properties and display options for the sheet
    ws.row_dimensions[1].height = 23.25
    ws.row_dimensions[2].height = 23.25
    _set_columns_width(ws, extra_column)
    ws.sheet_view.zoomScale = 85  # set zoom level to 85 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display
    _set_conditional_formatting(ws, extra_column)
    # Write columns titles
    row = 1
    max_col = _write_columns_title(ws, row, column_name, extra_column)
    # Set filter
    row += 1
    ws.auto_filter.ref = f"A{row}:{get_xl_column_letter(max_col)}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"A{row}"
    return ws, row


def _set_columns_width(ws: xl_ws.Worksheet, extra_column: Optional[str]):
    ws.column_dimensions[get_xl_column_letter(PARAMETER_NAME_COLUMN)].width = 30.5
    for column in range(PMC_FIRST_COLUMN, PMC_FIRST_COLUMN + NB_PMC):
        ws.column_dimensions[get_xl_column_letter(column)].width = 13.5
    ws.column_dimensions[get_xl_column_letter(STATUS_COLUMN)].width = 12.5
    ws.column_dimensions[get_xl_column_letter(COMMENTS_COLUMN)].width = 49.5
    if extra_column:
        ws.column_dimensions[get_xl_column_letter(IP_ADDRESS_STATUS2_COLUMN)].width = 33
        ws.column_dimensions[get_xl_column_letter(IP_ADDRESS_COMMENTS2_COLUMN)].width = 49.5


def _set_conditional_formatting(ws: xl_ws.Worksheet, extra_column: Optional[str]):
    status_range = get_cell_range(start_column=STATUS_COLUMN, end_column=STATUS_COLUMN)
    if extra_column:
        # Multiple ranges are separated by a space in openpyxl cell ranges
        status_range += " " + get_cell_range(start_column=IP_ADDRESS_STATUS2_COLUMN,
                                             end_column=IP_ADDRESS_STATUS2_COLUMN)

    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"OK\"", font_color=XlFontColor.ok, bg_color=XlBgColor.ok)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"KO\"", font_color=XlFontColor.ko, bg_color=XlBgColor.ko)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"NA\"", font_color=XlFontColor.na, bg_color=XlBgColor.na)


def _write_columns_title(ws: xl_ws.Worksheet, row: int, column_name: str, extra_column: Optional[str]) -> int:
    # Parameter Name
    create_merged_cell(ws, None, start_row=row, end_row=row+1,
                       start_column=PARAMETER_NAME_COLUMN, end_column=PARAMETER_NAME_COLUMN,
                       align_horizontal=XlAlign.center, bold=True, font_size=14)
    # PMC Address or Public Key
    create_merged_cell(ws, column_name, start_row=row, end_row=row+1,
                       start_column=PMC_FIRST_COLUMN, end_column=PMC_FIRST_COLUMN + (NB_PMC-1),
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_yellow,
                       font_size=14)
    # Status
    create_merged_cell(ws, "Unicity", start_row=row, end_row=row+1,
                       start_column=STATUS_COLUMN, end_column=STATUS_COLUMN,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange,
                       font_size=14)
    # Comments
    create_merged_cell(ws, "Comments", start_row=row, end_row=row+1,
                       start_column=COMMENTS_COLUMN, end_column=COMMENTS_COLUMN,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.light_grey,
                       font_size=14)
    if not extra_column:
        return COMMENTS_COLUMN
    else:
        # Second Status
        create_merged_cell(ws, extra_column, start_row=row, end_row=row+1,
                           start_column=IP_ADDRESS_STATUS2_COLUMN, end_column=IP_ADDRESS_STATUS2_COLUMN,
                           align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange,
                           font_size=14)
        # Second Comments
        create_merged_cell(ws, "Comments", start_row=row, end_row=row+1,
                           start_column=IP_ADDRESS_COMMENTS2_COLUMN, end_column=IP_ADDRESS_COMMENTS2_COLUMN,
                           align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.light_grey,
                           font_size=14)
        return IP_ADDRESS_COMMENTS2_COLUMN
