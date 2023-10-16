#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


def cf_dg_1():
    # HF General Data
    print_title(f"Verification of CF_DG_1\nHF General Data", color=Color.mint_green)
    _cf_1_check_switch(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.AIGUILLE))
    _cf_1_check_signal(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.SIGNAL))
    _cf_1_check_maz(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.ZAUM))
    _cf_1_check_platform(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.QUAI))
    _cf_1_check_flood_gate(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.FLOOD_GATE))
    _cf_1_check_block(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.BLOCK))
    _cf_1_check_asr(get_sub_dict_hf_general_data(TypeClasseObjetVariantHF.ASR))


def cf_dg_2():
    # LF General Data
    print_title(f"Verification of CF_DG_2\nLF General Data", color=Color.mint_green)
    _cf_2_check_signal(get_sub_dict_lf_general_data(TypeClasseObjetVariantBF.SIGNAL))
    _cf_2_check_maz(get_sub_dict_lf_general_data(TypeClasseObjetVariantBF.ZAUM))
    _cf_2_check_platform(get_sub_dict_lf_general_data(TypeClasseObjetVariantBF.QUAI))
    _cf_2_check_nv_psr(get_sub_dict_lf_general_data(TypeClasseObjetVariantBF.NV_PSR))


# ------- Constraint 1 (HF) Sub Functions ------- #
def _cf_1_check_switch(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.AIGUILLE}...")
    obj_dict = load_sheet(DCSYS.Aig)
    success = True
    for obj_name, obj in obj_dict.items():
        if _check_obj_msgs(DCSYS.Aig, msg_dict, obj_name, True,
                           "should exist for all Switches",
                           [TypeNomLogiqueVariantHF.SW_RIGHT_C,
                            TypeNomLogiqueVariantHF.SW_LEFT_C]) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _cf_1_check_signal(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.SIGNAL}...")
    obj_dict = load_sheet(DCSYS.Sig)
    success = True
    for obj_name, obj in obj_dict.items():
        is_not_buffer_or_pr = get_dc_sys_value(obj, DCSYS.Sig.Type) not in [SignalType.HEURTOIR,
                                                                            SignalType.PERMANENT_ARRET]

        if _check_obj_msgs(DCSYS.Sig, msg_dict, obj_name, is_not_buffer_or_pr,
                           "should exist for all Signals",
                           TypeNomLogiqueVariantHF.PR_ASPECT) is False:
            success = False

        is_home_signal = get_dc_sys_value(obj, DCSYS.Sig.Type) == SignalType.MANOEUVRE
        if _check_obj_msgs(DCSYS.Sig, msg_dict, obj_name, is_home_signal,
                           "should exist for all Home Signals",
                           TypeNomLogiqueVariantHF.IL_SET) is False:
            success = False

        func_stop = is_not_buffer_or_pr and (get_dc_sys_value(obj, DCSYS.Sig.WithFunc_Stop) == YesOrNo.O)
        if _check_obj_msgs(DCSYS.Sig, msg_dict, obj_name, func_stop,
                           "flag [With Func Stop] set to 'Y'",
                           TypeNomLogiqueVariantHF.FUNC_STOP_RQ) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _cf_1_check_maz(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.ZAUM}...")
    obj_dict = load_sheet(DCSYS.Zaum)
    success = True
    for obj_name, obj in obj_dict.items():
        if _check_obj_msgs(DCSYS.Zaum, msg_dict, obj_name, True,
                           "should exist for all MAZ",
                           [TypeNomLogiqueVariantHF.MVT_AUTH,
                            TypeNomLogiqueVariantHF.TRACTION_PWR_REGEN_AUTH,
                            TypeNomLogiqueVariantHF.UTO_MVT_AUTH,
                            TypeNomLogiqueVariantHF.AM_MVT_AUTH]) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _cf_1_check_platform(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.QUAI}...")
    obj_dict = load_sheet(DCSYS.Quai)
    success = True
    for obj_name, obj in obj_dict.items():
        if _check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, True,
                           "should exist for all Platforms",
                           TypeNomLogiqueVariantHF.PLATFORM_ACCESS) is False:
            success = False

        atb_zones = [atb[0] for atb in get_atb_zone_related_to_plt(obj_name)]
        origin_atb_mvt = True if atb_zones else False
        if _check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, origin_atb_mvt,
                           f"platform is origin of an ATB movement {atb_zones}",
                           [TypeNomLogiqueVariantHF.ATB_DEP,
                            TypeNomLogiqueVariantHF.ATB_CAN_DEP]) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _cf_1_check_flood_gate(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.FLOOD_GATE}...")
    obj_dict = load_sheet(DCSYS.Flood_Gate)
    success = True
    for obj_name, obj in obj_dict.items():
        if _check_obj_msgs(DCSYS.Flood_Gate, msg_dict, obj_name, True,
                           "should exist for all Flood Gates",
                           TypeNomLogiqueVariantHF.OPEN_AND_LOCKED) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _cf_1_check_block(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.BLOCK}...")
    obj_dict = load_sheet(DCSYS.CDV)
    success = True
    for obj_name, obj in obj_dict.items():
        broken_rail_detection = get_dc_sys_value(obj, DCSYS.CDV.BrokenRailDetection) == YesOrNo.O
        if _check_obj_msgs(DCSYS.CDV, msg_dict, obj_name, broken_rail_detection,
                           "flag [Broken Rail Detection] set to 'Y'",
                           TypeNomLogiqueVariantHF.BLOCK_MVT_AUTH) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _cf_1_check_asr(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantHF.ASR}...")
    obj_dict = load_sheet(DCSYS.ASR)
    success = True
    for obj_name, obj in obj_dict.items():
        if _check_obj_msgs(DCSYS.ASR, msg_dict, obj_name, True,
                           "should exist for all ASR",
                           TypeNomLogiqueVariantHF.BLOCK_MVT_AUTH) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


