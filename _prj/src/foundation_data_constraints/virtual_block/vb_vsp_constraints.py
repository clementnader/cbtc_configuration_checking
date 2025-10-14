#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_get_zones import get_objects_in_zone, get_dist_downstream_in_zone
from ...dc_sys_sheet_utils.virtual_block_utils import get_vb_downstream_limits
from ...dc_par import *


__all__ = ["cc_cv_19", "cc_cv_20"]


def cc_cv_19():
    print_title("Verification of CC_CV_19", color=Color.mint_green)
    at_rollback_dist = get_parameter_value("at_rollback_dist")

    no_ko = True
    vb_list = get_objects_list(DCSYS.CV)
    for vb_name in vb_list:
        sw_on_vb, nb_vb_limits, mid_status = _check_sw_on_vb(vb_name)
        if not mid_status:
            no_ko = False

        if (sw_on_vb is not None) or (nb_vb_limits == 3):
            continue  # check only for VB not containing a switch

        nb_vsp_by_direction = {Direction.CROISSANT: {"cnt": 0, "related_info": []},
                               Direction.DECROISSANT: {"cnt": 0, "related_info": []}}

        # Get signals VSP on the VB
        sig_vsp_on_vb = _get_signals_vsp_on_vb(vb_name)
        for sig_name in sig_vsp_on_vb:
            vsp_seg, vsp_x, vsp_direction = get_object_position(DCSYS.Sig.DistPap, sig_name)
            vsp_related_info, mid_status = _check_vsp_distance_to_vb_limit(
                vb_name, "Signal", sig_name, vsp_seg, vsp_x, vsp_direction, at_rollback_dist)
            if not mid_status:
                no_ko = False
            nb_vsp_by_direction[vsp_direction]["cnt"] += 1
            nb_vsp_by_direction[vsp_direction]["related_info"].append(vsp_related_info)

        # Get overlap VSP on the VB
        ixl_ovl_vsp_on_vb = _get_overlaps_vsp_on_vb(vb_name)
        for ixl_ovl_name in ixl_ovl_vsp_on_vb:
            vsp_seg, vsp_x, vsp_direction = get_object_position(DCSYS.IXL_Overlap.VitalStoppingPoint, ixl_ovl_name)
            vsp_related_info, mid_status = _check_vsp_distance_to_vb_limit(
                vb_name, "IXL_Overlap", ixl_ovl_name, vsp_seg, vsp_x, vsp_direction, at_rollback_dist)
            if not mid_status:
                no_ko = False
            nb_vsp_by_direction[vsp_direction]["cnt"] += 1
            nb_vsp_by_direction[vsp_direction]["related_info"].append(vsp_related_info)

        # Check number of VSP per direction
        for direction, info in nb_vsp_by_direction.items():
            if info["cnt"] > 1:
                print_error(f"Too many VSPs in direction {direction} on VB {vb_name}:")
                print("\t" + "\n\t".join(info["related_info"]))
                no_ko = False
    if no_ko:
        print_log("No KO found on the constraint.")


def _check_sw_on_vb(vb_name: str) -> tuple[Optional[list[str]], int, bool]:
    no_ko = True
    sw_on_vb = get_objects_in_zone(DCSYS.Aig, DCSYS.CV, vb_name)
    nb_vb_limits = len(get_object_position(DCSYS.CV, vb_name))
    if (sw_on_vb is not None) != (nb_vb_limits == 3):
        print_error(f"VB {vb_name} number of limits is not coherent with the presence of switch on the VB:"
                    f"\n{sw_on_vb = }\n{nb_vb_limits = }")
        no_ko = False
    if sw_on_vb is not None and len(sw_on_vb) != 1:
        print_error(f"Multiple switches on VB {vb_name}:\n{sw_on_vb = }")
        no_ko = False

    return sw_on_vb, nb_vb_limits, no_ko


def _get_signals_vsp_on_vb(vb_name: str) -> list[str]:
    sig_vsp_on_vb = get_objects_in_zone(DCSYS.Sig.DistPap, DCSYS.CV, vb_name,
                                        ignore_objects_on_zone_limits=True)
    if sig_vsp_on_vb is None:
        sig_vsp_on_vb = []
    # remove buffers from the list of signals
    sig_vsp_on_vb = [sig_name for sig_name in sig_vsp_on_vb
                     if get_dc_sys_value(sig_name, DCSYS.Sig.Type) != SignalType.HEURTOIR]
    return sig_vsp_on_vb


def _get_overlaps_vsp_on_vb(vb_name: str) -> list[str]:
    ixl_ovl_vsp_on_vb = get_objects_in_zone(DCSYS.IXL_Overlap.VitalStoppingPoint, DCSYS.CV, vb_name,
                                            ignore_objects_on_zone_limits=True)
    if ixl_ovl_vsp_on_vb is None:
        ixl_ovl_vsp_on_vb = []
    return ixl_ovl_vsp_on_vb


