#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def zc():
    # create_if_files()
    return


def cc():
    # check_diff_cc_param()
    # convert_ccparam()
    return


def additional_verif():
    # pretty_print_dict({key: val for cnt, (key, val) in enumerate(min_dist_between_tags(in_cbtc=True).items())
    #                    if cnt < 30})  # can take a while to process for the whole territory
    # get_slope_at_plt(in_cbtc=False)
    return


def parameters_constraints():
    # min_dist_between_platform_osp_and_end_of_next_platform(in_cbtc=False)
    return


def dc_par_customer_data():
    # min_length_multiple_path(in_cbtc=False)
    # min_distance_between_vsp_overlap(in_cbtc=False)
    # min_dist_between_two_last_signals_before_cbtc_territory_exit()  # TODO: to redo, we don't need to consider signals
    #                                                                    with a buffer just down the line
    # max_dist_local_tag_group(in_cbtc=False)
    # smallest_size_of_a_switch_block_heel(in_cbtc=False)
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


def survey():
    # check_survey()
    return


def constraints():
    # check_offset_correctness()

    # r_cdv_5(print_ok=False)  # TODO for r_cdv_5:
    #                             regarder pour prendre un param plutôt avec le hardware/hardware reference
    #                             plutôt que faire une diff avec le kit C11
    #                               plus: retourner un CSV pour pouvoir montrer les données;
    #                               vérifier l'histoire de tag_accurate_laying_uncertainty:
    #                                   ce n'est pas du tout marqué dans la contrainte donc peut-être à désactiver;
    #                               faire R_IVB_1 aussi.
    # r_dyntag_3()
    # cf_zsm_cbtc_10()
    # cf_dg_1()
    # cf_dg_2()
    # r_mes_pas_itf_1()
    # r_mes_pas_itf_3()
    # cf_signal_12()  # TODO: change the IVB limit upstream with the CDV (no need to use the control tables)
    # ixl_overlap_platform_related()
    return


def main():
    # print_all_colors()
    # show_colors()
    # test_rainbow()
    # test_moving_progress_bar()

    # get_mtor_ccte_ko()
    # patch_cc_mtor_ccte()
    # checksum_compare_parser()
    # convert_ccparam()

    # get_walkways_track_kp_pos()
    # pretty_print_dict(get_track_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_sigs_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_maz_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_tags_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_sws_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_plts_in_cbtc_ter(), max_lvl=0)

    # create_fouling_points_file()

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
    main()
