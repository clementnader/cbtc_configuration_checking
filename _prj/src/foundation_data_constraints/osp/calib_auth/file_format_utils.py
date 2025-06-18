#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["create_empty_verif_sheet",
           "OSP_NAME_COL", "OSP_TRACK_COL", "OSP_KP_COL", "OSP_DIRECTION_COL", "OSP_TYPE_COL",
           "TRAIN_TYPE_COL", "TRAIN_FRONT_TRACK_COL", "TRAIN_FRONT_KP_COL", "TRAIN_POLARITY_COL", "ACCEL_CAR_NB_COL",
           "ACCEL_CAR_WITH_TOL_START_TRACK_COL", "ACCEL_CAR_WITH_TOL_START_KP_COL",
           "ACCEL_CAR_WITH_TOL_END_TRACK_COL", "ACCEL_CAR_WITH_TOL_END_KP_COL",
           "SLOPE_CHANGE_UNDER_CAR_COL", "MIN_SLOPE_COL", "MAX_SLOPE_COL", "CONSTANT_SLOPE_COL",
           "OSP_CALIB_AUTH_COL", "STATUS_COL", "COMMENTS_COL"]


VERIF_SHEET = "OSP_Calib_Auth"

OSP_NAME_COL = "A"
OSP_TRACK_COL = "B"
OSP_KP_COL = "C"
OSP_DIRECTION_COL = "D"
OSP_TYPE_COL = "E"
TRAIN_TYPE_COL = "F"
TRAIN_FRONT_TRACK_COL = "G"
TRAIN_FRONT_KP_COL = "H"
ACCEL_CAR_NB_COL = "I"
TRAIN_POLARITY_COL = "J"
ACCEL_CAR_WITH_TOL_START_TRACK_COL = "K"
ACCEL_CAR_WITH_TOL_START_KP_COL = "L"
ACCEL_CAR_WITH_TOL_END_TRACK_COL = "M"
ACCEL_CAR_WITH_TOL_END_KP_COL = "N"
SLOPE_CHANGE_UNDER_CAR_COL = "O"
MIN_SLOPE_COL = "P"
MAX_SLOPE_COL = "Q"
CONSTANT_SLOPE_COL = "R"
OSP_CALIB_AUTH_COL = "S"
STATUS_COL = "T"
COMMENTS_COL = "U"


def create_empty_verif_sheet(wb: openpyxl.workbook.Workbook) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(VERIF_SHEET)
    ws = wb[VERIF_SHEET]
    # Set the new sheet as active
    wb.active = ws
    # Set properties and display options for the sheet
    _set_rows_height(ws)
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


def _set_rows_height(ws: xl_ws.Worksheet):
    ws.row_dimensions[1].height = 30


def _set_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[OSP_NAME_COL].width = 23
    ws.column_dimensions[OSP_TRACK_COL].width = 14
    ws.column_dimensions[OSP_KP_COL].width = 8.5
    ws.column_dimensions[OSP_DIRECTION_COL].width = 13.5
    ws.column_dimensions[OSP_TYPE_COL].width = 9.5
    ws.column_dimensions[TRAIN_TYPE_COL].width = 10
    ws.column_dimensions[TRAIN_FRONT_TRACK_COL].width = 14
    ws.column_dimensions[TRAIN_FRONT_KP_COL].width = 8.5
    ws.column_dimensions[TRAIN_POLARITY_COL].width = 8.5
    ws.column_dimensions[ACCEL_CAR_NB_COL].width = 15
    ws.column_dimensions[ACCEL_CAR_WITH_TOL_START_TRACK_COL].width = 14
    ws.column_dimensions[ACCEL_CAR_WITH_TOL_START_KP_COL].width = 8.5
    ws.column_dimensions[ACCEL_CAR_WITH_TOL_END_TRACK_COL].width = 14
    ws.column_dimensions[ACCEL_CAR_WITH_TOL_END_KP_COL].width = 8.5
    ws.column_dimensions[SLOPE_CHANGE_UNDER_CAR_COL].width = 12
    ws.column_dimensions[MIN_SLOPE_COL].width = 12
    ws.column_dimensions[MAX_SLOPE_COL].width = 12
    ws.column_dimensions[CONSTANT_SLOPE_COL].width = 12
    ws.column_dimensions[OSP_CALIB_AUTH_COL].width = 15
    ws.column_dimensions[STATUS_COL].width = 8.5
    ws.column_dimensions[COMMENTS_COL].width = 39


