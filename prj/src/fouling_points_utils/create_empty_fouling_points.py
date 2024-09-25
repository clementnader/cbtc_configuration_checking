#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..utils import *
from ..dc_sys_sheet_utils import *


FOULING_POINT_TEMPLATE = os.path.join(TEMPLATE_DIRECTORY, "Fouling Points template.xlsx")

OUTPUT_DIRECTORY = DESKTOP_DIRECTORY
FOULING_POINT_SHEET = "Fouling_Point"

FOULING_POINT_START_ROW = 3
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
    wb = load_xlsx_wb(FOULING_POINT_TEMPLATE, template=True)
    ws = wb[FOULING_POINT_SHEET]
    for row, (sw_name, sw_pos) in enumerate(sw_pos_dict.items(), start=FOULING_POINT_START_ROW):
        ws[f"{SW_NAME_COL}{row}"] = sw_name
        ws[f"{SW_KP_COL}{row}"] = sw_pos["kp"]
        ws[f"{SW_TRACK_COL}{row}"] = sw_pos["track"]
    wb.save(os.path.join(OUTPUT_DIRECTORY, "Fouling Points.xlsx"))
