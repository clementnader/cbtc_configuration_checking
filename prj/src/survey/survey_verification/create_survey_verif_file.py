#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...dc_sys import *
from ..survey_types import *
from ..survey_utils import *


__all__ = ["create_survey_verif_file"]


SURVEY_VERIF_TEMPLATE_RELATIVE_PATH = os.path.join("..", "..", "templates", "template_survey_verification.xlsx")
SURVEY_VERIF_TEMPLATE = get_full_path(__file__, SURVEY_VERIF_TEMPLATE_RELATIVE_PATH)

OUTPUT_DIRECTORY = DESKTOP_DIRECTORY
# OUTPUT_DIRECTORY = os.path.join(DESKTOP_DIRECTORY, "Correspondence with Site Survey")
VERIF_FILE_NAME = "Correspondence with Site Survey.xlsx"

START_ROW = 6
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
COMMENTS_COL = "K"
MANUAL_VERIFICATION_COL = "L"

TOOL_NAME = "Survey_Checking"


def create_survey_verif_file(survey_verif_dict: dict[str, dict[str, dict]], block_def_exists_bool: bool,
                             tool_version: str):
    try:
        res_file_path = _create_verif_file(survey_verif_dict, block_def_exists_bool, tool_version)
    except KeyboardInterrupt:
        _create_verif_file(survey_verif_dict, block_def_exists_bool, tool_version)
        raise KeyboardInterrupt
    return res_file_path


