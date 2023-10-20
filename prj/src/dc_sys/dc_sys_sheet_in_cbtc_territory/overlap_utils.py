#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ..load_database import *
from .signal_utils import *


__all__ = ["get_overlaps_in_cbtc_ter"]


def get_overlaps_in_cbtc_ter():
    ovl_dict = load_sheet(DCSYS.IXL_Overlap)
    sig_in_cbtc = get_sigs_in_cbtc_ter()

    within_cbtc_ovl_dict = dict()
    for ovl_name, ovl_value in ovl_dict.items():
        related_sig = get_dc_sys_value(ovl_value, DCSYS.IXL_Overlap.DestinationSignal)
        if related_sig in sig_in_cbtc:
            within_cbtc_ovl_dict[ovl_name] = ovl_value
    return within_cbtc_ovl_dict