def _check_vsp_distance_to_vb_limit(vb_name: str, object_type: str, object_name: str,
                                    vsp_seg: str, vsp_x: float, vsp_direction: str,
                                    at_rollback_dist: float) -> tuple[str, bool]:
    no_ko = True
    vsp_related_info = (f"VSP of {Color.beige}{object_type}{Color.reset} {Color.yellow}{object_name}"
                        f"{Color.reset} {(vsp_seg, vsp_x)}")

    downstream_limit = get_vb_downstream_limits(vb_name, vsp_direction)[0]
    dist = get_dist_downstream_in_zone(vsp_seg, vsp_x, downstream_limit[0], downstream_limit[1],
                                       vsp_direction == Direction.CROISSANT, DCSYS.CV, vb_name)
    if dist > at_rollback_dist:
        print_error(f"{vsp_related_info} is too far away from downstream limit of VB {vb_name} "
                    f"{downstream_limit}:\n\tdistance is {dist} > {at_rollback_dist=}")
        no_ko = False

    vsp_related_info += f" at {dist} from the VB downstream limit"
    return vsp_related_info, no_ko


def cc_cv_20():
    print_title("Verification of CC_CV_20", color=Color.mint_green)
    at_rollback_dist = get_parameter_value("at_rollback_dist")

    no_ko = True
    vb_list = get_objects_list(DCSYS.CV)
    for vb_name in vb_list:
        sw_on_vb, nb_vb_limits, mid_status = _check_sw_on_vb(vb_name)
        if not mid_status:
            no_ko = False

        if (sw_on_vb is None) and (nb_vb_limits == 2):
            continue  # check only for VB containing a switch

        sw_on_vb = sw_on_vb[0]
        nb_vsp = {"cnt": 0, "related_info": []}

        # Get signals VSP on the VB
        sig_vsp_on_vb = _get_signals_vsp_on_vb(vb_name)
        for sig_name in sig_vsp_on_vb:
            vsp_seg, vsp_x, vsp_direction = get_object_position(DCSYS.Sig.DistPap, sig_name)
            vsp_related_info, mid_status = _check_vsp_distance_to_switch(
                vb_name, "Signal", sig_name, sw_on_vb, vsp_seg, vsp_x, vsp_direction, at_rollback_dist)
            if not mid_status:
                no_ko = False
            nb_vsp["cnt"] += 1
            nb_vsp["related_info"].append(vsp_related_info)

        # Get overlap VSP on the VB
        ixl_ovl_vsp_on_vb = _get_overlaps_vsp_on_vb(vb_name)
        for ixl_ovl_name in ixl_ovl_vsp_on_vb:
            vsp_seg, vsp_x, vsp_direction = get_object_position(DCSYS.IXL_Overlap.VitalStoppingPoint, ixl_ovl_name)
            vsp_related_info, mid_status = _check_vsp_distance_to_switch(
                vb_name, "IXL_Overlap", ixl_ovl_name, sw_on_vb, vsp_seg, vsp_x, vsp_direction, at_rollback_dist)
            if not mid_status:
                no_ko = False
            nb_vsp["cnt"] += 1
            nb_vsp["related_info"].append(vsp_related_info)

        if nb_vsp["cnt"] > 1:
            print_error(f"Too many VSPs on VB {vb_name} containing switch {sw_on_vb}:")
            print("\t" + "\n\t".join(nb_vsp["related_info"]))
            no_ko = False
    if no_ko:
        print_log("No KO found on the constraint.")


def _check_vsp_distance_to_switch(vb_name: str, object_type: str, object_name: str, sw_on_vb: str,
                                  vsp_seg: str, vsp_x: float, vsp_direction: str,
                                  at_rollback_dist: float) -> tuple[str, bool]:
    no_ko = True
    vsp_related_info = (f"VSP of {Color.beige}{object_type}{Color.reset} {Color.yellow}{object_name}"
                        f"{Color.reset} {(vsp_seg, vsp_x, vsp_direction)}")

    sw_seg, sw_x = get_object_position(DCSYS.Aig, sw_on_vb)
    dist_to_sw = get_dist_downstream_in_zone(vsp_seg, vsp_x, sw_seg, sw_x,
                                             vsp_direction == Direction.CROISSANT, DCSYS.CV, vb_name)
    if dist_to_sw is None:
        print_error(f"{vsp_related_info} is not upstream the switch on {vb_name}, "
                    f"it is located on the heels part.")
        no_ko = False

    downstream_limits = get_vb_downstream_limits(vb_name, vsp_direction)
    for i, downstream_limit in enumerate(downstream_limits, start=1):
        dist = get_dist_downstream_in_zone(vsp_seg, vsp_x, downstream_limit[0], downstream_limit[1],
                                           vsp_direction == Direction.CROISSANT, DCSYS.CV, vb_name)
        if dist > at_rollback_dist:
            print_error(f"{vsp_related_info} is too far away from downstream limit of VB {vb_name} "
                        f"{downstream_limit}:\n\tdistance is {dist} > {at_rollback_dist=}")
            no_ko = False

    return vsp_related_info, no_ko
