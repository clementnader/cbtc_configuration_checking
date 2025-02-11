#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.cbtc_direction_zone_utils import get_cbtc_direction_zone_related_signals
from ...dc_sys_sheet_utils.signal_utils import get_ivb_limit_of_a_signal
from ...dc_par import *
from ...ixl_utils import get_distance_between_block_and_approach_zone


__all__ = ["r_zsm_3"]


VERIF_TEMPLATE = os.path.join(TEMPLATE_DIRECTORY, "template_r_zsm_3_verification.xlsx")

OUTPUT_DIRECTORY = "."
VERIF_FILE_NAME = "R_ZSM_3 Verification.xlsx"

VERIF_SHEET = "R_ZSM_3"
START_ROW = 3
SIGNAL_NAME_COL = "A"
TYPE_COL = "B"
DIRECTION_COL = "C"
RELATED_CDZ_COL = "D"
IXL_APZ_COL = "E"
DOWNSTREAM_LIM_SEG_COL = "F"
DOWNSTREAM_LIM_X_COL = "G"
DOWNSTREAM_LIM_TRACK_COL = "H"
DOWNSTREAM_LIM_KP_COL = "I"
UPSTREAM_LIM_SEG_COL = "J"
UPSTREAM_LIM_X_COL = "K"
UPSTREAM_LIM_TRACK_COL = "L"
UPSTREAM_LIM_KP_COL = "M"
IXL_APZ_LENGTH_COL = "N"
TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL = "O"
STATUS_COL = "P"
COMMENTS_COL = "Q"

FILE_TITLE = "Verification of R_ZSM_3"


def r_zsm_3(apz_with_tc: bool = False):
    # See in the corresponding ZC-IXL ICDD, if the default IXL Approach Zone is the first physical track circuit
    # or the first IVB. By default, the first IVB is taken as it is more conservative.
    print_title(f"Verification of R_ZSM_3", color=Color.mint_green)

    verif_dict = _compute_r_zsm_3_verif(apz_with_tc)

    try:
        _create_verif_file(verif_dict)
    except KeyboardInterrupt:
        _create_verif_file(verif_dict)
        raise KeyboardInterrupt


def _compute_r_zsm_3_verif(apz_with_tc: bool = False) -> dict[str, dict[str, Any]]:
    res_dict = dict()
    sig_dict = load_sheet(DCSYS.Sig)
    zsm_sigs_dict = get_cbtc_direction_zone_related_signals()
    nb_sigs = len(zsm_sigs_dict)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (sig_name, related_zsm_list) in enumerate(zsm_sigs_dict.items()):
        print_log(f"\r{progress_bar(i, nb_sigs)} processing verification of R_ZSM_3 of {sig_name}...", end="")
        sig_type = get_dc_sys_value(sig_dict[sig_name], DCSYS.Sig.Type)
        sig_direction = get_dc_sys_value(sig_dict[sig_name], DCSYS.Sig.Sens)
        res_dict[sig_name] = {"sig_name": sig_name, "sig_type": sig_type, "sig_direction": sig_direction}
        res_dict[sig_name]["related_zsm"] = ", ".join(related_zsm_list)

        (ivb_lim_seg, ivb_lim_x), ivb_lim_str = get_ivb_limit_of_a_signal(sig_name, sig_dict[sig_name])
        ivb_lim_track, ivb_lim_kp = from_seg_offset_to_kp(ivb_lim_seg, ivb_lim_x)
        res_dict[sig_name].update({"downstream_seg": ivb_lim_seg, "downstream_x": ivb_lim_x,
                                   "downstream_track": ivb_lim_track, "downstream_kp": ivb_lim_kp})

        apz_dist, corresponding_entrance, ivb_names = (
            get_distance_between_block_and_approach_zone(sig_name, ivb_lim_seg, ivb_lim_x, apz_with_tc))
        res_dict[sig_name]["ixl_apz"] = ivb_names

        if apz_dist is None:
            res_dict[sig_name]["status"] = "KO"
            res_dict[sig_name]["comments"] = ("Tool was unable to find upstream IXL Approach Zone limit "
                                              "and to compute a path.")
            continue

        res_dict[sig_name]["ixl_apz_dist"] = apz_dist

        corresponding_entrance_track, corresponding_entrance_kp = from_seg_offset_to_kp(*corresponding_entrance)
        res_dict[sig_name].update({"upstream_seg": corresponding_entrance[0],
                                   "upstream_x": corresponding_entrance[1],
                                   "upstream_track": corresponding_entrance_track,
                                   "upstream_kp": corresponding_entrance_kp})

    print_log(f"\r{progress_bar(nb_sigs, nb_sigs, end=True)} verification of R_ZSM_3 finished.\n")

    return res_dict


def _create_verif_file(verif_dict: dict[str, dict[str, Any]]) -> None:
    wb = load_xlsx_wb(VERIF_TEMPLATE, template=True)

    update_header_sheet_for_verif_file(wb, title=FILE_TITLE, c_d470=get_current_version())

    _update_verif_sheet(wb, verif_dict)

    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.abspath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"\"Verification of R_ZSM_3\" verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    open_excel_file(res_file_path)


