#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from src import *


def compare_dc_sys():
    # compare_all_sheets(start=None)
    # compare_sheet(DCSYS.Sig)

    # -- Generic Objects -- #
    # compare_sheet(DCSYS.Profil)
    # compare_sheet(DCSYS.ZLPV)
    # compare_sheet(DCSYS.Calib)
    # compare_sheet(DCSYS.Traction_Profiles)

    # compare_sheet(DCSYS.Seg)
    # compare_sheet(DCSYS.CDV)
    # compare_sheet(DCSYS.Troncon)
    # compare_sheet(DCSYS.ZSM_CBTC)
    # compare_sheet(DCSYS.PAS)
    # compare_sheet(DCSYS.Bal)
    # compare_sheet(DCSYS.Flux_Variant_BF)
    # compare_sheet(DCSYS.Flux_Variant_HF)
    return


def cc():
    # verification_of_the_md5_checksum()
    # get_mtor_ccte_ko()
    # patch_cc_mtor_ccte()
    # checksum_compare_parser()
    # check_diff_cc_param()
    # convert_cc_param()
    return


def additional_verif():
    # dc_tu_verification()  # v1.1
    # dc_tu_window()
    # min_dist_between_tags(in_cbtc=False)
    # pretty_print_dict({key: val for cnt, (key, val) in enumerate(min_dist_between_tags(in_cbtc=False).items())
    #                    if cnt < 30})  # can take a while to process for the whole territory
    # pretty_print_dict(get_slope_at_plt(in_cbtc=False))
    # pretty_print_dict(get_slope_at_overshoot_recovery_area(in_cbtc=False))
    return


def parameters_constraints():
    # min_dist_between_platform_osp_and_end_of_next_platform(in_cbtc=False)
    return


def dc_par_add_on_param():
    # get_max_slope(in_cbtc=False)
    # get_block_min_length(in_cbtc=False)
    # min_switch_area_length(in_cbtc=False)
    return


def route_and_overlap():
    # Create CSV files
    # parse_control_tables(
    #     CONTROL_TABLE_TYPE.route, use_csv_file=False,
    #     # verbose=True,
    #     # specific_page=10,
    #     # line_parts=(CONTROL_TABLE_LINE_PART.line,)
    # )
    # parse_control_tables(
    #     CONTROL_TABLE_TYPE.overlap, use_csv_file=False,
    #     # verbose=True,
    #     # specific_page=2,
    #     # line_parts=(CONTROL_TABLE_LINE_PART.line,)
    # )

    # Analyze DC_SYS with CSV files
    # check_route_control_tables(use_csv_file=True)
    # check_overlap_control_tables(use_csv_file=True)
    return


def dc_par_customer_data():
    # min_length_multiple_path(in_cbtc=False)  # trapezoid_length
    # min_distance_between_vsp_overlap(in_cbtc=False)
    # min_dist_between_two_last_signals_before_cbtc_territory_exit()  # TODO: to redo, we don't need to consider signals
    #                                                                    with a buffer just down the line
    # max_dist_local_tag_group(in_cbtc=False)
    # smallest_size_of_a_switch_block_heel(in_cbtc=False)
    return


def survey():
    # check_survey()  # v2.2
    # survey_window()
    # cctool_schema_window()
    return


def constraints():
    # check_offset_correctness()
    # check_upstream_and_downstream_ivb_of_all_signals()
    # check_cbtc_protecting_switch_area(do_print_warning=True)
    #
    # r_cdv_5(print_ok=True)  # TODO for r_cdv_5:
    #                             regarder pour prendre un param plutôt avec le hardware/hardware reference
    #                             plutôt que faire une diff avec le kit C11
    #                               plus: retourner un fichier de vérif pour pouvoir montrer les données;
    #                               vérifier l'histoire de tag_accurate_laying_uncertainty:
    #                                   ce n'est pas du tout marqué dans la contrainte donc peut-être à désactiver;
    #                               faire R_IVB_1 aussi.
    # r_dyntag_3()
    # cf_zsm_cbtc_10()
    # cf_dg_1()  # TODO: check correct Line Section
    # cf_dg_2()
    # r_mes_pas_itf_1(in_cbtc=False)  # TODO: find info to check if ZC receiving the Signal information
    #                                    PR_ASPECT, AP_CAN_RQ and IL_SET is correct in ZC Overlay
    #                                    il faut pas que le signal ait son VSP sur la limite du ZC, cf TSK
    # r_mes_pas_itf_3(in_cbtc=False)  # TODO: find a way to avoid raising KO if signal is at limit, cf KCR et TSK
    #                                    for Signal information X_RQ, STOP_ASSURE and CBTC_APZ,
    #                                       when checking ZC is correct in ZC Overlay
    #                                       (the standard rule is that both ZC shall send the info)
    #                                    ZC set by the tool for CBTC_OLZ and TRAIN_IN_BERTH
    #                                       -> it seems multiple ZC can do the job sometimes,
    #                                       and tool shall gives multiple ZC these times,
    #                                       re-work the way ZC is assigned.
    # r_tm_ats_itf_1(in_cbtc=False)
    # cf_signal_12(apz_with_tc=True)
    # r_zsm_3(apz_with_tc=True)
    # verif_calib_distance()
    # ixl_overlap_platform_related()
    # get_closest_vsp_in_rear()
    return


def main():
    # print(get_user_full_name())
    # print_named_colors()
    # print_all_colors()
    # test_rainbow()
    # test_moving_progress_bar()

    # get_walkways_track_kp_pos()
    # pretty_print_dict(get_track_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_sigs_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_maz_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_tags_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_switches_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_platforms_in_cbtc_ter(), max_lvl=0)

    # create_fouling_points_file()

    survey()

    route_and_overlap()

    constraints()

    additional_verif()

    dc_par_add_on_param()
    dc_par_customer_data()
    parameters_constraints()

    cc()

    compare_dc_sys()
    return


if __name__ == "__main__":
    skip_init = False
    # Initialization Commands
    if not skip_init:
        current_cctool_oo_version = get_ga_version_text()
        print_title(f"Working on {Color.cyan}{get_c_d470_version()}{Color.reset}\n"
                    f"with CCTool-OO Schema version:\n"
                    f"{Color.pale_green}{current_cctool_oo_version}{Color.reset}")
        regenerate_cctool_oo_schema_info()
        if get_ga_version_text() != current_cctool_oo_version:
            print_error(f"The compiled code is not in line with the current CCTool-OO Schema.")
            print(f"{Color.white}Relaunch the tool.{Color.reset}")
            sys.exit(1)
    # Main Functions
    main()
