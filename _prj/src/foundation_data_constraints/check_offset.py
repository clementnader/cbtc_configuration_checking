#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ..utils import *
from ..dc_sys.load_database.load_xl import *
from ..dc_sys import *


__all__ = ["check_dc_sys_track_kp_definition"]


START_LINE = 3


def check_dc_sys_track_kp_definition():
    check_dc_sys_global_definition()
    print_title(f"Verification of the Correspondence between (Segment, Offset) and (Track, KP)")
    success = True
    wb = load_dc_sys_wb()
    sheet_names = get_xl_sheet_names(wb)
    for sh_name in sheet_names:
        if "Comment" in sh_name or "MergeExcel_log" in sh_name:
            continue
        ws = get_xl_sheet_by_name(wb, sh_name)
        # if check_integers(ws) is False:
        #     success = False
        if verify_sheet(ws) is False:
            success = False
    if success:
        print_log("No KO has been raised in the verification of the correspondence between "
                  "(Segment, Offset) and (Track, KP).")


def check_integers(ws: xlrd.sheet):
    success = True
    nb_cols = ws.ncols
    for j in range(1, nb_cols+1):
        for i in range(3, get_xl_number_of_rows(ws) + 1):
            cell_value = get_xl_cell_value(ws, row=i, column=j)
            if cell_value is None:
                continue
            if isinstance(cell_value, float) or isinstance(cell_value, int):
                if check_xl_cell_style_percent(ws, row=i, column=j):
                    thousandth = round(round(cell_value*100*100, 6) % 1, 6)
                    cell_value_str = f"{cell_value:.4%}"
                else:
                    thousandth = round(round(cell_value*100, 6) % 1, 6)
                    cell_value_str = f"{cell_value}"
                if thousandth > 1E-6:
                    print_log(f"In sheet {Color.blue}{ws.name}{Color.reset}: "
                              f"cell at {Color.yellow}{get_xl_column_letter(j)}{i}{Color.reset} "
                              f"has more than 2 digits after the point: \"{cell_value_str}\".\t\t{thousandth = }")
                    success = False
            elif re.search(r"^[0-9]+([,.][0-9]+)?$", cell_value) is not None:
                if "," in cell_value or "." in cell_value:
                    print_warning(f"In sheet {Color.blue}{ws.name}{Color.reset}: "
                                  f"cell at {Color.yellow}{get_xl_column_letter(j)}{i}{Color.reset} "
                                  f"is not parsed as a number in Excel, "
                                  f"check its decimal separator: \"{cell_value}\".")
                    success = False
    return success


def verify_sheet(ws: xlrd.sheet):
    success = True
    seg_x_cols, track_kp_cols = find_seg_x_cols(ws)
    if check_correspondence_seg_x_track_kp(ws, seg_x_cols, track_kp_cols) is False:
        success = False
    for seg_col, x_col, _, _ in seg_x_cols:
        for i in range(START_LINE, get_xl_number_of_rows(ws) + 1):
            first_cell = get_xl_cell_value(ws, row=i, column=1)
            seg = get_xl_cell_value(ws, row=i, column=seg_col)
            x = get_xl_cell_value(ws, row=i, column=x_col)
            if verif_correct_offset_seg_x(seg, x, first_cell, i, seg_col, x_col, ws.name) is False:
                success = False
    for track_col, kp_col, _, _ in track_kp_cols:
        for i in range(START_LINE, get_xl_number_of_rows(ws) + 1):
            first_cell = get_xl_cell_value(ws, row=i, column=1)
            track = get_xl_cell_value(ws, row=i, column=track_col)
            kp = get_xl_cell_value(ws, row=i, column=kp_col)
            if verif_correct_offset_track_kp(track, kp, first_cell, i, track_col, kp_col, ws.name) is False:
                success = False
    return success


