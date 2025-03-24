#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from src import *


def compare_dc_sys():
    # compare_all_sheets(start=None)

    # -- Generic Objects -- #
    # compare_sheet(DCSYS.Profil)
    # compare_sheet(DCSYS.ZLPV)
    # compare_sheet(DCSYS.Calib)
    # compare_sheet(DCSYS.Traction_Profiles)

    # compare_sheet(DCSYS.Seg)
    # compare_sheet(DCSYS.Sig)
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
    # generate_cc_parameters_diff_reports()
    # check_diff_cc_param()
    # convert_cc_param()
    return


def zc():
    # check_pz_ze()
    # check_ze_impacte_fu()
    return


def additional_verif():
    # dc_tu_verification()  # v1.4
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
    # pretty_print_dict(get_block_min_length(in_cbtc=True))
    # pretty_print_dict(get_block_max_length(in_cbtc=False))
    # pretty_print_dict(min_switch_area_length(in_cbtc=False))
    return


def route_and_overlap():
    # GUI Window
    # control_tables_window()

    # Create CSV files
    # load_control_tables(
    #     CONTROL_TABLE_TYPE.route, use_csv_file=False,
    #     # supersede_input_file_number=1,
    #     # supersede_specific_pages=2,
    #     # debug=True,
    #     # print_pdf_code=True,
    # )
    # load_control_tables(
    #     CONTROL_TABLE_TYPE.overlap, use_csv_file=False,
    #     # supersede_input_file_number=1,
    #     # supersede_specific_pages=2,
    #     # debug=True,
    #     # print_pdf_code=True,
    # )

    # Analyze DC_SYS with CSV files
    # TODO: full rework of the association IXL name / DC_SYS name, take inspiration from the survey.
    # TODO: generate a result file and list at the end the missing info so that the alignment can be done manually.
    # check_route_control_tables(use_csv_file=True)
    # check_overlap_control_tables(use_csv_file=True)
    # verify_switches_along_the_routes()  # TODO
    # TODO: verif overlap: du signal jusqu'au VSP tous les IVB et aiguilles (+position) qu'on passe
    #  doivent être côté IXL et toutes les aiguilles (+position) doivent être côté CBTC
    # TODO: refaire les tests de correspondance sans dépendre de la variable PROJECT_NAME
    return


def dc_par_customer_data():
    # min_length_multiple_path(in_cbtc=False)  # trapezoid_length
    # min_dist_between_two_last_signals_before_cbtc_territory_exit()  # TODO: to redo, we don't need to consider signals
    #                                                                    with a buffer just down the line
    # smallest_size_of_a_switch_block_heel(in_cbtc=False)
    # max_dist_local_tag_group(in_cbtc=False)
    return


def survey():
    # check_survey()  # v2.8
    # survey_window()
    # cctool_oo_schema_window()
    return


def check_cdz_signals():
    cdz_dict = load_sheet(DCSYS.ZSM_CBTC)
    sig_dict = load_sheet(DCSYS.Sig)
    for cdz_name, cdz in cdz_dict.items():
        list_sigs = get_dc_sys_value(cdz, DCSYS.ZSM_CBTC.SignauxZsm.Sigman)
        for i, zsm_sig in enumerate(list_sigs, start=1):
            seg, x, direction = get_obj_position(DCSYS.Sig, zsm_sig)
            signal_ivb = get_dc_sys_value(sig_dict[zsm_sig], DCSYS.Sig.IvbJoint.UpstreamIvb)

            if is_point_in_zone(DCSYS.ZSM_CBTC, cdz_name, seg, x, direction):  # if signal in CDZ
                # TODO: we should check if there exist multiple signals on the CDZ in the same direction,
                #  and in that case probably that it should be the most in exit
                #  (greater offset for increasing direction).
                continue

            # TODO get first signal downstream ZSM in each direction

            if zsm_sig not in get_zones_intersecting_zone(DCSYS.ZSM_CBTC, DCSYS.IVB, signal_ivb):
                print_error(f"Related Signal {i} {Color.yellow}\"{zsm_sig}\"{Color.reset} is not inside CBTC Direction "
                            f"Zone {Color.beige}\"{cdz_name}\"{Color.reset}.")


