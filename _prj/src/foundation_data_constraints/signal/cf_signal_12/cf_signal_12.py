#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ....dc_sys_sheet_utils.signal_utils import get_ivb_limit_of_a_signal
from ....ixl_utils import get_distance_between_block_and_approach_zone, ixl_apz_definition_file, load_ixl_apz_file
from ...ixl_overlap.overlap_platform_related import is_ivb_plt_related
from .file_format_utils import *


__all__ = ["cf_signal_12"]


OUTPUT_DIRECTORY = "."
VERIF_FILE_NAME = "CF_SIGNAL_12 Verification.xlsx"
FILE_TITLE = "Verification of CF_SIGNAL_12"


def cf_signal_12(apz_with_tc: bool = False):
    # See in the corresponding ZC-IXL ICDD, if the default IXL Approach Zone is the first physical track circuit
    # or the first IVB. By default, the first IVB is taken as it is more conservative.
    print_title(f"Verification of CF_SIGNAL_12", color=Color.mint_green)

    load_ixl_apz_file()
    verif_dict = _compute_cf_signal_12_verif(apz_with_tc)
    _create_verif_file(verif_dict)


def _compute_cf_signal_12_verif(apz_with_tc: bool) -> dict[str, dict[str, Any]]:
    res_dict = dict()
    sig_dict = load_sheet(DCSYS.Sig)
    nb_sigs = len(sig_dict.keys())
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (sig_name, sig) in enumerate(sig_dict.items()):
        print_log_progress_bar(i, nb_sigs, f"computing the IXL Approach Zone length of {sig_name}")
        sig_type = get_dc_sys_value(sig, DCSYS.Sig.Type)
        sig_direction = get_dc_sys_value(sig, DCSYS.Sig.Sens)
        res_dict[sig_name] = {"sig_name": sig_name, "sig_type": sig_type, "sig_direction": sig_direction}
        if sig_type in [SignalType.HEURTOIR, SignalType.PERMANENT_ARRET]:
            res_dict[sig_name]["status"] = "NA"
            res_dict[sig_name]["comments"] = "Not a Home Signal."
            continue

        dlt_distance = get_dc_sys_value(sig, DCSYS.Sig.DelayedLtDistance)
        res_dict[sig_name]["dlt_distance"] = dlt_distance
        if dlt_distance == 0:
            res_dict[sig_name]["status"] = "OK"
            res_dict[sig_name]["comments"] = "0 is a safe value."
            continue

        (ivb_lim_seg, ivb_lim_x), ivb_lim_str = get_ivb_limit_of_a_signal(sig_name, sig)
        ivb_lim_track, ivb_lim_kp = from_seg_offset_to_track_kp(ivb_lim_seg, ivb_lim_x)
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

        last_ivb = _get_last_ivb(corresponding_entrance, ivb_names)
        if last_ivb is None:
            is_last_ivb_plt_rel = None
            plt_name = None
        else:
            is_last_ivb_plt_rel, plt_name = is_ivb_plt_related(last_ivb)
        res_dict[sig_name]["last_ivb_platform_related"] = (None if not is_last_ivb_plt_rel
                                                           else f"{last_ivb}\n{plt_name}")

        res_dict[sig_name]["ixl_apz_dist"] = apz_dist

        corresponding_entrance_track, corresponding_entrance_kp = from_seg_offset_to_track_kp(*corresponding_entrance)
        res_dict[sig_name].update({"upstream_seg": corresponding_entrance[0],
                                   "upstream_x": corresponding_entrance[1],
                                   "upstream_track": corresponding_entrance_track,
                                   "upstream_kp": corresponding_entrance_kp})

    print_log_progress_bar(nb_sigs, nb_sigs, "computation of IXL Approach Zone length finished", end=True)

    return res_dict


