#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from .file_format_utils import *


__all__ = ["create_verif_file"]


OUTPUT_DIRECTORY = "."


def create_verif_file(dc_sys_sheet_name: str, zones_kp_dict: dict):
    file_title = f"KP limits on tracks for {dc_sys_sheet_name}"
    verif_file_name = f"KP limits on tracks for {dc_sys_sheet_name}.xlsx"
    ws_name = dc_sys_sheet_name

    # Initialize Verification Workbook
    wb = create_empty_verification_file()
    # Update Header sheet
    update_header_sheet_for_verif_file(wb, title=file_title, c_d470=get_current_version())

    # Create Verification sheet
    ws, row = create_empty_verif_sheet(wb, ws_name, dc_sys_sheet_name)

    # Update Verification sheet
    color_bool = False
    track_dict = load_sheet(DCSYS.Voie)
    for object_name, sub_dict in zones_kp_dict.items():
        color_bool = not color_bool  # to alternate colors
        for track, list_min_max_kp in sub_dict.items():
            for min_kp, max_kp in list_min_max_kp:
                track_min_kp, track_max_kp = get_dc_sys_values(track_dict[track],
                                                               DCSYS.Voie.PkDebut, DCSYS.Voie.PkFin)
                if ((min_kp, max_kp) == (track_min_kp, track_max_kp)
                        or (max_kp, min_kp) == (track_min_kp, track_max_kp)):
                    comments = "Whole track is covered."
                elif min_kp == track_min_kp:
                    comments = "Limit 1 matches track Begin KP."
                elif min_kp == track_max_kp:
                    comments = "Limit 1 matches track End KP."
                elif max_kp == track_min_kp:
                    comments = "Limit 2 matches track Begin KP."
                elif max_kp == track_max_kp:
                    comments = "Limit 2 matches track End KP."
                else:
                    comments = None
                _add_line(ws, row, object_name, track, min_kp, max_kp, comments, color_bool)
                row += 1

    # Save workbook
    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(verif_file_name))
    res_file_path = os.path.realpath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"File containing the \"KP Limits for {dc_sys_sheet_name} zones\" is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    return res_file_path


def _add_line(ws: xl_ws.Worksheet, row: int, object_name: str, track: str, min_kp: float, max_kp: float,
              comments: Optional[str], color_bool: bool):
    bg_color = XlBgColor.light_blue if color_bool else XlBgColor.light_green
    # Object Name
    create_cell(ws, object_name, row=row, column=NAME_COL, borders=True, bg_color=bg_color)
    # Track
    create_cell(ws, track, row=row, column=TRACK_COL, borders=True)
    # Start KP
    create_cell(ws, min_kp, row=row, column=START_KP_COL, borders=True, nb_of_digits=2)
    # End KP
    create_cell(ws, max_kp, row=row, column=END_KP_COL, borders=True, nb_of_digits=2)
    # Automatic Comments
    create_cell(ws, comments, row=row, column=AUTOMATIC_COMMENTS_COL, borders=True,
                line_wrap=True, align_vertical=XlAlign.top)
    # Verification
    create_cell(ws, None, row=row, column=VERIFICATION_COL, borders=True, align_horizontal=XlAlign.center)
    # Comments
    create_cell(ws, None, row=row, column=COMMENTS_COL, borders=True,
                line_wrap=True, align_vertical=XlAlign.top)
