#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ....dc_sys_sheet_utils.signal_utils import get_ivb_limit_of_a_signal
from ....dc_sys_draw_path.dc_sys_path_and_distances import get_dist_downstream


__all__ = ["compute_cbtc_sig_apz"]


def compute_cbtc_sig_apz():
    res_dict = dict()
    sig_dict = load_sheet(DCSYS.Sig)
    sig_zone_dict = load_sheet(DCSYS.Sig_Zone)

    nb_sigs = len(sig_dict)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (sig_name, sig) in enumerate(sig_dict.items()):
        print_log_progress_bar(i, nb_sigs, f"verifying CBTC Approach Zone length of {sig_name}")
        sig_type = get_dc_sys_value(sig, DCSYS.Sig.Type)
        sig_direction = get_dc_sys_value(sig, DCSYS.Sig.Sens)
        sig_with_imc = get_dc_sys_value(sig, DCSYS.Sig.D_Libre)
        res_dict[sig_name] = {"sig_name": sig_name, "sig_type": sig_type, "sig_direction": sig_direction,
                              "sig_with_imc": sig_with_imc}

        if sig_type in [SignalType.HEURTOIR, SignalType.PERMANENT_ARRET]:
            res_dict[sig_name]["status"] = "NA"
            res_dict[sig_name]["comments"] = "Not a Home Signal."
            continue

        (ivb_lim_seg, ivb_lim_x), ivb_lim_str = get_ivb_limit_of_a_signal(sig_name, sig)
        ivb_lim_track, ivb_lim_kp = from_seg_offset_to_track_kp(ivb_lim_seg, ivb_lim_x)
        res_dict[sig_name].update({"downstream_seg": ivb_lim_seg, "downstream_x": ivb_lim_x,
                                   "downstream_track": ivb_lim_track, "downstream_kp": ivb_lim_kp})

        if sig_name not in sig_zone_dict:
            res_dict[sig_name]["status"] = "KO"
            res_dict[sig_name]["comments"] = "The signal does not appear in Sig_Zone sheet."
            continue

        sig_zone = sig_zone_dict[sig_name]
        sig_apz_limit_seg_list, sig_apz_limit_x_list = get_dc_sys_values(
            sig_zone, DCSYS.Sig_Zone.PointsDEntreeZoneDApproche.Seg, DCSYS.Sig_Zone.PointsDEntreeZoneDApproche.X)
        res_dict[sig_name].update({"sig_apz_limit_seg_list": sig_apz_limit_seg_list,
                                   "sig_apz_limit_x_list": sig_apz_limit_x_list})

        sig_apz_limit_track_list, sig_apz_limit_kp_list = list(), list()
        for sig_apz_limit_seg, sig_apz_limit_x in zip(sig_apz_limit_seg_list, sig_apz_limit_x_list):
            sig_apz_limit_track, sig_apz_limit_kp = from_seg_offset_to_track_kp(sig_apz_limit_seg, sig_apz_limit_x)
            sig_apz_limit_track_list.append(sig_apz_limit_track)
            sig_apz_limit_kp_list.append(sig_apz_limit_kp)
        res_dict[sig_name].update({"sig_apz_limit_track_list": sig_apz_limit_track_list,
                                   "sig_apz_limit_kp_list": sig_apz_limit_kp_list})

        if sig_with_imc == YesOrNo.N and not sig_apz_limit_seg_list:
            res_dict[sig_name]["status"] = "NA"
            res_dict[sig_name]["comments"] = "Attribute [With_IMC] is set to 'N', there is no CBTC Approach Zone."
            continue
        if sig_with_imc == YesOrNo.N and sig_apz_limit_seg_list:
            res_dict[sig_name]["status"] = "KO"
            res_dict[sig_name]["comments"] = ("Attribute [With_IMC] is set to 'N' "
                                              "so there should no be any CBTC Approach Zone.")
            continue
        if sig_with_imc == YesOrNo.O and not sig_apz_limit_seg_list:
            res_dict[sig_name]["status"] = "KO"
            res_dict[sig_name]["comments"] = ("Attribute [With_IMC] is set to 'Y' "
                                              "so there should be a defined CBTC Approach Zone.")
            continue

        dist_list = list()
        for sig_apz_limit_seg, sig_apz_limit_x in zip(sig_apz_limit_seg_list, sig_apz_limit_x_list):
            # get dist upstream the signal
            dist = get_dist_downstream(ivb_lim_seg, ivb_lim_x, sig_apz_limit_seg, sig_apz_limit_x,
                                       downstream=sig_direction == Direction.DECROISSANT)
            dist_list.append(dist)
        res_dict[sig_name].update({"dist_list": dist_list})

    print_log_progress_bar(nb_sigs, nb_sigs, "verification of CBTC Approach Zone length finished", end=True)
    return res_dict
