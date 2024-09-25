#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from .dc_tu_utils import *


__all__ = ["create_dc_tu_verif_file"]


DC_TU_VERIF_TEMPLATE_RELATIVE_PATH = os.path.join(TEMPLATE_DIRECTORY, "template_dc_tu_verification.xlsx")
DC_TU_VERIF_TEMPLATE = get_full_path(__file__, DC_TU_VERIF_TEMPLATE_RELATIVE_PATH)

OUTPUT_DIRECTORY = DESKTOP_DIRECTORY
VERIF_FILE_NAME = "Analysis of ADD_VERIF_XXX - DC_TU Verification.xlsx"

MONO_CC = "MonoCC"
BI_CC = "BiCC"

NB_PMC = 3

PMC_IP_ADDRESS_SHEET_NAME = "PMC_IP_Address"
PMC_SSH_KEY_SHEET_NAME = "PMC_SSH_Key"

START_LINE = 3

PARAMETER_NAME_COLUMN = 1
PMC_FIRST_COLUMN = 2
STATUS_COLUMN = 5
COMMENTS_COLUMN = 6
IP_ADDRESS_STATUS2_COLUMN = 7
IP_ADDRESS_COMMENTS2_COLUMN = 8

TOOL_NAME = "DC_TU_Checking"


def create_dc_tu_verif_file(ip_address_dict: dict, ssh_key_dict: dict, tool_version: str):
    try:
        res_file_path = _create_verif_file(ip_address_dict, ssh_key_dict, tool_version)
    except KeyboardInterrupt:
        _create_verif_file(ip_address_dict, ssh_key_dict, tool_version)
        raise KeyboardInterrupt
    return res_file_path


