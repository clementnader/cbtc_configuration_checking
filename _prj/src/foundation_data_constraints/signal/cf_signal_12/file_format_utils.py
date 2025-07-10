#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....dc_par import *


__all__ = ["create_empty_verif_sheet", "create_parameters_sheet", "create_constraint_sheet",
           "SIGNAL_NAME_COL", "TYPE_COL", "DIRECTION_COL", "IXL_APZ_COL",
           "DOWNSTREAM_LIM_SEG_COL", "DOWNSTREAM_LIM_X_COL", "DOWNSTREAM_LIM_TRACK_COL", "DOWNSTREAM_LIM_KP_COL",
           "UPSTREAM_LIM_SEG_COL", "UPSTREAM_LIM_X_COL", "UPSTREAM_LIM_TRACK_COL", "UPSTREAM_LIM_KP_COL",
           "IXL_APZ_LENGTH_COL", "LAST_IVB_PLATFORM_RELATED_COL", "VALUE_TO_REMOVE_COL", "MIN_DIST_COL",
           "DLT_DIST_COL", "STATUS_COL", "COMMENTS_COL"]


VERIF_SHEET = "CF_SIGNAL_12"

SIGNAL_NAME_COL = "A"
TYPE_COL = "B"
DIRECTION_COL = "C"
IXL_APZ_COL = "D"
DOWNSTREAM_LIM_SEG_COL = "E"
DOWNSTREAM_LIM_X_COL = "F"
DOWNSTREAM_LIM_TRACK_COL = "G"
DOWNSTREAM_LIM_KP_COL = "H"
UPSTREAM_LIM_SEG_COL = "I"
UPSTREAM_LIM_X_COL = "J"
UPSTREAM_LIM_TRACK_COL = "K"
UPSTREAM_LIM_KP_COL = "L"
IXL_APZ_LENGTH_COL = "M"
LAST_IVB_PLATFORM_RELATED_COL = "N"
VALUE_TO_REMOVE_COL = "O"
MIN_DIST_COL = "P"
DLT_DIST_COL = "Q"
STATUS_COL = "R"
COMMENTS_COL = "S"


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
    ws.column_dimensions[LAST_IVB_PLATFORM_RELATED_COL].width = 23
    ws.column_dimensions[VALUE_TO_REMOVE_COL].width = 10.5
    ws.column_dimensions[MIN_DIST_COL].width = 10.5
    ws.column_dimensions[DLT_DIST_COL].width = 10.5
    ws.column_dimensions[STATUS_COL].width = 8.5
    ws.column_dimensions[COMMENTS_COL].width = 39


