#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...dc_bop import *
from ...cctool_oo_schema import *
from ..load_database import *
from .signal_utils import *


__all__ = ["get_overlaps_in_cbtc_ter", "get_overlap"]


def get_overlaps_in_cbtc_ter():
    ovl_dict = load_sheet(DCSYS.IXL_Overlap)
    sig_in_cbtc = get_sigs_in_cbtc_ter()

    within_cbtc_ovl_dict = dict()
    for ovl_name, ovl_value in ovl_dict.items():
        related_sig = get_dc_sys_value(ovl_value, DCSYS.IXL_Overlap.DestinationSignal)
        if related_sig in sig_in_cbtc:
            within_cbtc_ovl_dict[ovl_name] = ovl_value
    return within_cbtc_ovl_dict


def get_overlap():
    overlap_dict = load_sheet(DCSYS.IXL_Overlap)
    for ovl_name, ovl_value in overlap_dict.items():
        overlap_dict[ovl_name]["Overlap Path Switch"] = _get_overlap_switch(ovl_value)
    return overlap_dict


def _get_overlap_switch(ovl_value: dict[str, str]):
    sw_list = list()
    for sw_name, sw_pos in get_dc_sys_zip_values(ovl_value, DCSYS.IXL_Overlap.Aiguille.Nom,
                                                 DCSYS.IXL_Overlap.Aiguille.Position):
        if sw_name is not None:
            sw_pos = convert_switch_pos_to_ixl(sw_name, sw_pos)
            sw_list.append(sw_name.upper() + sw_pos.upper())
    return sw_list