def _create_verif_file(ip_address_dict: dict, ssh_key_dict: dict, tool_version: str) -> str:
    wb = load_xlsx_wb(DC_TU_VERIF_TEMPLATE, template=True)
    update_header_sheet_for_verif_file(wb, TOOL_NAME, tool_version)

    _update_ip_addr_sheet(wb, ip_address_dict)
    _update_ssh_key_sheet(wb, ssh_key_dict)

    verif_file_name = f" - {get_c11_d470_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.join(OUTPUT_DIRECTORY, verif_file_name)
    save_xl_file(wb, res_file_path)
    print_success(f"Verification of DC_TU files is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    return res_file_path


def _update_ip_addr_sheet(wb: openpyxl.workbook.Workbook,
                          ip_addr_dict: dict[int, dict[int, dict[int, dict[str, Union[str, list[tuple[int, str]]]]]]]
                          ) -> None:
    ws = wb[PMC_IP_ADDRESS_SHEET_NAME]
    nb_of_diff_values = 2
    _update_values_sheet(ws, nb_of_diff_values, ip_addr_dict)


def _update_ssh_key_sheet(wb: openpyxl.workbook.Workbook,
                          ssh_key_dict: dict[int, dict[int, dict[int, dict[str, Union[str, list[tuple[int, str]]]]]]]
                          ) -> None:
    ws = wb[PMC_SSH_KEY_SHEET_NAME]
    nb_of_diff_values = 1
    _update_values_sheet(ws, nb_of_diff_values, ssh_key_dict)


def _update_values_sheet(ws: xl_ws.Worksheet, nb_of_diff_values: int,
                         values_dict: dict[int, dict[int, dict[int, dict[str, Union[str, list[tuple[int, str]]]]]]]
                         ) -> None:
    current_row = START_LINE
    color_bool = False
    list_of_values = list()
    list_of_ranges_for_duplicate_conditional_formatting = list()
    for prj_line_number, sub_dict in values_dict.items():
        current_row = _merged_cell_for_prj_line_number(ws, current_row, prj_line_number)
        for train_unit_number, sub_sub_dict in sub_dict.items():
            color_bool = not color_bool  # to alternate colors
            current_row = _merged_cell_for_train_unit_number(ws, current_row, train_unit_number, color_bool)
            for cc_num, sub_sub_sub_dict in sub_sub_dict.items():
                current_row, list_of_values = (
                    _update_param_sheet_per_cc(ws, current_row, cc_num, sub_sub_sub_dict, list_of_values, color_bool))
                list_of_ranges_for_duplicate_conditional_formatting.append(
                    f"$B${current_row-nb_of_diff_values}:$D${current_row-1}")
    _set_up_conditional_formatting(ws, list_of_ranges_for_duplicate_conditional_formatting)


def _update_param_sheet_per_cc(ws: xl_ws.Worksheet, current_row: int, cc_num: int,
                               param_dict: dict[str, Union[str, list[tuple[int, str]]]],
                               list_of_all_values: list[tuple[str, int, int]],
                               color_bool: bool
                               ) -> tuple[int, list[tuple[str, int, int]]]:

    for param_pattern, param_values in param_dict.items():
        if param_pattern == get_pattern(CC_ID_REGEX_PATTERN):
            param_values: str
            current_row = _merged_cell_for_cc_id(ws, current_row, cc_num, param_pattern, param_values, color_bool)
        elif param_pattern in [get_pattern(CC_PMC_ALPHA_ADDRESS_REGEX_PATTERN),
                               get_pattern(CC_PMC_BETA_ADDRESS_REGEX_PATTERN),
                               get_pattern(CC_PMC_SSH_PUBLIC_KEY_REGEX_PATTERN)]:
            param_values: list[tuple[int, str]]
            current_row = _add_row_for_param(ws, current_row, cc_num, param_pattern, param_values, list_of_all_values,
                                             color_bool)
    return current_row, list_of_all_values


def _merged_cell_for_prj_line_number(ws: xl_ws.Worksheet, current_row: int, prj_line_number: int) -> int:
    create_merged_cell(ws, f"LINE NUMBER {prj_line_number}",
                       start_row=current_row, start_column=PMC_FIRST_COLUMN,
                       end_row=current_row, end_column=STATUS_COLUMN - 1,
                       font_size=16, bold=True, align_horizontal=XlAlign.center, borders=True)
    return current_row + 1


def _merged_cell_for_train_unit_number(ws: xl_ws.Worksheet, current_row: int, train_unit_number: int,
                                       color_bool: bool) -> int:
    bg_color = XlBgColor.blue if color_bool else XlBgColor.green
    create_merged_cell(ws, f"{TRAIN_UNIT_ID} = {train_unit_number}",
                       start_row=current_row, start_column=PMC_FIRST_COLUMN,
                       end_row=current_row, end_column=STATUS_COLUMN - 1,
                       font_size=14, bold=True, bg_color=bg_color, align_horizontal=XlAlign.center, borders=True)
    return current_row + 1


def _merged_cell_for_cc_id(ws: xl_ws.Worksheet, current_row: int, cc_num: int, cc_id_pattern: str, cc_id_value: str,
                           color_bool: bool) -> int:
    cc_id_name = cc_id_pattern.replace("CCx", f"CC{cc_num}")
    bg_color = XlBgColor.blue if color_bool else XlBgColor.green
    create_merged_cell(ws, f"{cc_id_name} = {cc_id_value}",
                       start_row=current_row, start_column=PMC_FIRST_COLUMN,
                       end_row=current_row, end_column=STATUS_COLUMN - 1,
                       font_size=12, bold=True, bg_color=bg_color, align_horizontal=XlAlign.center, borders=True)
    return current_row + 1


def _add_row_for_param(ws: xl_ws.Worksheet, current_row: int, cc_num: int, param_pattern: str,
                       param_values: list[tuple[int, str]], list_of_all_values: list[tuple[str, int, int]],
                       color_bool: bool) -> int:
    bg_color = XlBgColor.light_blue if color_bool else XlBgColor.light_green
    # Write the PMC header line
    if param_pattern != get_pattern(CC_PMC_BETA_ADDRESS_REGEX_PATTERN):
        current_col = PMC_FIRST_COLUMN
        for pmc_num in range(1, NB_PMC+1):
            create_cell(ws, f"PMC {pmc_num}", row=current_row, column=current_col,
                        bold=True, bg_color=bg_color, align_horizontal=XlAlign.center, borders=True)
            current_col += 1
        current_row += 1
    # Write the parameter name cell
    param_name = param_pattern.replace("CCx", f"CC{cc_num}")
    create_cell(ws, f"{param_name}", row=current_row, column=PARAMETER_NAME_COLUMN,
                bg_color=bg_color, borders=True)
    # Write the parameter values for all the PMC
    current_col = PMC_FIRST_COLUMN
    dict_of_status = dict()
    for pmc_num, param_value in param_values:
        create_cell(ws, f"{param_value}", row=current_row, column=current_col,
                    bg_color=bg_color, borders=True)
        dict_of_status[pmc_num] = _manage_status(param_value, current_row, current_col, list_of_all_values)
        list_of_all_values.append((param_value, current_row, current_col))
        current_col += 1
    # Write the status and comments
    _set_status_and_comments_columns(ws, current_row, dict_of_status)
    return current_row + 1


def _manage_status(current_value: str, current_row: int, current_col: int,
                   list_of_all_values: list[tuple[str, int, int]]) -> dict[str, Union[str, list[str]]]:
    duplicate_cells = list()
    for value, row, column in list_of_all_values:
        if current_value == value:
            duplicate_cells.append(f"{get_xl_column_letter(column)}{row}")
    current_cell = f"{get_xl_column_letter(current_row)}{current_col}"
    return {"current_cell": current_cell, "duplicate_cells": duplicate_cells}


def _set_status_and_comments_columns(ws: xl_ws.Worksheet, current_row: int,
                                     dict_of_status: dict[int, dict[str, Union[str, list[str]]]]) -> None:
    # Status cell
    row_status = "KO" if any([status["duplicate_cells"] for status in dict_of_status.values()]) else "OK"
    create_cell(ws, f"{row_status}", row=current_row, column=STATUS_COLUMN,
                align_horizontal=XlAlign.center, borders=True)
    # Comments cell
    if row_status == "OK":
        create_cell(ws, None, row=current_row, column=COMMENTS_COLUMN,
                    line_wrap=True, borders=True)
    else:
        list_of_comments = list()
        for pmc_num, pmc_status_dict in dict_of_status.items():
            duplicate_cells = pmc_status_dict["duplicate_cells"]
            _rewrite_status_of_previous_cells(ws, duplicate_cells)
            list_of_comments.append(f"Value for PMC {pmc_num} is in duplicate with cell " +
                                    " and cell ".join(duplicate_cells) + ".")
        create_cell(ws, "\n".join(list_of_comments), row=current_row, column=COMMENTS_COLUMN,
                    line_wrap=True, borders=True)
    # Extra Status and Comments cells
    if ws.title == PMC_IP_ADDRESS_SHEET_NAME:
        create_cell(ws, None, row=current_row, column=IP_ADDRESS_STATUS2_COLUMN,
                    align_horizontal=XlAlign.center, borders=True)
        create_cell(ws, None, row=current_row, column=IP_ADDRESS_COMMENTS2_COLUMN,
                    line_wrap=True, borders=True)


def _rewrite_status_of_previous_cells(ws: xl_ws.Worksheet, duplicate_cells: list[str]) -> None:
    for cell in duplicate_cells:
        row, _ = get_row_and_column_from_cell(cell=cell)
        create_cell(ws, "KO", row=row, column=STATUS_COLUMN)


def _set_up_conditional_formatting(ws: xl_ws.Worksheet, list_of_ranges: list[str]):
    whole_range = " ".join(list_of_ranges).strip()
    add_unique_values_conditional_formatting(ws, whole_range, XlFontColor.ok, XlBgColor.ok)
    add_duplicate_values_conditional_formatting(ws, whole_range, XlFontColor.ko, XlBgColor.ko)