def _get_last_ivb(corresponding_entrance: tuple[str, float], ivb_names: str) -> Optional[str]:
    """ Get last IVB of the IXL APZ. """
    list_ivb = ivb_names.split(", ")
    for ivb_name in list_ivb:
        for ivb_seg, ivb_x in get_dc_sys_zip_values(ivb_name, DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X):
            if are_points_matching(*corresponding_entrance, ivb_seg, ivb_x):
                return ivb_name
    return None


def _create_verif_file(verif_dict: dict[str, dict[str, Any]]) -> None:
    # Initialize Verification Workbook
    wb = create_empty_verification_file()
    # Update Header sheet
    if ixl_apz_definition_file() is not None:
        ixl_apz_file = f"{os.path.split(ixl_apz_definition_file())[-1]}"
    else:
        ixl_apz_file = None
    update_header_sheet_for_verif_file(wb, title=FILE_TITLE, c_d470=get_current_version(),
                                       ixl_apz_file=ixl_apz_file)
    # Create Constraint sheet
    create_constraint_sheet(wb)
    # Create Verification sheet
    ws, row = create_empty_verif_sheet(wb)
    # Create Parameters sheet
    inhibit_simple_overshoot_recovery = create_parameters_sheet(wb)

    # Update Verification sheet
    _update_verif_sheet(ws, row, verif_dict, inhibit_simple_overshoot_recovery)

    # Save workbook
    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.realpath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"\"Verification of CF_SIGNAL_12\" verification file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    open_excel_file(res_file_path)


def _update_verif_sheet(ws: xl_ws.Worksheet, start_row: int, verif_dict: dict[str, dict[str, Any]],
                        inhibit_simple_overshoot_recovery: bool) -> None:

    for row, obj_val in enumerate(verif_dict.values(), start=start_row):
        sig_name = obj_val.get("sig_name")
        sig_type = obj_val.get("sig_type")
        sig_direction = obj_val.get("sig_direction")
        last_ivb_platform_related = obj_val.get("last_ivb_platform_related")
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

        _add_line_info(ws, row, sig_name, sig_type, sig_direction, ixl_apz,
                       downstream_seg, downstream_x, downstream_track, downstream_kp, upstream_seg, upstream_x,
                       upstream_track, upstream_kp, ixl_apz_dist, last_ivb_platform_related, dlt_distance)
        _add_value_to_remove(ws, row, status)
        _add_status(ws, row, status)
        _add_comments(ws, row, comments, inhibit_simple_overshoot_recovery, last_ivb_platform_related)

    if inhibit_simple_overshoot_recovery is True:
        # no overshoot recovery, the column for the Related Platform can be hidden
        ws.column_dimensions[LAST_IVB_PLATFORM_RELATED_COL].hidden = True


