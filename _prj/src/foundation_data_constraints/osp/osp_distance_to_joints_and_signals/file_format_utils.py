#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["create_empty_joint_verif_sheet", "OSP_NAME_COL", "OSP_SEG_COL", "OSP_X_COL", "OSP_DIRECTION_COL",
           "OSP_TRACK_COL", "OSP_KP_COL", "OSP_APPROACH_DIRECTION_COL", "OSP_TYPE_COL",
           "OSP_PERMANENT_STOP_COL", "OSP_PARKING_COL", "OSP_WASHING_COL",
           "JOINT_INC_NAME_COL", "JOINT_INC_DISTANCE_COL", "JOINT_DEC_NAME_COL", "JOINT_DEC_DISTANCE_COL",
           "JOINT_COMMENTS_COL",
           "create_empty_sig_verif_sheet", "SIG_INC_NAME_COL", "SIG_INC_TYPE_COL", "SIG_INC_DISTANCE_COL",
           "SIG_DEC_NAME_COL", "SIG_DEC_TYPE_COL", "SIG_DEC_DISTANCE_COL", "SIG_COMMENTS_COL"]


JOINT_VERIF_SHEET = "OSP_Joint_Dist"

OSP_NAME_COL = "A"
OSP_SEG_COL = "B"
OSP_X_COL = "C"
OSP_DIRECTION_COL = "D"
OSP_TRACK_COL = "E"
OSP_KP_COL = "F"
OSP_APPROACH_DIRECTION_COL = "G"
OSP_TYPE_COL = "H"
OSP_PERMANENT_STOP_COL = "I"
OSP_PARKING_COL = "J"
OSP_WASHING_COL = "K"

JOINT_INC_NAME_COL = "L"
JOINT_INC_DISTANCE_COL = "M"
JOINT_DEC_NAME_COL = "N"
JOINT_DEC_DISTANCE_COL = "O"
JOINT_COMMENTS_COL = "P"


def create_empty_joint_verif_sheet(wb: openpyxl.workbook.Workbook) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(JOINT_VERIF_SHEET)
    ws = wb[JOINT_VERIF_SHEET]
    # Set the new sheet as active
    wb.active = ws
    # Set properties and display options for the sheet
    _set_rows_height(ws)
    _set_columns_width(ws)
    _set_joint_columns_width(ws)
    ws.sheet_view.zoomScale = 100  # set zoom level to 100 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display
    # Write columns titles
    row = 1
    _write_columns_title(ws, row)
    _write_joint_columns_title(ws, row)
    # Set filter
    row += 1
    ws.auto_filter.ref = f"A{row}:{JOINT_COMMENTS_COL}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"B{row}"
    return ws, row


def _set_rows_height(ws: xl_ws.Worksheet):
    ws.row_dimensions[1].height = 30


def _set_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[OSP_NAME_COL].width = 23
    ws.column_dimensions[OSP_SEG_COL].width = 10
    ws.column_dimensions[OSP_X_COL].width = 7.5
    ws.column_dimensions[OSP_DIRECTION_COL].width = 14
    ws.column_dimensions[OSP_TRACK_COL].width = 14
    ws.column_dimensions[OSP_KP_COL].width = 8.5
    ws.column_dimensions[OSP_APPROACH_DIRECTION_COL].width = 14
    ws.column_dimensions[OSP_TYPE_COL].width = 14
    ws.column_dimensions[OSP_PERMANENT_STOP_COL].width = 14
    ws.column_dimensions[OSP_PARKING_COL].width = 14
    ws.column_dimensions[OSP_WASHING_COL].width = 14


def _set_joint_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[JOINT_INC_NAME_COL].width = 40
    ws.column_dimensions[JOINT_INC_DISTANCE_COL].width = 17
    ws.column_dimensions[JOINT_DEC_NAME_COL].width = 40
    ws.column_dimensions[JOINT_DEC_DISTANCE_COL].width = 17
    ws.column_dimensions[JOINT_COMMENTS_COL].width = 40


