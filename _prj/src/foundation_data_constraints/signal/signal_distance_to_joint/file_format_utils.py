#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["create_empty_verif_sheet", "SIGNAL_NAME_COL", "TYPE_COL", "SIG_SEG_COL", "SIG_X_COL", "SIG_DIRECTION_COL",
           "SIG_TRACK_COL", "SIG_KP_COL", "VSP_DISTANCE_COL",
           "JOINT_NAME_COL", "JOINT_SEG_COL", "JOINT_X_COL", "JOINT_TRACK_COL", "JOINT_KP_COL",
           "DISTANCE_COL"]


VERIF_SHEET = "Sig_Joint_Dist"

SIGNAL_NAME_COL = "A"
TYPE_COL = "B"
SIG_SEG_COL = "C"
SIG_X_COL = "D"
SIG_DIRECTION_COL = "E"
SIG_TRACK_COL = "F"
SIG_KP_COL = "G"
VSP_DISTANCE_COL = "H"
JOINT_NAME_COL = "I"
JOINT_SEG_COL = "J"
JOINT_X_COL = "K"
JOINT_TRACK_COL = "L"
JOINT_KP_COL = "M"
DISTANCE_COL = "N"


def create_empty_verif_sheet(wb: openpyxl.workbook.Workbook) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(VERIF_SHEET)
    ws = wb[VERIF_SHEET]
    # Set the new sheet as active
    wb.active = ws
    # Set properties and display options for the sheet
    _set_columns_width(ws)
    ws.sheet_view.zoomScale = 100  # set zoom level to 100 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display
    # Write columns titles
    row = 1
    _write_columns_title(ws, row)
    # Set filter
    row += 1
    ws.auto_filter.ref = f"A{row}:{DISTANCE_COL}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"B{row}"
    return ws, row


def _set_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[SIGNAL_NAME_COL].width = 23
    ws.column_dimensions[TYPE_COL].width = 19
    ws.column_dimensions[SIG_SEG_COL].width = 10
    ws.column_dimensions[SIG_X_COL].width = 7.5
    ws.column_dimensions[SIG_DIRECTION_COL].width = 14
    ws.column_dimensions[SIG_TRACK_COL].width = 14
    ws.column_dimensions[SIG_KP_COL].width = 8.5
    ws.column_dimensions[VSP_DISTANCE_COL].width = 14
    ws.column_dimensions[JOINT_NAME_COL].width = 40
    ws.column_dimensions[JOINT_SEG_COL].width = 10
    ws.column_dimensions[JOINT_X_COL].width = 7.5
    ws.column_dimensions[JOINT_TRACK_COL].width = 14
    ws.column_dimensions[JOINT_KP_COL].width = 8.5
    ws.column_dimensions[DISTANCE_COL].width = 16


def _write_columns_title(ws: xl_ws.Worksheet, row: int):
    # Signal name
    create_merged_cell(ws, f"Signal Name", start_row=row, end_row=row+1,
                       start_column=SIGNAL_NAME_COL, end_column=SIGNAL_NAME_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_yellow)
    # Type
    create_merged_cell(ws, f"Type", start_row=row, end_row=row+1,
                       start_column=TYPE_COL, end_column=TYPE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Signal Position
    create_merged_cell(ws, f"Signal Position", start_row=row, end_row=row,
                       start_column=SIG_SEG_COL, end_column=SIG_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Seg", row=row+1, column=SIG_SEG_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"X", row=row+1, column=SIG_X_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Direction", row=row+1, column=SIG_DIRECTION_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Track", row=row+1, column=SIG_TRACK_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"KP", row=row+1, column=SIG_KP_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    # VSP Distance
    create_merged_cell(ws, f"VSP Distance (Dist PAP)", start_row=row, end_row=row+1,
                       start_column=VSP_DISTANCE_COL, end_column=VSP_DISTANCE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_pink)
    # IVB Joint
    create_merged_cell(ws, f"IVB Joint", start_row=row, end_row=row,
                       start_column=JOINT_NAME_COL, end_column=JOINT_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"Name", row=row+1, column=JOINT_NAME_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"Seg", row=row+1, column=JOINT_SEG_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"X", row=row+1, column=JOINT_X_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"Track", row=row+1, column=JOINT_TRACK_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"KP", row=row+1, column=JOINT_KP_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Distance from signal to joint
    create_merged_cell(ws, f"Distance from signal to joint", start_row=row, end_row=row+1,
                       start_column=DISTANCE_COL, end_column=DISTANCE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
