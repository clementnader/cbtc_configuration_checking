#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *


__all__ = ["check_signal_with_overlap"]


def check_signal_with_overlap():
    print_bar(start="\n", end="")
    print_section_title(f"Verification of the correspondence between the signals flag [With overlap] "
                        f"and the list of overlaps.")
    sig_dict = load_sheet(DCSYS.Sig)
    ovl_dict = load_sheet(DCSYS.IXL_Overlap)

    dict_ovl_sigs = dict()
    for ovl_name, ovl in ovl_dict.items():
        corresponding_sig = get_dc_sys_value(ovl, DCSYS.IXL_Overlap.DestinationSignal)
        if corresponding_sig not in dict_ovl_sigs:
            dict_ovl_sigs[corresponding_sig] = list()
        dict_ovl_sigs[corresponding_sig].append(ovl_name)

    success = True
    for sig_name, sig in sig_dict.items():
        with_ovl = get_dc_sys_value(sig, DCSYS.Sig.Enc_Dep) == YesOrNo.O
        if with_ovl:
            if sig_name not in dict_ovl_sigs:
                success = False
                print_error(f"Signal {Color.yellow}{sig_name}{Color.reset} has flag [With overlap] set to 'Y', "
                            f"but there is no associated overlap in sheet IXL_Overlap.")
        else:
            if sig_name in dict_ovl_sigs:
                success = False
                print_error(f"Signal {Color.yellow}{sig_name}{Color.reset} has flag [With overlap] set to 'N', "
                            f"but there is associated overlap in sheet IXL_Overlap:\n"
                            f"{Color.beige}{dict_ovl_sigs[sig_name]}{Color.reset}")

    if success:
        print_log("No KO has been raised in the verification of the signals flag [With overlap].")
    print_bar(start="\n")
