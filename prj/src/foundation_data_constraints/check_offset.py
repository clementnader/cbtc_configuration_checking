#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..dc_sys.load_database.load_xl import *
from ..dc_sys import get_len_seg, get_track_limits, from_kp_to_seg_offset, from_seg_offset_to_kp, are_points_matching


START_LINE = 3


def check_offset_correctness():
    print_title(f"Verification of the offset correctness", color=Color.mint_green)
    success = True
    wb = load_wb()
    sheet_names = get_xl_sheets(wb)
    for sh_name in sheet_names:
        sh = get_xl_sheet_by_name(wb, sh_name)
        if verify_sheet(sh) is False:
            success = False
    if success:
        print_log("No KO has been raised in the offset correctness checking.")


def verify_sheet(sh: xlrd.sheet):
    success = True
    seg_x_cols, track_kp_cols = find_seg_x_cols(sh)
    if check_correspondence_seg_x_track_kp(sh, seg_x_cols, track_kp_cols) is False:
        success = False
    for seg_col, x_col in seg_x_cols:
        for i in range(START_LINE, get_xl_sh_nb_rows(sh) + 1):
            first_cell = get_xl_cell_value(sh, line=i, col=1)
            seg = get_xl_cell_value(sh, line=i, col=seg_col)
            x = get_xl_cell_value(sh, line=i, col=x_col)
            if verif_correct_offset_seg_x(seg, x, first_cell, i, seg_col, x_col, sh.name) is False:
                success = False
    for track_col, kp_col in track_kp_cols:
        for i in range(START_LINE, get_xl_sh_nb_rows(sh) + 1):
            first_cell = get_xl_cell_value(sh, line=i, col=1)
            track = get_xl_cell_value(sh, line=i, col=track_col)
            kp = get_xl_cell_value(sh, line=i, col=kp_col)
            if verif_correct_offset_track_kp(track, kp, first_cell, i, track_col, kp_col, sh.name) is False:
                success = False
    return success


def verif_correct_offset_seg_x(seg, x, first_cell, line, seg_col, x_col, sh_name):
    success = True
    if first_cell is None:
        return
    if seg is None and x is None:
        return
    if seg is None or x is None:
        print_warning(f"Strange pair (segment/offset) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{Color.yellow}{get_xl_column(seg_col)}{line}{Color.reset} and "
                      f"{Color.yellow}{get_xl_column(x_col)}{line}{Color.reset}"
                      f"\n{seg = } / {x = }")
        return False
    if not (isinstance(x, float) or isinstance(x, int)):
        if "." in x:
            print_warning(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                          f"Offset at {Color.yellow}{get_xl_column(x_col)}{line}{Color.reset} "
                          f"uses a dot \'.\' as the decimal separator"
                          f"\n{x = }")
            success = False
        x = float(x.replace(',', '.'))
    x = round(x, 3)
    len_seg = get_len_seg(seg)
    if not (0 <= x):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"Offset at cell {Color.yellow}{get_xl_column(x_col)}{line}{Color.reset} "
                    f"should be positive"
                    f"\n{x = }")
        success = False
    if not (x <= len_seg):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"Offset at cell {Color.yellow}{get_xl_column(x_col)}{line}{Color.reset} "
                    f"should be lower than "
                    f"the segment {seg} length ({len_seg})"
                    f"\n{x = }")
        success = False
    return success


def verif_correct_offset_track_kp(track, kp, first_cell, line, track_col, kp_col, sh_name):
    success = True
    if first_cell is None:
        return
    if track is None and kp is None:
        return
    if track is None or kp is None:
        print_warning(f"Strange pair (track/KP) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{Color.yellow}{get_xl_column(track_col)}{line}{Color.reset} and "
                      f"{Color.yellow}{get_xl_column(kp_col)}{line}{Color.reset}"
                      f"\n{track = } / {kp = }")
        return False
    if not (isinstance(kp, float) or isinstance(kp, int)):
        if "." in kp:
            print_warning(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                          f"KP at {Color.yellow}{get_xl_column(kp_col)}{line}{Color.reset} "
                          f"uses a dot \'.\' as the decimal separator"
                          f"\n{kp = }")
            success = False
        kp = float(kp.replace(',', '.'))
    kp = round(kp, 3)
    min_kp, max_kp = get_track_limits(track)
    if not (min_kp <= kp):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"KP at cell {Color.yellow}{get_xl_column(kp_col)}{line}{Color.reset} "
                    f"should be larger than the start kp of track {track} ({min_kp})"
                    f"\n{kp = }")
        success = False
    if not (kp <= max_kp):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"KP at cell {Color.yellow}{get_xl_column(kp_col)}{line}{Color.reset} "
                    f"should be lower than the end kp of track {track} ({max_kp})"
                    f"\n{kp = }")
        success = False
    return success


