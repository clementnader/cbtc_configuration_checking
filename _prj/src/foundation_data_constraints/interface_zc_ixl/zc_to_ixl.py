#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.msg_itf_utils import get_sub_dict_zc_ixl_itf
from ...dc_sys_sheet_utils.signal_utils import get_related_overlaps
from ...dc_sys_get_cbtc_territory import *
from ...dc_par import *
from ..signal import check_signal_with_overlap
from .common_functions import *

__all__ = ["r_mes_pas_itf_3"]

LIST_OF_TSR_SPEEDS = ["Speed_0", "Speed_5", "Speed_10",
                      "Speed_20", "Speed_25", "Speed_30", "Speed_35", "Speed_40", "Speed_45",
                      "Speed_50", "Speed_55", "Speed_60", "Speed_65", "Speed_70", "Speed_75", "Speed_80"]
# TODO si c'est possible, précharger cette liste avec les infos de TSR_Possible_Speeds


def r_mes_pas_itf_3(in_cbtc: bool = False):
    # ZC -> IXL Interface
    print_title(f"Verification of R_MES_PAS_ITF_3\nZC -> IXL Interface", color=Color.mint_green)
    _rule_3_check_plt(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.QUAI), in_cbtc)
    _rule_3_check_signal(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.SIGNAL), in_cbtc)
    if "AFiabiliser" in get_class_attr_dict(DCSYS.CDV):
        _rule_3_check_block(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.CDV), in_cbtc)
    _rule_3_check_ivb(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.IVB), in_cbtc)
    _rule_3_check_switch(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.AIGUILLE), in_cbtc)
    if "GES" in get_class_attr_dict(DCSYS) and "CBTC_PROTECTION_ZONE" in get_class_attr_dict(GESType):
        _rule_3_check_cbtc_protection_zone(get_sub_dict_zc_ixl_itf(GESType.CBTC_PROTECTION_ZONE), in_cbtc)
    if "PROTECTION_ZONE" in get_class_attr_dict(TypeClasseObjetPASMES):
        _rule_3_check_protection_zone(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.PROTECTION_ZONE), in_cbtc)
    _rule_3_check_tpz(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.SS), in_cbtc)
    _rule_3_check_cross_call(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.CROSSING_CALLING_AREA), in_cbtc)
    if "TSR_PREDEFINED_AREA_SPEED" in get_class_attr_dict(TypeClasseObjetPASMES):
        _rule_3_check_tsr_area_speed(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.TSR_PREDEFINED_AREA_SPEED), in_cbtc)


