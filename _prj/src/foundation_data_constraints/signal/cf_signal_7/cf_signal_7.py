#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ....dc_sys_draw_path.dc_sys_path_and_distances import get_next_objects_from_a_point
from ....fouling_points_utils import *
from .file_format_utils import *


__all__ = ["cf_signal_7"]


OUTPUT_DIRECTORY = "."
VERIF_FILE_NAME = "CF_SIGNAL_7 Verification.xlsx"
FILE_TITLE = "Verification of CF_SIGNAL_7"


def cf_signal_7():
    print_title(f"Verification of CF_SIGNAL_7", color=Color.mint_green)

    verif_dict = _compute_cf_signal_7_verif()
    _create_verif_file(verif_dict)


def _compute_cf_signal_7_verif() -> dict[str, dict[str, Any]]:
    res_dict = dict()
    sig_list = get_objects_list(DCSYS.Sig)
    fp_dict = load_fouling_point_info()
    if not fp_dict:
        print_warning("No Fouling Point information, the results will be only given for the switch as danger point.")
    nb_sigs = len(sig_list)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, sig_name in enumerate(sig_list):
        print_log_progress_bar(i, nb_sigs, f"finding the next switch point from {sig_name}")

        sig_seg, sig_x, sig_direction = get_dc_sys_values(sig_name, DCSYS.Sig.Seg, DCSYS.Sig.X, DCSYS.Sig.Sens)
        sig_track, sig_kp = from_seg_offset_to_track_kp(sig_seg, sig_x)
        sig_type = get_dc_sys_value(sig_name, DCSYS.Sig.Type)
        vsp_dist = get_dc_sys_value(sig_name, DCSYS.Sig.DistPap)
        res_dict[sig_name] = {"sig_name": sig_name, "sig_seg": sig_seg, "sig_x": sig_x, "sig_direction": sig_direction,
                              "sig_track": sig_track, "sig_kp": sig_kp, "sig_type": sig_type, "vsp_dist": vsp_dist}

        next_switch_list = get_next_objects_from_a_point(sig_seg, sig_x, sig_direction, DCSYS.Aig)
        if not next_switch_list:
            res_dict[sig_name]["status"] = "NA"
            res_dict[sig_name]["comments"] = "No switch after the signal."
            continue
        if len(next_switch_list) > 1:
            print_error(f"Multiple switches are found after signal {sig_name} in direction {sig_direction}:")
            print(next_switch_list)

        next_switch, polarity, dist_to_switch = next_switch_list[0]
        res_dict[sig_name].update({"next_switch": next_switch, "dist_to_switch": dist_to_switch})

        diverging_switch = ((is_switch_point_upstream_heels(next_switch) == polarity) ==
                            (sig_direction == Direction.CROISSANT))
        # We take into account if there is a depolarization point in-between the signal and the switch,
        # the diverging is according to the signal direction.
        danger_point = "Switch Point" if diverging_switch else "Fouling Point"
        res_dict[sig_name]["danger_point"] = danger_point

        if danger_point == "Switch Point":
            if dist_to_switch < vsp_dist:
                res_dict[sig_name]["comments"] = "The distance to the VSP is larger than the distance to the switch."

        else:  # danger point is fouling point
            if fp_dict:
                fp_dist = fp_dict.get(next_switch)
            else:
                fp_dist = None
            if fp_dist is None:
                res_dict[sig_name]["status"] = "KO"
                res_dict[sig_name]["comments"] = "No fouling point information for this switch."
                if dist_to_switch < vsp_dist:
                    res_dict[sig_name]["comments"] += ("The distance to the VSP is larger than the distance "
                                                       "to the switch (knowing that we don't even consider the FP "
                                                       "that the signal is supposed to protect).")
                continue
            res_dict[sig_name]["fp_dist"] = fp_dist
            if dist_to_switch - fp_dist < vsp_dist:
                res_dict[sig_name]["comments"] = ("The distance to the VSP is larger than the distance to the "
                                                  "fouling point.")

    print_log_progress_bar(nb_sigs, nb_sigs, "computation of distance from signals to switch and "
                                             "fouling point finished", end=True)

    return res_dict


def _create_verif_file(verif_dict: dict[str, dict[str, Any]]) -> None:
    # Initialize Verification Workbook
    wb = create_empty_verification_file()
    update_header_sheet_for_verif_file(wb, title=FILE_TITLE, c_d470=get_current_version(),
                                       fouling_point_file=get_fouling_point_file())
    # Create Constraint sheet
    create_constraint_sheet(wb)
    # Create Verification sheet
    ws, row = create_empty_verif_sheet(wb)

    # Update Verification sheet
    _update_verif_sheet(ws, row, verif_dict)

    # Save workbook
    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.realpath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"\"Verification of CF_SIGNAL_7\" verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    open_excel_file(res_file_path)


