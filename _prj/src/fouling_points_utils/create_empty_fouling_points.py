#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["init_fouling_points_file"]


FOULING_POINT_TEMPLATE = os.path.join(TEMPLATE_DIRECTORY, "template_fouling_points.xlsx")

OUTPUT_DIRECTORY = "."
OUTPUT_FILE_NAME = "Fouling Points.xlsx"
FOULING_POINT_SHEET = "Fouling_Point"

FOULING_POINT_START_ROW = 3
SW_NAME_COL = "A"
SW_KP_COL = "B"
FOULING_POINT_KP_COL = "C"
SW_KP_COL_OTHER_TRACK = "D"
FOULING_POINT_KP_COL_OTHER_TRACK = "E"
DIFFERENCE_COL = "F"
DIFFERENCE_COL_OTHER_TRACK = "G"

GREEN = "DAF2D0"
PURPLE = "F2CEEF"
SWITCH_COLORS = ["94DCF8", "83E28E", "E49EDD", "F7C7AC"]

FILE_TITLE = "Fouling Points"


def init_fouling_points_file():
    # Load the Excel template for the verification file
    wb = load_xlsx_wb(FOULING_POINT_TEMPLATE, template=True)
    # Create Header sheet
    create_empty_header_sheet(wb)
    # Update Header sheet
    update_header_sheet_for_verif_file(wb, title=FILE_TITLE, c_d470=get_current_version())

    # Initialize Fouling Point sheet
    _initialize_fp_sheet(wb)

    # Save workbook
    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(OUTPUT_FILE_NAME))
    res_file_path = os.path.realpath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"\"Fouling Points\" empty file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    return res_file_path


def _initialize_fp_sheet(wb: openpyxl.workbook.Workbook) -> None:
    ws = wb[FOULING_POINT_SHEET]
    sw_dict = load_sheet(DCSYS.Aig)
    sw_list = list(sw_dict.keys())

    for row, sw_name in enumerate(sw_list, start=FOULING_POINT_START_ROW):
        create_cell(ws, sw_name, row = row, column = SW_NAME_COL, bg_color=SWITCH_COLORS[0], borders=True)
        create_cell(ws, None, row = row, column = SW_KP_COL, bg_color=GREEN, borders=True)
        create_cell(ws, None, row = row, column = FOULING_POINT_KP_COL, bg_color=GREEN, borders=True)
        create_cell(ws, None, row = row, column = SW_KP_COL_OTHER_TRACK)
        create_cell(ws, None, row = row, column = FOULING_POINT_KP_COL_OTHER_TRACK)

        sw_kp_cell = f"{SW_KP_COL}{row}"
        fp_kp_cell = f"{FOULING_POINT_KP_COL}{row}"
        difference_formula = (f"= IF(AND(ISNUMBER({sw_kp_cell}), ISNUMBER({fp_kp_cell})),\n "
                              f"ABS({sw_kp_cell} - {fp_kp_cell}), \n"
                              f"\"\")")

        sw_kp_cell_other_track = f"{SW_KP_COL_OTHER_TRACK}{row}"
        fp_kp_cell_other_track = f"{FOULING_POINT_KP_COL_OTHER_TRACK}{row}"
        difference_formula_other_track = (f"= IF(AND(ISNUMBER({sw_kp_cell_other_track}), "
                                          f"ISNUMBER({fp_kp_cell_other_track})),\n "
                                          f"ABS({sw_kp_cell_other_track} - {fp_kp_cell_other_track}), \n"
                                          f"\"\")")

        create_cell(ws, difference_formula, row = row, column = DIFFERENCE_COL, bg_color=PURPLE, borders=True)
        create_cell(ws, difference_formula_other_track, row = row, column = DIFFERENCE_COL_OTHER_TRACK)
