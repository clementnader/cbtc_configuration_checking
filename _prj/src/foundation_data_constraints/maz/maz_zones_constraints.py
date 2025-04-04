#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path import *
from ...dc_sys_sheet_utils.line_section_utils import *
from ...dc_sys_sheet_utils.zc_utils import *


__all__ = ["cf_zaum_1", "cf_zaum_11"]


def cf_zaum_1():
    print_title("Verification of CF_ZAUM_1", color=Color.mint_green)
    no_ko = True
    maz_list = get_objects_list(DCSYS.Zaum)
    for maz_name in maz_list:
        other_maz_on_maz = get_objects_in_zone(DCSYS.Zaum, DCSYS.Zaum, maz_name)
        if other_maz_on_maz != [maz_name]:
            print_error(f"List of MAZ intersecting MAZ {maz_name} is not only composed on the MAZ itself: "
                        f"{other_maz_on_maz}.")
            no_ko = False
    if no_ko:
        print_log("No KO found on the constraint.")


def cf_zaum_11():
    print_title("Verification of CF_ZAUM_11", color=Color.mint_green)
    no_ko = True
    maz_list = get_objects_list(DCSYS.Zaum)
    for maz_name in maz_list:
        dedicated_ls = get_line_section_of_obj(DCSYS.Zaum, maz_name)[0]
        zc_name = get_zc_managing_ls(dedicated_ls)
        test, list_limits_not_in_big_zone = is_zone_completely_included_in_zone(DCSYS.Zaum, maz_name,
                                                                                DCSYS.PAS, zc_name)
        if not test:
            print_error(f"MAZ {maz_name}, whose dedicated line section is {dedicated_ls}, "
                        f"which is managed by {zc_name}, is not completely inside {zc_name}. "
                        f"These MAZ limits are not inside the ZC: {list_limits_not_in_big_zone}")
            no_ko = False
    if no_ko:
        print_log("No KO found on the constraint.")
