#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..survey_types import *


__all__ = ["create_verif_sheet",
           "NAME_COL", "DC_SYS_SHEET_COL", "DC_SYS_TRACK_COL", "DC_SYS_KP_COL",
           "BLOCK_DEF_LIMIT_NAME_COL",
           "SURVEY_NAME_COL", "SURVEY_TYPE_COL", "SURVEY_TRACK_COL", "SURVEYED_KP_COL",
           "DIFFERENCE_COL", "STATUS_COL", "AUTOMATIC_COMMENTS_COL", "MANUAL_VERIFICATION_COL", "COMMENTS_COL",
           "get_column", "get_tolerance_dict"]


NAME_COL = "A"
DC_SYS_SHEET_COL = "B"
DC_SYS_TRACK_COL = "C"
DC_SYS_KP_COL = "D"
BLOCK_DEF_LIMIT_NAME_COL = "E"
SURVEY_NAME_COL = "E"
SURVEY_TYPE_COL = "F"
SURVEY_TRACK_COL = "G"
SURVEYED_KP_COL = "H"
DIFFERENCE_COL = "I"
STATUS_COL = "J"
AUTOMATIC_COMMENTS_COL = "K"
MANUAL_VERIFICATION_COL = "L"
COMMENTS_COL = "M"


def create_verif_sheet(wb: openpyxl.workbook.Workbook, sheet_name: str, extra_column: bool
                       ) -> tuple[xl_ws.Worksheet, int]:
    wb.create_sheet(sheet_name)
    ws = wb[sheet_name]
    # Set properties and display options for the sheet
    ws.sheet_properties.tabColor = "0070C0"
    _set_columns_width(ws, extra_column)
    ws.sheet_view.zoomScale = 85  # set zoom level to 85 %
    ws.sheet_view.showGridLines = False  # turn off gridlines display
    _set_conditional_formatting(ws, extra_column)
    # Write location tolerance and set the defined name
    row = _write_tolerance_variable(wb, ws, sheet_name)
    # Write columns titles
    row += 1
    _write_columns_title(ws, row, extra_column)
    # Set filter
    row += 1
    ws.auto_filter.ref = f"A{row}:{get_column(COMMENTS_COL, extra_column)}{row}"
    # Freeze header rows
    row += 1
    ws.freeze_panes = f"B{row}"
    return ws, row


def _set_columns_width(ws: xl_ws.Worksheet, extra_column: bool):
    ws.column_dimensions[NAME_COL].width = 40
    ws.column_dimensions[DC_SYS_SHEET_COL].width = 12.5
    ws.column_dimensions[DC_SYS_TRACK_COL].width = 18
    ws.column_dimensions[DC_SYS_KP_COL].width = 13.5
    if extra_column:
        ws.column_dimensions[BLOCK_DEF_LIMIT_NAME_COL].width = 20.5
    ws.column_dimensions[get_column(SURVEY_NAME_COL, extra_column)].width = 33
    ws.column_dimensions[get_column(SURVEY_TYPE_COL, extra_column)].width = 12.5
    ws.column_dimensions[get_column(SURVEY_TRACK_COL, extra_column)].width = 18
    ws.column_dimensions[get_column(SURVEYED_KP_COL, extra_column)].width = 13.5
    ws.column_dimensions[get_column(DIFFERENCE_COL, extra_column)].width = 13.5
    ws.column_dimensions[get_column(STATUS_COL, extra_column)].width = 13.5
    ws.column_dimensions[get_column(AUTOMATIC_COMMENTS_COL, extra_column)].width = 45
    ws.column_dimensions[get_column(MANUAL_VERIFICATION_COL, extra_column)].width = 13.5
    ws.column_dimensions[get_column(COMMENTS_COL, extra_column)].width = 45


def _set_conditional_formatting(ws: xl_ws.Worksheet, extra_column: bool):
    diff_and_status_range = get_cell_range(start_column=get_column(DIFFERENCE_COL, extra_column),
                                           end_column=get_column(STATUS_COL, extra_column))
    status_range = get_cell_range(start_column=get_column(STATUS_COL, extra_column),
                                  end_column=get_column(STATUS_COL, extra_column))
    manual_range = get_cell_range(start_column=get_column(MANUAL_VERIFICATION_COL, extra_column),
                                  end_column=get_column(MANUAL_VERIFICATION_COL, extra_column))

    add_is_equal_conditional_formatting(ws, cell_range=diff_and_status_range,
                                        value="\"Not Surveyed\"", font_color=XlFontColor.dark_red, bold=True)
    add_is_equal_conditional_formatting(ws, cell_range=diff_and_status_range,
                                        value="\"Not in DC_SYS\"", font_color=XlFontColor.orange)
    # Multiple ranges are separated by a space in openpyxl cell ranges.
    add_is_equal_conditional_formatting(ws, cell_range=f"{status_range} {manual_range}",
                                        value="\"OK\"", font_color=XlFontColor.ok, bg_color=XlBgColor.ok)
    add_is_equal_conditional_formatting(ws, cell_range=f"{status_range} {manual_range}",
                                        value="\"KO\"", font_color=XlFontColor.ko, bg_color=XlBgColor.ko)
    add_is_equal_conditional_formatting(ws, cell_range=manual_range,
                                        value="\"NA\"", font_color=XlFontColor.na, bg_color=XlBgColor.na)


