#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src import *


def compare_dc_sys():
    # print(compare_sheets("ls"))
    # compare_sheets("zsm")
    # compare_sheets("zc_area")
    # compare_sheets("zlpv")
    # compare_sheets("slope")
    # compare_sheets("tag")
    # compare_sheets("calib")
    # compare_sheets("lf_data")
    # compare_sheets("hf_data")
    return


def additional_verif():
    # pretty_print_dict(min_dist_between_tags(in_cbtc=True))  # take a while to process for the whole territory
    # get_slope_at_plt(in_cbtc=True)
    return


def dc_par_constraints():
    # min_dist_between_platform_osp_and_end_of_next_platform(in_cbtc=True)
    return


def dc_par_customer_data():
    # max_dist_local_tag_group(in_cbtc=False)
    # min_dist_between_two_last_signals_before_cbtc_territory_exit()  # TODO: to verify
    # min_distance_between_vsp_overlap(in_cbtc=True)
    # smallest_size_of_a_switch_block_heel(in_cbtc=True)
    # min_length_multiple_path(in_cbtc=False)
    return


def dc_par_add_on_param():
    # get_max_slope(in_cbtc=False)
    # get_block_min_length(in_cbtc=True)
    return


def constraints():
    # check_offset_correctness()
    # r_cdv_5()  # TODO regarder pour prendre un param plutôt avec le hardware/hardware reference plutôt que faire une diff avec le kit C11
    # cf_zsm_cbtc_10()
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


def main():
    # print(get_depolarized_segs())
    # print()
    # for i, val in get_all_segs_linked().items():
    #     print(i, ":", {key: sorted(val_i) for key, val_i in val.items()})
    # min_slope, max_slope = get_max_slope(in_cbtc=False)
    # abs_max_slope = max(abs(min_slope), abs(max_slope))
    # sub_variables = dict()
    # at_rollback_dist = get_at_rollback_dist(abs_max_slope, variables=sub_variables)
    # print_sub_variables(sub_variables)
    # print_final_value({"at_rollback_dist": f"{at_rollback_dist} m"})

    # print_all_colors()
    # show_colors()
    # test_rainbow()

    # checksum_compare_parser()
    # convert_ccparam()

    # pretty_print_dict(get_sigs_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_maz_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_tags_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_sws_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_plts_in_cbtc_ter(), max_lvl=0)

    # create_cctool_oo_schema_info_file()
    # create_fouling_points_file()

    route_and_overlap()

    constraints()

    additional_verif()

    dc_par_add_on_param()
    dc_par_customer_data()
    dc_par_constraints()

    compare_dc_sys()
    return


if __name__ == "__main__":
    main()