# ------- Constraint 2 (LF) Sub Functions ------- #
def _cf_2_check_signal(msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetVariantBF.SIGNAL}...")
    obj_dict = load_sheet(DCSYS.Sig)
    success = True
    for obj_name, obj in obj_dict.items():
        is_not_buffer_or_pr = get_dc_sys_value(obj, DCSYS.Sig.Type) not in [SignalType.HEURTOIR,
                                                                            SignalType.PERMANENT_ARRET]
        if _check_obj_msgs(DCSYS.Sig, msg_dict, obj_name, is_not_buffer_or_pr,
                           "signal is related at least to a CBTC Equipment -> ? test that it exists for all Signals"
                           "except Permanent Red and Buffer",
                           TypeNomLogiqueVariantBF.FAILED_ZONE,
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
                           "should exist for all MAZ",
                           TypeNomLogiqueVariantBF.PROTECTION_LEVEL,
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
                           "should exist for all Platforms",
                           [TypeNomLogiqueVariantBF.T_ATP_MD_PROHIB_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.T_ATP_MD_PROHIB_REVERSE_DIR,
                            TypeNomLogiqueVariantBF.SAFETY_RELATED_PLATFORM_HOLD_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.SAFETY_RELATED_PLATFORM_HOLD_REVERSE_DIR,
                            TypeNomLogiqueVariantBF.SAFETY_RELATED_PLATFORM_SKIP_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.SAFETY_RELATED_PLATFORM_SKIP_REVERSE_DIR,
                            TypeNomLogiqueVariantBF.T_AD_PROHIB_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.T_AD_PROHIB_REVERSE_DIR,
                            TypeNomLogiqueVariantBF.TRAIN_HOLD_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.TRAIN_HOLD_REVERSE_DIR,
                            TypeNomLogiqueVariantBF.PLATFORM_SKIP_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.PLATFORM_SKIP_REVERSE_DIR],
                           is_hf=False) is False:
            success = False

        atb_zones = [atb[0] for atb in get_atb_zone_related_to_plt(obj_name)]
        origin_atb_mvt = True if atb_zones else False
        if _check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, origin_atb_mvt,
                           f"platform is origin of an ATB movement {atb_zones}",
                           [TypeNomLogiqueVariantBF.T_ATB_PROHIB_NORMAL_DIR,
                            TypeNomLogiqueVariantBF.T_ATB_PROHIB_REVERSE_DIR]) is False:
            success = False

        train_ahead_departure = get_dc_sys_value(obj, DCSYS.Quai.WithTad) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Quai, msg_dict, obj_name, train_ahead_departure,
                           f"flag [With TAD] set to 'Y'",
                           TypeNomLogiqueVariantBF.TRAIN_AHEAD_DEPARTURE) is False:
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
                           is_hf=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


