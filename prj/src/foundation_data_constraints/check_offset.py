#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..dc_sys.load_database.load_xl import *
from ..dc_sys import get_seg_len, get_track_limits, from_kp_to_seg_offset, from_seg_offset_to_kp, are_points_matching


START_LINE = 3


def check_offset_correctness():
    print_title(f"Verification of the offset correctness", color=Color.mint_green)
    success = True
    wb = load_wb()
    sheet_names = get_xl_sheet_names(wb)
    for sh_name in sheet_names:
        ws = get_xl_sheet_by_name(wb, sh_name)
        if verify_sheet(ws) is False:
            success = False
    if success:
        print_log("No KO has been raised in the offset correctness checking.")


def verify_sheet(ws: xlrd.sheet):
    success = True
    seg_x_cols, track_kp_cols = find_seg_x_cols(ws)
    if check_correspondence_seg_x_track_kp(ws, seg_x_cols, track_kp_cols) is False:
        success = False
    for seg_col, x_col in seg_x_cols:
        for i in range(START_LINE, get_xl_number_of_rows(ws) + 1):
            first_cell = get_xl_cell_value(ws, row=i, column=1)
            seg = get_xl_cell_value(ws, row=i, column=seg_col)
            x = get_xl_cell_value(ws, row=i, column=x_col)
            if verif_correct_offset_seg_x(seg, x, first_cell, i, seg_col, x_col, ws.name) is False:
                success = False
    for track_col, kp_col in track_kp_cols:
        for i in range(START_LINE, get_xl_number_of_rows(ws) + 1):
            first_cell = get_xl_cell_value(ws, row=i, column=1)
            track = get_xl_cell_value(ws, row=i, column=track_col)
            kp = get_xl_cell_value(ws, row=i, column=kp_col)
            if verif_correct_offset_track_kp(track, kp, first_cell, i, track_col, kp_col, ws.name) is False:
                success = False
    return success


def verif_correct_offset_seg_x(seg, x, first_cell, row, seg_col, x_col, sh_name):
    success = True
    if first_cell is None:
        return
    if seg is None and x is None:
        return
    if seg is None or x is None:
        print_warning(f"Strange pair (segment/offset) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{Color.yellow}{get_xl_column_letter(seg_col)}{row}{Color.reset} and "
                      f"{Color.yellow}{get_xl_column_letter(x_col)}{row}{Color.reset}"
                      f"\n{seg = } / {x = }")
        return False
    if not (isinstance(x, float) or isinstance(x, int)):
        if "." in x:
            print_warning(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                          f"Offset at {Color.yellow}{get_xl_column_letter(x_col)}{row}{Color.reset} "
                          f"uses a dot \'.\' as the decimal separator"
                          f"\n{x = }")
            success = False
        x = float(x.replace(',', '.'))
    x = round(x, 3)
    len_seg = get_seg_len(seg)
    if not (0 <= x):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"Offset at cell {Color.yellow}{get_xl_column_letter(x_col)}{row}{Color.reset} "
                    f"shall be positive"
                    f"\n{x = }")
        success = False
    if not (x <= len_seg):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"Offset at cell {Color.yellow}{get_xl_column_letter(x_col)}{row}{Color.reset} "
                    f"shall be lower than "
                    f"the segment {seg} length ({len_seg})"
                    f"\n{x = }")
        success = False
    return success


def verif_correct_offset_track_kp(track, kp, first_cell, row, track_col, kp_col, sh_name):
    success = True
    if first_cell is None:
        return
    if track is None and kp is None:
        return
    if track is None or kp is None:
        print_warning(f"Strange pair (track/KP) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{Color.yellow}{get_xl_column_letter(track_col)}{row}{Color.reset} and "
                      f"{Color.yellow}{get_xl_column_letter(kp_col)}{row}{Color.reset}"
                      f"\n{track = } / {kp = }")
        return False
    if not (isinstance(kp, float) or isinstance(kp, int)):
        if "." in kp:
            print_warning(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                          f"KP at {Color.yellow}{get_xl_column_letter(kp_col)}{row}{Color.reset} "
                          f"uses a dot \'.\' as the decimal separator"
                          f"\n{kp = }")
            success = False
        kp = float(kp.replace(',', '.'))
    kp = round(kp, 3)
    min_kp, max_kp = get_track_limits(track)
    if not (min_kp <= kp):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"KP at cell {Color.yellow}{get_xl_column_letter(kp_col)}{row}{Color.reset} "
                    f"shall be larger than the start KP of track {track} ({min_kp})"
                    f"\n{kp = }")
        success = False
    if not (kp <= max_kp):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"KP at cell {Color.yellow}{get_xl_column_letter(kp_col)}{row}{Color.reset} "
                    f"shall be lower than the end KP of track {track} ({max_kp})"
                    f"\n{kp = }")
        success = False
    return success


