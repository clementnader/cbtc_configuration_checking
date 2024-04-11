#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_sys_sheet_utils.cbtc_direction_zone_utils import get_cbtc_direction_zone_related_signals
from ..dc_sys_sheet_utils.signal_utils import get_ivb_limit_of_a_signal
from ..dc_par import *
from ..ixl_utils import get_distance_between_block_and_approach_zone


__all__ = ["r_zsm_3"]


def r_zsm_3(apz_with_tc: bool = False):
    # In nominal case the IXL approach zone locking for a dedicated signal is configured
    # to contain the first physical track circuit -> not always, see the corresponding ZC-IXL ICDD,
    # an option is implemented to choose if using the first TC or the first IVB.
    csv = ("Signal Name;Related ZSM;IXL Approach Zone;IVB Limit Downstream;;;;IVB Limit Upstream;;;;"
           "IXL APZ Distance;train_to_home_signal_max_dist;Automatic Status\n")
    csv += ";;;Seg;x;Track;KP;Seg;x;Track;KP;;;\n"
    print_title(f"Verification of R_ZSM_3", color=Color.mint_green)
    train_to_home_signal_max_dist = get_param_value("train_to_home_signal_max_dist")

    sig_dict = load_sheet(DCSYS.Sig)
    list_zsm_sigs = get_cbtc_direction_zone_related_signals()
    nb_sigs = len(list_zsm_sigs)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, (sig_name, related_zsm) in enumerate(list_zsm_sigs):
        print_log(f"\r{progress_bar(i, nb_sigs)} processing verification of R_ZSM_3 of {sig_name}...", end="")
        csv += f"{sig_name};{related_zsm};"

        (ivb_lim_seg, ivb_lim_x), ivb_lim_str = get_ivb_limit_of_a_signal(sig_name, sig_dict[sig_name])
        ivb_lim_track, ivb_lim_kp = from_seg_offset_to_kp(ivb_lim_seg, ivb_lim_x)

        apz_dist, corresponding_entrance, ivb_names = (
            get_distance_between_block_and_approach_zone(sig_name, ivb_lim_seg, ivb_lim_x, apz_with_tc))

        if apz_dist is None:
            csv += (f"{ivb_names};{ivb_lim_seg};{ivb_lim_x};{ivb_lim_track};{ivb_lim_kp};;;;;"
                    f";{train_to_home_signal_max_dist};{'KO'}\n")
            continue
        corresponding_entrance_track, corresponding_entrance_kp = from_seg_offset_to_kp(*corresponding_entrance)
        success = train_to_home_signal_max_dist <= apz_dist

        csv += (f"{ivb_names};{ivb_lim_seg};{ivb_lim_x};{ivb_lim_track};{ivb_lim_kp};"
                f"{corresponding_entrance[0]};{corresponding_entrance[1]};"
                f"{corresponding_entrance_track};{corresponding_entrance_kp};"
                f"{apz_dist};{train_to_home_signal_max_dist};{'OK' if success else 'KO'}\n")

    print_log(f"\r{progress_bar(nb_sigs, nb_sigs, end=True)} verification of R_ZSM_3 finished.\n")
    print(csv)
    return
