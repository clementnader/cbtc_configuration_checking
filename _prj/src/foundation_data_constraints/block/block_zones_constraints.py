#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path import *


__all__ = ["r_cdv_10"]


def r_cdv_10():
    print_title("Verification of R_CDV_10", color=Color.mint_green)
    no_ko = True
    block_dict = load_sheet(DCSYS.CDV)
    ivb_dict = load_sheet(DCSYS.IVB)
    for block_name, block_value in block_dict.items():
        list_zc = list()
        if get_dc_sys_value(block_value, DCSYS.CDV.DetectNcNrb) != YesOrNo.O:
            continue  # only for blocks with the [NRO NC Occupied Detection] attribute set to 'Y'

        ivb_intersecting_block = get_objects_in_zone(DCSYS.IVB, DCSYS.CDV, block_name)
        for ivb_name in ivb_intersecting_block:
            if "UsedByIxl" in get_class_attr_dict(DCSYS.IVB):
                if get_dc_sys_value(ivb_dict[ivb_name], DCSYS.IVB.UsedByIxl) != YesOrNo.O:
                    continue  # only when related IVB is used by IXL
            else:
                if get_dc_sys_value(ivb_dict[ivb_name], DCSYS.IVB.SentToIxl) != YesOrNo.O:
                    continue  # only when related IVB is sent to IXL

            corresponding_zc = get_dc_sys_value(ivb_dict[ivb_name], DCSYS.IVB.ZcName)
            list_zc.append((ivb_name, corresponding_zc))
        if list_zc and not all(zc[1] == list_zc[0][1] for zc in list_zc):  # if it is not the same ZC
            print_error(f"Block {block_name} has flag [NRO NC Occupied Detection] set to 'Y' and its IVB used by IXL "
                        f"are not all sent by a sole ZC: {list_zc}")
            no_ko = False

    if no_ko:
        print_log("No KO found on the constraint.")
