#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ....utils import *
from ....dc_sys import *
from ....dc_par import *
from .sig_apz_verif import *
from .file_format_utils import *


__all__ = ["check_cbtc_sig_apz"]


OUTPUT_DIRECTORY = "."
VERIF_FILE_NAME = "CBTC Signal Approach Zones Verification.xlsx"
FILE_TITLE = "Verification of CBTC Signal Approach Zones"


def check_cbtc_sig_apz():
    print_title(f"Verification of CBTC Signal Approach Zones", color=Color.mint_green)

    verif_dict = compute_cbtc_sig_apz()
    res_file_path = _create_verif_file(verif_dict)
    open_excel_file(res_file_path)


def _create_verif_file(verif_dict: dict[str, dict[str, Any]]) -> str:
    wb = create_empty_verification_file()
    # Update Header sheet
    update_header_sheet_for_verif_file(wb, title=FILE_TITLE, c_d470=get_current_version())
    # Create Verification sheet
    ws, row = create_empty_verif_sheet(wb)

    # Update Verification sheet
    _update_verif_sheet(ws, row, verif_dict)

    # Save workbook
    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.realpath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"\"Verification of CBTC Approach Zone\" verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    return res_file_path


def _update_verif_sheet(ws: xl_ws.Worksheet, row: int, verif_dict: dict[str, dict[str, Any]]) -> None:
    train_to_home_signal_max_dist = get_param_value("train_to_home_signal_max_dist")

    for obj_val in verif_dict.values():
        sig_name = obj_val.get("sig_name")
        sig_type = obj_val.get("sig_type")
        sig_direction = obj_val.get("sig_direction")
        sig_with_imc = obj_val.get("sig_with_imc")
        downstream_seg = obj_val.get("downstream_seg")
        downstream_x = obj_val.get("downstream_x")
        downstream_track = obj_val.get("downstream_track")
        downstream_kp = obj_val.get("downstream_kp")
        sig_apz_limit_seg_list = obj_val.get("sig_apz_limit_seg_list", list())
        sig_apz_limit_x_list = obj_val.get("sig_apz_limit_x_list", list())
        sig_apz_limit_track_list = obj_val.get("sig_apz_limit_track_list", list())
        sig_apz_limit_kp_list = obj_val.get("sig_apz_limit_kp_list", list())
        dist_list = obj_val.get("dist_list", list())
        status = obj_val.get("status")
        comments = obj_val.get("comments")

        # Multiple rows can be written at once for multiple Entry Points
        row = _add_line_info(ws, row, sig_name, sig_type, sig_direction, sig_with_imc,
                             downstream_seg, downstream_x, downstream_track, downstream_kp,
                             sig_apz_limit_seg_list, sig_apz_limit_x_list,
                             sig_apz_limit_track_list, sig_apz_limit_kp_list,
                             dist_list, train_to_home_signal_max_dist, status, comments)
        row += 1


