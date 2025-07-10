#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_path_and_distances import get_dist_downstream


__all__ = ["get_signals_distance_to_joint"]


def get_signals_distance_to_joint():
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

    csv = ""
    for line in res_dict.values():
        if not csv:
            csv += ";".join([key for key in line]) + "\n"
        csv += ";".join([str(val) for val in line.values()]) + "\n"
    csv = "sep=;\n" + csv

    result_file = "signal_joints.csv"
    result_file = f" - {get_current_version()}".join(os.path.splitext(result_file))
    with open(result_file, "w") as f:
        f.write(csv)
        print(f"{Color.white}CSV file with the signals joint location is available at{Color.reset}"
              f"\n{Color.yellow}{os.path.realpath(result_file)}{Color.reset}")
    open_excel_file(result_file)
