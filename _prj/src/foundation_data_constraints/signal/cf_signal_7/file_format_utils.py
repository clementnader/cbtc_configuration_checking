#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["create_empty_verif_sheet", "create_constraint_sheet",
           "SIGNAL_NAME_COL", "SIGNAL_SEG_COL", "SIGNAL_X_COL", "SIGNAL_DIRECTION_COL",
           "SIGNAL_TRACK_COL", "SIGNAL_KP_COL", "TYPE_COL", "VSP_DIST_COL", "NEXT_SWITCH_COL",
           "DANGER_POINT_COL", "DIST_TO_SWITCH_COL", "FP_DIST_COL", "DIST_TO_FP_COL",
           "STATUS_COL", "COMMENTS_COL"]


VERIF_SHEET = "CF_SIGNAL_7"

SIGNAL_NAME_COL = "A"
SIGNAL_SEG_COL = "B"
SIGNAL_X_COL = "C"
SIGNAL_DIRECTION_COL = "D"
SIGNAL_TRACK_COL = "E"
SIGNAL_KP_COL = "F"
TYPE_COL = "G"
VSP_DIST_COL = "H"
NEXT_SWITCH_COL = "I"
DANGER_POINT_COL = "J"
DIST_TO_SWITCH_COL = "K"
FP_DIST_COL = "L"
DIST_TO_FP_COL = "M"
STATUS_COL = "N"
COMMENTS_COL = "O"


def create_empty_verif_sheet(wb: openpyxl.workbook.Workbook) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(VERIF_SHEET)
    ws = wb[VERIF_SHEET]
    # Set the new sheet as active
    wb.active = ws
    # Set properties and display options for the sheet
    _set_columns_width(ws)
    ws.sheet_view.zoomScale = 100  # set zoom level to 100 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display
    _set_conditional_formatting(ws)
    # Write columns titles
    row = 1
    _write_columns_title(ws, row)
    # Set filter
    row += 1
    ws.auto_filter.ref = f"A{row}:{COMMENTS_COL}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"B{row}"
    return ws, row


def _set_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[SIGNAL_NAME_COL].width = 23
    ws.column_dimensions[SIGNAL_SEG_COL].width = 10
    ws.column_dimensions[SIGNAL_X_COL].width = 7.5
    ws.column_dimensions[SIGNAL_DIRECTION_COL].width = 13
    ws.column_dimensions[SIGNAL_TRACK_COL].width = 14
    ws.column_dimensions[SIGNAL_KP_COL].width = 8.5
    ws.column_dimensions[TYPE_COL].width = 19
    ws.column_dimensions[VSP_DIST_COL].width = 16
    ws.column_dimensions[NEXT_SWITCH_COL].width = 23
    ws.column_dimensions[DANGER_POINT_COL].width = 14
    ws.column_dimensions[DIST_TO_SWITCH_COL].width = 16
    ws.column_dimensions[FP_DIST_COL].width = 13
    ws.column_dimensions[DIST_TO_FP_COL].width = 16
    ws.column_dimensions[STATUS_COL].width = 8.5
    ws.column_dimensions[COMMENTS_COL].width = 39


def _set_conditional_formatting(ws: xl_ws.Worksheet):
    # Status Conditional Formatting
    status_range = get_cell_range(start_column=STATUS_COL, end_column=STATUS_COL)

    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"OK\"", font_color=XlFontColor.ok, bg_color=XlBgColor.ok)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"KO\"", font_color=XlFontColor.ko, bg_color=XlBgColor.ko)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"NA\"", font_color=XlFontColor.na, bg_color=XlBgColor.na)


def _write_columns_title(ws: xl_ws.Worksheet, row: int):
    # Signal name
    create_merged_cell(ws, f"Signal Name", start_row=row, end_row=row+1,
                       start_column=SIGNAL_NAME_COL, end_column=SIGNAL_NAME_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_yellow)
    # Signal Position
    create_merged_cell(ws, f"Seg", start_row=row, end_row=row+1,
                       start_column=SIGNAL_SEG_COL, end_column=SIGNAL_SEG_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_merged_cell(ws, f"X", start_row=row, end_row=row+1,
                       start_column=SIGNAL_X_COL, end_column=SIGNAL_X_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_merged_cell(ws, f"Direction", start_row=row, end_row=row+1,
                       start_column=SIGNAL_DIRECTION_COL, end_column=SIGNAL_DIRECTION_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_merged_cell(ws, f"Track", start_row=row, end_row=row+1,
                       start_column=SIGNAL_TRACK_COL, end_column=SIGNAL_TRACK_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_merged_cell(ws, f"KP", start_row=row, end_row=row+1,
                       start_column=SIGNAL_KP_COL, end_column=SIGNAL_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    # Type
    create_merged_cell(ws, f"Type", start_row=row, end_row=row+1,
                       start_column=TYPE_COL, end_column=TYPE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # VSP Distance
    create_merged_cell(ws, f"VSP Distance", start_row=row, end_row=row+1,
                       start_column=VSP_DIST_COL, end_column=VSP_DIST_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_pink)
    # Next switch after signal
    create_merged_cell(ws, f"Next switch after signal", start_row=row, end_row=row+1,
                       start_column=NEXT_SWITCH_COL, end_column=NEXT_SWITCH_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Danger Point Type
    create_merged_cell(ws, f"Danger Point Type", start_row=row, end_row=row+1,
                       start_column=DANGER_POINT_COL, end_column=DANGER_POINT_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Distance to switch
    create_merged_cell(ws, f"Distance to switch", start_row=row, end_row=row+1,
                       start_column=DIST_TO_SWITCH_COL, end_column=DIST_TO_SWITCH_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Fouling Point Distance
    create_merged_cell(ws, f"Fouling Point Distance", start_row=row, end_row=row+1,
                       start_column=FP_DIST_COL, end_column=FP_DIST_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    # Distance to Fouling Point
    create_merged_cell(ws, f"Distance to Fouling Point", start_row=row, end_row=row+1,
                       start_column=DIST_TO_FP_COL, end_column=DIST_TO_FP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    # Status
    create_merged_cell(ws, f"Status", start_row=row, end_row=row+1,
                       start_column=STATUS_COL, end_column=STATUS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
    # Comments
    create_merged_cell(ws, "Comments", start_row=row, end_row=row+1,
                       start_column=COMMENTS_COL, end_column=COMMENTS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)


CONSTRAINT_SHEET = "Constraint"

CONSTRAINT_DESCRIPTION_CELL_RANGE = "B4:N17"

CONSTRAINT_DESCRIPTION = """CF_SIGNAL_7:
 - If the signal protects a fouling point, the location of the VSP shall be provided upstream the fouling point (according to direction of the signal).
 - If the signal protects a switch point, the location of the VSP shall be provided upstream the switch point (according to direction of the signal)."""


def create_constraint_sheet(wb: openpyxl.workbook.Workbook):
    wb.create_sheet(CONSTRAINT_SHEET)
    ws = wb[CONSTRAINT_SHEET]
    # Set properties and display options for the sheet
    ws.sheet_view.zoomScale = 120  # set zoom level to 120 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display

    create_merged_cell(ws, CONSTRAINT_DESCRIPTION, cell_range=CONSTRAINT_DESCRIPTION_CELL_RANGE, borders=True)
    select_cell(ws, cell=CONSTRAINT_DESCRIPTION_CELL_RANGE.split(":")[0])
