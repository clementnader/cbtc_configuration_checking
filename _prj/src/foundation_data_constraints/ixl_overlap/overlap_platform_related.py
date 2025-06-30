#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_get_zones import get_zones_on_object, get_zones_intersecting_zone, get_objects_in_zone


__all__ = ["ixl_overlap_platform_related", "is_sig_plt_exit", "is_ivb_plt_related"]


def ixl_overlap_platform_related():
    print_section_title(f"Check platform exit signals definition...")
    plt_dict = load_sheet(DCSYS.Quai)
    for plt_name in plt_dict:
        _check_plt_exit_signal(plt_name)

    print_section_title(f"Check IXL_Overlap [Related Platform] attribute...")
    overlap_dict = load_sheet(DCSYS.IXL_Overlap)
    for ovl_name, ovl in overlap_dict.items():
        sig_name = get_dc_sys_value(ovl, DCSYS.IXL_Overlap.DestinationSignal)
        platform_related = (get_dc_sys_value(ovl, DCSYS.IXL_Overlap.PlatformRelated) == YesOrNo.O)
        shall_be_plt_rel, plt_name = is_sig_plt_exit(sig_name)
        if platform_related != shall_be_plt_rel:
            print_error(f"Overlap {Color.blue}{ovl_name}{Color.reset} related to signal "
                        f"{Color.yellow}{sig_name}{Color.reset} shall have "
                        f"flag {Color.white}[Platform Related]{Color.reset} set to "
                        f"{Color.cyan}'{'Y' if shall_be_plt_rel else 'N'}'{Color.reset}.")
            if shall_be_plt_rel:
                print(f"Indeed, signal {Color.yellow}{sig_name}{Color.reset} is exit of "
                      f"Platform {Color.mint_green}{plt_name}{Color.reset}.")


def is_sig_plt_exit(sig_name) -> tuple[bool, Optional[str]]:
    ivb_on_sig = get_zones_on_object(DCSYS.IVB, DCSYS.Sig, sig_name)
    if not ivb_on_sig:
        return False, None
    if len(ivb_on_sig) > 1:
        print_error(f"There are multiple IVBs on signal {sig_name}: {ivb_on_sig}.")
    ivb_name = ivb_on_sig[0]
    return is_ivb_plt_related(ivb_name)


def is_ivb_plt_related(ivb_name: str) -> tuple[bool, Optional[str]]:
    plt_on_ivb = get_zones_intersecting_zone(DCSYS.Quai, DCSYS.IVB, ivb_name)
    if not plt_on_ivb:
        return False, None
    if len(plt_on_ivb) > 1:
        print_error(f"There are multiple platforms on IVB {ivb_name}: {plt_on_ivb}.")
    plt_name = plt_on_ivb[0]
    return True, plt_name


def _check_plt_exit_signal(plt_name: str) -> None:
    ivb_on_plt = get_zones_intersecting_zone(DCSYS.IVB, DCSYS.Quai, plt_name)
    if not ivb_on_plt:
        print_error(f"There is no IVB covering platform {plt_name}.")
        return
    if len(ivb_on_plt) > 1:
        print_warning(f"There are multiple IVBs covering platform {Color.mint_green}{plt_name}{Color.reset}: "
                      f"{Color.default}{ivb_on_plt}{Color.reset}.")

    sigs_on_ivb = list()
    for ivb_name in ivb_on_plt:
        sigs_list = get_objects_in_zone(DCSYS.Sig, DCSYS.IVB, ivb_name)
        if sigs_list is None:
            continue
        sigs_on_ivb.extend([sig for sig in sigs_list if get_dc_sys_value(sig, DCSYS.Sig.Type) != SignalType.HEURTOIR])

    for direction in [Direction.CROISSANT, Direction.DECROISSANT]:
        sigs_in_direction = [sig for sig in sigs_on_ivb if get_dc_sys_value(sig, DCSYS.Sig.Sens) == direction]
        if not sigs_in_direction:
            print_error(f"There is no signal in {Color.orange}{direction}{Color.reset} covering IVB "
                        f"{Color.default}{ivb_on_plt}{Color.reset} covering platform "
                        f"{Color.mint_green}{plt_name}{Color.reset}.")
        if len(sigs_in_direction) > 1:
            print_error(f"There are multiple signals in {Color.orange}{direction}{Color.reset} covering IVB "
                        f"{Color.default}{ivb_on_plt}{Color.reset} covering platform "
                        f"{Color.mint_green}{plt_name}{Color.reset}: {Color.yellow}{sigs_in_direction}{Color.reset}.")
