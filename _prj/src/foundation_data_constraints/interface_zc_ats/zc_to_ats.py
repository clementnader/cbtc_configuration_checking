#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.msg_itf_utils import get_sub_dict_zc_ats_supervision
from ...dc_sys_sheet_utils.zc_utils import *
from ...dc_sys_get_cbtc_territory import *


__all__ = ["r_tm_ats_itf_1"]


def r_tm_ats_itf_1(in_cbtc: bool = False):
    # ZC -> ATS Interface
    print_title(f"Verification of R_TM_ATS_ITF_1\nZC -> ATS Interface", color=Color.mint_green)
    _check_block(get_sub_dict_zc_ats_supervision(TypeClasseObjetPASATS.CDV), in_cbtc)
    _check_dd(get_sub_dict_zc_ats_supervision(TypeClasseObjetPASATS.DP), in_cbtc)
    _check_plt(get_sub_dict_zc_ats_supervision(TypeClasseObjetPASATS.QUAI), in_cbtc)
    _check_ivb(get_sub_dict_zc_ats_supervision(TypeClasseObjetPASATS.IVB), in_cbtc)
    _check_switch(get_sub_dict_zc_ats_supervision("AIGUILLE"), in_cbtc)  # TypeClasseObjetPASATS.AIGUILLE
    _check_maz(get_sub_dict_zc_ats_supervision(TypeClasseObjetPASATS.ZAUM), in_cbtc)


# ------- Sub Functions ------- #
def _check_block(block_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASATS.CDV}...")
    if not in_cbtc:
        block_dict = load_sheet(DCSYS.CDV)
    else:
        block_dict = get_objects_in_cbtc_ter(DCSYS.CDV)
    success = True
    for block_name, block in block_dict.items():
        if not check_object_msgs(DCSYS.CDV, block_msg_dict, block_name, True,
                              "shall exist for all CDV",
                              TypeNomLogiqueInfoPASATS.ETAT_CDV,
                              only_one_zc=False):
            success = False

        block_brs = get_dc_sys_value(block, DCSYS.CDV.BrokenRailDetection) == YesOrNo.O
        if not check_object_msgs(DCSYS.CDV, block_msg_dict, block_name, block_brs,
                              "flag [Broken Rail Detection] set to 'Y'",
                              [TypeNomLogiqueInfoPASATS.BRS_STATE, TypeNomLogiqueInfoPASATS.BRSO_STATE],
                              only_one_zc=False):
            success = False
    if success:
        print_log(f"No KO.")


def _check_dd(dd_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASATS.DP}...")
    if not in_cbtc:
        dd_dict = load_sheet(DCSYS.DP)
    else:
        dd_dict = get_objects_in_cbtc_ter(DCSYS.DP)
    success = True
    for dd_name, dd in dd_dict.items():
        if not check_object_msgs(DCSYS.CDV, dd_msg_dict, dd_name, True,
                              "shall exist for all Discrete Detectors",
                              TypeNomLogiqueInfoPASATS.ETAT_DP,
                              only_one_zc=False):
            success = False
    if success:
        print_log(f"No KO.")


def _check_plt(plt_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASATS.QUAI}...")
    if not in_cbtc:
        plt_dict = load_sheet(DCSYS.Quai)
    else:
        plt_dict = get_objects_in_cbtc_ter(DCSYS.Quai)
    success = True
    for plt_name, plt in plt_dict.items():
        target_msg_types = ([TypeNomLogiqueInfoPASATS.HOLD_NORMAL_DIR,
                             TypeNomLogiqueInfoPASATS.SKIP_NORMAL_DIR,
                             TypeNomLogiqueInfoPASATS.SAFETY_RELATED_HOLD_NORMAL_DIR,
                             TypeNomLogiqueInfoPASATS.SAFETY_RELATED_SKIP_NORMAL_DIR]
                            if "REGULATION_HOLD_NORMAL_DIR" not in get_class_attributes_dict(TypeNomLogiqueInfoPASATS)
                               or "REGULATION_SKIP_NORMAL_DIR" not in get_class_attributes_dict(TypeNomLogiqueInfoPASATS)
                            else [TypeNomLogiqueInfoPASATS.REGULATION_HOLD_NORMAL_DIR,
                                  TypeNomLogiqueInfoPASATS.REGULATION_SKIP_NORMAL_DIR,
                                  TypeNomLogiqueInfoPASATS.SAFETY_RELATED_HOLD_NORMAL_DIR,
                                  TypeNomLogiqueInfoPASATS.SAFETY_RELATED_SKIP_NORMAL_DIR])
        if not check_object_msgs(DCSYS.Quai, plt_msg_dict, plt_name, True,
                              "shall exist for all Platforms",
                              target_msg_types,
                              only_one_zc=True, plt_end="normal"):
            success = False

        target_msg_types = ([TypeNomLogiqueInfoPASATS.HOLD_REVERSE_DIR,
                             TypeNomLogiqueInfoPASATS.SKIP_REVERSE_DIR,
                             TypeNomLogiqueInfoPASATS.SAFETY_RELATED_HOLD_REVERSE_DIR,
                             TypeNomLogiqueInfoPASATS.SAFETY_RELATED_SKIP_REVERSE_DIR]
                            if "REGULATION_HOLD_NORMAL_DIR" not in get_class_attributes_dict(TypeNomLogiqueInfoPASATS)
                               or "REGULATION_SKIP_NORMAL_DIR" not in get_class_attributes_dict(TypeNomLogiqueInfoPASATS)
                            else [TypeNomLogiqueInfoPASATS.REGULATION_HOLD_REVERSE_DIR,
                                  TypeNomLogiqueInfoPASATS.REGULATION_SKIP_REVERSE_DIR,
                                  TypeNomLogiqueInfoPASATS.SAFETY_RELATED_HOLD_REVERSE_DIR,
                                  TypeNomLogiqueInfoPASATS.SAFETY_RELATED_SKIP_REVERSE_DIR])
        if not check_object_msgs(DCSYS.Quai, plt_msg_dict, plt_name, True,
                              "shall exist for all Platforms",
                              target_msg_types,
                              only_one_zc=True, plt_end="reverse"):
            success = False
    if success:
        print_log(f"No KO.")


