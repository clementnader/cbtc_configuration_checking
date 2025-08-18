#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.msg_itf_utils import get_sub_dict_hf_general_data
from ...dc_sys_sheet_utils.platform_utils import get_atb_zone_related_to_plt
from .common_functions import *


__all__ = ["cf_dg_1"]


def cf_dg_1():
    # HF General Data
    print_title(f"Verification of CF_DG_1\nHF General Data", color=Color.mint_green)
    _cf_1_check_switch(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.AIGUILLE))
    _cf_1_check_signal(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.SIGNAL))
    _cf_1_check_maz(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.ZAUM))
    _cf_1_check_platform(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.QUAI))
    _cf_1_check_flood_gate(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.FLOOD_GATE))
    if "BLOCK" in get_class_attr_dict(TypeClasseObjetVariantHF):
        _cf_1_check_block(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.BLOCK))
    if "ASR" in get_class_attr_dict(TypeClasseObjetVariantHF):
        _cf_1_check_asr(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.ASR))


# ------- Constraint 1 (HF) Sub Functions ------- #
def _cf_1_check_switch(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.AIGUILLE}...")
    obj_dict = load_sheet(DCSYS.Aig)
    success = True
    for obj_name, obj in obj_dict.items():
        if not check_obj_msgs(DCSYS.Aig, msg_dict, obj_name, True, "shall exist for all Switches",
                              [TypeNomLogiqueVariantHF.SW_RIGHT_C,
                               TypeNomLogiqueVariantHF.SW_LEFT_C], shall_be_vital=True):
            success = False
    if success:
        print_log(f"No KO.")


def _cf_1_check_signal(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.SIGNAL}...")
    obj_dict = load_sheet(DCSYS.Sig)
    success = True
    for obj_name, obj in obj_dict.items():
        is_not_buffer_or_pr = get_dc_sys_value(obj, DCSYS.Sig.Type) not in [SignalType.HEURTOIR,
                                                                            SignalType.PERMANENT_ARRET]

        if not check_obj_msgs(DCSYS.Sig, msg_dict, obj_name, is_not_buffer_or_pr, "shall exist for all Signals",
                              TypeNomLogiqueVariantHF.PR_ASPECT, shall_be_vital=False):
            success = False

        is_home_signal = get_dc_sys_value(obj, DCSYS.Sig.Type) == SignalType.MANOEUVRE
        if not check_obj_msgs(DCSYS.Sig, msg_dict, obj_name, is_home_signal, "shall exist for all Home Signals",
                              TypeNomLogiqueVariantHF.IL_SET, shall_be_vital=True):
            success = False

        func_stop = is_not_buffer_or_pr and (get_dc_sys_value(obj, DCSYS.Sig.WithFunc_Stop) == YesOrNo.O)
        if not check_obj_msgs(DCSYS.Sig, msg_dict, obj_name, func_stop, "flag [With Func Stop] set to 'Y'",
                              TypeNomLogiqueVariantHF.FUNC_STOP_RQ, shall_be_vital=False):
            success = False
    if success:
        print_log(f"No KO.")


def _cf_1_check_maz(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.ZAUM}...")
    obj_dict = load_sheet(DCSYS.Zaum)
    success = True
    for obj_name, obj in obj_dict.items():
        if not check_obj_msgs(DCSYS.Zaum, msg_dict, obj_name, True, "shall exist for all MAZ",
                              [TypeNomLogiqueVariantHF.MVT_AUTH,
                               TypeNomLogiqueVariantHF.TRACTION_PWR_REGEN_AUTH,
                               TypeNomLogiqueVariantHF.UTO_MVT_AUTH], shall_be_vital=True):
            success = False
        if ("AM_MVT_AUTH" in get_class_attr_dict(TypeNomLogiqueVariantHF)
                and check_obj_msgs(DCSYS.Zaum, msg_dict, obj_name, True, "shall exist for all MAZ",
                                   TypeNomLogiqueVariantHF.AM_MVT_AUTH, shall_be_vital=True) is False):
            success = False
    if success:
        print_log(f"No KO.")


def _cf_1_check_platform(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.QUAI}...")
    obj_dict = load_sheet(DCSYS.Quai)
    success = True
    for obj_name, obj in obj_dict.items():
        if not check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, True, "shall exist for all Platforms",
                              TypeNomLogiqueVariantHF.PLATFORM_ACCESS, shall_be_vital=False):
            success = False

        atb_zones = [atb[0] for atb in get_atb_zone_related_to_plt(obj_name)]
        origin_atb_mvt = True if atb_zones else False
        if not check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, origin_atb_mvt,
                              f"platform is origin of an ATB movement {atb_zones}",
                              [TypeNomLogiqueVariantHF.ATB_DEP, TypeNomLogiqueVariantHF.ATB_CAN_DEP],
                              shall_be_vital=True):
            success = False
    if success:
        print_log(f"No KO.")


def _cf_1_check_flood_gate(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.FLOOD_GATE}...")
    obj_dict = load_sheet(DCSYS.Flood_Gate)
    success = True
    for obj_name, obj in obj_dict.items():
        if not check_obj_msgs(DCSYS.Flood_Gate, msg_dict, obj_name, True, "shall exist for all Flood Gates",
                              TypeNomLogiqueVariantHF.OPEN_AND_LOCKED, shall_be_vital=True):
            success = False
    if success:
        print_log(f"No KO.")


def _cf_1_check_block(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.BLOCK}...")
    obj_dict = load_sheet(DCSYS.CDV)
    success = True
    for obj_name, obj in obj_dict.items():
        broken_rail_detection = get_dc_sys_value(obj, DCSYS.CDV.BrokenRailDetection) == YesOrNo.O
        if not check_obj_msgs(DCSYS.CDV, msg_dict, obj_name, broken_rail_detection,
                              "flag [Broken Rail Detection] set to 'Y'", TypeNomLogiqueVariantHF.BLOCK_MVT_AUTH,
                              shall_be_vital=True):
            success = False
    if success:
        print_log(f"No KO.")


def _cf_1_check_asr(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.ASR}...")
    obj_dict = load_sheet(DCSYS.ASR)
    success = True
    for obj_name, obj in obj_dict.items():
        if not check_obj_msgs(DCSYS.ASR, msg_dict, obj_name, True, "shall exist for all ASR",
                              TypeNomLogiqueVariantHF.ASR_NOT_APPLIED, shall_be_vital=True):
            success = False
    if success:
        print_log(f"No KO.")
