#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path import *


__all__ = ["cc_cv_16", "cc_cv_18"]


def cc_cv_16():
    print_title("Verification of CC_CV_16", color=Color.mint_green)
    no_ko = True
    cv_list = get_objects_list(DCSYS.CV)
    for cv_name in cv_list:
        zsm_on_cv = get_objects_in_zone(DCSYS.ZSM_CBTC, DCSYS.CV, cv_name)
        if len(zsm_on_cv) > 1:
            print_error(f"Multiple CBTC Direction Zones are covering VB {cv_name}: "
                        f"{zsm_on_cv}.")
            no_ko = False
        if not zsm_on_cv:
            print(f"No CBTC Direction Zones is covering VB {cv_name}.")
            no_ko = False
    if no_ko:
        print_log("No KO found on the constraint.")


def cc_cv_18():
    print_title("Verification of CC_CV_18", color=Color.mint_green)
    no_ko = True
    cv_list = get_objects_list(DCSYS.CV)
    for cv_name in cv_list:
        sw_on_cv = get_objects_in_zone(DCSYS.Aig, DCSYS.CV, cv_name)
        cv_limits = len(get_object_position(DCSYS.CV, cv_name))
        if (sw_on_cv is not None) != (cv_limits == 3):
            print_error(f"VB {cv_name} number of limits is not coherent with the presence of switch on the VB:"
                        f"\n{sw_on_cv = }\n{cv_limits = }")
            no_ko = False
        if sw_on_cv is not None and len(sw_on_cv) != 1:
            print_error(f"Multiple switches on VB {cv_name}:\n{sw_on_cv = }")
            no_ko = False

        if (sw_on_cv is not None) or (cv_limits == 3):  # switch on VB
            sig_on_cv = get_objects_in_zone(DCSYS.Sig, DCSYS.CV, cv_name)
            if sig_on_cv:
                print_error(f"VB {cv_name} on switch {sw_on_cv} has a signal inside: {sig_on_cv}.")
                no_ko = False
    if no_ko:
        print_log("No KO found on the constraint.")