def _check_ivb(ivb_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASATS.IVB}...")
    if not in_cbtc:
        ivb_dict = load_sheet(DCSYS.IVB)
    else:
        ivb_dict = get_objects_in_cbtc_ter(DCSYS.IVB)
    success = True
    for ivb_name, ivb in ivb_dict.items():
        if not check_object_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, True,
                              "shall exist for all IVB",
                              TypeNomLogiqueInfoPASATS.PREVENTS_EID,
                              only_one_zc=True):
            success = False
    if success:
        print_log(f"No KO.")


def _check_switch(sw_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking AIGUILLE...")
    if not in_cbtc:
        sw_dict = load_sheet(DCSYS.Aig)
    else:
        sw_dict = get_objects_in_cbtc_ter(DCSYS.Aig)
    success = True
    for sw_name, sw in sw_dict.items():
        if not check_object_msgs(DCSYS.Aig, sw_msg_dict, sw_name, True,
                              "shall exist for switches",
                              TypeNomLogiqueInfoPASATS.PREVENTS_EID,
                              only_one_zc=True):
            success = False
    if success:
        print_log(f"No KO.")


def _check_maz(maz_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASATS.ZAUM}...")
    if not in_cbtc:
        maz_dict = load_sheet(DCSYS.Zaum)
    else:
        maz_dict = get_objects_in_cbtc_ter(DCSYS.Zaum)
    success = True
    for maz_name, maz in maz_dict.items():
        target_msg_types = ([TypeNomLogiqueInfoPASATS.MVT_AUTH,
                             TypeNomLogiqueInfoPASATS.UTO_MVT_AUTH]
                            if "AM_MVT_AUTH" not in get_class_attributes_dict(TypeNomLogiqueInfoPASATS)
                            else [TypeNomLogiqueInfoPASATS.MVT_AUTH,
                                  TypeNomLogiqueInfoPASATS.UTO_MVT_AUTH,
                                  TypeNomLogiqueInfoPASATS.AM_MVT_AUTH])
        if not check_object_msgs(DCSYS.Zaum, maz_msg_dict, maz_name, True,
                              "shall exist for MAZ",
                              target_msg_types,
                              only_one_zc=True):
            success = False
    if success:
        print_log(f"No KO.")


# ------- Common Sub Functions to test flows ------- #
def check_object_msgs(object_type, msg_dict: dict, object_name: str, condition: bool, condition_str: str,
                   target_msg_types: Union[str, list[str]], only_one_zc: bool, plt_end: str = None) -> bool:
    if not isinstance(target_msg_types, list):
        target_msg_types = [target_msg_types]
    object_type_str = get_sheet_name(object_type)

    associated_msgs = {msg_name: msg_info for msg_name, msg_info in msg_dict.items()
                       if get_dc_sys_value(msg_info, DCSYS.TM_PAS_ATS.NomObjet) == object_name
                       and get_dc_sys_value(msg_info, DCSYS.TM_PAS_ATS.NomLogiqueInfoAts) in target_msg_types}

    success = True
    if not condition:
        if associated_msgs:
            for target_msg_type in target_msg_types:
                associated_msg = {msg_name: msg_info for msg_name, msg_info in associated_msgs.items()
                                  if get_dc_sys_value(msg_info, DCSYS.TM_PAS_ATS.NomLogiqueInfoAts) == target_msg_type}
                _check_message_zc(object_type, object_name, associated_msg, object_type_str, target_msg_type,
                                  condition, condition_str, only_one_zc, plt_end)
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
        if not _check_message_zc(object_type, object_name, associated_msg, object_type_str, target_msg_type,
                                 condition, condition_str, only_one_zc, plt_end):
            success = False
    return success


def _check_message_zc(object_type, object_name: str, associated_msg, object_type_str, target_msg_type,
                      condition: bool, condition_str: str, only_one_zc: bool, plt_end: str = None) -> bool:
    success = True

    if only_one_zc:
        expected_zc_list, related_obj = get_zc_managing_object(object_type, object_name, plt_end=plt_end)
        managed = True  # boolean to tell we are not using all the ZC containing the object but only the one managing it
    else:
        expected_zc_list = get_zc_of_object(object_type, object_name)
        related_obj = None
        managed = False

    msg_zc_dict = dict()
    for associated_msg_name, associated_msg_info in associated_msg.items():
        zc_name = get_dc_sys_value(associated_msg_info, DCSYS.TM_PAS_ATS.Equipement)
        if zc_name in msg_zc_dict:
            print_error(f"The flow of type {Color.yellow}{target_msg_type}{Color.reset} for "
                        f"{object_type_str} {Color.blue}{object_name}{Color.reset} is defined multiple times "
                        f"for the same ZC {zc_name}.\n"
                        f"(The condition for the message {Color.white}*"
                        f"{condition_str.replace(Color.reset, Color.reset + Color.white)}"
                        f"{Color.reset} is {'not ' if condition else ''}met.)")
            print(msg_zc_dict[zc_name])
            print(associated_msg_name)
            success = False
        msg_zc_dict[zc_name] = associated_msg_name
    extra_msg_zc = {zc_name: info for zc_name, info in msg_zc_dict.items() if zc_name not in expected_zc_list}
    missing_zc = [zc_name for zc_name in expected_zc_list if zc_name not in msg_zc_dict]

    if only_one_zc:
        if len(msg_zc_dict) > 1:
            print_error(f"The flows of {object_type_str} of type {Color.yellow}{target_msg_type}{Color.reset} "
                        f"shall be sent by a sole ZC in ZC overlay.")
            print(f"{Color.pink}{expected_zc_list = }{Color.reset}" +
                  (f" <--> {related_obj}" if related_obj is not None else "") +
                  f"\nCurrent configuration:")
            for zc, msg in msg_zc_dict.items():
                print(f"\tfor {Color.beige}{zc = }{Color.reset}: {msg}")
            success = False

        elif extra_msg_zc:
            print(f"\nThe flows of {object_type_str} of type {Color.yellow}{target_msg_type}{Color.reset} "
                  f"shall be sent by a sole ZC in ZC overlay.")
            print_warning(f"Flow(s) of {object_type_str} {Color.blue}{object_name}{Color.reset} "
                          f"are indeed sent by a single ZC, but this ZC has to be "
                          f"{Color.pink}{expected_zc_list}{Color.reset}" +
                          (f" <--> {related_obj}" if related_obj is not None else "") +
                          " according to the tool."
                          "\nCurrent configuration:", no_newline=True)
            for zc, msg in msg_zc_dict.items():
                print(f"\tfor {Color.beige}{zc = }{Color.reset}: {msg}")
            success = False

    else:
        if extra_msg_zc:
            print_warning(f"Useless flow(s) to be removed as {object_type_str} {Color.blue}{object_name}{Color.reset} "
                          f"is not {'in' if not managed else 'managed by'} this ZC\n(but "
                          f"{'in' if not managed else 'by'} {expected_zc_list}" +
                          (f" <--> {related_obj}" if related_obj is not None else "") + "):")
            for zc, msg in extra_msg_zc.items():
                print(f"\tfor {Color.beige}{zc = }{Color.reset}: {msg}")
            success = False

        if missing_zc:
            print_error(f"A flow of type {Color.yellow}{target_msg_type}{Color.reset} shall be defined for "
                        f"{object_type_str} {Color.blue}{object_name}{Color.reset} "
                        f"for ZC {Color.pink}{missing_zc}{Color.reset} "
                        f"(object is {'in' if not managed else 'managed by'} {expected_zc_list}" +
                        (f" <--> {related_obj}" if related_obj is not None else "") + ").\n"
                        f"(The condition for the message {Color.white}"
                        f"{condition_str.replace(Color.reset, Color.reset + Color.white)}"
                        f"{Color.reset} is {'not ' if not condition else ''}met.)"
                        "\nCurrent configuration:")
            for zc, msg in msg_zc_dict.items():
                print(f"\tfor {Color.beige}{zc = }{Color.reset}: {msg}")
            success = False

    return success