# ------- Rule 3 (ZC -> IXL) Sub Functions ------- #
def _rule_3_check_plt(plt_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.QUAI}...")
    if not in_cbtc:
        plt_dict = load_sheet(DCSYS.Quai)
    else:
        plt_dict = get_objects_in_cbtc_ter(DCSYS.Quai)
    success = True
    for plt_name, plt in plt_dict.items():
        is_psd_msg_routed = get_dc_sys_value(plt, DCSYS.Quai.PsdMessagesRouted) == YesOrNo.O
        if check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, is_psd_msg_routed,
                          "flag [PSD Messages Routed] set to 'Y'",
                          [TypeNomLogiqueInfoPASMES.TRAIN_AT_PLATFORM,
                           TypeNomLogiqueInfoPASMES.OPEN_CMD_L,
                           TypeNomLogiqueInfoPASMES.OPEN_CMD_R,
                           TypeNomLogiqueInfoPASMES.CLOSE_CMD_L,
                           TypeNomLogiqueInfoPASMES.CLOSE_CMD_R],
                          shall_be_vital=True, only_one_zc=True) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_signal(sig_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.SIGNAL}...")
    check_signal_with_overlap()  # first verify the flag [With overlap]
    if not in_cbtc:
        sig_dict = load_sheet(DCSYS.Sig)
    else:
        sig_dict = get_objects_in_cbtc_ter(DCSYS.Sig)
    success = True
    for sig_name, sig in sig_dict.items():
        is_not_buffer_or_pr = get_dc_sys_value(sig, DCSYS.Sig.Type) not in [SignalType.HEURTOIR,
                                                                            SignalType.PERMANENT_ARRET]

        with_overlap = (is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.Enc_Dep) == YesOrNo.O
                        and get_dc_sys_value(sig, DCSYS.Sig.OverlapType) == Edep_Type.NO_CBTC_REQUEST)
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, with_overlap,
                          "flag [With overlap] set to 'Y' and [Overlap Type] = 'NO_CBTC_REQUEST'",
                          TypeNomLogiqueInfoPASMES.CBTC_OLZ, shall_be_vital=True,
                          only_one_zc=True, sig_upstream_ivb=True) is False:
            success = False

        concealable = is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.Annulable) == YesOrNo.O
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, concealable, "flag [Concealable] set to 'Y'",
                          TypeNomLogiqueInfoPASMES.X_RQ, shall_be_vital=True) is False:
            success = False

        sa_or_overlap = ((is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.Du_Assistee) == YesOrNo.O)
                         or with_overlap)
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, sa_or_overlap, "flag [With SA] set to 'Y' or "
                          "flag [With overlap] set to 'Y' and [Overlap Type] = 'NO_CBTC_REQUEST'",
                          TypeNomLogiqueInfoPASMES.STOP_ASSURE, shall_be_vital=True) is False:
            success = False

        with_imc = is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.D_Libre) == YesOrNo.O
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, with_imc, "flag [With IMC] set to 'Y'",
                          TypeNomLogiqueInfoPASMES.CBTC_APZ, shall_be_vital=True) is False:
            success = False

        if "TypeDa" in get_class_attr_dict(DCSYS.Sig):
            with_arc = (is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.Da_Passage) == YesOrNo.O
                        and get_dc_sys_value(sig, DCSYS.Sig.TypeDa) in [TypeDA.SECTIONAL_RELEASE,
                                                                        TypeDA.TRAIN_PASSAGE_PROVING])
            if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, with_arc, "flag [With ARC] set to 'Y' and "
                              "[ARC Type] = 'SECTIONAL_RELEASE' or 'TRAIN_PASSAGE_PROVING'",
                              TypeNomLogiqueInfoPASMES.TRAIN_PASS_HS, shall_be_vital=True,
                              only_one_zc=True, sig_upstream_ivb=False) is False:
                success = False

        related_ovl_list = get_related_overlaps(sig_name)
        ovl_names = [ovl[0] for ovl in related_ovl_list]
        tpp = [get_dc_sys_value(related_ovl[1], DCSYS.IXL_Overlap.WithTpp) == YesOrNo.O
               for related_ovl in related_ovl_list]
        if any(tpp) and not all(tpp):
            print_error(f"All the overlaps related to signal {Color.blue}{sig_name}{Color.reset} "
                        f"do not have the same flag [With TPP]:")
            print(ovl_names)
        with_tpp_overlap = is_not_buffer_or_pr and with_overlap and any(tpp)
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, with_tpp_overlap,
                          f"flag [With overlap] set to 'Y' and [Overlap Type] = 'NO_CBTC_REQUEST' "
                          f"and the related IXL Overlap {Color.yellow}{ovl_names}{Color.reset} "
                          f"flag [With TPP] set to 'Y'", TypeNomLogiqueInfoPASMES.TRAIN_IN_BERTH,
                          shall_be_vital=True,
                          only_one_zc=True, sig_upstream_ivb=True) is False:
            success = False

        func_stop = is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.WithFunc_Stop) == YesOrNo.O
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, func_stop,
                          "flag [With Func Stop] set to 'Y'",
                          [TypeNomLogiqueInfoPASMES.FUNC_STOP_ACCEPT,
                           TypeNomLogiqueInfoPASMES.FUNC_STOP_REJECT], shall_be_vital=False) is False:
            success = False

        is_home_signal = get_dc_sys_value(sig, DCSYS.Sig.Type) == SignalType.MANOEUVRE
        train_app_provided = is_home_signal and get_dc_sys_value(sig, DCSYS.Sig.CbtcTrainAppProvided) == YesOrNo.O
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, train_app_provided,
                          "Home Signal with flag [CBTC Train App provided] set to 'Y'",
                          TypeNomLogiqueInfoPASMES.CBTC_TRAIN_IN_APPROACH, shall_be_vital=True) is False:
            success = False

    if success is True:
        print_log(f"No KO.")


