#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_sheet_utils.signal_utils import get_ivb_limit_of_a_signal
from ..dc_par import *
from ..ixl_utils import get_distance_between_block_and_approach_zone


__all__ = ["cf_signal_12"]


def cf_signal_12(no_overshoot: bool = False, apz_with_tc: bool = False):
    # In nominal case the IXL approach zone locking for a dedicated signal is configured
    # to contain the first physical track circuit -> not always, see the corresponding ZC-IXL ICDD,
    # an option is implemented to choose if using the first TC or the first IVB.
    csv = ("Signal Name;Type;Direction;IXL Approach Zone;IVB Limit Downstream;;;;IVB Limit Upstream;;;;"
           "IXL APZ Distance;Distance minus value to remove;DLT Distance;Automatic Status;Comments\n")
    csv += ";;;;Seg;x;Track;KP;Seg;x;Track;KP;;;;;\n"
    print_title(f"Verification of CF_SIGNAL_12", color=Color.mint_green)
    at_deshunt_max_dist = get_param_value("at_deshunt_max_dist")
    block_laying_uncertainty = get_param_value("block_laying_uncertainty")
    mtc_rollback_dist = get_param_value("mtc_rollback_dist")
    at_rollback_dist = get_param_value("at_rollback_dist")
    overshoot_recovery_dist = get_param_value("overshoot_recovery_dist")
    overshoot_recovery_stopping_max_dist = get_param_value("overshoot_recovery_stopping_max_dist")
    if no_overshoot:
        value_to_remove = (at_deshunt_max_dist + block_laying_uncertainty +
                           max(mtc_rollback_dist, at_rollback_dist))
    else:
        value_to_remove = (at_deshunt_max_dist + block_laying_uncertainty +
                           max(mtc_rollback_dist, at_rollback_dist,
                               overshoot_recovery_dist + overshoot_recovery_stopping_max_dist))

    sig_dict = load_sheet(DCSYS.Sig)
    nb_sigs = len(sig_dict.keys())
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (sig_name, sig) in enumerate(sig_dict.items()):
        print_log(f"\r{progress_bar(i, nb_sigs)} processing verification of DLT distance of {sig_name}...", end="")
        sig_type = get_dc_sys_value(sig, DCSYS.Sig.Type)
        sig_direction = get_dc_sys_value(sig, DCSYS.Sig.Sens)
        csv += f"{sig_name};{sig_type};{sig_direction};"
        if sig_type in [SignalType.HEURTOIR, SignalType.PERMANENT_ARRET]:
            csv += f";;;;;;;;;;;;{'NA'};\n"
            continue

        dlt_distance = get_dc_sys_value(sig, DCSYS.Sig.DelayedLtDistance)
        if dlt_distance == 0:
            csv += f";;;;;;;;;;;{dlt_distance};{'OK'};0 is a safe value\n"
            continue
        (ivb_lim_seg, ivb_lim_x), ivb_lim_str = get_ivb_limit_of_a_signal(sig_name, sig)
        ivb_lim_track, ivb_lim_kp = from_seg_offset_to_kp(ivb_lim_seg, ivb_lim_x)

        min_dist, corresponding_entrance, ivb_names = (
            get_distance_between_block_and_approach_zone(sig_name, ivb_lim_seg, ivb_lim_x, apz_with_tc))

        if min_dist is None:
            csv += (f"{ivb_names};{ivb_lim_seg};{ivb_lim_x};{ivb_lim_track};{ivb_lim_kp};;;;;;;{dlt_distance};{'KO'};"
                    f"Tool was unable to find upstream IXL Approach Zone limit and to compute a path.\n")
            continue
        corresponding_entrance_track, corresponding_entrance_kp = from_seg_offset_to_kp(*corresponding_entrance)
        test_value = round(min_dist - value_to_remove, 3)
        success = dlt_distance <= test_value

        csv += (f"{ivb_names};{ivb_lim_seg};{ivb_lim_x};{ivb_lim_track};{ivb_lim_kp};"
                f"{corresponding_entrance[0]};{corresponding_entrance[1]};"
                f"{corresponding_entrance_track};{corresponding_entrance_kp};"
                f"{min_dist};{test_value};{dlt_distance};{'OK' if success else 'KO'};\n")

    print_log(f"\r{progress_bar(nb_sigs, nb_sigs, end=True)} verification of DLT distance finished.\n")
    print(csv)
    return
