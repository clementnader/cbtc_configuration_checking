#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path import *


__all__ = ["cf_ivb_1_2", "cf_ivb_2"]


def cf_ivb_1_2():
    print_title("Verification of CF_IVB_1_2", color=Color.mint_green)
    no_ko = True
    ivb_list = get_objects_list(DCSYS.IVB)
    for ivb_name in ivb_list:
        other_ivb_on_ivb = get_objects_in_zone(DCSYS.IVB, DCSYS.IVB, ivb_name)
        if other_ivb_on_ivb != [ivb_name]:
            print_error(f"List of IVBs intersecting IVB {ivb_name} is not only composed on the IVB itself: "
                        f"{other_ivb_on_ivb}.")
            no_ko = False
    if no_ko:
        print_log("No KO found on the constraint.")


def cf_ivb_2():
    print_title("Verification of CF_IVB_2", color=Color.mint_green)
    no_ko = True
    ivb_list = get_objects_list(DCSYS.IVB)
    for ivb_name in ivb_list:
        cdv_on_ivb = get_objects_in_zone(DCSYS.CDV, DCSYS.IVB, ivb_name)
        if not cdv_on_ivb:
            print(f"No block found recovering IVB {ivb_name}.")
            no_ko = False
            continue
        if len(cdv_on_ivb) > 1:
            print_error(f"Multiple blocks found recovering IVB {ivb_name}: {cdv_on_ivb}")
            no_ko = False
        cdv_name = cdv_on_ivb[0]
        test, list_limits_not_in_big_zone = is_zone_completely_included_in_zone(DCSYS.IVB, ivb_name,
                                                                                DCSYS.CDV, cdv_name)
        if not test:
            print_error(f"IVB {ivb_name} is covered by block {cdv_on_ivb} but it is not completely included in it. "
                        f"These IVB limits are not inside the block: {list_limits_not_in_big_zone}")
            no_ko = False
    if no_ko:
        print_log("No KO found on the constraint.")
