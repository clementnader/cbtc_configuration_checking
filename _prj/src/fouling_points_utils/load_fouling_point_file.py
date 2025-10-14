#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..utils import *
from ..database_location import DATABASE_LOCATION


__all__ = ["get_fouling_point_file", "load_fouling_point_info"]


FP_SHEET = r"Fouling_Point"
FIRST_ROW = 3
SW_NAME_COLUMN = "A"
SW_KP_COLUMN = "B"
FOULING_POINT_KP_COLUMN = "C"


def get_fouling_point_file() -> Optional[str]:
    fp_addr = DATABASE_LOCATION.fouling_point_addr
    if not fp_addr:
        return None
    display_info = f"{os.path.split(fp_addr)[-1]} (sheet \"{FP_SHEET}\")"
    return display_info


def load_fouling_point_info() -> Optional[dict[str, float]]:
    if not DATABASE_LOCATION.fouling_point_addr:
        return None
    res_dict = dict()
    wb = load_xlsx_wb(DATABASE_LOCATION.fouling_point_addr)
    ws = get_xl_sheet_by_name(wb, FP_SHEET)
    for row in range(FIRST_ROW, get_xl_number_of_rows(ws) + 1):
        sw_name = get_xl_cell_value(ws, row=row, column=SW_NAME_COLUMN)
        sw_kp = get_xl_float_value(ws, row=row, column=SW_KP_COLUMN)
        fp_kp = get_xl_float_value(ws, row=row, column=FOULING_POINT_KP_COLUMN)
        if sw_name is None or sw_kp is None or fp_kp is None:
            continue

        res_dict[sw_name] = round(abs(sw_kp - fp_kp), 9)
    return res_dict