def _add_line_info(ws: xl_ws.Worksheet, row: int, sig_name: str,
                   sig_type: str, sig_direction: str, ixl_apz: Optional[str],
                   downstream_seg: Optional[str], downstream_x: Optional[float],
                   downstream_track: Optional[str], downstream_kp: Optional[float],
                   upstream_seg: Optional[str], upstream_x: Optional[float],
                   upstream_track: Optional[str], upstream_kp: Optional[float],
                   ixl_apz_dist: Optional[float], last_ivb_platform_related: Optional[str],
                   dlt_distance: Optional[float]) -> None:
    # Signal Name
    create_cell(ws, sig_name, row=row, column=SIGNAL_NAME_COL, borders=True)
    # Type
    create_cell(ws, sig_type, row=row, column=TYPE_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Direction
    create_cell(ws, sig_direction, row=row, column=DIRECTION_COL, borders=True,
                align_horizontal=XlAlign.center)
    # IXL Approach Zone
    create_cell(ws, ixl_apz, row=row, column=IXL_APZ_COL, borders=True, line_wrap=True,
                align_horizontal=XlAlign.center)
    # Downstream Seg
    create_cell(ws, downstream_seg, row=row, column=DOWNSTREAM_LIM_SEG_COL, borders=True)
    # Downstream x
    create_cell(ws, downstream_x, row=row, column=DOWNSTREAM_LIM_X_COL, borders=True,
                nb_of_digits=2)
    # Downstream Track
    create_cell(ws, downstream_track, row=row, column=DOWNSTREAM_LIM_TRACK_COL, borders=True)
    # Downstream KP
    create_cell(ws, downstream_kp, row=row, column=DOWNSTREAM_LIM_KP_COL, borders=True,
                nb_of_digits=2)
    # Upstream Seg
    create_cell(ws, upstream_seg, row=row, column=UPSTREAM_LIM_SEG_COL, borders=True)
    # Upstream x
    create_cell(ws, upstream_x, row=row, column=UPSTREAM_LIM_X_COL, borders=True,
                nb_of_digits=2)
    # Upstream Track
    create_cell(ws, upstream_track, row=row, column=UPSTREAM_LIM_TRACK_COL, borders=True)
    # Upstream KP
    create_cell(ws, upstream_kp, row=row, column=UPSTREAM_LIM_KP_COL, borders=True,
                nb_of_digits=2)
    # IXL APZ Length
    create_cell(ws, ixl_apz_dist, row=row, column=IXL_APZ_LENGTH_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)
    # Last IVB Platform Related
    create_cell(ws, last_ivb_platform_related, row=row, column=LAST_IVB_PLATFORM_RELATED_COL, borders=True,
                line_wrap=True, align_horizontal=XlAlign.center)
    # DLT Distance
    create_cell(ws, dlt_distance, row=row, column=DLT_DIST_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)


def _add_value_to_remove(ws: xl_ws.Worksheet, row: int, status: Optional[str]) -> None:
    if status is not None:
        create_cell(ws, None, row=row, column=VALUE_TO_REMOVE_COL, borders=True,
                    align_horizontal=XlAlign.center)
        return
    # Value to remove
    formula = (f'= IF(OR(inhibit_simple_overshoot_recovery = TRUE, {LAST_IVB_PLATFORM_RELATED_COL}{row} = ""),\n '
               f'(at_deshunt_max_dist + block_laying_uncertainty + MAX(mtc_rollback_dist, at_rollback_dist)),\n '
               f'(at_deshunt_max_dist + block_laying_uncertainty + MAX(mtc_rollback_dist, at_rollback_dist, '
               f'overshoot_recovery_dist + overshoot_recovery_stopping_max_dist)))')
    create_cell(ws, formula, row=row, column=VALUE_TO_REMOVE_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=3)


def _add_status(ws: xl_ws.Worksheet, row: int, status: Optional[str]) -> None:
    if status is not None:
        create_cell(ws, None, row=row, column=MIN_DIST_COL, borders=True, align_horizontal=XlAlign.center)
        create_cell(ws, status, row=row, column=STATUS_COL, borders=True, align_horizontal=XlAlign.center)
        return
    # Minimum Distance
    min_dist_formula = f'= {IXL_APZ_LENGTH_COL}{row} - {VALUE_TO_REMOVE_COL}{row}'
    create_cell(ws, min_dist_formula, row=row, column=MIN_DIST_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=3)
    # Status
    status_formula = f'= IF({DLT_DIST_COL}{row} <= {MIN_DIST_COL}{row}, "OK", "KO")'
    create_cell(ws, status_formula, row=row, column=STATUS_COL, borders=True,
                align_horizontal=XlAlign.center)


def _add_comments(ws: xl_ws.Worksheet, row: int, comments: Optional[str],
                  inhibit_simple_overshoot_recovery: bool, platform_related: Optional[str]) -> None:
    # Comments
    if comments is not None:
        create_cell(ws, comments, row=row, column=COMMENTS_COL, borders=True, line_wrap=True)
        return
    if not inhibit_simple_overshoot_recovery and platform_related is not None:
        comments = ("Overshoot Recovery parameters are considered only when last IVB of the IXL APZ is platform "
                    "related, where overshoot recovery can be used and let a train leave the APZ.")
    create_cell(ws, comments, row=row, column=COMMENTS_COL, borders=True, line_wrap=True)