def verif_correct_offset_seg_x(seg, x, first_cell, row, seg_col, x_col, sh_name) -> Optional[bool]:
    success = True
    if first_cell is None:
        return
    if seg is None and x is None:
        return
    if seg is None or x is None:
        print_warning(f"Strange pair (segment/offset) ({seg} / {x}) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{Color.yellow}{get_xl_column_letter(seg_col)}{row}{Color.reset} and "
                      f"{Color.yellow}{get_xl_column_letter(x_col)}{row}{Color.reset}.")
        return False
    if not (isinstance(x, float) or isinstance(x, int)):
        try:
            x = float(x.replace(",", "."))
        except ValueError:
            print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                        f"Offset ({x}) at {Color.yellow}{get_xl_column_letter(x_col)}{row}{Color.reset} "
                        f"is not a number.")
            return False
    x = round(x, 3)
    len_seg = get_seg_len(seg)
    if not (0 <= x):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"Offset ({x}) at cell {Color.yellow}{get_xl_column_letter(x_col)}{row}{Color.reset} "
                    f"shall be positive.")
        success = False
    if not (x <= len_seg):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"Offset ({x}) at cell {Color.yellow}{get_xl_column_letter(x_col)}{row}{Color.reset} "
                    f"shall be lower than the segment {seg} length ({len_seg}).")
        success = False
    return success


def verif_correct_offset_track_kp(track, kp, first_cell, row, track_col, kp_col, sh_name) -> Optional[bool]:
    success = True
    if first_cell is None:
        return
    if track is None and kp is None:
        return
    if track is None or kp is None:
        print_warning(f"Strange pair (track/KP) ({track} / {kp}) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{Color.yellow}{get_xl_column_letter(track_col)}{row}{Color.reset} and "
                      f"{Color.yellow}{get_xl_column_letter(kp_col)}{row}{Color.reset}.")
        return False
    if not (isinstance(kp, float) or isinstance(kp, int)):
        try:
            kp = float(kp.replace(",", "."))
        except ValueError:
            print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                        f"KP ({kp}) at {Color.yellow}{get_xl_column_letter(kp_col)}{row}{Color.reset} "
                        f"is not a number.")
            return False
    kp = round(kp, 4)
    min_kp, max_kp = get_track_limits(track)
    if not (min_kp <= kp):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"KP ({kp}) at cell {Color.yellow}{get_xl_column_letter(kp_col)}{row}{Color.reset} "
                    f"shall be larger than the start KP of track {track} (min = {min_kp}).")
        success = False
    if not (kp <= max_kp):
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"KP ({kp}) at cell {Color.yellow}{get_xl_column_letter(kp_col)}{row}{Color.reset} "
                    f"shall be lower than the end KP of track {track} (max = {max_kp}).")
        success = False
    return success


def find_seg_x_cols(ws: xlrd.sheet) -> tuple[list[tuple[int, int, str, str]], list[tuple[int, int, str, str]]]:
    nb_cols = ws.ncols
    is_prev_seg = False
    is_prev_track = False
    seg_x_cols = list()
    track_kp_cols = list()
    prev_cell = ""
    title = ""
    for j in range(1, nb_cols+1):
        cell1 = get_xl_cell_value(ws, row=1, column=j)
        cell2 = get_xl_cell_value(ws, row=2, column=j)
        if not cell1 and not cell2:
            break  # if there is an empty column, it means it is done and extra columns are simply comments
        if cell1 is not None:
            title = cell1
        cell = f"{title}" if not cell2 else f"{title}::{cell2}"
        cell_to_test = f"{cell}".strip().lower()
        if cell_to_test.endswith("seg"):
            is_prev_seg = True
            is_prev_track = False
        elif cell_to_test.endswith("voie") or cell_to_test.endswith("track"):
            is_prev_seg = False
            is_prev_track = True
        elif is_prev_seg and cell_to_test.endswith("x"):
            seg_x_cols.append((j-1, j, prev_cell, cell))
            is_prev_seg = False
            is_prev_track = False
        elif is_prev_track and (cell_to_test.endswith("pk") or cell_to_test.endswith("kp")):
            track_kp_cols.append((j-1, j, prev_cell, cell))
            is_prev_seg = False
            is_prev_track = False
        else:
            is_prev_seg = False
            is_prev_track = False
        prev_cell = cell
    return seg_x_cols, track_kp_cols


