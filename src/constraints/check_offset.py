#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..dc_sys.load_database.load_xl import load_wb
from ..dc_sys.dc_sys_utils import get_len_seg, get_track_limits

START_LINE = 3


def check_offset_correctness():
    wb = load_wb()
    sheet_names = wb.sheet_names()
    for sh_name in sheet_names:
        sh = wb.sheet_by_name(sh_name)
        verify_sheet(sh)


def verify_sheet(sh: xlrd.sheet):
    xlrd_line_ref = get_xlrd_line(START_LINE)
    seg_x_cols, track_kp_cols = find_seg_x_cols(sh)
    for seg_col, x_col in seg_x_cols:
        for i in range(xlrd_line_ref, sh.nrows):
            first_cell = sh.cell_value(i, 0)
            seg = sh.cell_value(i, seg_col)
            x = sh.cell_value(i, x_col)
            verif_correct_offset_seg_x(seg, x, first_cell, i, x_col, sh.name)
    for track_col, kp_col in track_kp_cols:
        for i in range(xlrd_line_ref, sh.nrows):
            first_cell = sh.cell_value(i, 0)
            track = sh.cell_value(i, track_col)
            kp = sh.cell_value(i, kp_col)
            verif_correct_offset_track_kp(track, kp, first_cell, i, kp_col, sh.name)


def verif_correct_offset_seg_x(seg, x, first_cell, line, col, sh_name):
    if first_cell == "":
        return
    if seg == "" and x == "":
        return
    if seg == "" or x == "":
        print_warning(f"Strange pair (segment/offset) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{get_xl_column(col-1)}{get_xl_line(line)} and {get_xl_column(col)}{get_xl_line(line)}"
                      f"\n{seg=}/{x=}")
        return
    if not (isinstance(x, float) or isinstance(x, int)):
        print_warning(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"Offset at {get_xl_column(col)}{get_xl_line(line)} is a string"
                      f"\n{x=}")
        x = float(x)
    x = round(x, 3)
    len_seg = get_len_seg(seg)
    if not (0 <= x):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"Offset at cell {get_xl_column(col)}{get_xl_line(line)} should be positive"
                    f"\n{x=}")
    if not (x <= len_seg):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"Offset at cell {get_xl_column(col)}{get_xl_line(line)} should be lower than "
                    f"the segment {seg} length ({len_seg})"
                    f"\n{x=}")


def verif_correct_offset_track_kp(track, kp, first_cell, line, col, sh_name):
    if first_cell == "":
        return
    if track == "" and kp == "":
        return
    if track == "" or kp == "":
        print_warning(f"Strange pair (track/KP) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{get_xl_line(line)}{get_xl_column(col-1)} and {get_xl_line(line)}{get_xl_column(col)}"
                      f"\n{track=}/{kp=}")
        return
    if not (isinstance(kp, float) or isinstance(kp, int)):
        print_warning(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"KP at {get_xl_column(col)}{get_xl_line(line)} is a string"
                      f"\n{kp=}")
        kp = float(kp)
    kp = round(kp, 3)
    min_kp, max_kp = get_track_limits(track)
    if not (min_kp <= kp):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"KP at cell {get_xl_column(col)}{get_xl_line(line)} should be larger than "
                    f"the start kp of track {track} ({min_kp})"
                    f"\n{kp=}")
    if not (kp <= max_kp):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"KP at cell {get_xl_column(col)}{get_xl_line(line)} should be lower than "
                    f"the end kp of track {track} ({max_kp})"
                    f"\n{kp=}")


def find_seg_x_cols(sh: xlrd.sheet) -> tuple[list[tuple], list[tuple]]:
    nb_cols = sh.ncols
    is_prev_seg = False
    is_prev_track = False
    seg_x_cols = list()
    track_kp_cols = list()
    for j in range(nb_cols):
        cell1 = f"{sh.cell_value(0, j)}".strip().lower()
        try:
            cell2 = f"{sh.cell_value(1, j)}".strip().lower()
            cell = cell1 if not cell2 else cell2
        except IndexError:
            cell = cell1
        if cell.endswith("seg"):
            is_prev_seg = True
            is_prev_track = False
        elif cell.endswith("voie"):
            is_prev_seg = False
            is_prev_track = True
        elif is_prev_seg and cell.endswith("x"):
            seg_x_cols.append((j-1, j))
            is_prev_seg = False
            is_prev_track = False
        elif is_prev_track and cell.endswith("pk"):
            track_kp_cols.append((j-1, j))
            is_prev_seg = False
            is_prev_track = False
        else:
            is_prev_seg = False
            is_prev_track = False
    return seg_x_cols, track_kp_cols
