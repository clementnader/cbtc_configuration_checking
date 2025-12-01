#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.msg_itf_utils import get_sub_dict_ats_atc
from ...dc_sys_get_cbtc_territory import *


__all__ = ["ats_atc_sheet_verif"]


def ats_atc_sheet_verif(in_cbtc: bool = False):
    # ZC -> ATS Interface
    print_title(f"Verification of ATS_ATC sheet\nATS -> ATC Interface", color=Color.mint_green)
    _check_plt(get_sub_dict_ats_atc(TypeClasseObjetATSATC.QUAI), in_cbtc)
    _check_nv_psr(get_sub_dict_ats_atc(TypeClasseObjetATSATC.NV_PSR), in_cbtc)


# ------- Sub Functions ------- #
def _check_plt(plt_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetATSATC.QUAI}...")
    if not in_cbtc:
        plt_dict = load_sheet(DCSYS.Quai)
    else:
        plt_dict = get_objects_in_cbtc_ter(DCSYS.Quai)
    success = True
    for plt_name, plt in plt_dict.items():
        driving_modes = load_sheet(DCSYS.Driving_Modes)

        atp_md_mode = any(get_dc_sys_value(driving_mode, DCSYS.Driving_Modes.Group) == DrivingModesGroups.T_ATP_MD
                          for driving_mode in driving_modes)
        target_msg_types = [TypeNomLogiqueInfoATSCBTC.CMCC_INTERDIT_DIR_IMPAIR,
                            TypeNomLogiqueInfoATSCBTC.CMCC_INTERDIT_DIR_PAIR]
        if not check_object_msgs(DCSYS.Quai, plt_msg_dict, plt_name, atp_md_mode,
                                 "ATP_MD mode exists on the project",
                                 target_msg_types):
            success = False

        ad_mode = any(get_dc_sys_value(driving_mode, DCSYS.Driving_Modes.Group) == DrivingModesGroups.T_AD
                      for driving_mode in driving_modes)
        target_msg_types = [TypeNomLogiqueInfoATSCBTC.CPA_INTERDIT_DIR_IMPAIR,
                            TypeNomLogiqueInfoATSCBTC.CPA_INTERDIT_DIR_PAIR]
        if not check_object_msgs(DCSYS.Quai, plt_msg_dict, plt_name, ad_mode,
                                 "AD mode exists on the project",
                                 target_msg_types):
            success = False

        atb_mode = any(get_dc_sys_value(driving_mode, DCSYS.Driving_Modes.Group) == DrivingModesGroups.T_ATB
                       for driving_mode in driving_modes)
        target_msg_types = [TypeNomLogiqueInfoATSCBTC.CRA_INTERDIT_DIR_IMPAIR,
                            TypeNomLogiqueInfoATSCBTC.CRA_INTERDIT_DIR_PAIR]
        if not check_object_msgs(DCSYS.Quai, plt_msg_dict, plt_name, atb_mode,
                                 "ATB mode exists on the project",
                                 target_msg_types):
            success = False

        target_msg_types = ([TypeNomLogiqueInfoATSCBTC.HOLD_NORMAL_DIR,
                             TypeNomLogiqueInfoATSCBTC.SKIP_NORMAL_DIR,
                             TypeNomLogiqueInfoATSCBTC.HOLD_REVERSE_DIR,
                             TypeNomLogiqueInfoATSCBTC.SKIP_REVERSE_DIR]
                            if "SAFETY_RELATED_HOLD_NORMAL_DIR" not in get_class_attributes_dict(TypeNomLogiqueInfoATSCBTC)
                               or "SAFETY_RELATED_SKIP_NORMAL_DIR" not in get_class_attributes_dict(TypeNomLogiqueInfoATSCBTC)
                            else [TypeNomLogiqueInfoATSCBTC.SAFETY_RELATED_HOLD_NORMAL_DIR,
                                  TypeNomLogiqueInfoATSCBTC.SAFETY_RELATED_SKIP_NORMAL_DIR,
                                  TypeNomLogiqueInfoATSCBTC.SAFETY_RELATED_HOLD_REVERSE_DIR,
                                  TypeNomLogiqueInfoATSCBTC.SAFETY_RELATED_SKIP_REVERSE_DIR])
        if not check_object_msgs(DCSYS.Quai, plt_msg_dict, plt_name, True,
                                 "shall exist for all Platforms",
                                 target_msg_types):
            success = False
    if success:
        print_log(f"No KO.")


def _check_nv_psr(nv_psr_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetATSATC.NV_PSR}...")
    if not in_cbtc:
        nv_psr_dict = load_sheet(DCSYS.NV_PSR)
    else:
        nv_psr_dict = get_objects_in_cbtc_ter(DCSYS.NV_PSR)
    success = True
    for nv_psr_name, nv_psr in nv_psr_dict.items():
        can_be_relaxed = get_dc_sys_value(nv_psr, DCSYS.NV_PSR.WithRelaxation) == YesOrNo.O
        if not check_object_msgs(DCSYS.Quai, nv_psr_msg_dict, nv_psr_name, can_be_relaxed,
                                 "flag [With Relaxation] set to 'Y'",
                                 TypeNomLogiqueInfoATSCBTC.NV_PSR_RELAXATION_CONDITION):
            success = False
    if success:
        print_log(f"No KO.")


# ------- Common Sub Functions to test flows ------- #
def check_object_msgs(object_type, msg_dict: dict, object_name: str, condition: bool, condition_str: str,
                   target_msg_types: Union[str, list[str]]) -> bool:
    if not isinstance(target_msg_types, list):
        target_msg_types = [target_msg_types]
    object_type_str = get_sheet_name(object_type)

    associated_msgs = {msg_name: msg_info for msg_name, msg_info in msg_dict.items()
                       if get_dc_sys_value(msg_info, DCSYS.TM_PAS_ATS.NomObjet) == object_name
                       and get_dc_sys_value(msg_info, DCSYS.TM_PAS_ATS.NomLogiqueInfoAts) in target_msg_types}

    success = True
    if not condition:
        if associated_msgs:
            print_warning(f"Useless flow(s) to be removed as the condition for the message {Color.white}"
                          f"{condition_str.replace(Color.reset, Color.reset + Color.white)}{Color.reset} "
                          f"is not met for {object_type_str} {Color.blue}{object_name}{Color.reset}.")
            for msg_name, msg_info in associated_msgs.items():
                print(f"\t{Color.beige}{msg_name}{Color.reset}", end="\n\t\t")
                print(msg_info)
            success = False
        return success

    for target_msg_type in target_msg_types:
        associated_msg = {msg_name: msg_info for msg_name, msg_info in associated_msgs.items()
                          if get_dc_sys_value(msg_info, DCSYS.TM_PAS_ATS.NomLogiqueInfoAts) == target_msg_type}
        if not associated_msg:
            print_error(f"A flow of type {Color.yellow}{target_msg_type}{Color.reset} shall be defined for "
                        f"{object_type_str} {Color.blue}{object_name}{Color.reset} "
                        f"as the condition for the message {Color.white}"
                        f"{condition_str.replace(Color.reset, Color.reset + Color.white)}{Color.reset} is met.")
            success = False
            continue
    return success
