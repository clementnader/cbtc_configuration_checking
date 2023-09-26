#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


def ixl_overlap_platform_related():
    overlap_dict = load_sheet(DCSYS.IXL_Overlap)
    for ovl_name, ovl in overlap_dict.items():
        sig_name = get_dc_sys_value(ovl, DCSYS.IXL_Overlap.DestinationSignal)
        platform_related = (get_dc_sys_value(ovl, DCSYS.IXL_Overlap.PlatformRelated) == YesOrNo.O)
        should_be_plt_rel, plt_name, plt_limit = is_sig_downstream_a_plt(sig_name)
        if platform_related != should_be_plt_rel:
            print_error(f"Overlap {Color.blue}{ovl_name}{Color.reset} related to signal "
                        f"{Color.yellow}{sig_name}{Color.reset} should have "
                        f"flag {Color.white}[Platform Related]{Color.reset} set to "
                        f"{Color.cyan}'{'Y' if should_be_plt_rel else 'N'}'{Color.reset}.")
            if should_be_plt_rel:
                print(f"Indeed, signal {Color.yellow}{sig_name}{Color.reset} is downstream "
                      f"{Color.beige}{plt_limit}{Color.reset} of "
                      f"Platform {Color.mint_green}{plt_name}{Color.reset}.")


def is_sig_downstream_a_plt(sig_name):
    sig_dict = load_sheet(DCSYS.Sig)
    ref_sig = sig_dict[sig_name]
    sig_seg, other_sig_x = get_dc_sys_values(ref_sig, DCSYS.Sig.Seg, DCSYS.Sig.X)
    sig_direction = get_dc_sys_value(ref_sig, DCSYS.Sig.Sens)
    plt, other_sig = get_sigs_and_plt_upstream(sig_name, sig_seg, other_sig_x, sig_direction)

    if plt is None and other_sig is None:  # end of track or a switch upstream
        return False, None, None
    if plt is None and other_sig is not None:
        return False, None, None
    if plt is not None and other_sig is None:
        plt_name, plt_limit, plt_x = plt
        return True, plt_name, plt_limit

    if plt is not None and other_sig is not None:
        plt_name, plt_limit, plt_x = plt
        _, other_sig_x = other_sig
        if sig_direction == Direction.CROISSANT:
            if plt_x < other_sig_x:  # other_sig is closer to the ref_sig
                return False, None, None
            return True, plt_name, plt_limit  # plt is closer to the ref_sig
        else:
            if plt_x > other_sig_x:  # other_sig is closer to the ref_sig
                return False, None, None
            return True, plt_name, plt_limit  # plt is closer to the ref_sig


def get_sigs_and_plt_upstream(sig_name, sig_seg, sig_x, sig_direction):
    plt = plt_upstream_on_seg(sig_seg, sig_direction, ref_x=sig_x)
    sig = another_sig_upstream_on_seg(sig_name, sig_seg, sig_direction, ref_x=sig_x)

    seg = sig_seg
    downstream = False if sig_direction == Direction.CROISSANT else True
    while plt is None and sig is None:
        next_segs = get_linked_segs(seg, downstream)
        if not next_segs or len(next_segs) == 2:
            break
        seg = next_segs[0]
        plt = plt_upstream_on_seg(seg, sig_direction)
        sig = another_sig_upstream_on_seg(sig_name, seg, sig_direction)
    return plt, sig


def plt_upstream_on_seg(ref_seg, ref_direction: str, ref_x: float = None):
    plt_dict = load_sheet(DCSYS.Quai)
    plt_ends_on_seg = list()
    for plt_name, plt in plt_dict.items():
        limits = [(seg, x, f"Platform Limit {i}") for i, (seg, x) in (enumerate(get_dc_sys_zip_values(plt,
                  DCSYS.Quai.ExtremiteDuQuai.Seg, DCSYS.Quai.ExtremiteDuQuai.X), start=1))]
        if (ref_direction == Direction.CROISSANT) == is_platform_limit_1_upstream_limit_2(plt_name):
            upstream_limit = limits[0]  # Upstream Limit is Limit 1 in the direction of the signal
        else:
            upstream_limit = limits[1]
        test_seg, test_x, plt_limit = upstream_limit
        if test_seg == ref_seg:
            if ref_x is None or (ref_direction == Direction.CROISSANT and test_x <= ref_x) \
                    or (ref_direction == Direction.DECROISSANT and test_x >= ref_x):
                plt_ends_on_seg.append((plt_name, plt_limit, test_x))
    if not plt_ends_on_seg:
        return None
    return sorted(plt_ends_on_seg, key=lambda x: x[2], reverse=(ref_direction == Direction.CROISSANT))[0]


def another_sig_upstream_on_seg(ref_sig_name, ref_seg, ref_direction: str, ref_x: float = None):
    sig_dict = load_sheet(DCSYS.Sig)
    sigs_on_seg = list()
    for sig_name, sig in sig_dict.items():
        if sig_name == ref_sig_name:
            continue
        test_seg, test_x = get_dc_sys_values(sig, DCSYS.Sig.Seg, DCSYS.Sig.X)
        test_direction = get_dc_sys_value(sig, DCSYS.Sig.Sens)
        if test_direction == ref_direction and test_seg == ref_seg:
            if ref_x is None or (ref_direction == Direction.CROISSANT and test_x <= ref_x) \
                    or (ref_direction == Direction.DECROISSANT and test_x >= ref_x):
                sigs_on_seg.append((sig_name, test_x))
    if not sigs_on_seg:
        return None
    return sorted(sigs_on_seg, key=lambda x: x[1], reverse=(ref_direction == Direction.CROISSANT))[0]
# If we are in "CROISSANT", the closest sig upstream will be the one with the largest offset, the reverse otherwise.
