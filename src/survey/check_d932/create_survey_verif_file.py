#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...dc_sys import *
from ..d932_utils import *


__all__ = ["create_survey_verif_file"]


SURVEY_VERIF_TEMPLATE_RELATIVE_PATH = os.path.join("..", "..", "templates", "template_survey_verification.xlsx")
FILE_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))
SURVEY_VERIF_TEMPLATE = os.path.join(FILE_DIRECTORY_PATH, SURVEY_VERIF_TEMPLATE_RELATIVE_PATH)

OUTPUT_DIRECTORY = os.path.join(os.getenv("UserProfile"), r"Desktop")
VERIF_FILE_NAME = "Correspondence with Site Survey.xlsx"

START_LINE = 6
NAME_COL = "A"
TRACK_COL = "B"
DC_SYS_KP_COL = "C"
SURVEY_TRACK_COL = "D"
SURVEYED_KP_COL = "E"
DESIGN_KP_COL = "F"
DIFFERENCE_COL = "G"
STATUS_COL = "H"


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
        sh = wb.get_sheet_by_name(sheet_name)
        _update_verif_sheet(sheet_name, sh, verif_dict)
    verif_file_name = f"_{get_c_d470_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.join(OUTPUT_DIRECTORY, verif_file_name)
    try:
        wb.save(res_file_path)
    except PermissionError:
        print_error(f"Permission denied to write at {res_file_path = }."
                    f"\nYou have to close it if you want it to be overwritten.")
        if input(f"Do you want to retry? (Y/N) ").upper() in ["Y", "YES"]:
            wb.save(res_file_path)
    print_success(f"Correspondence with Site Survey verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    return res_file_path


def _update_verif_sheet(sheet_name: str, sh, verif_dict: dict[str, dict]):
    tolerance = _get_tolerance(sheet_name)
    for line, (obj_name, obj_val) in enumerate(verif_dict.items(), start=START_LINE):
        track = obj_val["track"]
        dc_sys_kp = obj_val["dc_sys_kp"]
        survey_obj_comment = obj_val["survey_object_comment"]
        survey_track = obj_val["survey_track"]
        survey_track_comment = obj_val["survey_track_comment"]
        surveyed_kp = obj_val["surveyed_kp"]
        surveyed_kp_comment = obj_val["surveyed_kp_comment"]
        design_kp = obj_val["design_kp"]
        design_kp_comment = obj_val["design_kp_comment"]
        _add_line_info(sh, line, obj_name, track, dc_sys_kp, survey_track, surveyed_kp, design_kp)
        _add_line_comments(sh, line, survey_obj_comment, survey_track_comment, surveyed_kp_comment, design_kp_comment)
        _add_line_calculations(sh, line, tolerance)


def _add_line_info(sh, line: int, obj_name: str, track: str, dc_sys_kp: float,
                   survey_track: float, surveyed_kp: float, design_kp: float):
    sh[f"{NAME_COL}{line}"] = obj_name
    sh[f"{TRACK_COL}{line}"] = track
    sh[f"{DC_SYS_KP_COL}{line}"] = dc_sys_kp
    sh[f"{SURVEY_TRACK_COL}{line}"] = survey_track
    sh[f"{SURVEYED_KP_COL}{line}"] = surveyed_kp
    sh[f"{DESIGN_KP_COL}{line}"] = design_kp


def _add_line_comments(sh, line: int, survey_object_comment: str, survey_track_comment: str,
                       surveyed_kp_comment: str, design_kp_comment: str):
    if survey_object_comment is not None:
        add_cell_comment(sh, survey_object_comment, cell=f"{NAME_COL}{line}")
    if survey_track_comment is not None:
        add_cell_comment(sh, survey_track_comment, cell=f"{SURVEY_TRACK_COL}{line}")
    if surveyed_kp_comment is not None:
        add_cell_comment(sh, surveyed_kp_comment, cell=f"{SURVEYED_KP_COL}{line}")
    if design_kp_comment is not None:
        add_cell_comment(sh, design_kp_comment, cell=f"{DESIGN_KP_COL}{line}")


def _add_line_calculations(sh, line: int, tolerance: str):
    sh[f"{DIFFERENCE_COL}{line}"] = f'= IF(ISBLANK(A{line}), "", ' \
                                    f'IF(ISBLANK(C{line}), "Not in DC_SYS", ' \
                                    f'IF(ISBLANK(E{line}), "Not Surveyed", ' \
                                    f'C{line} - E{line})))'
    sh[f"{STATUS_COL}{line}"] = f'= IF(G{line} = "", "", ' \
                                f'IF(G{line} = "Not in DC_SYS", "Not in DC_SYS", ' \
                                f'IF(G{line} = "Not Surveyed", "Not Surveyed", ' \
                                f'IF(ABS(G{line}) <= {tolerance}, "OK", "KO"))))'


def _get_tolerance(sheet_name: str):
    for val in SURVEY_TYPES_DICT.values():
        if val["res_sheet"] == sheet_name:
            return val["tol"]
    print_error(f"{sheet_name = } not found inside SURVEY_TYPES_DICT:\n"
                f"{SURVEY_TYPES_DICT = }")
    return None