def _update_verif_sheet(ws: xl_ws.Worksheet, start_row: int, verif_dict: dict[str, dict[str, Any]]) -> None:

    for row, obj_val in enumerate(verif_dict.values(), start=start_row):
        sig_name = obj_val.get("sig_name")
        sig_seg = obj_val.get("sig_seg")
        sig_x = obj_val.get("sig_x")
        sig_direction = obj_val.get("sig_direction")
        sig_track = obj_val.get("sig_track")
        sig_kp = obj_val.get("sig_kp")
        sig_type = obj_val.get("sig_type")
        vsp_dist = obj_val.get("vsp_dist")
        next_switch = obj_val.get("next_switch")
        danger_point = obj_val.get("danger_point")
        dist_to_switch = obj_val.get("dist_to_switch")
        fp_dist = obj_val.get("fp_dist")
        status = obj_val.get("status")
        comments = obj_val.get("comments")

        _add_line_info(ws, row, sig_name, sig_seg, sig_x, sig_direction, sig_track, sig_kp, sig_type, vsp_dist,
                       next_switch, danger_point, dist_to_switch, fp_dist)
        _add_dist_to_fp(ws, row, fp_dist)
        _add_status(ws, row, status)
        _add_comments(ws, row, comments)


def _add_line_info(ws: xl_ws.Worksheet, row: int, sig_name: str,
                   sig_seg: Optional[str], sig_x: Optional[float], sig_direction: str,
                   sig_track: Optional[str], sig_kp: Optional[float],
                   sig_type: str, vsp_dist: Optional[float],
                   next_switch: Optional[str], danger_point: Optional[str], dist_to_switch: Optional[float],
                   fp_dist: Optional[float]) -> None:
    # Signal Name
    create_cell(ws, sig_name, row=row, column=SIGNAL_NAME_COL, borders=True)
    # Signal Seg
    create_cell(ws, sig_seg, row=row, column=SIGNAL_SEG_COL, borders=True)
    # Signal x
    create_cell(ws, sig_x, row=row, column=SIGNAL_X_COL, borders=True, nb_of_digits=2)
    # Signal Direction
    create_cell(ws, sig_direction, row=row, column=SIGNAL_DIRECTION_COL, borders=True, align_horizontal=XlAlign.center)
    # Signal Track
    create_cell(ws, sig_track, row=row, column=SIGNAL_TRACK_COL, borders=True)
    # Signal KP
    create_cell(ws, sig_kp, row=row, column=SIGNAL_KP_COL, borders=True, nb_of_digits=2)
    # Type
    create_cell(ws, sig_type, row=row, column=TYPE_COL, borders=True, align_horizontal=XlAlign.center)
    # VSP Distance
    create_cell(ws, vsp_dist, row=row, column=VSP_DIST_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)
    # Newt Switch
    create_cell(ws, next_switch, row=row, column=NEXT_SWITCH_COL, borders=True, align_horizontal=XlAlign.center)
    # Danger Point
    create_cell(ws, danger_point, row=row, column=DANGER_POINT_COL, borders=True, align_horizontal=XlAlign.center)
    # Distance to switch
    create_cell(ws, dist_to_switch, row=row, column=DIST_TO_SWITCH_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)
    # Fouling Point distance
    create_cell(ws, fp_dist, row=row, column=FP_DIST_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)


def _add_dist_to_fp(ws: xl_ws.Worksheet, row: int, fp_dist: Optional[float]) -> None:
    if fp_dist is None:
        create_cell(ws, None, row=row, column=DIST_TO_FP_COL, borders=True,
                    align_horizontal=XlAlign.center)
        return
    # Distance to fouling point
    formula = f'= {DIST_TO_SWITCH_COL}{row} - {FP_DIST_COL}{row}'
    create_cell(ws, formula, row=row, column=DIST_TO_FP_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)


def _add_status(ws: xl_ws.Worksheet, row: int, status: Optional[str]) -> None:
    if status is not None:
        create_cell(ws, status, row=row, column=STATUS_COL, borders=True, align_horizontal=XlAlign.center)
        return
    # Status
    status_formula = (f'= IF({VSP_DIST_COL}{row} <= IF({DANGER_POINT_COL}{row} = "Switch Point", '
                      f'{DIST_TO_SWITCH_COL}{row}, {DIST_TO_FP_COL}{row}), "OK", "KO")')
    create_cell(ws, status_formula, row=row, column=STATUS_COL, borders=True,
                align_horizontal=XlAlign.center)


def _add_comments(ws: xl_ws.Worksheet, row: int, comments: Optional[str]) -> None:
    # Comments
    create_cell(ws, comments, row=row, column=COMMENTS_COL, borders=True, line_wrap=True)