def find_seg_x_cols(ws: xlrd.sheet) -> tuple[list[tuple], list[tuple]]:
    nb_cols = ws.ncols
    is_prev_seg = False
    is_prev_track = False
    seg_x_cols = list()
    track_kp_cols = list()
    for j in range(1, nb_cols+1):
        cell1 = get_xl_cell_value(ws, row=1, column=j)
        try:
            cell2 = get_xl_cell_value(ws, row=2, column=j)
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


def check_correspondence_seg_x_track_kp(ws, seg_x_cols, track_kp_cols):
    success = True
    for (seg_col, x_col), (track_col, kp_col) in zip(seg_x_cols, track_kp_cols):
        for i in range(START_LINE, get_xl_number_of_rows(ws) + 1):
            first_cell = get_xl_cell_value(ws, row=i, column=1)
            if first_cell is None:
                continue
            if test_match_x_kp(ws, i, seg_col, x_col, track_col, kp_col, ws.name, first_cell) is False:
                success = False
    return success


def test_match_x_kp(ws, row, seg_col, x_col, track_col, kp_col, sh_name, first_cell):
    success = True
    tolerance = .01

    seg = get_xl_cell_value(ws, row=row, column=seg_col)
    track = get_xl_cell_value(ws, row=row, column=track_col)
    if seg is None and track is None:
        return True
    if seg is None or track is None:
        print_warning(f"Strange pair (seg/track) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{Color.yellow}{get_xl_column_letter(seg_col)}{row}{Color.reset} and "
                      f"{Color.yellow}{get_xl_column_letter(track_col)}{row}{Color.reset}"
                      f"\n{seg = } / {track = }")
        return False
    x = round(get_xl_float_value(ws, row=row, column=x_col), 2)
    kp = round(get_xl_float_value(ws, row=row, column=kp_col), 2)

    test_seg, test_x = from_kp_to_seg_offset(track, kp)
    if test_seg is None or test_x is None:
        print(f"Error in sheet {Color.blue}{sh_name}{Color.reset}: at row {row}.")
        success = False
        skip_verif_seg_x = True
    else:
        test_x = round(test_x, 2)
        skip_verif_seg_x = False
    test_track, test_kp = from_seg_offset_to_kp(seg, x)
    test_kp = round(test_kp, 2)

    if not skip_verif_seg_x and not are_points_matching(seg, x, test_seg, test_x, tolerance=tolerance):
        success = False
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"at row {Color.yellow}{row}{Color.reset} ({Color.beige}{first_cell = }{Color.reset}), "
                    f"(segment, offset) {Color.light_green}{(seg, x)}{Color.reset} "
                    f"(at columns {get_xl_column_letter(seg_col)} and {get_xl_column_letter(x_col)})\n"
                    f"is different from the one recalculated {Color.light_green}{(test_seg, test_x)}{Color.reset}\n"
                    f"with the (track, KP) {Color.light_blue}{(track, kp)}{Color.reset} "
                    f"(at columns {get_xl_column_letter(track_col)} and {get_xl_column_letter(kp_col)}).")
    if track != test_track or round(abs(kp - test_kp), 2) > tolerance:
        success = False
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"at row {Color.yellow}{row}{Color.reset} ({Color.beige}{first_cell = }{Color.reset}), "
                    f"(track, KP) {Color.light_blue}{(track, kp)}{Color.reset} "
                    f"(at columns {get_xl_column_letter(track_col)} and {get_xl_column_letter(kp_col)})\n"
                    f"is different from the one recalculated {Color.light_blue}{(test_track, test_kp)}{Color.reset}\n"
                    f"with the (segment, offset) {Color.light_green}{(seg, x)}{Color.reset} "
                    f"(at columns {get_xl_column_letter(seg_col)} and {get_xl_column_letter(x_col)}).")
    return success
