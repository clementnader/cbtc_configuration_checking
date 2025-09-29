#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ....dc_sys_draw_path.dc_sys_path_and_distances import get_next_objects_from_a_point
from ....dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point
from .file_format_utils import *


__all__ = ["get_osp_not_platform_related_distance_to_joints_and_signals"]


OUTPUT_DIRECTORY = "."
VERIF_FILE_NAME = "OSP to Joints and Signals Distance.xlsx"
FILE_TITLE = "Distance from OSP not platform related to joints and signals"


def get_osp_not_platform_related_distance_to_joints_and_signals():
    print_title(f"Computing distance from OSP (not platform related) to joints and signals", color=Color.mint_green)

    verif_dict = _compute_osp_distance_dict()
    _create_verif_file(verif_dict)


def _compute_osp_distance_dict() -> dict[str, dict[str, Any]]:
    res_dict = dict()
    osp_list = get_objects_list(DCSYS.PtA)
    nb_osp = len(osp_list)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, osp_name in enumerate(osp_list):
        print_log_progress_bar(i, nb_osp, f"distance from {osp_name}")
        osp_position = get_object_position(DCSYS.PtA, osp_name)
        osp_seg, osp_x, osp_direction, osp_track, osp_kp = add_track_kp_to_position(osp_position)
        osp_approach_direction = get_dc_sys_value(osp_name, DCSYS.PtA.SensApproche)
        osp_type = get_dc_sys_value(osp_name, DCSYS.PtA.TypePtAto)
        osp_permanent_stop = get_dc_sys_value(osp_name, DCSYS.PtA.ArretPermanentCpa)
        osp_parking = get_dc_sys_value(osp_name, DCSYS.PtA.ParkingPosition)
        osp_washing = get_dc_sys_value(osp_name, DCSYS.PtA.WashingOsp)

        res_dict[osp_name] = {
            "osp_name": osp_name,
            "osp_seg": osp_seg, "osp_x": osp_x, "osp_direction": osp_direction, "osp_track": osp_track, "osp_kp": osp_kp,
            "osp_approach_direction": osp_approach_direction, "osp_type": osp_type,
            "osp_permanent_stop": osp_permanent_stop, "osp_parking": osp_parking, "osp_washing": osp_washing,
        }
        res_dict[osp_name].update(_compute_dist_to_joint(osp_seg, osp_x, osp_direction))
        res_dict[osp_name].update(_compute_dist_to_sig(osp_seg, osp_x))
    print_log_progress_bar(nb_osp, nb_osp, f"computation of distance from OSPs finished", end=True)

    return res_dict


def _compute_dist_to_joint(osp_seg: str, osp_x: float, osp_direction: str) -> dict[str, Any]:
    current_ivb = get_zones_on_point(DCSYS.IVB, osp_seg, osp_x, osp_direction)[0]
    next_ivb_inc = get_next_objects_from_a_point(osp_seg, osp_x, Direction.CROISSANT, DCSYS.IVB,
                                                 skip_object_on_point=current_ivb)
    next_ivb_dec = get_next_objects_from_a_point(osp_seg, osp_x, Direction.DECROISSANT, DCSYS.IVB,
                                                 skip_object_on_point=current_ivb)
    comments_list = list()
    joint_inc = None
    joint_dec = None
    if not next_ivb_inc:
        joint_inc = f"{current_ivb} / end-of-track"
        next_ivb_inc = get_next_objects_from_a_point(osp_seg, osp_x, Direction.CROISSANT, DCSYS.IVB)
    if not next_ivb_dec:
        joint_dec = f"end-of-track / {current_ivb}"
        next_ivb_dec = get_next_objects_from_a_point(osp_seg, osp_x, Direction.DECROISSANT, DCSYS.IVB)
    if len(next_ivb_inc) > 1:
        comments_list.append(f"OSP is placed on an IVB containing a diverging switch downstream the OSP.")
        next_ivb_inc.sort(key=lambda a: a[2])  # sort according to the distance
    if len(next_ivb_dec) > 1:
        comments_list.append(f"OSP is placed on an IVB containing a diverging switch upstream the OSP.")
        next_ivb_dec.sort(key=lambda a: a[2])  # sort according to the distance

    next_ivb_inc, _, dist_inc = next_ivb_inc[0]
    next_ivb_dec, _, dist_dec = next_ivb_dec[0]

    res_dict = {
        "joint_inc": joint_inc if joint_inc is not None else f"{current_ivb} / {next_ivb_inc}",
        "joint_dist_inc": dist_inc,
        "joint_dec": joint_dec if joint_dec is not None else f"{next_ivb_dec} / {current_ivb}",
        "joint_dist_dec": dist_dec,
        "joint_comments": "\n".join(comments_list),
    }
    return res_dict


