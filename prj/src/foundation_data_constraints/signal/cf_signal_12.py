#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.signal_utils import get_ivb_limit_of_a_signal
from ...dc_par import *
from ...ixl_utils import get_distance_between_block_and_approach_zone
from ..ixl_overlap.overlap_platform_related import is_sig_downstream_a_plt


__all__ = ["cf_signal_12"]


VERIF_TEMPLATE_RELATIVE_PATH = os.path.join("..", "..", "templates", "template_cf_signal_12_verification.xlsx")
VERIF_TEMPLATE = get_full_path(__file__, VERIF_TEMPLATE_RELATIVE_PATH)

OUTPUT_DIRECTORY = DESKTOP_DIRECTORY
VERIF_FILE_NAME = "CF_SIGNAL_12 Verification.xlsx"

PARAMETERS_SHEET = "Parameters"
PARAM_NAME_COL = "A"
PARAM_VALUE_COL = "B"

VERIF_SHEET = "CF_SIGNAL_12"
START_ROW = 3
SIGNAL_NAME_COL = "A"
TYPE_COL = "B"
DIRECTION_COL = "C"
PLATFORM_RELATED_COL = "D"
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
VALUE_TO_REMOVE_COL = "O"
MIN_DIST_COL = "P"
DLT_DIST_COL = "Q"
STATUS_COL = "R"
COMMENTS_COL = "S"


def cf_signal_12(apz_with_tc: bool = False):
    # See in the corresponding ZC-IXL ICDD, if the default IXL Approach Zone is the first physical track circuit
    # or the first IVB. By default, the first IVB is taken as it is more conservative.
    print_title(f"Verification of CF_SIGNAL_12", color=Color.mint_green)

    verif_dict = _compute_cf_signal_12_verif(apz_with_tc)

    try:
        _create_verif_file(verif_dict)
    except KeyboardInterrupt:
        _create_verif_file(verif_dict)
        raise KeyboardInterrupt


def _compute_cf_signal_12_verif(apz_with_tc: bool) -> dict[str, dict[str, Any]]:
    res_dict = dict()
    sig_dict = load_sheet(DCSYS.Sig)
    nb_sigs = len(sig_dict.keys())
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (sig_name, sig) in enumerate(sig_dict.items()):
        print_log(f"\r{progress_bar(i, nb_sigs)} processing computation of IXL Approach Zone Length "
                  f"of {sig_name}...", end="")
        sig_type = get_dc_sys_value(sig, DCSYS.Sig.Type)
        sig_direction = get_dc_sys_value(sig, DCSYS.Sig.Sens)
        res_dict[sig_name] = {"sig_name": sig_name, "sig_type": sig_type, "sig_direction": sig_direction}
        if sig_type in [SignalType.HEURTOIR, SignalType.PERMANENT_ARRET]:
            res_dict[sig_name]["status"] = "NA"
            continue

        is_plt_rel, plt, plt_limit = is_sig_downstream_a_plt(sig_name)
        res_dict[sig_name]["platform_related"] = None if not is_plt_rel else "\n".join([plt, plt_limit])

        dlt_distance = get_dc_sys_value(sig, DCSYS.Sig.DelayedLtDistance)
        res_dict[sig_name]["dlt_distance"] = dlt_distance
        if dlt_distance == 0:
            res_dict[sig_name]["status"] = "OK"
            res_dict[sig_name]["comments"] = "0 is a safe value."
            continue

        (ivb_lim_seg, ivb_lim_x), ivb_lim_str = get_ivb_limit_of_a_signal(sig_name, sig)
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

    print_log(f"\r{progress_bar(nb_sigs, nb_sigs, end=True)} computation of IXL Approach Zone Length finished.\n")

    return res_dict