# ------- Common Sub Functions to test flows ------- #
def _check_obj_msgs(obj_type, msg_dict: dict, obj_name: str, condition: bool, condition_str: str,
                    target_msg_types: Union[str, list[str]],  # should_be_vital: bool,
                    is_hf: bool = True):
    if not isinstance(target_msg_types, list):
        target_msg_types = [target_msg_types]
    obj_type_str = get_sh_name(obj_type)

    obj_class = DCSYS.Flux_Variant_HF if is_hf else DCSYS.Flux_Variant_BF

    associated_msgs = {msg_name: msg_info for msg_name, msg_info in msg_dict.items()
                       if get_dc_sys_value(msg_info, obj_class.NomObjet) == obj_name
                       and get_dc_sys_value(msg_info, obj_class.NomLogiqueInfo) in target_msg_types}

    success = True
    if not condition:
        if associated_msgs:
            print_warning(f"Useless flow(s) to be removed as the condition {Color.white}"
                          f"{condition_str.replace(Color.reset, Color.reset + Color.white)}{Color.reset} "
                          f"is not met for {obj_type_str} {Color.blue}{obj_name}{Color.reset}:")
            for msg_name, msg_info in associated_msgs.items():
                print(f"\t{Color.beige}{msg_name}{Color.reset}", end="\n\t\t")
                print(msg_info)
            success = False
        return success

    for target_msg_type in target_msg_types:
        associated_msg = {msg_name: msg_info for msg_name, msg_info in associated_msgs.items()
                          if get_dc_sys_value(msg_info, obj_class.NomLogiqueInfo) == target_msg_type}
        if not associated_msg:
            print_error(f"A flow of type {Color.yellow}{target_msg_type}{Color.reset} should be defined for "
                        f"{obj_type_str} {Color.blue}{obj_name}{Color.reset} "
                        f"as the condition {Color.white}{condition_str.replace(Color.reset, Color.reset + Color.white)}"
                        f"{Color.reset} is met.")
            success = False
            continue
        # The constraint does not specify if the message should be vital or not.
        # for associated_msg_name, associated_msg_info in associated_msg.items():
        #     is_msg_vital = (get_dc_sys_value(associated_msg_info, obj_class.TypeFoncSecu)
        #                     == VitalOrNotType.SECU)
        #     if is_msg_vital != should_be_vital:
        #         print_error(f"Flow {Color.beige}{associated_msg_name}{Color.reset} "
        #                     f"for {obj_type_str} {Color.blue}{obj_name}{Color.reset} "
        #                     f"of type {Color.yellow}{target_msg_type}{Color.reset} "
        #                     f"should be of type {Color.orange}"
        #                     f"{VitalOrNotType.SECU if should_be_vital else VitalOrNotType.FONC}{Color.reset} "
        #                     f"instead of {VitalOrNotType.SECU if is_msg_vital else VitalOrNotType.FONC}\n"
        #                     f"(the condition {Color.white}"
        #                     f"{condition_str.replace(Color.reset, Color.reset + Color.white)}{Color.reset} is met):",
        #                     end="\n\t\t")
        #         print(associated_msg_info)
        #         success = False
    return success
