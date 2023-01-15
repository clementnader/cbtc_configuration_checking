#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src import *


def compare_sheets():
    # print(compare_hf_data())
    # print(compare_lf_data())
    # print(compare_calib())
    # print(compare_tag())
    # print(compare_slope())
    # print(compare_zlpv())
    # compare_zc_area()
    # compare_zsm()
    return


def dc_par_add_on_param():
    # get_max_slope(in_cbtc=False)
    # get_block_min_length(in_cbtc=True)
    return


def dc_par_customer_data():
    # max_dist_local_tag_group(in_cbtc=True)
    # min_dist_between_two_last_signals_before_cbtc_territory_exit()  # TODO: to verify
    # min_distance_between_vsp_overlap(in_cbtc=True)
    # smallest_size_of_a_switch_block_heel(in_cbtc=True)
    return


def dc_par_constraints():
    # min_dist_between_platform_osp_and_end_of_next_platform(in_cbtc=True)
    return


def additional_verif():
    # min_dist_between_tags(in_cbtc=True)  # take a while to process for the whole territory
    # get_slope_at_plt(in_cbtc=True)
    return


def constraints():
    r_cdv_5()  # TODO
    # cf_zsm_cbtc_10(tolerance=.0)
    return


def main():
    # pretty_print_dict(get_sws_in_cbtc_ter(), max_lvl=0)
    # pretty_print_dict(get_plts_in_cbtc_ter(), max_lvl=0)

    # create_cctool_oo_schema_info_file()
    # create_fouling_points_file()

    constraints()

    additional_verif()

    dc_par_add_on_param()
    dc_par_customer_data()
    dc_par_constraints()

    # compare_sheets()
    return


if __name__ == "__main__":
    main()
