#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ..dc_sys_utils import *

FOULING_POINT_TEMPLATE_RELATIVE_PATH = os.path.join("..", "..", "templates", "Fouling Points template.xlsx")
FILE_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))
FOULING_POINT_TEMPLATE = os.path.join(FILE_DIRECTORY_PATH, FOULING_POINT_TEMPLATE_RELATIVE_PATH)
OUTPUT_DIRECTORY = os.path.join(os.getenv("UserProfile"), r"Desktop")
FOULING_POINT_SHEET = "Fouling_Point"
FOULING_POINT_START_LINE = 3
SW_NAME_COL = 'A'
SW_KP_COL = 'B'
FOULING_POINT_COL = 'C'


def create_fouling_points_file():
    sw_pos_dict = get_switch_pos()
    wb = load_xlsx_wb(FOULING_POINT_TEMPLATE)
    sh = wb.get_sheet_by_name(FOULING_POINT_SHEET)
    for line, (sw_name, sw_pos) in enumerate(sw_pos_dict.items(), start=FOULING_POINT_START_LINE):
        sh[f"{SW_NAME_COL}{line}"] = sw_name
        sh[f"{SW_KP_COL}{line}"] = sw_pos["kp"]
    wb.save(os.path.join(OUTPUT_DIRECTORY, "Fouling Points.xlsx"))


def get_switch_pos():
    sw_dict = load_sheet("sw")
    sw_cols_name = get_cols_name("sw")

    seg_dict = load_sheet("seg")
    seg_cols_name = get_cols_name("seg")

    sw_pos_dict = dict()
    for sw, sw_info in sw_dict.items():
        track, kp = give_sw_kp_pos(sw_info, sw_cols_name, seg_dict, seg_cols_name)
        sw_pos_dict[sw] = {"track": track, "kp": kp}

    return sw_pos_dict