def _set_conditional_formatting(ws: xl_ws.Worksheet):
    # Not Constant Slope Conditional Formatting
    constant_slope_range = get_cell_range(start_column=CONSTANT_SLOPE_COL, end_column=CONSTANT_SLOPE_COL)
    constant_slope_formula = f'AND({CONSTANT_SLOPE_COL}1 <> "", {CONSTANT_SLOPE_COL}1 = {False})'

    add_formula_conditional_formatting(ws, cell_range=constant_slope_range, formula=constant_slope_formula,
                                       font_color=XlFontColor.ko, bg_color=XlBgColor.ko)

    # Accelerometers Calibration not allowed Conditional Formatting
    calib_auth_range = get_cell_range(start_column=OSP_CALIB_AUTH_COL, end_column=OSP_CALIB_AUTH_COL)
    calib_auth_formula = f'AND({OSP_CALIB_AUTH_COL}1 <> "", {OSP_CALIB_AUTH_COL}1 = {False})'

    add_formula_conditional_formatting(ws, cell_range=calib_auth_range, formula=calib_auth_formula,
                                       bg_color=XlBgColor.grey)

    # Status Conditional Formatting
    status_range = get_cell_range(start_column=STATUS_COL, end_column=STATUS_COL)

    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"OK\"", font_color=XlFontColor.ok, bg_color=XlBgColor.ok)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"KO\"", font_color=XlFontColor.ko, bg_color=XlBgColor.ko)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"NA\"", font_color=XlFontColor.na, bg_color=XlBgColor.na)


def _write_columns_title(ws: xl_ws.Worksheet, row: int):
    # OSP name
    create_merged_cell(ws, f"OSP Name", start_row=row, end_row=row+1,
                       start_column=OSP_NAME_COL, end_column=OSP_NAME_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_yellow)
    # OSP Position
    create_merged_cell(ws, f"OSP Position", start_row=row, end_row=row,
                       start_column=OSP_TRACK_COL, end_column=OSP_TYPE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Track", row=row+1, column=OSP_TRACK_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"KP", row=row+1, column=OSP_KP_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Direction", row=row+1, column=OSP_DIRECTION_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    create_cell(ws, f"Type", row=row+1, column=OSP_TYPE_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    # Train Type
    create_merged_cell(ws, f"Train Type", start_row=row, end_row=row+1,
                       start_column=TRAIN_TYPE_COL, end_column=TRAIN_TYPE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Train Front Position
    create_merged_cell(ws, f"Train Front Position", start_row=row, end_row=row,
                       start_column=TRAIN_FRONT_TRACK_COL, end_column=TRAIN_FRONT_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    create_cell(ws, f"Track", row=row+1, column=TRAIN_FRONT_TRACK_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    create_cell(ws, f"KP", row=row+1, column=TRAIN_FRONT_KP_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Train Polarity
    create_merged_cell(ws, f"Train Polarity", start_row=row, end_row=row+1,
                       start_column=TRAIN_POLARITY_COL, end_column=TRAIN_POLARITY_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Car with Accelerometer
    create_merged_cell(ws, f"Car with Accelerometer", start_row=row, end_row=row+1,
                       start_column=ACCEL_CAR_NB_COL, end_column=ACCEL_CAR_NB_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Car Position
    create_merged_cell(ws, f"Car Position with tolerance around OSP", start_row=row, end_row=row,
                       start_column=ACCEL_CAR_WITH_TOL_START_TRACK_COL, end_column=ACCEL_CAR_WITH_TOL_END_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"Start Track", row=row+1, column=ACCEL_CAR_WITH_TOL_START_TRACK_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"Start KP", row=row+1, column=ACCEL_CAR_WITH_TOL_START_KP_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"End Track", row=row+1, column=ACCEL_CAR_WITH_TOL_END_TRACK_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    create_cell(ws, f"End KP", row=row+1, column=ACCEL_CAR_WITH_TOL_END_KP_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Slope under Car
    create_merged_cell(ws, f"Slope under car", start_row=row, end_row=row,
                       start_column=SLOPE_CHANGE_UNDER_CAR_COL, end_column=MAX_SLOPE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_pink)
    create_cell(ws, f"Slope change", row=row+1, column=SLOPE_CHANGE_UNDER_CAR_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_pink)
    create_cell(ws, f"Min Slope", row=row+1, column=MIN_SLOPE_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_pink)
    create_cell(ws, f"Max Slope", row=row+1, column=MAX_SLOPE_COL,
                align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_pink)
    # Constant Slope under Car
    create_merged_cell(ws, f"Constant slope under car", start_row=row, end_row=row+1,
                       start_column=CONSTANT_SLOPE_COL, end_column=CONSTANT_SLOPE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_pink)
    # Allow Accelerometers Calibration
    create_merged_cell(ws, f"Allow Accelerometers Calibration", start_row=row, end_row=row+1,
                       start_column=OSP_CALIB_AUTH_COL, end_column=OSP_CALIB_AUTH_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    # Status
    create_merged_cell(ws, f"Status", start_row=row, end_row=row+1,
                       start_column=STATUS_COL, end_column=STATUS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
    # Comments
    create_merged_cell(ws, "Comments", start_row=row, end_row=row+1,
                       start_column=COMMENTS_COL, end_column=COMMENTS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
