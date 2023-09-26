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
SW_TRACK_COL = 'D'


def create_fouling_points_file():
    sw_pos_dict = get_switch_position_dict()
    try:
        _make_file(sw_pos_dict)
    except KeyboardInterrupt:
        _make_file(sw_pos_dict)
        raise KeyboardInterrupt


def _make_file(sw_pos_dict):
    wb = load_xlsx_wb(FOULING_POINT_TEMPLATE)
    sh = wb.get_sheet_by_name(FOULING_POINT_SHEET)
    for line, (sw_name, sw_pos) in enumerate(sw_pos_dict.items(), start=FOULING_POINT_START_LINE):
        sh[f"{SW_NAME_COL}{line}"] = sw_name
        sh[f"{SW_KP_COL}{line}"] = sw_pos["kp"]
        sh[f"{SW_TRACK_COL}{line}"] = sw_pos["track"]
    wb.save(os.path.join(OUTPUT_DIRECTORY, "Fouling Points.xlsx"))
