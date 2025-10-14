#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....dc_par import *
from ....dc_par_add_on_parameters import *


__all__ = ["create_empty_verif_sheet", "create_parameters_sheet",
           "SWITCH_NAME_COL", "SW_BLOCK_LOCKING_AREA_START_COL", "SW_BLOCK_LOCKING_AREA_NB_COL",
           "CBTC_PROTECTING_SW_AREA_START_COL", "CBTC_PROTECTING_SW_AREA_NB_COL",
           "FOULING_POINT_DISTANCE_COL", "LOCAL_SPEED_COL", "DIST_TO_PROTECT_COL",
           "COMPUTED_LIST_IVB_TO_PROTECT_COL", "IVB_THAT_SHALL_BE_ADDED_COL", "IVB_THAT_CAN_BE_REMOVED_COL",
           "STATUS_COL", "COMMENTS_COL"]


VERIF_SHEET = "CBTC Protecting Switch Area"

SWITCH_NAME_COL = 1
SW_BLOCK_LOCKING_AREA_START_COL = 2
SW_BLOCK_LOCKING_AREA_NB_COL = 10
CBTC_PROTECTING_SW_AREA_START_COL = SW_BLOCK_LOCKING_AREA_START_COL + SW_BLOCK_LOCKING_AREA_NB_COL
CBTC_PROTECTING_SW_AREA_NB_COL = 10
FOULING_POINT_DISTANCE_COL = CBTC_PROTECTING_SW_AREA_START_COL + CBTC_PROTECTING_SW_AREA_NB_COL
LOCAL_SPEED_COL = FOULING_POINT_DISTANCE_COL + 1
DIST_TO_PROTECT_COL = LOCAL_SPEED_COL + 1
COMPUTED_LIST_IVB_TO_PROTECT_COL = DIST_TO_PROTECT_COL + 1
IVB_THAT_SHALL_BE_ADDED_COL = COMPUTED_LIST_IVB_TO_PROTECT_COL + 1
IVB_THAT_CAN_BE_REMOVED_COL = IVB_THAT_SHALL_BE_ADDED_COL + 1
STATUS_COL = IVB_THAT_CAN_BE_REMOVED_COL + 1
COMMENTS_COL = STATUS_COL + 1


def create_empty_verif_sheet(wb: openpyxl.workbook.Workbook) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(VERIF_SHEET)
    ws = wb[VERIF_SHEET]
    # Set the new sheet as active
    wb.active = ws
    # Set properties and display options for the sheet
    ws.row_dimensions[1].height = 30
    ws.row_dimensions[2].height = 30
    _set_columns_width(ws)
    ws.sheet_view.zoomScale = 85  # set zoom level to 85 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display
    _set_conditional_formatting(ws)
    # Write columns titles
    row = 1
    _write_columns_title(ws, row)
    # Set filter
    row += 1
    ws.auto_filter.ref = f"A{row}:{get_xl_column_letter(COMMENTS_COL)}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"B{row}"
    return ws, row


def _set_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[get_xl_column_letter(SWITCH_NAME_COL)].width = 18

    for sw_block_locking_area_col in range(SW_BLOCK_LOCKING_AREA_START_COL,
                                           SW_BLOCK_LOCKING_AREA_START_COL+SW_BLOCK_LOCKING_AREA_NB_COL):
        ws.column_dimensions[get_xl_column_letter(sw_block_locking_area_col)].width = 16.5

    for cbtc_protecting_sw_area_col in range(CBTC_PROTECTING_SW_AREA_START_COL,
                                             CBTC_PROTECTING_SW_AREA_START_COL+CBTC_PROTECTING_SW_AREA_NB_COL):
        ws.column_dimensions[get_xl_column_letter(cbtc_protecting_sw_area_col)].width = 16.5

    ws.column_dimensions[get_xl_column_letter(FOULING_POINT_DISTANCE_COL)].width = 22.5
    ws.column_dimensions[get_xl_column_letter(LOCAL_SPEED_COL)].width = 13
    ws.column_dimensions[get_xl_column_letter(DIST_TO_PROTECT_COL)].width = 24
    ws.column_dimensions[get_xl_column_letter(COMPUTED_LIST_IVB_TO_PROTECT_COL)].width = 30
    ws.column_dimensions[get_xl_column_letter(IVB_THAT_SHALL_BE_ADDED_COL)].width = 16.5
    ws.column_dimensions[get_xl_column_letter(IVB_THAT_CAN_BE_REMOVED_COL)].width = 16.5
    ws.column_dimensions[get_xl_column_letter(STATUS_COL)].width = 8.5
    ws.column_dimensions[get_xl_column_letter(COMMENTS_COL)].width = 39