def _create_verif_file(verif_dict: dict[str, dict[str, Any]]) -> None:
    wb = load_xlsx_wb(VERIF_TEMPLATE)

    update_header_sheet_for_verif_file(wb)
    inhibit_simple_overshoot_recovery = _fill_parameters_sheet(wb)

    _update_verif_sheet(wb, verif_dict, inhibit_simple_overshoot_recovery)

    verif_file_name = f" - {get_c_d470_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.join(OUTPUT_DIRECTORY, verif_file_name)
    save_xl_file(wb, res_file_path)
    print_success(f"\"Verification of CF_SIGNAL_12\" verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    open_excel_file(res_file_path)


def _fill_parameters_sheet(wb: openpyxl.workbook.Workbook) -> bool:
    params_dict = {
        "at_deshunt_max_dist": get_param_value("at_deshunt_max_dist"),
        "block_laying_uncertainty": get_param_value("block_laying_uncertainty"),
        "mtc_rollback_dist": get_param_value("mtc_rollback_dist"),
        "at_rollback_dist": get_param_value("at_rollback_dist"),
        "overshoot_recovery_dist": get_param_value("overshoot_recovery_dist"),
        "overshoot_recovery_stopping_max_dist": get_param_value("overshoot_recovery_stopping_max_dist"),
        "inhibit_simple_overshoot_recovery": get_param_value("inhibit_simple_overshoot_recovery"),
    }

    ws = get_xl_sheet_by_name(wb, PARAMETERS_SHEET)
    for row in range(START_ROW, get_xl_number_of_rows(ws) + 1):
        param_name = get_xl_cell_value(ws, row=row, column=PARAM_NAME_COL).lower().strip()
        create_cell(ws, params_dict.get(param_name), row=row, column=PARAM_VALUE_COL, borders=True)

    return params_dict["inhibit_simple_overshoot_recovery"]


def _update_verif_sheet(wb: openpyxl.workbook.Workbook, verif_dict: dict[str, dict[str, Any]],
                        inhibit_simple_overshoot_recovery: bool) -> None:
    ws = get_xl_sheet_by_name(wb, VERIF_SHEET)

    for row, obj_val in enumerate(verif_dict.values(), start=START_ROW):
        sig_name = obj_val.get("sig_name")
        sig_type = obj_val.get("sig_type")
        sig_direction = obj_val.get("sig_direction")
        platform_related = obj_val.get("platform_related")
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
        dlt_distance = obj_val.get("dlt_distance")
        status = obj_val.get("status")
        comments = obj_val.get("comments")

        _add_line_info(ws, row, sig_name, sig_type, sig_direction, platform_related, ixl_apz,
                       downstream_seg, downstream_x, downstream_track, downstream_kp,
                       upstream_seg, upstream_x, upstream_track, upstream_kp,
                       ixl_apz_dist, dlt_distance)
        _add_value_to_remove(ws, row, status, inhibit_simple_overshoot_recovery, platform_related)
        _add_status(ws, row, status)
        _add_comments(ws, row, comments, inhibit_simple_overshoot_recovery, platform_related)


def _add_line_info(ws: xl_ws.Worksheet, row: int, sig_name: str,
                   sig_type: str, sig_direction: str, platform_related: Optional[str], ixl_apz: Optional[str],
                   downstream_seg: Optional[str], downstream_x: Optional[float],
                   downstream_track: Optional[str], downstream_kp: Optional[float],
                   upstream_seg: Optional[str], upstream_x: Optional[float],
                   upstream_track: Optional[str], upstream_kp: Optional[float],
                   ixl_apz_dist: Optional[float], dlt_distance: Optional[float]) -> None:
    # Signal Name
    create_cell(ws, sig_name, row=row, column=SIGNAL_NAME_COL, borders=True)
    # Type
    create_cell(ws, sig_type, row=row, column=TYPE_COL, borders=True, center_horizontal=True)
    # Direction
    create_cell(ws, sig_direction, row=row, column=DIRECTION_COL, borders=True, center_horizontal=True)
    # IXL Approach Zone
    create_cell(ws, ixl_apz, row=row, column=IXL_APZ_COL, borders=True, line_wrap=True, center_horizontal=True)
    # Platform Related
    create_cell(ws, platform_related, row=row, column=PLATFORM_RELATED_COL,
                borders=True, line_wrap=True, center_horizontal=True)
    if platform_related is not None:
        set_bg_color(ws, XlBgColor.light_pink, row=row, column=PLATFORM_RELATED_COL)
    # Downstream Seg
    create_cell(ws, downstream_seg, row=row, column=DOWNSTREAM_LIM_SEG_COL, borders=True, center_horizontal=True)
    # Downstream x
    create_cell(ws, downstream_x, row=row, column=DOWNSTREAM_LIM_X_COL, borders=True, center_horizontal=True)
    # Downstream Track
    create_cell(ws, downstream_track, row=row, column=DOWNSTREAM_LIM_TRACK_COL, borders=True, center_horizontal=True)
    # Downstream KP
    create_cell(ws, downstream_kp, row=row, column=DOWNSTREAM_LIM_KP_COL, borders=True, center_horizontal=True)
    # Upstream Seg
    create_cell(ws, upstream_seg, row=row, column=UPSTREAM_LIM_SEG_COL, borders=True, center_horizontal=True)
    # Upstream x
    create_cell(ws, upstream_x, row=row, column=UPSTREAM_LIM_X_COL, borders=True, center_horizontal=True)
    # Upstream Track
    create_cell(ws, upstream_track, row=row, column=UPSTREAM_LIM_TRACK_COL, borders=True, center_horizontal=True)
    # Upstream KP
    create_cell(ws, upstream_kp, row=row, column=UPSTREAM_LIM_KP_COL, borders=True, center_horizontal=True)
    # IXL APZ Length
    create_cell(ws, ixl_apz_dist, row=row, column=IXL_APZ_LENGTH_COL, borders=True, center_horizontal=True)
    # DLT Distance
    create_cell(ws, dlt_distance, row=row, column=DLT_DIST_COL, borders=True, center_horizontal=True)


def _add_value_to_remove(ws: xl_ws.Worksheet, row: int, status: Optional[str],
                         inhibit_simple_overshoot_recovery: bool, platform_related: Optional[str]) -> None:
    if status is not None:
        create_cell(ws, None, row=row, column=VALUE_TO_REMOVE_COL, borders=True, center_horizontal=True)
        return
    # Value to remove
    formula = (f'= IF(OR(inhibit_simple_overshoot_recovery = TRUE, {PLATFORM_RELATED_COL}{row} = ""), '
               f'(at_deshunt_max_dist + block_laying_uncertainty + MAX(mtc_rollback_dist, at_rollback_dist)),'
               f'(at_deshunt_max_dist + block_laying_uncertainty + MAX(mtc_rollback_dist, at_rollback_dist,'
               f'overshoot_recovery_dist + overshoot_recovery_stopping_max_dist)))')
    create_cell(ws, formula, row=row, column=VALUE_TO_REMOVE_COL, borders=True, center_horizontal=True)
    if not inhibit_simple_overshoot_recovery and platform_related is not None:
        set_bg_color(ws, XlBgColor.light_pink, row=row, column=VALUE_TO_REMOVE_COL)


def _add_status(ws: xl_ws.Worksheet, row: int, status: Optional[str]) -> None:
    if status is not None:
        create_cell(ws, None, row=row, column=MIN_DIST_COL, borders=True, center_horizontal=True)
        create_cell(ws, status, row=row, column=STATUS_COL, borders=True, center_horizontal=True)
        return
    # Minimum Distance
    min_dist_formula = f'= {IXL_APZ_LENGTH_COL}{row} - {VALUE_TO_REMOVE_COL}{row}'
    create_cell(ws, min_dist_formula, row=row, column=MIN_DIST_COL, borders=True, center_horizontal=True)
    # Status
    status_formula = f'= IF({DLT_DIST_COL}{row} <= {MIN_DIST_COL}{row}, "OK", "KO")'
    create_cell(ws, status_formula, row=row, column=STATUS_COL, borders=True, center_horizontal=True)


def _add_comments(ws: xl_ws.Worksheet, row: int, comments: Optional[str],
                  inhibit_simple_overshoot_recovery: bool, platform_related: Optional[str]) -> None:
    # Comments
    if comments is not None:
        create_cell(ws, comments, row=row, column=COMMENTS_COL, borders=True, line_wrap=True)
        return
    if not inhibit_simple_overshoot_recovery and platform_related is not None:
        comments = ("Overshoot Recovery Parameters are considered only for platform-related signals, "
                    "where overshoot recovery can be used.")
    create_cell(ws, comments, row=row, column=COMMENTS_COL, borders=True, line_wrap=True)
