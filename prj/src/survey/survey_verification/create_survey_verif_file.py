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
VERIF_FILE_NAME = "Correspondence with Site Survey.xlsx"

START_ROW = 5
NAME_COL = "A"
TRACK_COL = "B"
DC_SYS_KP_COL = "C"
SURVEY_TRACK_COL = "D"
SURVEYED_KP_COL = "E"
DIFFERENCE_COL = "F"
STATUS_COL = "G"
COMMENTS_COL = "H"
MANUAL_VERIFICATION_COL = "I"


def create_survey_verif_file(survey_verif_dict: dict[str, dict[str, dict]]):
    try:
        res_file_path = _create_verif_file(survey_verif_dict)
    except KeyboardInterrupt:
        _create_verif_file(survey_verif_dict)
        raise KeyboardInterrupt
    return res_file_path


def _create_verif_file(survey_verif_dict: dict[str, dict[str, dict]]):
    wb = load_xlsx_wb(SURVEY_VERIF_TEMPLATE)
    update_header_sheet_for_verif_file(wb)
    _update_menu_sheet(wb)
    for sheet_name, verif_dict in survey_verif_dict.items():
        ws = wb.get_sheet_by_name(sheet_name)
        _update_verif_sheet(sheet_name, ws, verif_dict)
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


def _update_verif_sheet(sheet_name: str, ws, verif_dict: dict[str, dict]) -> None:
    tolerance = _get_tolerance(sheet_name)
    for row, (obj_full_name, obj_val) in enumerate(verif_dict.items(), start=START_ROW):
        obj_name = obj_full_name[0]
        track = obj_val["track"]
        dc_sys_kp = obj_val["dc_sys_kp"]
        survey_track = obj_val["survey_track"]
        surveyed_kp = obj_val["surveyed_kp"]
        surveyed_kp_comment = obj_val["surveyed_kp_comment"]
        comments = obj_val["comments"]

        reverse_polarity = check_polarity(dc_sys_kp, surveyed_kp)

        _add_line_info(ws, row, obj_name, track, dc_sys_kp, survey_track, surveyed_kp)
        _add_line_cell_comments(ws, row, surveyed_kp_comment)
        _add_line_calculations(ws, row, tolerance)
        _add_line_comments_column(ws, row, comments, tolerance, reverse_polarity)


def _add_line_info(ws, row: int, obj_name: str, track: str, dc_sys_kp: float,
                   survey_track: float, surveyed_kp: float) -> None:
    # Name
    create_cell(ws, obj_name, row=row, column=NAME_COL, borders=True)
    # DC_SYS Track
    create_cell(ws, track, row=row, column=TRACK_COL, borders=True)
    if track is not None:
        set_bg_color(ws, XlBgColor.light_yellow, row=row, column=TRACK_COL)
    # DC_SYS KP
    create_cell(ws, dc_sys_kp, row=row, column=DC_SYS_KP_COL, borders=True)
    if dc_sys_kp is not None:
        set_bg_color(ws, XlBgColor.light_yellow, row=row, column=DC_SYS_KP_COL)
    # Survey Track
    create_cell(ws, survey_track, row=row, column=SURVEY_TRACK_COL, borders=True)
    if survey_track is not None:
        set_bg_color(ws, XlBgColor.light_green, row=row, column=SURVEY_TRACK_COL)
    # Surveyed KP
    create_cell(ws, surveyed_kp, row=row, column=SURVEYED_KP_COL, borders=True)
    if surveyed_kp is not None:
        set_bg_color(ws, XlBgColor.light_green, row=row, column=SURVEYED_KP_COL)


def _add_line_cell_comments(ws, row: int, surveyed_kp_comment: str) -> None:
    # Comments on Surveyed KP cell to tell from which survey info comes
    if surveyed_kp_comment is not None:
        add_cell_comment(ws, surveyed_kp_comment, row=row, column=SURVEYED_KP_COL)


def _add_line_calculations(ws, row: int, tolerance: str) -> None:
    # Difference
    difference_formula = (f'= IF(ISBLANK({NAME_COL}{row}), "", '
                          f'IF(ISBLANK({DC_SYS_KP_COL}{row}), "Not in DC_SYS", '
                          f'IF(ISBLANK({SURVEYED_KP_COL}{row}), "Not Surveyed", '
                          f'{DC_SYS_KP_COL}{row} - {SURVEYED_KP_COL}{row})))')
    create_cell(ws, difference_formula, row=row, column=DIFFERENCE_COL, borders=True)
    set_fixed_number_of_digits(ws, 4, row=row, column=DIFFERENCE_COL)
    # Status
    status_formula = (f'= IF({DIFFERENCE_COL}{row} = "", "", '
                      f'IF({DIFFERENCE_COL}{row} = "Not in DC_SYS", "Not in DC_SYS", '
                      f'IF({DIFFERENCE_COL}{row} = "Not Surveyed", "Not Surveyed", '
                      f'IF(ABS({DIFFERENCE_COL}{row}) <= {tolerance}, "OK", "KO"))))')
    create_cell(ws, status_formula, row=row, column=STATUS_COL, borders=True, center_horizontal=True)


def _add_line_comments_column(ws, row: int, comments: str, tolerance: str, reverse_polarity: bool) -> None:
    if reverse_polarity:
        if comments is None:
            comments = '= '
        else:
            comments = f'= "{comments}\n\n" & '
        comments += (f'"Opposite sign in survey.\n'
                     f'Difference with absolute signs makes " & '
                     f'ROUND(ABS({DC_SYS_KP_COL}{row}) - ABS({SURVEYED_KP_COL}{row}), 4) & ",\nwhich is "'
                     f' & IF(ABS(ABS({DC_SYS_KP_COL}{row}) - ABS({SURVEYED_KP_COL}{row})) <= {tolerance},'
                     f' "lower", "larger") & " than the tolerance " & {tolerance}'
                     f' & IF(ABS(ABS({DC_SYS_KP_COL}{row}) - ABS({SURVEYED_KP_COL}{row})) <= {tolerance},'
                     f' " -> OK", " -> KO") & "."')
    # Comments
    create_cell(ws, comments, row=row, column=COMMENTS_COL, borders=True, line_wrap=True)
    if reverse_polarity:
        # line feeds inside a formula are not directly taken into account by the line wrap to autofit the row height
        adjust_fixed_row_height(ws, row=row, column=COMMENTS_COL)
    # Manual Verification
    create_cell(ws, None, row=row, column=MANUAL_VERIFICATION_COL, borders=True, center_horizontal=True)


def _get_tolerance(sheet_name: str) -> Optional[str]:
    for val in SURVEY_TYPES_DICT.values():
        if val["res_sheet"] == sheet_name:
            return val["tol"]
    print_error(f"{sheet_name = } not found inside SURVEY_TYPES_DICT:\n"
                f"{SURVEY_TYPES_DICT = }")
    return None