def check_correspondence_seg_x_track_kp(ws, seg_x_cols: list[tuple[int, int, str, str]],
                                        track_kp_cols: list[tuple[int, int, str, str]]) -> bool:
    success = True
    for ((seg_col, x_col, seg_col_name, x_col_name),
         (track_col, kp_col, track_col_name, kp_col_name)) in zip(seg_x_cols, track_kp_cols):
        for i in range(START_LINE, get_xl_number_of_rows(ws) + 1):
            first_cell = get_xl_cell_value(ws, row=i, column=1)
            if first_cell is None:
                continue
            if test_match_x_kp(ws, i, seg_col, x_col, track_col, kp_col, ws.name, first_cell,
                               seg_col_name, x_col_name, track_col_name, kp_col_name) is False:
                success = False
    return success


def test_match_x_kp(ws, row: int, seg_col: int, x_col: int, track_col: int, kp_col: int,
                    sh_name: str, first_cell: str,
                    seg_col_name: str, x_col_name: str, track_col_name: str, kp_col_name: str) -> bool:
    success = True
    percent_style = check_xl_cell_style_percent(ws, row=row, column=x_col)
    tolerance = 1E-2 if not percent_style else 1E-4

    seg = get_xl_cell_value(ws, row=row, column=seg_col)
    track = get_xl_cell_value(ws, row=row, column=track_col)
    if seg is None and track is None:
        return True
    if seg is None or track is None:
        print_warning(f"Strange pair (seg/track) for columns \"{seg_col_name}\"/\"{track_col_name}\": "
                      f"({seg} / {track}) in sheet {Color.blue}{sh_name}{Color.reset}: "
                      f"{Color.yellow}{get_xl_column_letter(seg_col)}{row}{Color.reset} and "
                      f"{Color.yellow}{get_xl_column_letter(track_col)}{row}{Color.reset}.")
        return False
    x = round(get_xl_float_value(ws, row=row, column=x_col), 4)
    kp = round(get_xl_float_value(ws, row=row, column=kp_col), 4)

    test_seg, test_x = from_kp_to_seg_offset(track, kp)
    if test_seg is None or test_x is None:
        print(f"Error in sheet {Color.blue}{sh_name}{Color.reset}: at row {row}.")
        success = False
        skip_verif_seg_x = True
    else:
        test_x = round(test_x, 4)
        skip_verif_seg_x = False
    test_track, test_kp = from_seg_offset_to_kp(seg, x)
    test_kp = round(test_kp, 4)

    if not skip_verif_seg_x and not are_points_matching(seg, x, test_seg, test_x, tolerance=tolerance):
        success = False
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"at row {Color.yellow}{row}{Color.reset} ({Color.beige}{first_cell = }{Color.reset}), "
                    f"(segment, offset) {Color.light_green}{(seg, x)}{Color.reset} "
                    f"(at columns {get_xl_column_letter(seg_col)} \"{seg_col_name}\" "
                    f"and {get_xl_column_letter(x_col)} \"{x_col_name}\")\n"
                    f"is different from the one recalculated {Color.light_green}{(test_seg, test_x)}{Color.reset} "
                    f"from the (track, KP) {Color.light_blue}{(track, kp)}{Color.reset} "
                    f"(at columns {get_xl_column_letter(track_col)} \"{track_col_name}\" "
                    f"and {get_xl_column_letter(kp_col)} \"{kp_col_name}\").")
    if track != test_track or round(abs(kp - test_kp), 4) > tolerance:
        success = False
        print_error(f"In sheet {Color.blue}{sh_name}{Color.reset}: "
                    f"at row {Color.yellow}{row}{Color.reset} ({Color.beige}{first_cell = }{Color.reset}), "
                    f"(track, KP) {Color.light_blue}{(track, kp)}{Color.reset} "
                    f"(at columns {get_xl_column_letter(track_col)} \"{track_col_name}\" "
                    f"and {get_xl_column_letter(kp_col)} \"{kp_col_name}\")\n"
                    f"is different from the one recalculated {Color.light_blue}{(test_track, test_kp)}{Color.reset} "
                    f"from the (segment, offset) {Color.light_green}{(seg, x)}{Color.reset} "
                    f"(at columns {get_xl_column_letter(seg_col)} \"{seg_col_name}\" "
                    f"and {get_xl_column_letter(x_col)} \"{x_col_name}\").")
    return success
