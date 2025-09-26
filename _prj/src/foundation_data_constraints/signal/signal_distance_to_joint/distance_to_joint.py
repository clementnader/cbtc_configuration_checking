#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ....dc_sys_draw_path.dc_sys_path_and_distances import get_dist_downstream
from .file_format_utils import *


__all__ = ["get_signals_distance_to_joint"]


OUTPUT_DIRECTORY = "."
VERIF_FILE_NAME = "Signal to Joint Distance.xlsx"
FILE_TITLE = "Distance from signal to joint"


def get_signals_distance_to_joint():
    print_title(f"Computing distance from signal to joint", color=Color.mint_green)

    verif_dict = _compute_signals_distance_to_joint_dict()
    _create_verif_file(verif_dict)


def _compute_signals_distance_to_joint_dict() -> dict[str, dict[str, Any]]:
    res_dict = dict()
    sig_list = get_objects_list(DCSYS.Sig)
    for sig_name in sig_list:
        sig_type = get_dc_sys_value(sig_name, DCSYS.Sig.Type)
        if sig_type != SignalType.MANOEUVRE:
            continue
        sig_vsp_distance = get_dc_sys_value(sig_name, DCSYS.Sig.DistPap)
        sig_position = get_object_position(DCSYS.Sig, sig_name)
        sig_seg, sig_x, sig_direction, sig_track, sig_kp = add_track_kp_to_position(sig_position)

        ivb_downstream, ivb_upstream = get_dc_sys_values(sig_name, DCSYS.Sig.IvbJoint.DownstreamIvb,
                                                         DCSYS.Sig.IvbJoint.UpstreamIvb)
        ivb_d_limits = get_object_position(DCSYS.IVB, ivb_downstream)
        ivb_u_limits = get_object_position(DCSYS.IVB, ivb_upstream)
        common_limit = None
        for ivb_d_limit in ivb_d_limits:
            for ivb_u_limit in ivb_u_limits:
                if are_points_matching(*ivb_d_limit, *ivb_u_limit):
                    common_limit = ivb_d_limit
        joint_seg, joint_x, joint_track, joint_kp = add_track_kp_to_position(common_limit)

        distance = get_dist_downstream(sig_seg, sig_x, joint_seg, joint_x, downstream=sig_direction==Direction.CROISSANT)

        res_dict[sig_name] = {
            "sig_name": sig_name, "sig_type": sig_type,
            "sig_seg": sig_seg, "sig_x": sig_x, "sig_direction": sig_direction, "sig_track": sig_track, "sig_kp": sig_kp,
            "sig_vsp_distance": sig_vsp_distance,
            "sig_joint": f"{ivb_downstream} / {ivb_upstream}",
            "joint_seg": joint_seg, "joint_x": joint_x, "joint_track": joint_track, "joint_kp": joint_kp,
            "distance": distance
        }

    return res_dict


def _create_verif_file(verif_dict: dict[str, dict[str, Any]]) -> None:
    # Initialize Verification Workbook
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
    print_success(f"\"Signal to Joint Distance\" computation file is available at:\n"
                  f"{Color.blue}{res_file_path}{Color.reset}")
    open_excel_file(res_file_path)


def _update_verif_sheet(ws: xl_ws.Worksheet, start_row: int, verif_dict: dict[str, dict[str, Any]]) -> None:

    for row, obj_val in enumerate(verif_dict.values(), start=start_row):
        sig_name = obj_val.get("sig_name")
        sig_type = obj_val.get("sig_type")
        sig_seg = obj_val.get("sig_seg")
        sig_x = obj_val.get("sig_x")
        sig_direction = obj_val.get("sig_direction")
        sig_track = obj_val.get("sig_track")
        sig_kp = obj_val.get("sig_kp")
        sig_vsp_distance = obj_val.get("sig_vsp_distance")
        sig_joint = obj_val.get("sig_joint")
        joint_seg = obj_val.get("joint_seg")
        joint_x = obj_val.get("joint_x")
        joint_track = obj_val.get("joint_track")
        joint_kp = obj_val.get("joint_kp")
        distance = obj_val.get("distance")

        _add_line_info(ws, row, sig_name, sig_type, sig_seg, sig_x, sig_direction, sig_track, sig_kp,
                       sig_vsp_distance, sig_joint, joint_seg, joint_x,
                       joint_track, joint_kp, distance)


def _add_line_info(ws: xl_ws.Worksheet, row: int, sig_name: str, sig_type: str,
                   sig_seg: str, sig_x: float, sig_direction: str, sig_track: str, sig_kp: float,
                   sig_vsp_distance: float, sig_joint: str, joint_seg: str, joint_x: float,
                   joint_track: str, joint_kp: float, distance: float) -> None:
    # Signal Name
    create_cell(ws, sig_name, row=row, column=SIGNAL_NAME_COL, borders=True)
    # Type
    create_cell(ws, sig_type, row=row, column=TYPE_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Signal Seg
    create_cell(ws, sig_seg, row=row, column=SIG_SEG_COL, borders=True)
    # Signal x
    create_cell(ws, sig_x, row=row, column=SIG_X_COL, borders=True,
                nb_of_digits=2)
    # Signal Direction
    create_cell(ws, sig_direction, row=row, column=SIG_DIRECTION_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Signal Track
    create_cell(ws, sig_track, row=row, column=SIG_TRACK_COL, borders=True)
    # Signal KP
    create_cell(ws, sig_kp, row=row, column=SIG_KP_COL, borders=True,
                nb_of_digits=2)
    # VSP Distance
    create_cell(ws, sig_vsp_distance, row=row, column=VSP_DISTANCE_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)
    # IVB Joint Name
    create_cell(ws, sig_joint, row=row, column=JOINT_NAME_COL, borders=True,
                align_horizontal=XlAlign.center)
    # Joint Seg
    create_cell(ws, joint_seg, row=row, column=JOINT_SEG_COL, borders=True)
    # Joint x
    create_cell(ws, joint_x, row=row, column=JOINT_X_COL, borders=True,
                nb_of_digits=2)
    # Joint Track
    create_cell(ws, joint_track, row=row, column=JOINT_TRACK_COL, borders=True)
    # Joint KP
    create_cell(ws, joint_kp, row=row, column=JOINT_KP_COL, borders=True,
                nb_of_digits=2)
    # Distance
    create_cell(ws, distance, row=row, column=DISTANCE_COL, borders=True,
                align_horizontal=XlAlign.center, nb_of_digits=2)
