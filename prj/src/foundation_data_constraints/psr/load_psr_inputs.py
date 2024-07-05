#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ...utils import *


__all__ = ["get_psr_definition"]

PSR_INPUT_FILE = (r"C:\Users\naderc\Desktop\KCR"
                  r"\CR-ASTS-GEN=Gen-PF=PW=TRA-DES-REP-108100-01.00"
                  r" - ATT 001 - Sydhavn Extension Speed limits table.xlsx")

TRACK_41_FILE = "Track 41"
TRACK_42_FILE = "Track 42"

START_LINE = 9
FROM_COLUMN = 3
TO_COLUMN = 4
SPEED_COLUMN = 40


def get_psr_definition() -> dict[str, dict[int, dict[str, float]]]:
    psr_dict = dict()
    wb = load_xlsx_wb(PSR_INPUT_FILE)
    for sheet_name, track_name in ((TRACK_41_FILE, "TRACK_41"), (TRACK_42_FILE, "TRACK_42")):
        psr_dict[track_name] = dict()
        ws = get_xl_sheet_by_name(wb, sheet_name)
        for row in range(START_LINE, get_xl_number_of_rows(ws) + 1):
            speed = get_xl_float_value(ws, row=row, column=SPEED_COLUMN)
            if speed is None:
                continue
            from_kp = get_xl_float_value(ws, row=row, column=FROM_COLUMN)
            to_kp = get_xl_float_value(ws, row=row, column=TO_COLUMN)
            psr_dict[track_name][row] = {"speed": speed, "from_kp": from_kp, "to_kp": to_kp}
    return psr_dict
