#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_draw_path.dc_sys_path_and_distances import is_seg_downstream
from ..dc_sys_draw_path.dc_sys_get_zones import get_zones_on_point
from .ivb_utils import get_next_ivb_limits_from_point


__all__ = ["get_related_overlaps", "get_routes_starting_from_signal", "get_ivb_limit_of_a_signal",
           "check_upstream_and_downstream_ivb_of_all_signals"]


def get_related_overlaps(sig_name: str):
    ovl_dict = load_sheet(DCSYS.IXL_Overlap)
    related_ovl = list()
    for ovl_name, ovl in ovl_dict.items():
        if get_dc_sys_value(ovl, DCSYS.IXL_Overlap.DestinationSignal) == sig_name:
            related_ovl.append((ovl_name, ovl))
    return related_ovl


def get_routes_starting_from_signal(sig_name: str):
    route_dict = load_sheet(DCSYS.Iti)
    related_routes = list()
    for route_name, route in route_dict.items():
        if get_dc_sys_value(route, DCSYS.Iti.SignalOrig) == sig_name:
            related_routes.append((route_name, route))
    return related_routes


def get_ivb_limit_of_a_signal(sig_name: str, sig_value) -> tuple[tuple[str, float], str]:
    sig_seg, sig_x = get_dc_sys_values(sig_value, DCSYS.Sig.Seg, DCSYS.Sig.X)
    sig_direction = get_dc_sys_value(sig_value, DCSYS.Sig.Sens)
    next_ivb_limits = get_next_ivb_limits_from_point(sig_seg, sig_x, downstream=sig_direction == Direction.CROISSANT)
    if len(next_ivb_limits) != 1:
        print_error(f"There is not a direct IVB limit after the signal {sig_name}")
        print(f"{next_ivb_limits = }")
    return next_ivb_limits[0]


def check_upstream_and_downstream_ivb_of_all_signals() -> None:
    print_title(f"Verification of configuration of IVB upstream and downstream of signals.",
                color=Color.mint_green)
    sig_dict = load_sheet(DCSYS.Sig)
    for sig_name, sig_value in sig_dict.items():
        sig_type = get_dc_sys_value(sig_value, DCSYS.Sig.Type)
        if sig_type == SignalType.HEURTOIR:
            continue
        check_upstream_and_downstream_ivb_of_a_signal(sig_name)


def check_upstream_and_downstream_ivb_of_a_signal(sig_name: str) -> None:
    sig_dict = load_sheet(DCSYS.Sig)
    sig_value = sig_dict[sig_name]
    sig_seg, sig_x = get_dc_sys_values(sig_value, DCSYS.Sig.Seg, DCSYS.Sig.X)
    sig_type = get_dc_sys_value(sig_value, DCSYS.Sig.Type)
    sig_direction = get_dc_sys_value(sig_value, DCSYS.Sig.Sens)
    # at a limit between two IVB, the signal is considered to belong to the IVB in rear

    list_ivb_on_sig = get_zones_on_point(DCSYS.IVB, sig_seg, sig_x, direction=sig_direction)
    if not list_ivb_on_sig:
        if sig_type == SignalType.PERMANENT_ARRET:
            print_log(f"Permanently Red {sig_name} is on no IVB.")
        else:
            print_error(f"Signal {sig_name} is on no IVB.")
        return
    if len(list_ivb_on_sig) > 1:
        print_error(f"Signal {sig_name} is on multiple IVBs: {list_ivb_on_sig}.")
        return
    upstream_ivb = list_ivb_on_sig[0]
    dc_sys_upstream_ivb = get_dc_sys_value(sig_value, DCSYS.Sig.IvbJoint.UpstreamIvb)
    if upstream_ivb != dc_sys_upstream_ivb:
        print_error(f"For {sig_name}, tool has computed IVB {upstream_ivb} as the upstream IVB but in DC_SYS, "
                    f"{dc_sys_upstream_ivb} is configured.")

    ivb_dict = load_sheet(DCSYS.IVB)
    ivb_limits = list(get_dc_sys_zip_values(ivb_dict[upstream_ivb], DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X))
    joint_limit = [(seg, x) for (seg, x) in ivb_limits if is_seg_downstream(sig_seg, seg, sig_x, x,
                   downstream=(sig_direction == Direction.CROISSANT))]
    if not joint_limit:
        print_error(f"No joint of the signal found for {sig_name}.")
        return
    if len(joint_limit) > 1:
        print_error(f"Multiple joints of the signal found for {sig_name}: {joint_limit}.")
        return
    joint_limit = joint_limit[0]

    list_ivb_after_sig = get_zones_on_point(DCSYS.IVB, *joint_limit, direction=get_reverse_direction(sig_direction))
    if not list_ivb_after_sig:
        if sig_type == SignalType.PERMANENT_ARRET:
            pass
        else:
            print_error(f"Signal {sig_name} has no IVB downstream. It should be a Permanently Red.")
        downstream_ivb = None
    else:
        if len(list_ivb_after_sig) > 1:
            print_error(f"Signal {sig_name} has multiple IVBs downstream: {list_ivb_after_sig}.")
            return
        downstream_ivb = list_ivb_after_sig[0]
    dc_sys_downstream_ivb = get_dc_sys_value(sig_value, DCSYS.Sig.IvbJoint.DownstreamIvb)
    if downstream_ivb != dc_sys_downstream_ivb:
        print_error(f"For {sig_name}, tool has computed IVB {downstream_ivb} as the downstream IVB but in DC_SYS, "
                    f"{dc_sys_downstream_ivb} is configured.")
