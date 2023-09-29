#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...dc_sys import *
from ..d932_utils import *


__all__ = ["create_survey_verif_file"]


SURVEY_VERIF_TEMPLATE_RELATIVE_PATH = os.path.join("..", "..", "templates", "template_survey_verification.xlsx")
SURVEY_VERIF_TEMPLATE = get_full_path(__file__, SURVEY_VERIF_TEMPLATE_RELATIVE_PATH)

OUTPUT_DIRECTORY = DESKTOP_DIRECTORY
VERIF_FILE_NAME = "Correspondence with Site Survey.xlsx"

START_LINE = 5
NAME_COL = "A"
TRACK_COL = "B"
DC_SYS_KP_COL = "C"
SURVEY_TRACK_COL = "D"
SURVEYED_KP_COL = "E"
DIFFERENCE_COL = "F"
STATUS_COL = "G"


def create_survey_verif_file(survey_verif_dict: dict[str, dict[str, dict]]):
    try:
        res_file_path = _create_verif_file(survey_verif_dict)
    except KeyboardInterrupt:
        _create_verif_file(survey_verif_dict)
        raise KeyboardInterrupt
    return res_file_path


def _create_verif_file(survey_verif_dict: dict[str, dict[str, dict]]):
    wb = load_xlsx_wb(SURVEY_VERIF_TEMPLATE)
    for sheet_name, verif_dict in survey_verif_dict.items():
        ws = wb.get_sheet_by_name(sheet_name)
        _update_verif_sheet(sheet_name, ws, verif_dict)
    verif_file_name = f" - {get_c_d470_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.join(OUTPUT_DIRECTORY, verif_file_name)
    save_xl_file(wb, res_file_path)
    print_success(f"Correspondence with Site Survey verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    return res_file_path


def _update_verif_sheet(sheet_name: str, ws, verif_dict: dict[str, dict]):
    tolerance = _get_tolerance(sheet_name)
    for line, (obj_name, obj_val) in enumerate(verif_dict.items(), start=START_LINE):
        track = obj_val["track"]
        dc_sys_kp = obj_val["dc_sys_kp"]
        survey_track = obj_val["survey_track"]
        surveyed_kp = obj_val["surveyed_kp"]
        surveyed_kp_comment = obj_val["surveyed_kp_comment"]
        _add_line_info(ws, line, obj_name, track, dc_sys_kp, survey_track, surveyed_kp)
        _add_line_comments(ws, line, surveyed_kp_comment)
        _add_line_calculations(ws, line, tolerance)


def _add_line_info(ws, line: int, obj_name: str, track: str, dc_sys_kp: float,
                   survey_track: float, surveyed_kp: float):
    ws[f"{NAME_COL}{line}"] = obj_name
    ws[f"{TRACK_COL}{line}"] = track
    if track is not None:
        set_bg_color(ws, hex_color=XlBgColor.light_yellow, cell=f"{TRACK_COL}{line}")
    ws[f"{DC_SYS_KP_COL}{line}"] = dc_sys_kp
    if dc_sys_kp is not None:
        set_bg_color(ws, hex_color=XlBgColor.light_yellow, cell=f"{DC_SYS_KP_COL}{line}")
    ws[f"{SURVEY_TRACK_COL}{line}"] = survey_track
    if survey_track is not None:
        set_bg_color(ws, hex_color=XlBgColor.light_green, cell=f"{SURVEY_TRACK_COL}{line}")
    ws[f"{SURVEYED_KP_COL}{line}"] = surveyed_kp
    if surveyed_kp is not None:
        set_bg_color(ws, hex_color=XlBgColor.light_green, cell=f"{SURVEYED_KP_COL}{line}")


def _add_line_comments(ws, line: int, surveyed_kp_comment: str):
    add_cell_comment(ws, surveyed_kp_comment, cell=f"{SURVEYED_KP_COL}{line}")


def _add_line_calculations(ws, line: int, tolerance: str):
    ws[f"{DIFFERENCE_COL}{line}"] = f'= IF(ISBLANK({NAME_COL}{line}), "", ' \
                                    f'IF(ISBLANK({DC_SYS_KP_COL}{line}), "Not in DC_SYS", ' \
                                    f'IF(ISBLANK({SURVEYED_KP_COL}{line}), "Not Surveyed", ' \
                                    f'{DC_SYS_KP_COL}{line} - {SURVEYED_KP_COL}{line})))'
    ws[f"{STATUS_COL}{line}"] = f'= IF({DIFFERENCE_COL}{line} = "", "", ' \
                                f'IF({DIFFERENCE_COL}{line} = "Not in DC_SYS", "Not in DC_SYS", ' \
                                f'IF({DIFFERENCE_COL}{line} = "Not Surveyed", "Not Surveyed", ' \
                                f'IF(ABS({DIFFERENCE_COL}{line}) <= {tolerance}, "OK", "KO"))))'
    center_horizontal_alignment(ws, cell=f"{STATUS_COL}{line}")


def _get_tolerance(sheet_name: str):
    for val in SURVEY_TYPES_DICT.values():
        if val["res_sheet"] == sheet_name:
            return val["tol"]
    print_error(f"{sheet_name = } not found inside SURVEY_TYPES_DICT:\n"
                f"{SURVEY_TYPES_DICT = }")
    return None