def find_seg_x_cols(sh: xlrd.sheet) -> tuple[list[tuple], list[tuple]]:
    nb_cols = sh.ncols
    is_prev_seg = False
    is_prev_track = False
    seg_x_cols = list()
    track_kp_cols = list()
    for j in range(1, nb_cols+1):
        cell1 = get_xl_cell_value(sh, line=1, col=j)
        try:
            cell2 = get_xl_cell_value(sh, line=2, col=j)
            cell = cell1 if not cell2 else cell2
        except IndexError:
            cell = cell1
        cell = f"{cell}".strip().lower()
        if cell.endswith("seg"):
            is_prev_seg = True
            is_prev_track = False
        elif cell.endswith("voie") or cell.endswith("track"):
            is_prev_seg = False
            is_prev_track = True
        elif is_prev_seg and cell.endswith("x"):
            seg_x_cols.append((j-1, j))
            is_prev_seg = False
            is_prev_track = False
        elif is_prev_track and (cell.endswith("pk") or cell.endswith("kp")):
            track_kp_cols.append((j-1, j))
            is_prev_seg = False
            is_prev_track = False
        else:
            is_prev_seg = False
            is_prev_track = False
    return seg_x_cols, track_kp_cols


def check_correspondence_seg_x_track_kp(sh, seg_x_cols, track_kp_cols):
    success = True
    for (seg_col, x_col), (track_col, kp_col) in zip(seg_x_cols, track_kp_cols):
        for i in range(START_LINE, get_xl_sh_nb_rows(sh) + 1):
            first_cell = get_xl_cell_value(sh, line=i, col=1)
            if first_cell is None:
                continue
            if test_match_x_kp(sh, i, seg_col, x_col, track_col, kp_col, sh.name, first_cell) is False:
                success = False
    return success


def test_match_x_kp(sh, line, seg_col, x_col, track_col, kp_col, sh_name, first_cell):
    success = True
    tolerance = .01

    seg = get_xl_cell_value(sh, line=line, col=seg_col)
    track = get_xl_cell_value(sh, line=line, col=track_col)
    if seg is None and track is None:
        return True
    if seg is None or track is None:
        print_warning(f"Strange pair (seg/track) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{Color.yellow}{get_xl_column(seg_col)}{line}{Color.reset} and "
                      f"{Color.yellow}{get_xl_column(track_col)}{line}{Color.reset}"
                      f"\n{seg = } / {track = }")
        return False
    x = round(get_xl_float_value(sh, line=line, col=x_col), 2)
    kp = round(get_xl_float_value(sh, line=line, col=kp_col), 2)

    test_seg, test_x = from_kp_to_seg_offset(track, kp)
    test_x = round(test_x, 2)
    test_track, test_kp = from_seg_offset_to_kp(seg, x)
    test_kp = round(test_kp, 2)

    if not are_points_matching(seg, x, test_seg, test_x, tolerance=tolerance):
        success = False
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"at line {Color.yellow}{line}{Color.reset} ({Color.beige}{first_cell = }{Color.reset}), "
                    f"(SEG, OFFSET) {Color.light_green}{(seg, x)}{Color.reset} "
                    f"(at columns {get_xl_column(seg_col)} and {get_xl_column(x_col)})\n"
                    f"is different from the one recalculated {Color.light_green}{(test_seg, test_x)}{Color.reset}\n"
                    f"with the (TRACK, KP) {Color.light_blue}{(track, kp)}{Color.reset} "
                    f"(at columns {get_xl_column(track_col)} and {get_xl_column(kp_col)}).")
    if track != test_track or round(abs(kp - test_kp), 2) > tolerance:
        success = False
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"at line {Color.yellow}{line}{Color.reset} ({Color.beige}{first_cell = }{Color.reset}), "
                    f"(TRACK, KP) {Color.light_blue}{(track, kp)}{Color.reset} "
                    f"(at columns {get_xl_column(track_col)} and {get_xl_column(kp_col)})\n"
                    f"is different from the one recalculated {Color.light_blue}{(test_track, test_kp)}{Color.reset}\n"
                    f"with the (SEG, OFFSET) {Color.light_green}{(seg, x)}{Color.reset} "
                    f"(at columns {get_xl_column(seg_col)} and {get_xl_column(x_col)}).")
    return success