def _write_columns_title(ws: xl_ws.Worksheet, row: int):
    # OSP name
    create_merged_cell(ws, f"OSP Name", start_row=row, end_row=row+1,
                       start_column=OSP_NAME_COL, end_column=OSP_NAME_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_yellow)
    # OSP Position
    create_merged_cell(ws, f"OSP Position", start_row=row, end_row=row,
                       start_column=OSP_SEG_COL, end_column=OSP_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Seg", row=row+1, column=OSP_SEG_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"X", row=row+1, column=OSP_X_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Direction", row=row+1, column=OSP_DIRECTION_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Track", row=row+1, column=OSP_TRACK_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"KP", row=row+1, column=OSP_KP_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    # Approach Direction
    create_merged_cell(ws, f"Approach Direction", start_row=row, end_row=row+1,
                       start_column=OSP_APPROACH_DIRECTION_COL, end_column=OSP_APPROACH_DIRECTION_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    # OSP Type
    create_merged_cell(ws, f"Alignment Type", start_row=row, end_row=row+1,
                       start_column=OSP_TYPE_COL, end_column=OSP_TYPE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_pink)
    # Automatic Driving Permanent Stop
    create_merged_cell(ws, f"Automatic Driving Permanent Stop", start_row=row, end_row=row+1,
                       start_column=OSP_PERMANENT_STOP_COL, end_column=OSP_PERMANENT_STOP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Parking Position
    create_merged_cell(ws, f"Parking Position", start_row=row, end_row=row+1,
                       start_column=OSP_PARKING_COL, end_column=OSP_PARKING_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Washing Related
    create_merged_cell(ws, f"Washing Related", start_row=row, end_row=row+1,
                       start_column=OSP_WASHING_COL, end_column=OSP_WASHING_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)


def _write_joint_columns_title(ws: xl_ws.Worksheet, row: int):
    # Next IVB Joint in increasing direction
    create_merged_cell(ws, f"Next IVB Joint in increasing direction", start_row=row, end_row=row,
                       start_column=JOINT_INC_NAME_COL, end_column=JOINT_INC_DISTANCE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"IVB Joint Name", row=row+1, column=JOINT_INC_NAME_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"Distance from OSP to joint", row=row+1, column=JOINT_INC_DISTANCE_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan,
                line_wrap=True)
    # Next IVB Joint in decreasing direction
    create_merged_cell(ws, f"Next IVB Joint in decreasing direction", start_row=row, end_row=row,
                       start_column=JOINT_DEC_NAME_COL, end_column=JOINT_DEC_DISTANCE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    create_cell(ws, f"IVB Joint Name", row=row+1, column=JOINT_DEC_NAME_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    create_cell(ws, f"Distance from OSP to joint", row=row+1, column=JOINT_DEC_DISTANCE_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue,
                line_wrap=True)
    # Automatic Comments
    create_merged_cell(ws, f"Automatic Comments", start_row=row, end_row=row+1,
                       start_column=JOINT_COMMENTS_COL, end_column=JOINT_COMMENTS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)


SIG_VERIF_SHEET = "OSP_Sig_Dist"

SIG_INC_NAME_COL = "L"
SIG_INC_TYPE_COL = "M"
SIG_INC_DISTANCE_COL = "N"
SIG_DEC_NAME_COL = "O"
SIG_DEC_TYPE_COL = "P"
SIG_DEC_DISTANCE_COL = "Q"
SIG_COMMENTS_COL = "R"


def create_empty_sig_verif_sheet(wb: openpyxl.workbook.Workbook) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(SIG_VERIF_SHEET)
    ws = wb[SIG_VERIF_SHEET]
    # Set properties and display options for the sheet
    _set_rows_height(ws)
    _set_columns_width(ws)
    _set_sig_columns_width(ws)
    ws.sheet_view.zoomScale = 100  # set zoom level to 100 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display
    # Write columns titles
    row = 1
    _write_columns_title(ws, row)
    _write_sig_columns_title(ws, row)
    # Set filter
    row += 1
    ws.auto_filter.ref = f"A{row}:{SIG_COMMENTS_COL}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"B{row}"
    return ws, row


def _set_sig_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[SIG_INC_NAME_COL].width = 23
    ws.column_dimensions[SIG_INC_TYPE_COL].width = 18
    ws.column_dimensions[SIG_INC_DISTANCE_COL].width = 17
    ws.column_dimensions[SIG_DEC_NAME_COL].width = 23
    ws.column_dimensions[SIG_DEC_TYPE_COL].width = 18
    ws.column_dimensions[SIG_DEC_DISTANCE_COL].width = 17
    ws.column_dimensions[SIG_COMMENTS_COL].width = 40


def _write_sig_columns_title(ws: xl_ws.Worksheet, row: int):
    # Next Signal in increasing direction
    create_merged_cell(ws, f"Next Signal in increasing direction", start_row=row, end_row=row,
                       start_column=SIG_INC_NAME_COL, end_column=SIG_INC_DISTANCE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"Signal Name", row=row+1, column=SIG_INC_NAME_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"Signal Type", row=row+1, column=SIG_INC_TYPE_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"Distance from OSP to signal", row=row+1, column=SIG_INC_DISTANCE_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan,
                line_wrap=True)
    # Next Signal in decreasing direction
    create_merged_cell(ws, f"Next Signal in decreasing direction", start_row=row, end_row=row,
                       start_column=SIG_DEC_NAME_COL, end_column=SIG_DEC_DISTANCE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    create_cell(ws, f"Signal Name", row=row+1, column=SIG_DEC_NAME_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    create_cell(ws, f"Signal Type", row=row+1, column=SIG_DEC_TYPE_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    create_cell(ws, f"Distance from OSP to signal", row=row+1, column=SIG_DEC_DISTANCE_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue,
                line_wrap=True)
    # Automatic Comments
    create_merged_cell(ws, f"Automatic Comments", start_row=row, end_row=row+1,
                       start_column=SIG_COMMENTS_COL, end_column=SIG_COMMENTS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