def _rule_3_check_block(block_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.CDV}...")
    if not in_cbtc:
        block_dict = load_sheet(DCSYS.CDV)
    else:
        block_dict = get_objects_in_cbtc_ter(DCSYS.CDV)
    success = True
    for block_name, block in block_dict.items():
        overriden = get_dc_sys_value(block, DCSYS.CDV.AFiabiliser) == YesOrNo.O
        if check_obj_msgs(DCSYS.CDV, block_msg_dict, block_name, overriden, "flag [Overriden] set to 'Y'",
                          TypeNomLogiqueInfoPASMES.ZC_BLOCK, shall_be_vital=True) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_ivb(ivb_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.IVB}...")
    if not in_cbtc:
        ivb_dict = load_sheet(DCSYS.IVB)
    else:
        ivb_dict = get_objects_in_cbtc_ter(DCSYS.IVB)
    success = True
    for ivb_name, ivb in ivb_dict.items():
        sent_ixl = get_dc_sys_value(ivb, DCSYS.IVB.SentToIxl) == YesOrNo.O
        if check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, sent_ixl, "flag [Sent To IXL] set to 'Y'",
                          TypeNomLogiqueInfoPASMES.IXL_VIRTUAL_BLOCK, shall_be_vital=True, only_one_zc=True) is False:
            success = False

        block_freed = get_dc_sys_value(ivb, DCSYS.IVB.BlockFreed) == YesOrNo.O
        if check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, block_freed, "flag [Block Freed] set to 'Y'",
                          TypeNomLogiqueInfoPASMES.BLOCK_FREED, shall_be_vital=True) is False:
            success = False

        if check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, True, "shall exist for all IVB",
                          [TypeNomLogiqueInfoPASMES.AUTHORIZED_NORMAL,
                           TypeNomLogiqueInfoPASMES.AUTHORIZED_REVERSE], shall_be_vital=True) is False:
            success = False

        unlock_normal = get_dc_sys_value(ivb, DCSYS.IVB.UnlockNormal) == YesOrNo.O
        if check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, unlock_normal, "flag [Unlock Normal] set to 'Y'",
                          TypeNomLogiqueInfoPASMES.UNLOCK_DL_NORMAL, shall_be_vital=True, only_one_zc=True) is False:
            success = False

        unlock_reverse = get_dc_sys_value(ivb, DCSYS.IVB.UnlockReverse) == YesOrNo.O
        if check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, unlock_reverse, "flag [Unlock Reverse] set to 'Y'",
                          TypeNomLogiqueInfoPASMES.UNLOCK_DL_REVERSE, shall_be_vital=True, only_one_zc=True) is False:
            success = False

    if success is True:
        print_log(f"No KO.")