def _set_conditional_formatting(ws: xl_ws.Worksheet):
    # Overshoot Recovery Parameters Formatting
    # Multiple ranges are separated by a space in openpyxl cell ranges
    upstream_ivb_plt_rel_n_value_to_remove_range = (get_cell_range(start_column=LAST_IVB_PLATFORM_RELATED_COL,
                                                                   start_row=3,
                                                                   end_column=LAST_IVB_PLATFORM_RELATED_COL) +
                                                    " " + get_cell_range(start_column=VALUE_TO_REMOVE_COL,
                                                                         start_row=3,
                                                                         end_column=VALUE_TO_REMOVE_COL))

    add_formula_conditional_formatting(ws, cell_range=upstream_ivb_plt_rel_n_value_to_remove_range,
                                       formula=f"AND(inhibit_simple_overshoot_recovery = FALSE, "
                                               f"${LAST_IVB_PLATFORM_RELATED_COL}3<>\"\")",
                                       bg_color=XlBgColor.light_pink2)

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
    # Type
    create_merged_cell(ws, f"Type", start_row=row, end_row=row+1,
                       start_column=TYPE_COL, end_column=TYPE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Direction
    create_merged_cell(ws, f"Direction", start_row=row, end_row=row+1,
                       start_column=DIRECTION_COL, end_column=DIRECTION_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
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
    # Last IVB Platform Related
    create_merged_cell(ws, f"Last IVB\nPlatform Related", start_row=row, end_row=row+1,
                       start_column=LAST_IVB_PLATFORM_RELATED_COL, end_column=LAST_IVB_PLATFORM_RELATED_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_pink)
    # Value to remove
    create_merged_cell(ws, f"Value to remove", start_row=row, end_row=row+1,
                       start_column=VALUE_TO_REMOVE_COL, end_column=VALUE_TO_REMOVE_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # Maximum Distance
    create_merged_cell(ws, f"Maximum Distance", start_row=row, end_row=row+1,
                       start_column=MIN_DIST_COL, end_column=MIN_DIST_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_cyan)
    # DLT Distance
    create_merged_cell(ws, f"DLT Distance", start_row=row, end_row=row+1,
                       start_column=DLT_DIST_COL, end_column=DLT_DIST_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True, bg_color=XlBgColor.dc_sys_orange)
    # Status
    create_merged_cell(ws, f"Status", start_row=row, end_row=row+1,
                       start_column=STATUS_COL, end_column=STATUS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)
    # Comments
    create_merged_cell(ws, "Comments", start_row=row, end_row=row+1,
                       start_column=COMMENTS_COL, end_column=COMMENTS_COL,
                       align_horizontal=XlAlign.center, bold=True, borders=True)


PARAMETERS_SHEET = "Parameters"

PARAM_NAME_COL = "A"
PARAM_VALUE_COL = "B"
PARAM_UNIT_COL = "C"


def create_parameters_sheet(wb: openpyxl.workbook.Workbook) -> bool:
    ws, start_row = _create_empty_parameters_sheet(wb)

    params_dict = {
        "at_deshunt_max_dist": get_param_with_unit("at_deshunt_max_dist"),
        "block_laying_uncertainty": get_param_with_unit("block_laying_uncertainty"),
        "at_rollback_dist": get_param_with_unit("at_rollback_dist"),
        "mtc_rollback_dist": get_param_with_unit("mtc_rollback_dist"),
        "overshoot_recovery_dist": get_param_with_unit("overshoot_recovery_dist"),
        "overshoot_recovery_stopping_max_dist": get_param_with_unit("overshoot_recovery_stopping_max_dist"),
        "inhibit_simple_overshoot_recovery": get_param_with_unit("inhibit_simple_overshoot_recovery"),
    }

    for row, (param_name, param_info) in enumerate(params_dict.items(), start=start_row):
        param_value, param_unit = param_info
        create_cell(ws, param_name, row=row, column=PARAM_NAME_COL, borders=True)
        create_cell(ws, param_value, row=row, column=PARAM_VALUE_COL, borders=True)
        create_defined_name(wb, PARAMETERS_SHEET, name=param_name, row=row, column=PARAM_VALUE_COL)
        create_cell(ws, param_unit, row=row, column=PARAM_UNIT_COL, borders=True)

    return params_dict["inhibit_simple_overshoot_recovery"][0]


def _create_empty_parameters_sheet(wb: openpyxl.workbook.Workbook) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(PARAMETERS_SHEET)
    ws = wb[PARAMETERS_SHEET]
    # Set properties and display options for the sheet
    _set_param_sheet_columns_width(ws)
    ws.sheet_view.zoomScale = 100  # set zoom level to 100 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display
    # Write columns titles
    row = 1
    _write_param_sheet_columns_title(ws, row)
    # Set filter
    row += 1
    ws.auto_filter.ref = f"A{row}:{PARAM_UNIT_COL}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"B{row}"
    return ws, row


def _set_param_sheet_columns_width(ws: xl_ws.Worksheet):
    ws.column_dimensions[PARAM_NAME_COL].width = 38
    ws.column_dimensions[PARAM_VALUE_COL].width = 13
    ws.column_dimensions[PARAM_UNIT_COL].width = 13


def _write_param_sheet_columns_title(ws: xl_ws.Worksheet, row: int):
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


CONSTRAINT_SHEET = "Constraint"

CONSTRAINT_DESCRIPTION_CELL_RANGE = "B4:N17"

CONSTRAINT_DESCRIPTION = """CF_SIGNAL_12:
Delayed legitimate turnback distance shall ensure the following properties:
 - A train shall lock the Signalling approaching zone for sure: therefore it shall be less than the distance between the block limit of the signal and the closest entrance of signalling approach zones of any routes starting from the signal minus at_deshunt_max_dist minus block_laying_uncertainty minus max ([mtc_rollback_dist], [at_rollback_dist], [overshoot_recovery_dist] + [overshoot_recovery_stopping_max_dist]).
 - There shall be no civil infrastructure (switch point, fouling point, derailer, flood gate….) at less than this distance from the block limit of the signal that a train does not lock for sure by shunting the proper blocks.

0 is a safe value.

If Overshoot Recovery is active (inhibition parameter inhibit_simple_overshoot_recovery set to False), the overshoot recovery parameters in the formula are considered only when last IVB of the IXL APZ (upstream the signal) is platform related, where overshoot recovery can be used and let a train leave the APZ."""


def create_constraint_sheet(wb: openpyxl.workbook.Workbook):
    wb.create_sheet(CONSTRAINT_SHEET)
    ws = wb[CONSTRAINT_SHEET]
    # Set properties and display options for the sheet
    ws.sheet_view.zoomScale = 120  # set zoom level to 120 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display

    create_merged_cell(ws, CONSTRAINT_DESCRIPTION, cell_range=CONSTRAINT_DESCRIPTION_CELL_RANGE, borders=True)
    select_cell(ws, cell=CONSTRAINT_DESCRIPTION_CELL_RANGE.split(":")[0])