def _write_tolerance_variable(wb: openpyxl.workbook.Workbook, ws: xl_ws.Worksheet, sheet_name: str):
    tolerance_dict = get_tolerance_dict(sheet_name)
    if isinstance(tolerance_dict, tuple):
        list_tol = [tolerance_dict]
    else:
        list_tol = list(tolerance_dict.values())
    row = 1
    for row, (type_str, tolerance, tol_value) in enumerate(list_tol, start=1):
        create_cell(ws, f"Tolerance on {type_str} location:", row=row, column=1, borders=True)
        create_cell(ws, tol_value, row=row, column=2, borders=True, bold=True, bg_color=XlBgColor.special_blue)
        create_defined_name(wb, sheet_name, name=tolerance, row=row, column=2)
        create_cell(ws, "m", row=row, column=3, borders=True)
        row += 1
    return row


def _write_columns_title(ws: xl_ws.Worksheet, row: int, extra_column: bool):
    # DC_SYS information
    create_merged_cell(ws, "DC_SYS", start_row=row, end_row=row, start_column=NAME_COL, end_column=DC_SYS_KP_COL,
                       align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.yellow)
    create_cell(ws, "Data Name", row=row+1, column=NAME_COL, align_horizontal=XlAlign.center, bold=True,
                bg_color=XlBgColor.yellow)
    create_cell(ws, "Sheet", row=row+1, column=DC_SYS_SHEET_COL, align_horizontal=XlAlign.center, bold=True,
                bg_color=XlBgColor.yellow)
    create_cell(ws, "Track", row=row+1, column=DC_SYS_TRACK_COL, align_horizontal=XlAlign.center, bold=True,
                bg_color=XlBgColor.yellow)
    create_cell(ws, "KP", row=row+1, column=DC_SYS_KP_COL, align_horizontal=XlAlign.center, bold=True,
                bg_color=XlBgColor.yellow)
    draw_exterior_borders_of_a_range(ws, start_row=row, end_row=row+1, start_column=NAME_COL, end_column=DC_SYS_KP_COL)
    # Block Definition
    if extra_column:
        create_merged_cell(ws, "Block Def. Name", start_row=row, end_row=row+1, start_column=BLOCK_DEF_LIMIT_NAME_COL,
                           end_column=BLOCK_DEF_LIMIT_NAME_COL, borders=True, align_horizontal=XlAlign.center,
                           bold=True, border_style=xl_borders.BORDER_MEDIUM, bg_color=XlBgColor.grey)
    # Survey information
    create_merged_cell(ws, "Survey", start_row=row, end_row=row,
                       start_column=get_column(SURVEY_NAME_COL, extra_column),
                       end_column=get_column(SURVEYED_KP_COL, extra_column),
                       align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.green)
    create_cell(ws, "Reference", row=row+1, column=get_column(SURVEY_NAME_COL, extra_column),
                align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.green)
    create_cell(ws, "Type", row=row+1, column=get_column(SURVEY_TYPE_COL, extra_column),
                align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.green)
    create_cell(ws, "Track", row=row+1, column=get_column(SURVEY_TRACK_COL, extra_column),
                align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.green)
    create_cell(ws, "Surveyed KP", row=row+1, column=get_column(SURVEYED_KP_COL, extra_column),
                align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.green)
    draw_exterior_borders_of_a_range(ws, start_row=row, end_row=row+1,
                                     start_column=get_column(SURVEY_NAME_COL, extra_column),
                                     end_column=get_column(SURVEYED_KP_COL, extra_column))
    # Status
    create_merged_cell(ws, "Difference", start_row=row, end_row=row+1,
                       start_column=get_column(DIFFERENCE_COL, extra_column),
                       end_column=get_column(DIFFERENCE_COL, extra_column),
                       align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.blue)
    create_merged_cell(ws, "Status", start_row=row, end_row=row+1,
                       start_column=get_column(STATUS_COL, extra_column),
                       end_column=get_column(STATUS_COL, extra_column),
                       align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.blue)
    create_merged_cell(ws, "Automatic Comments", start_row=row, end_row=row+1,
                       start_column=get_column(AUTOMATIC_COMMENTS_COL, extra_column),
                       end_column=get_column(AUTOMATIC_COMMENTS_COL, extra_column),
                       align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.blue)
    create_merged_cell(ws, "Manual Verification", start_row=row, end_row=row+1,
                       start_column=get_column(MANUAL_VERIFICATION_COL, extra_column),
                       end_column=get_column(MANUAL_VERIFICATION_COL, extra_column),
                       align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.blue)
    create_merged_cell(ws, "Comments", start_row=row, end_row=row+1,
                       start_column=get_column(COMMENTS_COL, extra_column),
                       end_column=get_column(COMMENTS_COL, extra_column),
                       align_horizontal=XlAlign.center, bold=True, bg_color=XlBgColor.blue)
    draw_exterior_borders_of_a_range(ws, start_row=row, end_row=row+1,
                                     start_column=get_column(DIFFERENCE_COL, extra_column),
                                     end_column=get_column(COMMENTS_COL, extra_column))


def get_column(default_col: str, extra_col: bool = False) -> str:
    if not extra_col or default_col < BLOCK_DEF_LIMIT_NAME_COL:
        return default_col
    else:
        return get_xl_column_letter(get_xl_column_number(default_col) + 1)


def get_tolerance_dict(sheet_name: str) -> Optional[Union[tuple[str, str, float], dict[str, tuple[str, str, float]]]]:
    for val in SURVEY_TYPES_DICT.values():
        if val["res_sheet"] == sheet_name:
            return val["tol"]
    print_error(f"{sheet_name = } not found inside SURVEY_TYPES_DICT:\n"
                f"{SURVEY_TYPES_DICT = }")
    return None