def _rule_3_check_switch(sw_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.AIGUILLE}...")
    if not in_cbtc:
        sw_dict = load_sheet(DCSYS.Aig)
    else:
        sw_dict = get_objects_in_cbtc_ter(DCSYS.Aig)
    success = True
    for sw_name, sw in sw_dict.items():
        free_to_move = get_dc_sys_value(sw, DCSYS.Aig.FreeToMove) == YesOrNo.O
        if check_obj_msgs(DCSYS.Aig, sw_msg_dict, sw_name, free_to_move, "flag [Free To Move] set to 'Y'",
                          TypeNomLogiqueInfoPASMES.CBTC_FREE_TO_MOVE, shall_be_vital=True) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_cbtc_protection_zone(cbtc_pz_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {GESType.CBTC_PROTECTION_ZONE}...")
    if not in_cbtc:
        cbtc_pz_dict = load_sheet(DCSYS.CBTC_Protection_Zone)
    else:
        cbtc_pz_dict = get_objects_in_cbtc_ter(DCSYS.CBTC_Protection_Zone)
    success = True
    for cbtc_pz_name, cbtc_pz in cbtc_pz_dict.items():
        if check_obj_msgs(DCSYS.CBTC_Protection_Zone, cbtc_pz_msg_dict, cbtc_pz_name, True,
                          "shall exist for all CBTC Protection Zones",
                          TypeNomLogiqueInfoPASMES.PROTECTION_NOT_REQUIRED,
                          shall_be_vital=True) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_protection_zone(pz_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.PROTECTION_ZONE}...")
    if not in_cbtc:
        pz_dict = load_sheet(DCSYS.Protection_Zone)
    else:
        pz_dict = get_objects_in_cbtc_ter(DCSYS.Protection_Zone)
    success = True
    for pz_name, pz in pz_dict.items():
        cbtc_controlled = get_dc_sys_value(pz, DCSYS.Protection_Zone.CbtcControlledFlag) == YesOrNo.O
        if check_obj_msgs(DCSYS.Protection_Zone, pz_msg_dict, pz_name, cbtc_controlled,
                          "flag [CBTC Controlled] set to 'Y'", TypeNomLogiqueInfoPASMES.MOVEMENT_AUTHORIZED,
                          shall_be_vital=True) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_tpz(tpz_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.SS}...")
    if not in_cbtc:
        tpz_dict = load_sheet(DCSYS.SS)
    else:
        tpz_dict = get_objects_in_cbtc_ter(DCSYS.SS)
    success = True
    for tpz_name, tpz in tpz_dict.items():
        if "POWER_AUTHORIZED" in get_class_attr_dict(TypeNomLogiqueInfoPASMES):
            if check_obj_msgs(DCSYS.SS, tpz_msg_dict, tpz_name, True, "shall exist for all Traction Power Zone",
                              TypeNomLogiqueInfoPASMES.POWER_AUTHORIZED, shall_be_vital=True) is False:
                success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_cross_call(cross_call_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.CROSSING_CALLING_AREA}...")
    if not in_cbtc:
        cross_call_dict = load_sheet(DCSYS.Crossing_Calling_Area)
    else:
        cross_call_dict = get_objects_in_cbtc_ter(DCSYS.Crossing_Calling_Area)
    success = True
    for cross_call_name, cross_call in cross_call_dict.items():
        if "CROSSING_AUTH_REQUEST" in get_class_attr_dict(TypeNomLogiqueInfoPASMES):
            if check_obj_msgs(DCSYS.SS, cross_call_msg_dict, cross_call_name, True,
                              "shall exist for all Crossing Calling Area",
                              TypeNomLogiqueInfoPASMES.CROSSING_AUTH_REQUEST, shall_be_vital=False) is False:
                success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_tsr_area_speed(tsr_area_speed_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.TSR_PREDEFINED_AREA_SPEED}...")
    tsr_interfaced_with_vhmi = get_param_value("tsr_interfaced_with_VHMI")
    if not in_cbtc:
        tsr_area_dict = load_sheet(DCSYS.TSR_Area)
    else:
        tsr_area_dict = get_objects_in_cbtc_ter(DCSYS.TSR_Area)
    missing_speeds_dict = {key: {speed: False for speed in LIST_OF_TSR_SPEEDS} for key in tsr_area_dict}
    tsr_speed_dict = load_sheet(DCSYS.TSR_Possible_Speeds)
    wayside_eqpt_dict = load_sheet(DCSYS.Wayside_Eqpt)
    success = True
    for tsr_area_name, tsr_area in tsr_area_dict.items():
        tsr_area_missing_speeds = list()
        for tsr_speed in tsr_speed_dict.keys():
            tsr_area_speed_name = tsr_area_name + "_" + tsr_speed
            for zc_name in get_all_zc():
                is_zc_zcr = (get_dc_sys_value(wayside_eqpt_dict[zc_name], DCSYS.Wayside_Eqpt.Function.Zcr)[0]
                             == YesOrNo.O)
                zcr_and_interfaced_with_hmi = is_zc_zcr and tsr_interfaced_with_vhmi
                if check_obj_msgs(DCSYS.TSR_Area, tsr_area_speed_msg_dict, tsr_area_speed_name,
                                  zcr_and_interfaced_with_hmi, f"message transmitter {zc_name} is a ZCR "
                                                               f"and [tsr_interfaced_with_VHMI] = true",
                                  TypeNomLogiqueInfoPASMES.TSR_AREA_SPEED_SUPERVISION, shall_be_vital=True,
                                  obj_type_str="TSR_Area_Possible_Speeds", zc=zc_name, tsr_speed=tsr_speed,
                                  tsr_area_missing_speeds=tsr_area_missing_speeds) is False:
                    success = False
        if tsr_area_missing_speeds:
            # print_warning(f"The following speeds have no message "
            #               f"{TypeNomLogiqueInfoPASMES.TSR_AREA_SPEED_SUPERVISION} "
            #               f"for TSR_Area {Color.blue}{tsr_area_name}{Color.reset}:")
            # print(tsr_area_missing_speeds)
            for speed in tsr_area_missing_speeds:
                missing_speeds_dict[tsr_area_name][speed] = True
    csv = "TSR_Area;" + ";".join(LIST_OF_TSR_SPEEDS) + "\n"
    for tsr_area, speed_dict in missing_speeds_dict.items():
        csv += f"{tsr_area};"
        for is_missing in speed_dict.values():
            csv += f"{'Missing' if is_missing else ''};"
        csv += "\n"
    print(csv)
    if success is True:
        print_log(f"No KO.")
