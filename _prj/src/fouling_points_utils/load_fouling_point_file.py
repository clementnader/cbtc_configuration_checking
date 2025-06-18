#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..database_location import DATABASE_LOC


__all__ = ["load_fouling_point_info"]


FP_SHEET = r"Fouling_Point"
FIRST_ROW = 3
SW_NAME_COLUMN = "A"
SW_KP_COLUMN = "B"
FOULING_POINT_KP_COLUMN = "C"


def load_fouling_point_info() -> Optional[dict[str, float]]:
    if DATABASE_LOC.fouling_point_addr is None:
        return None
    res_dict = dict()
    wb = load_xlsx_wb(DATABASE_LOC.fouling_point_addr)
    ws = get_xl_sheet_by_name(wb, FP_SHEET)
    for row in range(FIRST_ROW, get_xl_number_of_rows(ws) + 1):
        sw_name = get_xl_cell_value(ws, row=row, column=SW_NAME_COLUMN)
        sw_kp = get_xl_float_value(ws, row=row, column=SW_KP_COLUMN)
        fp_kp = get_xl_float_value(ws, row=row, column=FOULING_POINT_KP_COLUMN)
        if sw_name is None or sw_kp is None or fp_kp is None:
            continue

        res_dict[sw_name] = round(abs(sw_kp - fp_kp), 9)
    return res_dict
