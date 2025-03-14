#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.msg_itf_utils import get_sub_dict_lf_general_data
from ...dc_sys_sheet_utils.platform_utils import get_atb_zone_related_to_plt
from .common_functions import *


__all__ = ["cf_dg_2"]


def cf_dg_2():
    # LF General Data
    print_title(f"Verification of CF_DG_2\nLF General Data", color=Color.mint_green)
    _cf_2_check_signal(get_sub_dict_lf_general_data(TypeClasseObjetVariantBF.SIGNAL))
    _cf_2_check_maz(get_sub_dict_lf_general_data(TypeClasseObjetVariantBF.ZAUM))
    _cf_2_check_platform(get_sub_dict_lf_general_data(TypeClasseObjetVariantBF.QUAI))
    _cf_2_check_nv_psr(get_sub_dict_lf_general_data(TypeClasseObjetVariantBF.NV_PSR))


# ------- Constraint 2 (LF) Sub Functions ------- #
def _cf_2_check_signal(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantBF.SIGNAL}...")
    obj_dict = load_sheet(DCSYS.Sig)
    success = True
    for obj_name, obj in obj_dict.items():
        is_not_buffer_or_pr = get_dc_sys_value(obj, DCSYS.Sig.Type) not in [SignalType.HEURTOIR,
                                                                            SignalType.PERMANENT_ARRET]
        if _check_obj_msgs(DCSYS.Sig, msg_dict, obj_name, is_not_buffer_or_pr,
                           "shall exist for all Signals except Permanently Red and Buffer",
                           TypeNomLogiqueVariantBF.FAILED_ZONE,
                           shall_be_vital=False,
                           is_hf=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _cf_2_check_maz(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantBF.ZAUM}...")
    obj_dict = load_sheet(DCSYS.Zaum)
    success = True
    for obj_name, obj in obj_dict.items():
        if _check_obj_msgs(DCSYS.Zaum, msg_dict, obj_name, True,
                           "shall exist for all MAZ",
                           TypeNomLogiqueVariantBF.PROTECTION_LEVEL,
                           shall_be_vital=True,
                           is_hf=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _cf_2_check_platform(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantBF.QUAI}...")
    obj_dict = load_sheet(DCSYS.Quai)
    success = True
    for obj_name, obj in obj_dict.items():
        if _check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, True,
                           "shall exist for all Platforms",
                           [TypeNomLogiqueVariantBF.SAFETY_RELATED_PLATFORM_HOLD_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.SAFETY_RELATED_PLATFORM_HOLD_REVERSE_DIR,
                            TypeNomLogiqueVariantBF.SAFETY_RELATED_PLATFORM_SKIP_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.SAFETY_RELATED_PLATFORM_SKIP_REVERSE_DIR],
                           shall_be_vital=True,
                           is_hf=False) is False:
            success = False

        if _check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, True,
                           "shall exist for all Platforms",
                           [TypeNomLogiqueVariantBF.T_ATP_MD_PROHIB_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.T_ATP_MD_PROHIB_REVERSE_DIR,
                            TypeNomLogiqueVariantBF.T_AD_PROHIB_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.T_AD_PROHIB_REVERSE_DIR],
                           shall_be_vital=False,
                           is_hf=False) is False:
            success = False
        if _check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, True,
                           "shall exist for all Platforms",
                           # [TypeNomLogiqueVariantBF.TRAIN_HOLD_NORMAL_DIR,
                           #  TypeNomLogiqueVariantBF.TRAIN_HOLD_REVERSE_DIR,
                           #  TypeNomLogiqueVariantBF.PLATFORM_SKIP_NORMAL_DIR,
                           #  TypeNomLogiqueVariantBF.PLATFORM_SKIP_REVERSE_DIR]
                           ["TRAIN_HOLD_NORMAL_DIR",
                            "TRAIN_HOLD_REVERSE_DIR",
                            "PLATFORM_SKIP_NORMAL_DIR",
                            "PLATFORM_SKIP_REVERSE_DIR"],
                           shall_be_vital=False,
                           is_hf=False) is False:
            success = False

        atb_zones = [atb[0] for atb in get_atb_zone_related_to_plt(obj_name)]
        origin_atb_mvt = True if atb_zones else False
        if _check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, origin_atb_mvt,
                           f"platform is origin of an ATB movement {atb_zones}",
                           [TypeNomLogiqueVariantBF.T_ATB_PROHIB_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.T_ATB_PROHIB_REVERSE_DIR],
                           shall_be_vital=False,
                           is_hf=False) is False:
            success = False

        train_ahead_departure = get_dc_sys_value(obj, DCSYS.Quai.WithTad) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, train_ahead_departure,
                           f"flag [With TAD] set to 'Y'",
                           TypeNomLogiqueVariantBF.TRAIN_AHEAD_DEPARTURE,
                           shall_be_vital=True,
                           is_hf=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _cf_2_check_nv_psr(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantBF.NV_PSR}...")
    obj_dict = load_sheet(DCSYS.NV_PSR)
    success = True
    for obj_name, obj in obj_dict.items():
        can_be_relaxed = get_dc_sys_value(obj, DCSYS.NV_PSR.WithRelaxation) == YesOrNo.O
        if _check_obj_msgs(DCSYS.NV_PSR, msg_dict, obj_name, can_be_relaxed,
                           "flag [With Relaxation] set to 'Y'",
                           TypeNomLogiqueVariantBF.NV_PSR_RELAXATION_CONDITION,
                           shall_be_vital=False,
                           is_hf=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")
