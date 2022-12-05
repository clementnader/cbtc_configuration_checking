#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.dc_sys_pkg import *
from src.compare import *
from src.constraints import *
from src.dc_par.customer_data import *
from src.dc_par.constraints import *


def main():
    print()
    # print(compare_lf_data())
    # print(compare_calib())
    # print(compare_bal())
    # print(compare_slopes())
    # print(compare_zlpv())
    # compare_limits_zc_area()
    # compare_limits_zsm_cbtc()
    # cf_zsm_cbtc_10(tolerance=.0)
    # print(get_sw_dict(load_wb()))
    # min_distance_between_vsp_overlap(same_dir=True)
    # min_dist_between_two_last_signals_before_cbtc_territory_exit(same_dir=True)
    # max_dist_local_tag_group()
    # smallest_size_of_a_switch_block_heel()
    # min_dist_between_platform_osp_and_end_of_next_platform()
    get_seg_within_cbtc_ter()


if __name__ == "__main__":
    main()