def _compute_dist_to_sig(osp_seg: str, osp_x: float) -> dict[str, Any]:
    next_sig_inc = get_next_objects_from_a_point(osp_seg, osp_x, Direction.CROISSANT, DCSYS.Sig,
                                                 obj_direction=Direction.CROISSANT)
    next_sig_dec = get_next_objects_from_a_point(osp_seg, osp_x, Direction.DECROISSANT, DCSYS.Sig,
                                                 obj_direction=Direction.DECROISSANT)
    comments_list = list()
    if not next_sig_inc:
        comments_list.append(f"No signal downstream the OSP.")
        next_sig_inc = [(None, None, None)]
    if not next_sig_dec:
        comments_list.append(f"No signal upstream the OSP.")
        next_sig_dec = [(None, None, None)]
    if len(next_sig_inc) > 1:
        comments_list.append(f"There is a diverging switch downstream the OSP before reaching a signal.")
        next_sig_inc.sort(key=lambda a: a[2])  # sort according to the distance
    if len(next_sig_dec) > 1:
        comments_list.append(f"There is a diverging switch upstream the OSP before reaching a signal.")
        next_sig_dec.sort(key=lambda a: a[2])  # sort according to the distance

    next_sig_inc, _, dist_inc = next_sig_inc[0]
    next_sig_dec, _, dist_dec = next_sig_dec[0]

    res_dict = {
        "sig_inc": next_sig_inc,
        "sig_type_inc": get_dc_sys_value(next_sig_inc, DCSYS.Sig.Type) if next_sig_inc else None,
        "sig_dist_inc": dist_inc,
        "sig_dec": next_sig_dec,
        "sig_type_dec": get_dc_sys_value(next_sig_dec, DCSYS.Sig.Type) if next_sig_dec else None,
        "sig_dist_dec": dist_dec,
        "sig_comments": "\n".join(comments_list),
    }
    return res_dict