def _set_conditional_formatting(ws: xl_ws.Worksheet):
    status_range = get_cell_range(start_column=STATUS_COL, end_column=STATUS_COL)

    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"OK\"", font_color=XlFontColor.ok, bg_color=XlBgColor.ok)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"KO\"", font_color=XlFontColor.ko, bg_color=XlBgColor.ko)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"Warning\"", font_color=XlFontColor.warning, bg_color=XlBgColor.warning)
    add_is_equal_conditional_formatting(ws, cell_range=status_range,
                                        value="\"NA\"", font_color=XlFontColor.na, bg_color=XlBgColor.na)

    missing_ivb_range = get_cell_range(start_column=IVB_THAT_SHALL_BE_ADDED_COL, end_column=IVB_THAT_SHALL_BE_ADDED_COL,
                                       start_row=3)
    formula = f"{get_xl_column_letter(IVB_THAT_SHALL_BE_ADDED_COL)}3<>\"\""
    add_formula_conditional_formatting(ws, cell_range=missing_ivb_range,
                                       formula=formula, font_color=XlFontColor.ko, bg_color=XlBgColor.ko)


def _write_columns_title(ws: xl_ws.Worksheet, row: int):
    # Switch Name
    create_merged_cell(ws, f"Switch Name", start_row=row, end_row=row+1,
                       start_column=SWITCH_NAME_COL, end_column=SWITCH_NAME_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_yellow)
    # Switch block locking area
    create_merged_cell(ws, f"Switch block locking area", start_row=row, end_row=row,
                       start_column=SW_BLOCK_LOCKING_AREA_START_COL,
                       end_column=SW_BLOCK_LOCKING_AREA_START_COL+SW_BLOCK_LOCKING_AREA_NB_COL-1,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    for ivb_num, sw_block_locking_area_col in enumerate(
            range(SW_BLOCK_LOCKING_AREA_START_COL,
                  SW_BLOCK_LOCKING_AREA_START_COL+SW_BLOCK_LOCKING_AREA_NB_COL), start=1):
        create_cell(ws, f"IVB {ivb_num}", row=row+1, column=sw_block_locking_area_col,
                    align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_blue)
    # CBTC protecting switch area
    create_merged_cell(ws, f"CBTC protecting switch area", start_row=row, end_row=row,
                       start_column=CBTC_PROTECTING_SW_AREA_START_COL,
                       end_column=CBTC_PROTECTING_SW_AREA_START_COL+CBTC_PROTECTING_SW_AREA_NB_COL-1,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    for ivb_num, cbtc_protecting_sw_area_col in enumerate(
            range(CBTC_PROTECTING_SW_AREA_START_COL,
                  CBTC_PROTECTING_SW_AREA_START_COL+CBTC_PROTECTING_SW_AREA_NB_COL), start=1):
        create_cell(ws, f"IVB {ivb_num}", row=row+1, column=cbtc_protecting_sw_area_col,
                    align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_green)
    # Fouling Point Distance
    create_merged_cell(ws, f"Distance between switch and fouling point", start_row=row, end_row=row+1,
                       start_column=FOULING_POINT_DISTANCE_COL, end_column=FOULING_POINT_DISTANCE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_yellow)
    # Local Speed
    create_merged_cell(ws, f"Local Speed (km/h)", start_row=row, end_row=row+1,
                       start_column=LOCAL_SPEED_COL, end_column=LOCAL_SPEED_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Distance to protect
    create_merged_cell(ws, f"Distance travelled during oc_zc_data_freshness_threshold + ixl_cycle_time (m)",
                       start_row=row, end_row=row+1,
                       start_column=DIST_TO_PROTECT_COL, end_column=DIST_TO_PROTECT_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # List IVB to protect
    create_merged_cell(ws, f"Computed list of IVBs from which we can access the switch point or the fouling "
                           f"point within the distance", start_row=row, end_row=row+1,
                       start_column=COMPUTED_LIST_IVB_TO_PROTECT_COL, end_column=COMPUTED_LIST_IVB_TO_PROTECT_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # IVB that shall be added
    create_merged_cell(ws, f"IVB that shall be added", start_row=row, end_row=row+1,
                       start_column=IVB_THAT_SHALL_BE_ADDED_COL, end_column=IVB_THAT_SHALL_BE_ADDED_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # IVB that can be removed
    create_merged_cell(ws, f"IVB that can be removed", start_row=row, end_row=row+1,
                       start_column=IVB_THAT_CAN_BE_REMOVED_COL, end_column=IVB_THAT_CAN_BE_REMOVED_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Status
    create_merged_cell(ws, f"Status", start_row=row, end_row=row+1,
                       start_column=STATUS_COL, end_column=STATUS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
    # Comments
    create_merged_cell(ws, "Automatic Comments", start_row=row, end_row=row+1,
                       start_column=COMMENTS_COL, end_column=COMMENTS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)


PARAMETERS_SHEET = "Parameters"

PARAM_NAME_COL = "A"
PARAM_VALUE_COL = "B"
PARAM_UNIT_COL = "C"


def create_parameters_sheet(wb: openpyxl.workbook.Workbook) -> None:
    ws, start_row = _create_empty_parameters_sheet(wb)

    params_dict = {
        "oc_zc_data_freshness_threshold": get_parameter_value_with_unit("oc_zc_data_freshness_threshold"),
        "ixl_cycle_time": get_parameter_value_with_unit("ixl_cycle_time"),
        "rs_max_speed": (get_train_max_speed()*3.6, "km/h"),
        "line_max_speed": get_parameter_value_with_unit("line_max_speed", keep_km_per_h=True),
    }

    for row, (parameter_name, parameter_info) in enumerate(params_dict.items(), start=start_row):
        parameter_value, parameter_unit = parameter_info
        create_cell(ws, parameter_name, row=row, column=PARAM_NAME_COL, borders=True)
        create_cell(ws, parameter_value, row=row, column=PARAM_VALUE_COL, borders=True)
        create_defined_name(wb, PARAMETERS_SHEET, name=parameter_name, row=row, column=PARAM_VALUE_COL)
        create_cell(ws, parameter_unit, row=row, column=PARAM_UNIT_COL, borders=True)


def _create_empty_parameters_sheet(wb: openpyxl.workbook.Workbook) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(PARAMETERS_SHEET)
    ws = wb[PARAMETERS_SHEET]
    # Set properties and display options for the sheet
    _set_parameter_sheet_columns_width(ws)
    ws.sheet_view.zoomScale = 100  # set zoom level to 100 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display
    # Write columns titles
    row = 1
    _write_parameter_sheet_columns_title(ws, row)
    # Set filter
    row += 1
    ws.auto_filter.ref = f"A{row}:{PARAM_UNIT_COL}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"B{row}"
    return ws, row


def _set_parameter_sheet_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[PARAM_NAME_COL].width = 38
    ws.column_dimensions[PARAM_VALUE_COL].width = 13
    ws.column_dimensions[PARAM_UNIT_COL].width = 13


def _write_parameter_sheet_columns_title(ws: xl_ws.Worksheet, row: int):
    # Parameter Name
    create_merged_cell(ws, f"Parameter Name", start_row=row, end_row=row+1,
                       start_column=PARAM_NAME_COL, end_column=PARAM_NAME_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_yellow)
    # Value
    create_merged_cell(ws, f"Value", start_row=row, end_row=row+1,
                       start_column=PARAM_VALUE_COL, end_column=PARAM_VALUE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_yellow)
    # Unit
    create_merged_cell(ws, f"Unit", start_row=row, end_row=row+1,
                       start_column=PARAM_UNIT_COL, end_column=PARAM_UNIT_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_yellow)