def _create_verif_file(survey_verif_dict: dict[str, dict[str, dict]], block_def_exists_bool: bool,
                       tool_version: str):
    if block_def_exists_bool:
        wb = load_xlsx_wb(SURVEY_VERIF_TEMPLATE.removesuffix(".xlsx") + "_block_def.xlsx")
    else:
        wb = load_xlsx_wb(SURVEY_VERIF_TEMPLATE)

    update_header_sheet_for_verif_file(wb, TOOL_NAME, tool_version)
    _update_menu_sheet(wb)

    for sheet_name, verif_dict in survey_verif_dict.items():
        ws = wb.get_sheet_by_name(sheet_name)
        extra_column = (sheet_name == "Block_Joint") and block_def_exists_bool
        _update_verif_sheet(sheet_name, ws, verif_dict, extra_column)

    verif_file_name = f" - {get_c_d470_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.join(OUTPUT_DIRECTORY, verif_file_name)
    save_xl_file(wb, res_file_path)
    print_success(f"\"Correspondence with Site Survey\" verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    return res_file_path


def _update_menu_sheet(wb):
    if get_ga_version() >= (7, 2, 0, 0):
        return
    ws = wb.get_sheet_by_name("Survey")
    ws.delete_rows(17)  # for older GA versions, delete PSD line that was not verified here


def _update_verif_sheet(sheet_name: str, ws, verif_dict: dict[str, dict], extra_column: bool) -> None:
    tolerance_dict = _get_tolerance_dict(sheet_name)
    multiple_dc_sys_objets = _get_multiple_dc_sys_objets(sheet_name)
    multiple_survey_objets = _get_multiple_survey_objets(sheet_name)
    row: int
    for row, (obj_full_name, obj_val) in enumerate(verif_dict.items(), start=START_ROW):
        obj_name = obj_full_name[0]
        dc_sys_sheet = obj_val["dc_sys_sheet"]
        dc_sys_track = obj_val["dc_sys_track"]
        block_def_limit_name = obj_val.get("block_def_limit_name")
        dc_sys_kp = obj_val["dc_sys_kp"]
        survey_name = obj_val["survey_name"]
        survey_type = obj_val["survey_type"]
        survey_track = obj_val["survey_track"]
        surveyed_kp = obj_val["surveyed_kp"]
        surveyed_kp_comment = obj_val["surveyed_kp_comment"]
        comments = obj_val["comments"]

        obj_name = None if dc_sys_sheet is None else obj_name

        tolerance = _get_tolerance(tolerance_dict, dc_sys_sheet)
        dc_sys_color = _get_dc_sys_color(multiple_dc_sys_objets, dc_sys_sheet)
        survey_color = _get_survey_color(multiple_survey_objets, survey_type)

        reverse_polarity = check_polarity(dc_sys_kp, surveyed_kp)

        _add_line_info(ws, row, obj_name, dc_sys_sheet, dc_sys_track, dc_sys_kp,
                       survey_name, survey_type, survey_track, surveyed_kp, dc_sys_color, survey_color,
                       extra_column)
        if extra_column:
            _add_block_def_info(ws, row, block_def_limit_name)
        _add_line_cell_comments(ws, row, surveyed_kp_comment, extra_column)
        _add_line_calculations(ws, row, tolerance, extra_column)
        _add_line_comments_column(ws, row, comments, tolerance, reverse_polarity, extra_column)


def _add_line_info(ws, row: int, obj_name: str, dc_sys_sheet: str, dc_sys_track: str, dc_sys_kp: float,
                   survey_name: str, survey_type: str, survey_track: float, surveyed_kp: float,
                   dc_sys_color: str, survey_color: str, extra_column: bool) -> None:
    # Name
    create_cell(ws, obj_name, row=row, column=NAME_COL, borders=True)
    if obj_name is not None:
        set_bg_color(ws, dc_sys_color, row=row, column=NAME_COL)
    # DC_SYS Sheet
    create_cell(ws, dc_sys_sheet, row=row, column=DC_SYS_SHEET_COL, borders=True)
    if dc_sys_sheet is not None:
        set_bg_color(ws, dc_sys_color, row=row, column=DC_SYS_SHEET_COL)
    # DC_SYS Track
    create_cell(ws, dc_sys_track, row=row, column=DC_SYS_TRACK_COL, borders=True)
    if dc_sys_track is not None:
        set_bg_color(ws, dc_sys_color, row=row, column=DC_SYS_TRACK_COL)
    # DC_SYS KP
    create_cell(ws, dc_sys_kp, row=row, column=DC_SYS_KP_COL, borders=True)
    if dc_sys_kp is not None:
        set_bg_color(ws, dc_sys_color, row=row, column=DC_SYS_KP_COL)
    # Survey Name
    create_cell(ws, survey_name, row=row, column=_get_column(SURVEY_NAME_COL, extra_column), borders=True)
    if survey_name is not None:
        set_bg_color(ws, survey_color, row=row, column=_get_column(SURVEY_NAME_COL, extra_column))
    # Survey Type
    create_cell(ws, survey_type, row=row, column=_get_column(SURVEY_TYPE_COL, extra_column), borders=True)
    if survey_type is not None:
        set_bg_color(ws, survey_color, row=row, column=_get_column(SURVEY_TYPE_COL, extra_column))
    # Survey Track
    create_cell(ws, survey_track, row=row, column=_get_column(SURVEY_TRACK_COL, extra_column), borders=True)
    if survey_track is not None:
        set_bg_color(ws, survey_color, row=row, column=_get_column(SURVEY_TRACK_COL, extra_column))
    # Surveyed KP
    create_cell(ws, surveyed_kp, row=row, column=_get_column(SURVEYED_KP_COL, extra_column), borders=True)
    if surveyed_kp is not None:
        set_bg_color(ws, survey_color, row=row, column=_get_column(SURVEYED_KP_COL, extra_column))


def _add_block_def_info(ws, row: int, block_def_limit_name: str) -> None:
    # Block Def. Limit Name
    create_cell(ws, block_def_limit_name, row=row, column=BLOCK_DEF_LIMIT_NAME_COL, borders=True)
    if block_def_limit_name is not None:
        set_bg_color(ws, XlBgColor.light_grey, row=row, column=BLOCK_DEF_LIMIT_NAME_COL)


def _add_line_cell_comments(ws, row: int, surveyed_kp_comment: str, extra_column: bool) -> None:
    # Comments on Surveyed KP cell to tell from which survey info comes
    if surveyed_kp_comment is not None:
        add_cell_comment(ws, surveyed_kp_comment, row=row, column=_get_column(SURVEYED_KP_COL, extra_column))


def _add_line_calculations(ws, row: int, tolerance: str, extra_column: bool) -> None:
    # Difference
    difference_formula = (f'= IF(ISBLANK({NAME_COL}{row}), "Not in DC_SYS", '
                          f'IF(ISBLANK({_get_column(SURVEY_NAME_COL, extra_column)}{row}), "Not Surveyed", '
                          f'{DC_SYS_KP_COL}{row} - {_get_column(SURVEYED_KP_COL, extra_column)}{row}))')
    create_cell(ws, difference_formula, row=row, column=_get_column(DIFFERENCE_COL, extra_column), borders=True)
    set_fixed_number_of_digits(ws, 4, row=row, column=_get_column(DIFFERENCE_COL, extra_column))
    # Status
    status_formula = (f'= IF({_get_column(DIFFERENCE_COL, extra_column)}{row} = "Not in DC_SYS", "Not in DC_SYS", '
                      f'IF({_get_column(DIFFERENCE_COL, extra_column)}{row} = "Not Surveyed", "Not Surveyed", '
                      f'IF(ABS({_get_column(DIFFERENCE_COL, extra_column)}{row}) <= {tolerance}, "OK", "KO")))')
    create_cell(ws, status_formula, row=row, column=_get_column(STATUS_COL, extra_column),
                borders=True, center_horizontal=True)


def _add_line_comments_column(ws, row: int, comments: str, tolerance: str, reverse_polarity: bool,
                              extra_column: bool) -> None:
    if reverse_polarity:
        if comments is None:
            full_comments = '= '
        else:
            full_comments = f'= "{comments}\n\n" & '
        full_comments += (f'"Opposite sign in survey.\n'
                          f'Difference with absolute signs makes " & '
                          f'ROUND(ABS({DC_SYS_KP_COL}{row}) - '
                          f'ABS({_get_column(SURVEYED_KP_COL, extra_column)}{row}), 4) & ",\nwhich is "'
                          f' & IF(ABS(ABS({DC_SYS_KP_COL}{row}) - '
                          f'ABS({_get_column(SURVEYED_KP_COL, extra_column)}{row})) <= {tolerance},'
                          f' "lower", "larger") & " than the tolerance " & {tolerance}'
                          f' & IF(ABS(ABS({DC_SYS_KP_COL}{row}) - '
                          f'ABS({_get_column(SURVEYED_KP_COL, extra_column)}{row})) <= {tolerance},'
                          f' " -> OK", " -> KO") & "."')
    else:
        full_comments = comments
    # Comments
    create_cell(ws, full_comments, row=row, column=_get_column(COMMENTS_COL, extra_column),
                borders=True, line_wrap=True)
    if reverse_polarity:
        # line feeds inside a formula are not directly taken into account by the line wrap to autofit the row height
        extra_row = 1 if comments else 0
        adjust_fixed_row_height(ws, row=row, column=_get_column(COMMENTS_COL, extra_column), extra_row=extra_row)
    # Manual Verification
    create_cell(ws, None, row=row, column=_get_column(MANUAL_VERIFICATION_COL, extra_column),
                borders=True, center_horizontal=True)


def _get_tolerance_dict(sheet_name: str) -> Optional[Union[str, dict[str, str]]]:
    for val in SURVEY_TYPES_DICT.values():
        if val["res_sheet"] == sheet_name:
            return val["tol"]
    print_error(f"{sheet_name = } not found inside SURVEY_TYPES_DICT:\n"
                f"{SURVEY_TYPES_DICT = }")
    return None


def _get_tolerance(tolerance_dict: Optional[Union[str, dict[str, str]]], dc_sys_sheet: str) -> Optional[str]:
    if tolerance_dict is None:
        return None
    if isinstance(tolerance_dict, str):
        return tolerance_dict
    return tolerance_dict.get(dc_sys_sheet)


def _get_multiple_dc_sys_objets(sheet_name: str) -> Optional[list]:
    for val in SURVEY_TYPES_DICT.values():
        if val["res_sheet"] == sheet_name:
            return val.get("multiple_dc_sys_objets")
    print_error(f"{sheet_name = } not found inside SURVEY_TYPES_DICT:\n"
                f"{SURVEY_TYPES_DICT = }")
    return None


def _get_dc_sys_color(multiple_dc_sys_objets: Optional[list], dc_sys_sheet: str):
    list_colors = [XlBgColor.light_yellow, XlBgColor.light_orange, XlBgColor.light_pink]
    if dc_sys_sheet is None:
        return list_colors[0]
    if not multiple_dc_sys_objets:
        return list_colors[0]
    for obj, color in zip(multiple_dc_sys_objets, list_colors):
        if obj == dc_sys_sheet:
            return color
    print_warning(f"{dc_sys_sheet = } not found inside multiple_dc_sys_objets or not enough colors defined:\n"
                  f"{multiple_dc_sys_objets = }\n"
                  f"{list_colors = }")
    return list_colors[0]


def _get_multiple_survey_objets(sheet_name: str) -> Optional[list[tuple]]:
    for val in SURVEY_TYPES_DICT.values():
        if val["res_sheet"] == sheet_name:
            return val.get("multiple_survey_objets")
    print_error(f"{sheet_name = } not found inside SURVEY_TYPES_DICT:\n"
                f"{SURVEY_TYPES_DICT = }")
    return None


def _get_survey_color(multiple_survey_objets: Optional[list[tuple]], survey_type: str):
    list_colors = [XlBgColor.light_green, XlBgColor.light_blue2, XlBgColor.light_blue3]
    if survey_type is None:
        return list_colors[0]
    if not multiple_survey_objets:
        return list_colors[0]
    for obj, color in zip(multiple_survey_objets, list_colors):
        obj_name, inf_lim, sup_lim = obj
        list_survey_objects = SURVEY_TYPES_DICT[obj_name]["survey_type_names"][inf_lim:sup_lim]
        if survey_type.upper() in list_survey_objects:
            return color
    print_warning(f"{survey_type = } not found inside multiple_survey_objets or not enough colors defined:\n"
                  f"{multiple_survey_objets = }\n"
                  f"{list_colors = }")
    return list_colors[0]


def _get_column(default_col: str, extra_col: bool = False) -> str:
    if not extra_col or default_col < BLOCK_DEF_LIMIT_NAME_COL:
        return default_col
    else:
        return get_xl_column_letter(get_xl_column_number(default_col) + 1)