def constraints():
    # check_dc_sys_zones_definition()
    # check_dc_sys_track_kp_definition()
    # get_zones_kp_limits(DCSYS.Protection_Zone)

    # check_upstream_and_downstream_ivb_of_all_signals()
    # check_cbtc_protecting_switch_area(do_print_warning=False)
    #
    # r_cdv_5(print_ok=True)  # TODO for r_cdv_5:
    #                             regarder pour prendre un param plutôt avec le hardware/hardware reference
    #                             plutôt que faire une diff avec le kit C11
    #                               plus: retourner un fichier de vérif pour pouvoir montrer les données;
    #                               vérifier l'histoire de tag_accurate_laying_uncertainty:
    #                                   ce n'est pas du tout marqué dans la contrainte donc peut-être à désactiver;
    #                               faire R_IVB_1 aussi.
    # check_psr_41_42()
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
    # ats_atc_sheet_verif(in_cbtc=False)  # TODO: Check if extra flows exist for object that does not exist per type,
    #                                           and if extra object type exists.
    # zcr_zc_sheet_verif(in_cbtc=False)
    # check_signal_with_overlap()

    # check_cbtc_sig_apz()
    # cf_signal_12(apz_with_tc=False)  # TODO: write IXL APZ info in Header sheet
    # r_zsm_3(apz_with_tc=False)
    # verif_calib_distance()
    # ixl_overlap_platform_related()
    # get_closest_vsp_in_rear()

    # get_par_worst_suspect_coupling_overrun_additionnal_dist()  # TODO ça marche comme l'outil de Damien mais à voir pour speeder ça (13mn sur KCR)
    return


def main():
    # print(get_user_full_name())
    # print_named_colors()
    # print_all_colors()
    # test_rainbow()
    # test_moving_progress_bar()

    # check_switch_flank_protection(in_cbtc=False)  # TODO
    # get_walkways_track_kp_pos()
    # pretty_print_dict(list(get_all_segs_in_cbtc_ter()), max_lvl=0)
    # pretty_print_dict(get_objects_in_cbtc_ter(DCSYS.Voie), max_lvl=0)
    # pretty_print_dict(get_objects_in_cbtc_ter(DCSYS.Profil), max_lvl=0)
    # pretty_print_dict(get_objects_in_cbtc_ter(DCSYS.Sig), max_lvl=0)
    # pretty_print_dict(get_objects_in_cbtc_ter(DCSYS.Zaum), max_lvl=0)
    # pretty_print_dict(get_objects_in_cbtc_ter(DCSYS.Bal), max_lvl=0)
    # pretty_print_dict(get_objects_in_cbtc_ter(DCSYS.Aig), max_lvl=0)
    # pretty_print_dict(get_objects_in_cbtc_ter(DCSYS.Quai), max_lvl=0)

    # init_fouling_points_file()  # create empty fouling points file with the list of switches from DC_SYS

    survey()

    route_and_overlap()

    constraints()

    additional_verif()

    dc_par_add_on_param()
    dc_par_customer_data()
    parameters_constraints()

    cc()
    zc()

    compare_dc_sys()
    return


if __name__ == "__main__":
    skip_init = False
    # skip_init = True

    # Initialization Commands
    if skip_init:
        print_title(f"Working on {Color.cyan}{get_current_version()}{Color.reset}\n"
                    f"{Color.orange}skipping the reloading of CCTool-OO Schema{Color.reset}")
    else:
        current_cctool_oo_version = get_ga_version_text()
        if len(sys.argv) > 1 and sys.argv[1] == "skip_regen":
            # we skip regeneration in case we just regenerated the info if the main Python instance
            pass
        else:  # default, regenerate CCTool-OO Schema info
            print()
            regenerate_cctool_oo_schema_info()

        if get_ga_version_text() != current_cctool_oo_version:
            # CCTool-OO Schema is not in line we relaunch the tool with a new python instance
            # to take into account the regenerated files.
            print_log(f"Launch another Python instance to take into account the CCTool-OO Schema.")
            python_exe = sys.executable
            launch_cmd(f"{python_exe} \"cbtc_configuration_checking.py\" skip_regen")
            sys.exit(0)

        print_title(f"Working on {Color.cyan}{get_current_version()}{Color.reset}\n"
                    f"with CCTool-OO Schema version: "
                    f"{Color.pale_green}{current_cctool_oo_version}{Color.reset}")

    # Main Functions
    main()
