#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_sub_dict_hf_general_data", "get_sub_dict_lf_general_data",
           "get_sub_dict_ixl_zc_itf", "get_sub_dict_zc_ixl_itf",
           "get_sub_dict_zc_ats_supervision"]


def get_sub_dict_hf_general_data(attribute: str):
    hf_gd_dict = load_sheet(DCSYS.Flux_Variant_HF)
    return {key: val for key, val in hf_gd_dict.items()
            if get_dc_sys_value(val, DCSYS.Flux_Variant_HF.ClasseObjet) == attribute}


def get_sub_dict_lf_general_data(attribute: str):
    lf_gd_dict = load_sheet(DCSYS.Flux_Variant_BF)
    return {key: val for key, val in lf_gd_dict.items()
            if get_dc_sys_value(val, DCSYS.Flux_Variant_BF.ClasseObjet) == attribute}


def get_sub_dict_ixl_zc_itf(attribute: str):
    itf_zc_ixl_dict = load_sheet(DCSYS.Flux_MES_PAS)
    return {key: val for key, val in itf_zc_ixl_dict.items()
            if get_dc_sys_value(val, DCSYS.Flux_MES_PAS.ClasseObjet) == attribute}


def get_sub_dict_zc_ixl_itf(attribute: str):
    itf_zc_ixl_dict = load_sheet(DCSYS.Flux_PAS_MES)
    return {key: val for key, val in itf_zc_ixl_dict.items()
            if get_dc_sys_value(val, DCSYS.Flux_PAS_MES.ClasseObjet) == attribute}


def get_sub_dict_zc_ats_supervision(attribute: str):
    zc_ats_supervision_dict = load_sheet(DCSYS.TM_PAS_ATS)
    return {key: val for key, val in zc_ats_supervision_dict.items()
            if get_dc_sys_value(val, DCSYS.TM_PAS_ATS.ClasseObjet) == attribute}