def _add_line_info(ws: xl_ws.Worksheet, row: int,
                   sig_name: str, sig_type: str, sig_direction: str, sig_with_imc: str,
                   downstream_seg: str, downstream_x: float, downstream_track: str, downstream_kp: float,
                   sig_apz_limit_seg_list: list[str], sig_apz_limit_x_list: list[float],
                   sig_apz_limit_track_list: list[str], sig_apz_limit_kp_list: list[float],
                   dist_list: Optional[list[float]], train_to_home_signal_max_dist: float,
                   status: Optional[str], comments: Optional[str]) -> int:

    end_row = row + len(sig_apz_limit_seg_list) - 1 if sig_apz_limit_seg_list else row

    # Signal Name
    create_merged_cell(ws, sig_name, start_row=row, end_row=end_row,
                       start_column=SIGNAL_NAME_COL, end_column=SIGNAL_NAME_COL,
                       borders=True, line_wrap=False)
    # Type
    create_merged_cell(ws, sig_type, start_row=row, end_row=end_row,
                       start_column=TYPE_COL, end_column=TYPE_COL,
                       borders=True, line_wrap=False, align_horizontal=XlAlign.center)
    # Direction
    create_merged_cell(ws, sig_direction, start_row=row, end_row=end_row,
                       start_column=DIRECTION_COL, end_column=DIRECTION_COL,
                       borders=True, line_wrap=False, align_horizontal=XlAlign.center)
    # With IMC
    create_merged_cell(ws, sig_with_imc, start_row=row, end_row=end_row,
                       start_column=WITH_IMC_COL, end_column=WITH_IMC_COL,
                       borders=True, line_wrap=False, align_horizontal=XlAlign.center)
    # Downstream Seg
    create_merged_cell(ws, downstream_seg, start_row=row, end_row=end_row,
                       start_column=DOWNSTREAM_LIM_SEG_COL, end_column=DOWNSTREAM_LIM_SEG_COL,
                       borders=True, line_wrap=False)
    # Downstream x
    create_merged_cell(ws, downstream_x, start_row=row, end_row=end_row,
                       start_column=DOWNSTREAM_LIM_X_COL, end_column=DOWNSTREAM_LIM_X_COL,
                       borders=True, line_wrap=False, nb_of_digits=2)
    # Downstream Track
    create_merged_cell(ws, downstream_track, start_row=row, end_row=end_row,
                       start_column=DOWNSTREAM_LIM_TRACK_COL, end_column=DOWNSTREAM_LIM_TRACK_COL,
                       borders=True, line_wrap=False)
    # Downstream KP
    create_merged_cell(ws, downstream_kp, start_row=row, end_row=end_row,
                       start_column=DOWNSTREAM_LIM_KP_COL, end_column=DOWNSTREAM_LIM_KP_COL,
                       borders=True, line_wrap=False, nb_of_digits=2)

    if not sig_apz_limit_seg_list:
        # Upstream Seg
        create_cell(ws, None, row=row, column=UPSTREAM_LIM_SEG_COL, borders=True)
        # Upstream x
        create_cell(ws, None, row=row, column=UPSTREAM_LIM_X_COL, borders=True, nb_of_digits=2)
        # Upstream Track
        create_cell(ws, None, row=row, column=UPSTREAM_LIM_TRACK_COL, borders=True)
        # Upstream KP
        create_cell(ws, None, row=row, column=UPSTREAM_LIM_KP_COL, borders=True, nb_of_digits=2)
        # CBTC APZ Length
        create_cell(ws, None, row=row, column=CBTC_APZ_LENGTH_COL, borders=True,
                    align_horizontal=XlAlign.center, nb_of_digits=2)
        # Minimum Distance
        create_cell(ws, None, row=row, column=TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL, borders=True,
                    align_horizontal=XlAlign.center, nb_of_digits=2)
        # Status
        _add_status(ws, row, status)
        # Comments
        _add_comments(ws, row, comments)
        return row

    for row, (upstream_seg, upstream_x, upstream_track, upstream_kp, cbtc_apz_dist) in enumerate(
            zip(sig_apz_limit_seg_list, sig_apz_limit_x_list, sig_apz_limit_track_list, sig_apz_limit_kp_list,
                dist_list), start=row):
        # Upstream Seg
        create_cell(ws, upstream_seg, row=row, column=UPSTREAM_LIM_SEG_COL, borders=True)
        # Upstream x
        create_cell(ws, upstream_x, row=row, column=UPSTREAM_LIM_X_COL, borders=True, nb_of_digits=2)
        # Upstream Track
        create_cell(ws, upstream_track, row=row, column=UPSTREAM_LIM_TRACK_COL, borders=True)
        # Upstream KP
        create_cell(ws, upstream_kp, row=row, column=UPSTREAM_LIM_KP_COL, borders=True, nb_of_digits=2)
        # CBTC APZ Length
        create_cell(ws, cbtc_apz_dist, row=row, column=CBTC_APZ_LENGTH_COL, borders=True,
                    align_horizontal=XlAlign.center, nb_of_digits=2)
        # Minimum Distance
        create_cell(ws, train_to_home_signal_max_dist, row=row, column=TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL, borders=True,
                    align_horizontal=XlAlign.center, nb_of_digits=2)
        # Status
        _add_status(ws, row, status)
        # Comments
        _add_comments(ws, row, comments)

    return row


def _add_status(ws: xl_ws.Worksheet, row: int, status: Optional[str]) -> None:
    if status is not None:
        create_cell(ws, status, row=row, column=STATUS_COL, borders=True, align_horizontal=XlAlign.center)
        return
    # Status
    status_formula = f'= IF({CBTC_APZ_LENGTH_COL}{row} >= {TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL}{row}, "OK", "KO")'
    create_cell(ws, status_formula, row=row, column=STATUS_COL, borders=True, align_horizontal=XlAlign.center)


def _add_comments(ws: xl_ws.Worksheet, row: int, comments: Optional[str]) -> None:
    # Comments
    if comments is not None:
        create_cell(ws, comments, row=row, column=COMMENTS_COL, borders=True, line_wrap=True)
        return
    create_cell(ws, comments, row=row, column=COMMENTS_COL, borders=True, line_wrap=True)
