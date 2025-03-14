#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["create_empty_verif_sheet", "create_constraint_sheet",
           "SIGNAL_NAME_COL", "TYPE_COL", "DIRECTION_COL", "RELATED_CDZ_COL", "IXL_APZ_COL",
           "DOWNSTREAM_LIM_SEG_COL", "DOWNSTREAM_LIM_X_COL", "DOWNSTREAM_LIM_TRACK_COL", "DOWNSTREAM_LIM_KP_COL",
           "UPSTREAM_LIM_SEG_COL", "UPSTREAM_LIM_X_COL", "UPSTREAM_LIM_TRACK_COL", "UPSTREAM_LIM_KP_COL",
           "IXL_APZ_LENGTH_COL", "TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL", "STATUS_COL", "COMMENTS_COL"]


VERIF_SHEET = "R_ZSM_3"

SIGNAL_NAME_COL = "A"
TYPE_COL = "B"
DIRECTION_COL = "C"
RELATED_CDZ_COL = "D"
IXL_APZ_COL = "E"
DOWNSTREAM_LIM_SEG_COL = "F"
DOWNSTREAM_LIM_X_COL = "G"
DOWNSTREAM_LIM_TRACK_COL = "H"
DOWNSTREAM_LIM_KP_COL = "I"
UPSTREAM_LIM_SEG_COL = "J"
UPSTREAM_LIM_X_COL = "K"
UPSTREAM_LIM_TRACK_COL = "L"
UPSTREAM_LIM_KP_COL = "M"
IXL_APZ_LENGTH_COL = "N"
TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL = "O"
STATUS_COL = "P"
COMMENTS_COL = "Q"


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
    ws.column_dimensions[TYPE_COL].width = 19
    ws.column_dimensions[DIRECTION_COL].width = 13
    ws.column_dimensions[RELATED_CDZ_COL].width = 20.5
    ws.column_dimensions[IXL_APZ_COL].width = 19.5
    ws.column_dimensions[DOWNSTREAM_LIM_SEG_COL].width = 10
    ws.column_dimensions[DOWNSTREAM_LIM_X_COL].width = 7.5
    ws.column_dimensions[DOWNSTREAM_LIM_TRACK_COL].width = 14
    ws.column_dimensions[DOWNSTREAM_LIM_KP_COL].width = 8.5
    ws.column_dimensions[UPSTREAM_LIM_SEG_COL].width = 10
    ws.column_dimensions[UPSTREAM_LIM_X_COL].width = 7.5
    ws.column_dimensions[UPSTREAM_LIM_TRACK_COL].width = 14
    ws.column_dimensions[UPSTREAM_LIM_KP_COL].width = 8.5
    ws.column_dimensions[IXL_APZ_LENGTH_COL].width = 10.5
    ws.column_dimensions[TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL].width = 33
    ws.column_dimensions[STATUS_COL].width = 8.5
    ws.column_dimensions[COMMENTS_COL].width = 39


def _set_conditional_formatting(ws: xl_ws.Worksheet):
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
    # Type
    create_merged_cell(ws, f"Type", start_row=row, end_row=row+1,
                       start_column=TYPE_COL, end_column=TYPE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Direction
    create_merged_cell(ws, f"Direction", start_row=row, end_row=row+1,
                       start_column=DIRECTION_COL, end_column=DIRECTION_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Related CBTC Direction Zone
    create_merged_cell(ws, f"Related CBTC Direction Zone", start_row=row, end_row=row+1,
                       start_column=RELATED_CDZ_COL, end_column=RELATED_CDZ_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_pink)
    # IXL APZ
    create_merged_cell(ws, f"IXL Approach Zone", start_row=row, end_row=row+1,
                       start_column=IXL_APZ_COL, end_column=IXL_APZ_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Signal Downstream Limit
    create_merged_cell(ws, f"Signal Downstream Limit", start_row=row, end_row=row,
                       start_column=DOWNSTREAM_LIM_SEG_COL, end_column=DOWNSTREAM_LIM_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Seg", row=row+1, column=DOWNSTREAM_LIM_SEG_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"X", row=row+1, column=DOWNSTREAM_LIM_X_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Track", row=row+1, column=DOWNSTREAM_LIM_TRACK_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"KP", row=row+1, column=DOWNSTREAM_LIM_KP_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    # APZ Upstream Limit
    create_merged_cell(ws, f"IXL APZ Upstream Limit", start_row=row, end_row=row,
                       start_column=UPSTREAM_LIM_SEG_COL, end_column=UPSTREAM_LIM_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    create_cell(ws, f"Seg", row=row+1, column=UPSTREAM_LIM_SEG_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    create_cell(ws, f"X", row=row+1, column=UPSTREAM_LIM_X_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    create_cell(ws, f"Track", row=row+1, column=UPSTREAM_LIM_TRACK_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    create_cell(ws, f"KP", row=row+1, column=UPSTREAM_LIM_KP_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    # IXL APZ Length
    create_merged_cell(ws, f"IXL APZ Length", start_row=row, end_row=row+1,
                       start_column=IXL_APZ_LENGTH_COL, end_column=IXL_APZ_LENGTH_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Minimum Length
    create_merged_cell(ws, f"Minimum Length\ntrain_to_home_signal_max_dist", start_row=row, end_row=row + 1,
                       start_column=TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL, end_column=TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Status
    create_merged_cell(ws, f"Status", start_row=row, end_row=row+1,
                       start_column=STATUS_COL, end_column=STATUS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
    # Comments
    create_merged_cell(ws, "Comments", start_row=row, end_row=row+1,
                       start_column=COMMENTS_COL, end_column=COMMENTS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)


CONSTRAINT_SHEET = "Constraint"
CONSTRAINT_DESCRIPTION_CELL_RANGE = "B4:J12"

CONSTRAINT_DESCRIPTION = """R_ZSM_3:
The train, whose end is within a certain region ([train_to_home_signal_max_dist]) from a home signal at the end of a CBTC Direction Zone, shall occupy the IL approach area (if any). This rule ensures the route exiting the CBTC Direction Zone cannot be cancelled in IMC, leading to a head on collision with another train, authorized to take a route in opposite direction.

Check for each signal associated to a CBTC Direction zone exit that if an approach area exists, then [train_to_home_signal_max_dist] distance is included in the approach area."""


def create_constraint_sheet(wb: openpyxl.workbook.Workbook):
    wb.create_sheet(CONSTRAINT_SHEET)
    ws = wb[CONSTRAINT_SHEET]
    # Set properties and display options for the sheet
    ws.sheet_view.zoomScale = 120  # set zoom level to 120 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display

    create_merged_cell(ws, CONSTRAINT_DESCRIPTION, cell_range=CONSTRAINT_DESCRIPTION_CELL_RANGE, borders=True)
    select_cell(ws, cell=CONSTRAINT_DESCRIPTION_CELL_RANGE.split(":")[0])