def _update_verif_sheet(wb: openpyxl.workbook.Workbook, verif_dict: dict[str, dict[str, Any]]) -> None:
    ws = get_xl_sheet_by_name(wb, VERIF_SHEET)

    for row, obj_val in enumerate(verif_dict.values(), start=START_ROW):
        sig_name = obj_val.get("sig_name")
        sig_type = obj_val.get("sig_type")
        sig_direction = obj_val.get("sig_direction")
        related_zsm = obj_val.get("related_zsm")
        ixl_apz = obj_val.get("ixl_apz")
        downstream_seg = obj_val.get("downstream_seg")
        downstream_x = obj_val.get("downstream_x")
        downstream_track = obj_val.get("downstream_track")
        downstream_kp = obj_val.get("downstream_kp")
        upstream_seg = obj_val.get("upstream_seg")
        upstream_x = obj_val.get("upstream_x")
        upstream_track = obj_val.get("upstream_track")
        upstream_kp = obj_val.get("upstream_kp")
        ixl_apz_dist = obj_val.get("ixl_apz_dist")
        status = obj_val.get("status")
        comments = obj_val.get("comments")

        train_to_home_signal_max_dist = get_param_value("train_to_home_signal_max_dist")

        _add_line_info(ws, row, sig_name, sig_type, sig_direction, related_zsm, ixl_apz,
                       downstream_seg, downstream_x, downstream_track, downstream_kp,
                       upstream_seg, upstream_x, upstream_track, upstream_kp,
                       ixl_apz_dist, train_to_home_signal_max_dist, comments)
        _add_status(ws, row, status)


def _add_line_info(ws: xl_ws.Worksheet, row: int, sig_name: str,
                   sig_type: str, sig_direction: str, related_zsm: str, ixl_apz: str,
                   downstream_seg: str, downstream_x: float,
                   downstream_track: str, downstream_kp: float,
                   upstream_seg: Optional[str], upstream_x: Optional[float],
                   upstream_track: Optional[str], upstream_kp: Optional[float],
                   ixl_apz_dist: Optional[float],
                   train_to_home_signal_max_dist: Optional[float], comments: Optional[str]) -> None:
    # Signal Name
    create_cell(ws, sig_name, row=row, column=SIGNAL_NAME_COL, borders=True)
    # Type
    create_cell(ws, sig_type, row=row, column=TYPE_COL, borders=True, align_horizontal=XlAlign.center)
    # Direction
    create_cell(ws, sig_direction, row=row, column=DIRECTION_COL, borders=True, align_horizontal=XlAlign.center)
    # Related CDZ
    create_cell(ws, related_zsm, row=row, column=RELATED_CDZ_COL, borders=True, line_wrap=True, align_horizontal=XlAlign.center)
    # IXL Approach Zone
    create_cell(ws, ixl_apz, row=row, column=IXL_APZ_COL, borders=True, line_wrap=True, align_horizontal=XlAlign.center)
    # Downstream Seg
    create_cell(ws, downstream_seg, row=row, column=DOWNSTREAM_LIM_SEG_COL, borders=True, align_horizontal=XlAlign.center)
    # Downstream x
    create_cell(ws, downstream_x, row=row, column=DOWNSTREAM_LIM_X_COL, borders=True, align_horizontal=XlAlign.center)
    # Downstream Track
    create_cell(ws, downstream_track, row=row, column=DOWNSTREAM_LIM_TRACK_COL, borders=True, align_horizontal=XlAlign.center)
    # Downstream KP
    create_cell(ws, downstream_kp, row=row, column=DOWNSTREAM_LIM_KP_COL, borders=True, align_horizontal=XlAlign.center)
    # Upstream Seg
    create_cell(ws, upstream_seg, row=row, column=UPSTREAM_LIM_SEG_COL, borders=True, align_horizontal=XlAlign.center)
    # Upstream x
    create_cell(ws, upstream_x, row=row, column=UPSTREAM_LIM_X_COL, borders=True, align_horizontal=XlAlign.center)
    # Upstream Track
    create_cell(ws, upstream_track, row=row, column=UPSTREAM_LIM_TRACK_COL, borders=True, align_horizontal=XlAlign.center)
    # Upstream KP
    create_cell(ws, upstream_kp, row=row, column=UPSTREAM_LIM_KP_COL, borders=True, align_horizontal=XlAlign.center)
    # IXL APZ Length
    create_cell(ws, ixl_apz_dist, row=row, column=IXL_APZ_LENGTH_COL, borders=True, align_horizontal=XlAlign.center)
    # train_to_home_signal_max_dist
    create_cell(ws, train_to_home_signal_max_dist, row=row, column=TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL,
                borders=True, align_horizontal=XlAlign.center)
    # Comments
    create_cell(ws, comments, row=row, column=COMMENTS_COL, borders=True, line_wrap=True)


def _add_status(ws: xl_ws.Worksheet, row: int, status: Optional[str]) -> None:
    if status is not None:
        create_cell(ws, status, row=row, column=STATUS_COL, borders=True, align_horizontal=XlAlign.center)
        return
    # Status
    status_formula = f'= IF({IXL_APZ_LENGTH_COL}{row} >= {TRAIN_TO_HOME_SIGNAL_MAX_DIST_COL}{row}, "OK", "KO")'
    create_cell(ws, status_formula, row=row, column=STATUS_COL, borders=True, align_horizontal=XlAlign.center)