def _create_verif_file(verif_dict: dict[str, dict[str, Any]]) -> None:
    # Initialize Verification Workbook
    wb = create_empty_verification_file()
    # Update Header sheet
    update_header_sheet_for_verif_file(wb, title=FILE_TITLE, c_d470=get_current_version())
    # Create Joint Verification sheet
    joint_ws, row = create_empty_joint_verif_sheet(wb)
    # Create Signal Verification sheet
    sig_ws, row = create_empty_sig_verif_sheet(wb)

    # Update Joint Verification sheet
    _update_joint_verif_sheet(joint_ws, row, verif_dict)
    # Update Signal Verification sheet
    _update_sig_verif_sheet(sig_ws, row, verif_dict)

    # Save workbook
    verif_file_name = f" - {get_current_version()}".join(os.path.splitext(VERIF_FILE_NAME))
    res_file_path = os.path.realpath(os.path.join(OUTPUT_DIRECTORY, verif_file_name))
    save_xl_file(wb, res_file_path)
    print_success(f"\"Distance from OSP to Joints and Signals\" computation file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    open_excel_file(res_file_path)


def _add_osp_line_info(ws: xl_ws.Worksheet, row: int, osp_name: str, osp_seg: str, osp_x: float, osp_direction: str,
                         osp_track: str, osp_kp: float, osp_approach_direction: str, osp_type: str,
                         osp_permanent_stop: str, osp_parking: str, osp_washing: str) -> None:
    # OSP Name
    create_cell(ws, osp_name, row=row, column=OSP_NAME_COL, borders=True)
    # OSP Seg
    create_cell(ws, osp_seg, row=row, column=OSP_SEG_COL, borders=True)
    # OSP x
    create_cell(ws, osp_x, row=row, column=OSP_X_COL, borders=True,
                nb_of_digits=2)
    # OSP Direction
    create_cell(ws, osp_direction, row=row, column=OSP_DIRECTION_COL, borders=True,
                align_horizontal=XlAlign.center)
    # OSP Track
    create_cell(ws, osp_track, row=row, column=OSP_TRACK_COL, borders=True)
    # OSP KP
    create_cell(ws, osp_kp, row=row, column=OSP_KP_COL, borders=True,
                nb_of_digits=2)
    # Approach Direction
    create_cell(ws, osp_approach_direction, row=row, column=OSP_APPROACH_DIRECTION_COL, borders=True,
                align_horizontal=XlAlign.center)
    # OSP Type
    create_cell(ws, osp_type, row=row, column=OSP_TYPE_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Automatic Driving Permanent Stop
    create_cell(ws, osp_permanent_stop, row=row, column=OSP_PERMANENT_STOP_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Parking Position
    create_cell(ws, osp_parking, row=row, column=OSP_PARKING_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Washing Related
    create_cell(ws, osp_washing, row=row, column=OSP_WASHING_COL, borders=True,
                align_horizontal=XlAlign.center)


def _update_joint_verif_sheet(ws: xl_ws.Worksheet, start_row: int, verif_dict: dict[str, dict[str, Any]]) -> None:
    joint_sheet_comments = False

    for row, obj_val in enumerate(verif_dict.values(), start=start_row):
        osp_name = obj_val.get("osp_name")
        osp_seg = obj_val.get("osp_seg")
        osp_x = obj_val.get("osp_x")
        osp_direction = obj_val.get("osp_direction")
        osp_track = obj_val.get("osp_track")
        osp_kp = obj_val.get("osp_kp")
        osp_approach_direction = obj_val.get("osp_approach_direction")
        osp_type = obj_val.get("osp_type")
        osp_permanent_stop = obj_val.get("osp_permanent_stop")
        osp_parking = obj_val.get("osp_parking")
        osp_washing = obj_val.get("osp_washing")
        _add_osp_line_info(ws, row, osp_name, osp_seg, osp_x, osp_direction, osp_track, osp_kp,
                           osp_approach_direction, osp_type, osp_permanent_stop, osp_parking, osp_washing)

        joint_inc = obj_val.get("joint_inc")
        joint_dist_inc = obj_val.get("joint_dist_inc")
        joint_dec = obj_val.get("joint_dec")
        joint_dist_dec = obj_val.get("joint_dist_dec")
        joint_comments = obj_val.get("joint_comments")
        if joint_comments:
            joint_sheet_comments = True

        _add_joint_line_info(ws, row, joint_inc, joint_dist_inc, joint_dec, joint_dist_dec, joint_comments)

    if not joint_sheet_comments:  # no automatic comments, the column can be hidden
        ws.column_dimensions[JOINT_COMMENTS_COL].hidden = True


def _add_joint_line_info(ws: xl_ws.Worksheet, row: int, joint_inc: str, joint_dist_inc: float,
                         joint_dec: str, joint_dist_dec: float, joint_comments: str) -> None:
    # Next IVB Joint in increasing direction
    create_cell(ws, joint_inc, row=row, column=JOINT_INC_NAME_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Distance
    create_cell(ws, joint_dist_inc, row=row, column=JOINT_INC_DISTANCE_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)
    # Next IVB Joint in decreasing direction
    create_cell(ws, joint_dec, row=row, column=JOINT_DEC_NAME_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Distance
    create_cell(ws, joint_dist_dec, row=row, column=JOINT_DEC_DISTANCE_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)
    # Comments
    create_cell(ws, joint_comments, row=row, column=JOINT_COMMENTS_COL, borders=True,
                line_wrap=True)


def _update_sig_verif_sheet(ws: xl_ws.Worksheet, start_row: int, verif_dict: dict[str, dict[str, Any]]) -> None:
    sig_sheet_comments = False

    for row, obj_val in enumerate(verif_dict.values(), start=start_row):
        osp_name = obj_val.get("osp_name")
        osp_seg = obj_val.get("osp_seg")
        osp_x = obj_val.get("osp_x")
        osp_direction = obj_val.get("osp_direction")
        osp_track = obj_val.get("osp_track")
        osp_kp = obj_val.get("osp_kp")
        osp_approach_direction = obj_val.get("osp_approach_direction")
        osp_type = obj_val.get("osp_type")
        osp_permanent_stop = obj_val.get("osp_permanent_stop")
        osp_parking = obj_val.get("osp_parking")
        osp_washing = obj_val.get("osp_washing")
        _add_osp_line_info(ws, row, osp_name, osp_seg, osp_x, osp_direction, osp_track, osp_kp,
                           osp_approach_direction, osp_type, osp_permanent_stop, osp_parking, osp_washing)

        sig_inc = obj_val.get("sig_inc")
        sig_type_inc = obj_val.get("sig_type_inc")
        sig_dist_inc = obj_val.get("sig_dist_inc")
        sig_dec = obj_val.get("sig_dec")
        sig_type_dec = obj_val.get("sig_type_dec")
        sig_dist_dec = obj_val.get("sig_dist_dec")
        sig_comments = obj_val.get("sig_comments")
        if sig_comments:
            sig_sheet_comments = True

        _add_sig_line_info(ws, row, sig_inc, sig_type_inc, sig_dist_inc, sig_dec, sig_type_dec, sig_dist_dec, sig_comments)

    if not sig_sheet_comments:  # no automatic comments, the column can be hidden
        ws.column_dimensions[JOINT_COMMENTS_COL].hidden = True


def _add_sig_line_info(ws: xl_ws.Worksheet, row: int, sig_inc: str, sig_type_inc: str, dist_inc: float,
                       sig_dec: str, sig_type_dec: str, dist_dec: float, comments: str) -> None:
    # Next Signal in increasing direction
    create_cell(ws, sig_inc, row=row, column=SIG_INC_NAME_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Signal Type
    create_cell(ws, sig_type_inc, row=row, column=SIG_INC_TYPE_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Distance
    create_cell(ws, dist_inc, row=row, column=SIG_INC_DISTANCE_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)
    # Next Signal in decreasing direction
    create_cell(ws, sig_dec, row=row, column=SIG_DEC_NAME_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Signal Type
    create_cell(ws, sig_type_dec, row=row, column=SIG_DEC_TYPE_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Distance
    create_cell(ws, dist_dec, row=row, column=SIG_DEC_DISTANCE_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)
    # Comments
    create_cell(ws, comments, row=row, column=SIG_COMMENTS_COL, borders=True,
                line_wrap=True)
