#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *
from ..dc_par import *


def r_mes_pas_itf_1():
    # IXL -> ZC Interface
    print_title(f"Verification of R_MES_PAS_ITF_1\nIXL -> ZC Interface", color=Color.mint_green)
    _rule_1_check_plt(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.QUAI))
    _rule_1_check_signal(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.SIGNAL))
    _rule_1_check_switch(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.AIGUILLE))
    _rule_1_check_block(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.CDV))
    _rule_1_check_ivb(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.IVB))
    _rule_1_check_dd(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.DP))
    _rule_1_check_passage_detector(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.PASSAGE_DETECTOR))
    _rule_1_check_tpz(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.SS))
    _rule_1_check_ovl(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.IXL_OVERLAP))
    _rule_1_check_protection_zone(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.PROTECTION_ZONE))
    _rule_1_check_flood_gate(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.FLOOD_GATE))
    _rule_1_check_traffic_stop(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.TRAFFIC_STOP))
    _rule_1_check_asr(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.ASR))
    _rule_1_check_tsr_area(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.TSR_PREDEFINED_AREA))


def r_mes_pas_itf_3():
    # ZC -> IXL Interface
    print_title(f"Verification of R_MES_PAS_ITF_3\nZC -> IXL Interface", color=Color.mint_green)
    _rule_3_check_plt(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.QUAI))
    _rule_3_check_signal(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.SIGNAL))
    _rule_3_check_block(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.CDV))
    _rule_3_check_ivb(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.IVB))
    _rule_3_check_switch(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.AIGUILLE))
    _rule_3_check_protection_zone(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.PROTECTION_ZONE))
    _rule_3_check_tpz(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.SS))
    _rule_3_check_cross_call(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.CROSSING_CALLING_AREA))
    _rule_3_check_tsr_area_speed(get_sub_dict_zc_ixl_itf(TypeClasseObjetPASMES.TSR_PREDEFINED_AREA_SPEED))


# ------- Rule 1 (IXL -> ZC) Sub Functions ------- #
def _rule_1_check_plt(plt_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.QUAI}...")
    plt_dict = load_sheet(DCSYS.Quai)
    success = True
    for plt_name, plt in plt_dict.items():
        atb_zones = [atb[0] for atb in get_atb_zone_related_to_plt(plt_name)]
        origin_atb_mvt = True if atb_zones else False
        if _check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, origin_atb_mvt,
                           f"platform is origin of an ATB movement {atb_zones}",
                           TypeNomLogiqueInfoMESPAS.B_ATB,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False

        ws_eqpt_dict = load_sheet(DCSYS.Wayside_Eqpt)
        related_ws_eqpt = get_dc_sys_value(plt, DCSYS.Quai.RelatedWaysideEquip)
        with_ess = get_dc_sys_value(plt, DCSYS.Quai.WithEss) == YesOrNo.O and \
            get_dc_sys_value(ws_eqpt_dict[related_ws_eqpt], DCSYS.Wayside_Eqpt.Function.Zc[0])
        if _check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, with_ess,
                           f"flag [With ESS] set to 'Y' "
                           f"and [Related Wayside Equip] {related_ws_eqpt} is a ZC",
                           TypeNomLogiqueInfoMESPAS.B_ESS,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False

        with_th = get_dc_sys_value(plt, DCSYS.Quai.WithTh) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, with_th,
                           f"flag [With TH] set to 'Y'",
                           TypeNomLogiqueInfoMESPAS.B_TH,
                           should_be_vital=False,
                           is_flux_pas_mes=False) is False:
            success = False

        with_tad = get_dc_sys_value(plt, DCSYS.Quai.WithTad) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, with_tad,
                           f"flag [With TAD] set to 'Y'",
                           TypeNomLogiqueInfoMESPAS.B_TAD,
                           should_be_vital=False,
                           is_flux_pas_mes=False) is False:
            success = False

        psd_msg_routed = get_dc_sys_value(plt, DCSYS.Quai.PsdMessagesRouted) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, psd_msg_routed,
                           f"flag [PSD Messages Routed] set to 'Y'",
                           TypeNomLogiqueInfoMESPAS.DEPARTURE_AUTH,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_signal(sig_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.SIGNAL}...")
    sig_dict = load_sheet(DCSYS.Sig)
    success = True
    for sig_name, sig in sig_dict.items():
        is_not_buffer_or_pr = get_dc_sys_value(sig, DCSYS.Sig.Type) not in [SignalType.HEURTOIR,
                                                                            SignalType.PERMANENT_ARRET]

        cbtc_terr_exit_or_with_iatp = get_dc_sys_value(sig, DCSYS.Sig.SortieTerritoireCbtc) == YesOrNo.O or \
            get_dc_sys_value(sig, DCSYS.Sig.WithIatpDepCheck) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, is_not_buffer_or_pr,
                           "should exist for all Signals (excluding buffers and permanent reds)",
                           TypeNomLogiqueInfoMESPAS.PR_ASPECT,
                           should_be_vital=cbtc_terr_exit_or_with_iatp,
                           is_flux_pas_mes=False,
                           vital_condition=cbtc_terr_exit_or_with_iatp,
                           vital_condition_str="flag [CBTC Territory exit] set to 'Y' "
                                               "or flag [With IATP dep check] set to 'Y'") is False:
            success = False

        with_sa = is_not_buffer_or_pr and (get_dc_sys_value(sig, DCSYS.Sig.Du_Assistee) == YesOrNo.O)
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, with_sa,
                           "flag [With SA] set to 'Y'",
                           TypeNomLogiqueInfoMESPAS.AP_CAN_RQ,
                           should_be_vital=False,
                           is_flux_pas_mes=False) is False:
            success = False

        is_home_signal = get_dc_sys_value(sig, DCSYS.Sig.Type) == SignalType.MANOEUVRE
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, is_home_signal,
                           "should exist for all Home Signals",
                           TypeNomLogiqueInfoMESPAS.IL_SET,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False

        func_stop = is_not_buffer_or_pr and (get_dc_sys_value(sig, DCSYS.Sig.WithFunc_Stop) == YesOrNo.O)
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, func_stop,
                           "flag [With Func Stop] set to 'Y'",
                           TypeNomLogiqueInfoMESPAS.FUNC_STOP_RQ,
                           should_be_vital=False,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_switch(sw_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.AIGUILLE}...")
    sig_dict = load_sheet(DCSYS.Aig)
    success = True
    for sw_name, sw in sig_dict.items():
        if _check_obj_msgs(DCSYS.Aig, sw_msg_dict, sw_name, True,
                           "should exist for all switches",
                           [TypeNomLogiqueInfoMESPAS.SW_RIGHT_C,
                            TypeNomLogiqueInfoMESPAS.SW_LEFT_C],
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_block(block_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.CDV}...")
    block_dict = load_sheet(DCSYS.CDV)
    success = True
    for block_name, block in block_dict.items():
        if _check_obj_msgs(DCSYS.CDV, block_msg_dict, block_name, True,
                           "should exist for all CDV",
                           TypeNomLogiqueInfoMESPAS.BLOCK,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False

        block_not_held = get_dc_sys_value(block, DCSYS.CDV.IxlGivesNotHeldStatus) == YesOrNo.O
        if _check_obj_msgs(DCSYS.CDV, block_msg_dict, block_name, block_not_held,
                           "flag [Block Not Held] set to 'Y'",
                           TypeNomLogiqueInfoMESPAS.BLOCK_NOT_HELD,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False

        block_init_status = get_dc_sys_value(block, DCSYS.CDV.IxlGivesBlockInitStatus) == YesOrNo.O
        if _check_obj_msgs(DCSYS.CDV, block_msg_dict, block_name, block_init_status,
                           "flag [With Block Init Status Exchanged] set to 'Y'",
                           TypeNomLogiqueInfoMESPAS.BLOCK_INIT_STATUS,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_ivb(ivb_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.IVB}...")
    ivb_dict = load_sheet(DCSYS.IVB)
    success = True
    for ivb_name, ivb in ivb_dict.items():
        direction_locking_block = get_dc_sys_value(ivb, DCSYS.IVB.DirectionLockingBlock) == YesOrNo.O
        if _check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, direction_locking_block,
                           "flag [Direction Locking Block] set to 'Y'",
                           [TypeNomLogiqueInfoMESPAS.BLOCK_NORMAL_DIRECTION_L,
                            TypeNomLogiqueInfoMESPAS.BLOCK_REVERSE_DIRECTION_L],
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_dd(dd_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.DP}...")
    dd_dict = load_sheet(DCSYS.DP)
    success = True
    for dd_name, dd in dd_dict.items():
        if _check_obj_msgs(DCSYS.DP, dd_msg_dict, dd_name, True,
                           "should exist for all Discrete Detectors",
                           TypeNomLogiqueInfoMESPAS.DD,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_passage_detector(pass_det_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.PASSAGE_DETECTOR}...")
    pass_det_dict = load_sheet(DCSYS.Passage_Detector)
    success = True
    for pass_det_name, pass_det in pass_det_dict.items():
        if _check_obj_msgs(DCSYS.Passage_Detector, pass_det_msg_dict, pass_det_name, True,
                           "should exist for all Passage Detectors",
                           TypeNomLogiqueInfoMESPAS.NO_PASSAGE,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_tpz(tpz_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.SS}...")
    tpz_dict = load_sheet(DCSYS.SS)
    success = True
    for tpz_name, tpz in tpz_dict.items():
        if _check_obj_msgs(DCSYS.SS, tpz_msg_dict, tpz_name, True,
                           "should exist for all Passage Detectors",
                           [TypeNomLogiqueInfoMESPAS.TRACTION_PWR_REGEN_AUTH,
                            TypeNomLogiqueInfoMESPAS.MVT_AUTH,
                            TypeNomLogiqueInfoMESPAS.UTO_MVT_AUTH,
                            TypeNomLogiqueInfoMESPAS.PROTECTION_LEVEL],
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_ovl(ovl_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.IXL_OVERLAP}...")
    ovl_dict = load_sheet(DCSYS.IXL_Overlap)
    sig_dict = load_sheet(DCSYS.Sig)
    success = True
    for ovl_name, ovl in ovl_dict.items():
        related_sig = get_dc_sys_value(ovl, DCSYS.IXL_Overlap.DestinationSignal)
        with_overlap = get_dc_sys_value(sig_dict[related_sig], DCSYS.Sig.Enc_Dep) == YesOrNo.O and \
            get_dc_sys_value(sig_dict[related_sig], DCSYS.Sig.OverlapType) == Edep_Type.NO_CBTC_REQUEST
        if _check_obj_msgs(DCSYS.IXL_Overlap, ovl_msg_dict, ovl_name, with_overlap,
                           f"signal upstream the overlap ({related_sig}) has flag [With overlap] set to 'Y' "
                           f"and [Overlap Type] = 'NO_CBTC_REQUEST'",
                           TypeNomLogiqueInfoMESPAS.OLZ_OVERLAP_LK,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_protection_zone(pz_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.PROTECTION_ZONE}...")
    pz_dict = load_sheet(DCSYS.Protection_Zone)
    success = True
    for pz_name, pz in pz_dict.items():
        if _check_obj_msgs(DCSYS.Protection_Zone, pz_msg_dict, pz_name, True,
                           "should exist for all Protection Zones",
                           TypeNomLogiqueInfoMESPAS.MVT_AUTH,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_flood_gate(fg_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.FLOOD_GATE}...")
    fg_dict = load_sheet(DCSYS.Flood_Gate)
    success = True
    for fg_name, fg in fg_dict.items():
        if _check_obj_msgs(DCSYS.Flood_Gate, fg_msg_dict, fg_name, True,
                           "should exist for all Flood Gates",
                           TypeNomLogiqueInfoMESPAS.OPEN_AND_LOCKED,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_traffic_stop(stop_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.TRAFFIC_STOP}...")
    stop_dict = load_sheet(DCSYS.Traffic_Stop)
    success = True
    for stop_name, stop in stop_dict.items():
        if _check_obj_msgs(DCSYS.Traffic_Stop, stop_msg_dict, stop_name, True,
                           "should exist for all Traffic Stops",
                           TypeNomLogiqueInfoMESPAS.STOP,
                           should_be_vital=False,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_asr(asr_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.ASR}...")
    asr_dict = load_sheet(DCSYS.ASR)
    success = True
    for asr_name, asr in asr_dict.items():
        if _check_obj_msgs(DCSYS.ASR, asr_msg_dict, asr_name, True,
                           "should exist for all ASR",
                           TypeNomLogiqueInfoMESPAS.ASR_NOT_APPLIED,
                           should_be_vital=True,
                           is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_tsr_area(tsr_area_msg_dict: dict):
    list_of_speeds = ["Speed_0", "Speed_5", "Speed_10",
                      "Speed_20", "Speed_25", "Speed_30", "Speed_35", "Speed_40", "Speed_45",
                      "Speed_50", "Speed_55", "Speed_60", "Speed_65", "Speed_70", "Speed_75", "Speed_80"]
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.TSR_PREDEFINED_AREA}...")
    tsr_interfaced_with_vhmi = get_param_value("tsr_interfaced_with_VHMI")
    tsr_area_dict = load_sheet(DCSYS.TSR_Area)
    missing_speeds_dict = {key: {speed: False for speed in list_of_speeds} for key in tsr_area_dict}
    tsr_speed_dict = load_sheet(DCSYS.TSR_Possible_Speeds)
    wayside_eqpt_dict = load_sheet(DCSYS.Wayside_Eqpt)
    success = True
    for tsr_area_name, tsr_area in tsr_area_dict.items():
        tsr_area_missing_speeds_for_set_cmd = list()
        tsr_area_missing_speeds_for_remove_cmd = list()
        for tsr_speed in tsr_speed_dict.keys():
            tsr_area_speed_name = tsr_area_name + "_" + tsr_speed
            for zc_name in get_all_zc():
                is_zc_zcr = get_dc_sys_value(wayside_eqpt_dict[zc_name], DCSYS.Wayside_Eqpt.Function.Zcr)[0] \
                                == YesOrNo.O
                zcr_and_interfaced_with_hmi = is_zc_zcr and tsr_interfaced_with_vhmi

                if _check_obj_msgs(DCSYS.TSR_Area, tsr_area_msg_dict, tsr_area_speed_name,
                                   zcr_and_interfaced_with_hmi, f"message transmitter {zc_name} is a ZCR "
                                   f"and [tsr_interfaced_with_VHMI] = true",
                                   TypeNomLogiqueInfoMESPAS.TSR_AREA_SPEED_SET_CMD, should_be_vital=False,
                                   is_flux_pas_mes=False,
                                   obj_type_str="TSR_Area_Possible_Speeds", zc=zc_name, tsr_speed=tsr_speed,
                                   tsr_area_missing_speeds=tsr_area_missing_speeds_for_set_cmd) is False:
                    success = False

                if _check_obj_msgs(DCSYS.TSR_Area, tsr_area_msg_dict, tsr_area_speed_name,
                                   zcr_and_interfaced_with_hmi, f"message transmitter {zc_name} is a ZCR "
                                   f"and [tsr_interfaced_with_VHMI] = true",
                                   TypeNomLogiqueInfoMESPAS.TSR_AREA_SPEED_REMOVE_CMD, should_be_vital=True,
                                   is_flux_pas_mes=False,
                                   obj_type_str="TSR_Area_Possible_Speeds", zc=zc_name, tsr_speed=tsr_speed,
                                   tsr_area_missing_speeds=tsr_area_missing_speeds_for_remove_cmd) is False:
                    success = False
        if tsr_area_missing_speeds_for_set_cmd == tsr_area_missing_speeds_for_remove_cmd:
            for speed in tsr_area_missing_speeds_for_set_cmd:
                missing_speeds_dict[tsr_area_name][speed] = True
            # print_warning(f"The following speeds have no messages {TypeNomLogiqueInfoMESPAS.TSR_AREA_SPEED_SET_CMD} "
            #               f"and {TypeNomLogiqueInfoMESPAS.TSR_AREA_SPEED_REMOVE_CMD} "
            #               f"for TSR_Area {Color.blue}{tsr_area_name}{Color.reset}:")
            # print(tsr_area_missing_speeds_for_set_cmd)
        else:
            print_error(f"The missing speeds for messages {TypeNomLogiqueInfoMESPAS.TSR_AREA_SPEED_SET_CMD} "
                        f"and {TypeNomLogiqueInfoMESPAS.TSR_AREA_SPEED_REMOVE_CMD} do not correspond:")
            print(f"{tsr_area_missing_speeds_for_set_cmd = }")
            print(f"{tsr_area_missing_speeds_for_remove_cmd = }")
    csv = "TSR_Area;" + ";".join(list_of_speeds) + "\n"
    for tsr_area, speed_dict in missing_speeds_dict.items():
        csv += f"{tsr_area};"
        for is_missing in speed_dict.values():
            csv += f"{'Missing' if is_missing else ''};"
        csv += "\n"
    print(csv)
    if success is True:
        print_log(f"No KO.")


# ------- Rule 3 (ZC -> IXL) Sub Functions ------- #
def _rule_3_check_plt(plt_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.QUAI}...")
    plt_dict = load_sheet(DCSYS.Quai)
    success = True
    for plt_name, plt in plt_dict.items():
        is_psd_msg_routed = get_dc_sys_value(plt, DCSYS.Quai.PsdMessagesRouted) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, is_psd_msg_routed,
                           "flag [PSD Messages Routed] set to 'Y'",
                           [TypeNomLogiqueInfoPASMES.TRAIN_AT_PLATFORM,
                            TypeNomLogiqueInfoPASMES.OPEN_CMD_L,
                            TypeNomLogiqueInfoPASMES.OPEN_CMD_R,
                            TypeNomLogiqueInfoPASMES.CLOSE_CMD_L,
                            TypeNomLogiqueInfoPASMES.CLOSE_CMD_R],
                           should_be_vital=True) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_signal(sig_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.SIGNAL}...")
    sig_dict = load_sheet(DCSYS.Sig)
    success = True
    for sig_name, sig in sig_dict.items():
        is_not_buffer_or_pr = get_dc_sys_value(sig, DCSYS.Sig.Type) not in [SignalType.HEURTOIR,
                                                                            SignalType.PERMANENT_ARRET]

        with_overlap = is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.Enc_Dep) == YesOrNo.O and \
            get_dc_sys_value(sig, DCSYS.Sig.OverlapType) == Edep_Type.NO_CBTC_REQUEST
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, with_overlap,
                           "flag [With overlap] set to 'Y' and [Overlap Type] = 'NO_CBTC_REQUEST'",
                           TypeNomLogiqueInfoPASMES.CBTC_OLZ, should_be_vital=True) is False:
            success = False

        concealable = is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.Annulable) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, concealable, "flag [Concealable] set to 'Y'",
                           TypeNomLogiqueInfoPASMES.X_RQ, should_be_vital=True) is False:
            success = False

        sa_or_overlap = (is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.Du_Assistee) == YesOrNo.O) \
            or with_overlap
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, sa_or_overlap, "flag [With SA] set to 'Y' or "
                           "flag [With overlap] set to 'Y' and [Overlap Type] = 'NO_CBTC_REQUEST'",
                           TypeNomLogiqueInfoPASMES.STOP_ASSURE, should_be_vital=True) is False:
            success = False

        with_imc = is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.D_Libre) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, with_imc, "flag [With IMC] set to 'Y'",
                           TypeNomLogiqueInfoPASMES.CBTC_APZ, should_be_vital=True) is False:
            success = False

        with_arc = is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.Da_Passage) == YesOrNo.O and \
            get_dc_sys_value(sig, DCSYS.Sig.TypeDa) in [TypeDA.SECTIONAL_RELEASE, TypeDA.TRAIN_PASSAGE_PROVING]
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, with_arc, "flag [With ARC] set to 'Y' and "
                           "[ARC Type] = 'SECTIONAL_RELEASE' or 'TRAIN_PASSAGE_PROVING'",
                           TypeNomLogiqueInfoPASMES.TRAIN_PASS_HS, should_be_vital=True) is False:
            success = False

        related_ovl_list = get_related_overlaps(sig_name)
        ovl_names = [ovl[0] for ovl in related_ovl_list]
        tpp = [get_dc_sys_value(related_ovl[1], DCSYS.IXL_Overlap.WithTpp) == YesOrNo.O for related_ovl in related_ovl_list]
        if any(tpp) and not all(tpp):
            print_error(f"All the overlaps related to signal {Color.blue}{sig_name}{Color.reset} "
                        f"do not have the same flag [With TPP]:")
            print(ovl_names)
        with_tpp_overlap = is_not_buffer_or_pr and with_overlap and any(tpp)
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, with_tpp_overlap,
                           f"flag [With overlap] set to 'Y' and [Overlap Type] = 'NO_CBTC_REQUEST' "
                           f"and the related IXL Overlap {Color.yellow}{ovl_names}{Color.reset} "
                           f"flag [With TPP] set to 'Y'", TypeNomLogiqueInfoPASMES.TRAIN_IN_BERTH,
                           should_be_vital=True) is False:
            success = False

        func_stop = is_not_buffer_or_pr and get_dc_sys_value(sig, DCSYS.Sig.WithFunc_Stop) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, func_stop, "flag [With Func Stop] set to 'Y'",
                           [TypeNomLogiqueInfoPASMES.FUNC_STOP_ACCEPT,
                            TypeNomLogiqueInfoPASMES.FUNC_STOP_REJECT], should_be_vital=False) is False:
            success = False

        is_home_signal = get_dc_sys_value(sig, DCSYS.Sig.Type) == SignalType.MANOEUVRE
        train_app_provided = is_home_signal and get_dc_sys_value(sig, DCSYS.Sig.CbtcTrainAppProvided) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, train_app_provided,
                           "Home Signal with flag [CBTC Train App provided] set to 'Y'",
                           TypeNomLogiqueInfoPASMES.CBTC_TRAIN_IN_APPROACH, should_be_vital=True) is False:
            success = False

    if success is True:
        print_log(f"No KO.")


def _rule_3_check_block(block_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.CDV}...")
    block_dict = load_sheet(DCSYS.CDV)
    success = True
    for block_name, block in block_dict.items():
        overriden = get_dc_sys_value(block, DCSYS.CDV.AFiabiliser) == YesOrNo.O
        if _check_obj_msgs(DCSYS.CDV, block_msg_dict, block_name, overriden, "flag [Overriden] set to 'Y'",
                           TypeNomLogiqueInfoPASMES.ZC_BLOCK, should_be_vital=True) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_ivb(ivb_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.IVB}...")
    ivb_dict = load_sheet(DCSYS.IVB)
    success = True
    for ivb_name, ivb in ivb_dict.items():
        sent_ixl = get_dc_sys_value(ivb, DCSYS.IVB.SentToIxl) == YesOrNo.O
        if _check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, sent_ixl, "flag [Sent To IXL] set to 'Y'",
                           TypeNomLogiqueInfoPASMES.IXL_VIRTUAL_BLOCK, should_be_vital=True) is False:
            success = False

        block_freed = get_dc_sys_value(ivb, DCSYS.IVB.BlockFreed) == YesOrNo.O
        if _check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, block_freed, "flag [Block Freed] set to 'Y'",
                           TypeNomLogiqueInfoPASMES.BLOCK_FREED, should_be_vital=True) is False:
            success = False

        if _check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, True, "should exist for all IVB",
                           [TypeNomLogiqueInfoPASMES.AUTHORIZED_NORMAL,
                            TypeNomLogiqueInfoPASMES.AUTHORIZED_REVERSE], should_be_vital=True) is False:
            success = False

        unlock_normal = get_dc_sys_value(ivb, DCSYS.IVB.UnlockNormal) == YesOrNo.O
        if _check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, unlock_normal, "flag [Unlock Normal] set to 'Y'",
                           TypeNomLogiqueInfoPASMES.UNLOCK_DL_NORMAL, should_be_vital=True) is False:
            success = False

        unlock_reverse = get_dc_sys_value(ivb, DCSYS.IVB.UnlockReverse) == YesOrNo.O
        if _check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, unlock_reverse, "flag [Unlock Reverse] set to 'Y'",
                           TypeNomLogiqueInfoPASMES.UNLOCK_DL_REVERSE, should_be_vital=True) is False:
            success = False

    if success is True:
        print_log(f"No KO.")


def _rule_3_check_switch(sw_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.AIGUILLE}...")
    sw_dict = load_sheet(DCSYS.Aig)
    success = True
    for sw_name, sw in sw_dict.items():
        free_to_move = get_dc_sys_value(sw, DCSYS.Aig.FreeToMove) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Aig, sw_msg_dict, sw_name, free_to_move, "flag [Free To Move] set to 'Y'",
                           TypeNomLogiqueInfoPASMES.CBTC_FREE_TO_MOVE, should_be_vital=True) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_protection_zone(pz_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.PROTECTION_ZONE}...")
    pz_dict = load_sheet(DCSYS.Protection_Zone)
    success = True
    for pz_name, pz in pz_dict.items():
        cbtc_controlled = get_dc_sys_value(pz, DCSYS.Protection_Zone.CbtcControlledFlag) == YesOrNo.O
        if _check_obj_msgs(DCSYS.Protection_Zone, pz_msg_dict, pz_name, cbtc_controlled,
                           "flag [CBTC Controlled] set to 'Y'", TypeNomLogiqueInfoPASMES.MOVEMENT_AUTHORIZED,
                           should_be_vital=True) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_tpz(tpz_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.SS}...")
    tpz_dict = load_sheet(DCSYS.SS)
    success = True
    for tpz_name, tpz in tpz_dict.items():
        if _check_obj_msgs(DCSYS.SS, tpz_msg_dict, tpz_name, True, "should exist for all Traction Power Zone",
                           TypeNomLogiqueInfoPASMES.POWER_AUTHORIZED, should_be_vital=True) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_cross_call(cross_call_msg_dict: dict):
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.CROSSING_CALLING_AREA}...")
    cross_call_dict = load_sheet(DCSYS.Crossing_Calling_Area)
    success = True
    for cross_call_name, cross_call in cross_call_dict.items():
        if _check_obj_msgs(DCSYS.SS, cross_call_msg_dict, cross_call_name, True,
                           "should exist for all Crossing Calling Area",
                           TypeNomLogiqueInfoPASMES.CROSSING_AUTH_REQUEST,
                           should_be_vital=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_3_check_tsr_area_speed(tsr_area_speed_msg_dict: dict):
    list_of_speeds = ["Speed_0", "Speed_5", "Speed_10",
                      "Speed_20", "Speed_25", "Speed_30", "Speed_35", "Speed_40", "Speed_45",
                      "Speed_50", "Speed_55", "Speed_60", "Speed_65", "Speed_70", "Speed_75", "Speed_80"]
    print_section_title(f"\nChecking {TypeClasseObjetPASMES.TSR_PREDEFINED_AREA_SPEED}...")
    tsr_interfaced_with_vhmi = get_param_value("tsr_interfaced_with_VHMI")
    tsr_area_dict = load_sheet(DCSYS.TSR_Area)
    missing_speeds_dict = {key: {speed: False for speed in list_of_speeds} for key in tsr_area_dict}
    tsr_speed_dict = load_sheet(DCSYS.TSR_Possible_Speeds)
    wayside_eqpt_dict = load_sheet(DCSYS.Wayside_Eqpt)
    success = True
    for tsr_area_name, tsr_area in tsr_area_dict.items():
        tsr_area_missing_speeds = list()
        for tsr_speed in tsr_speed_dict.keys():
            tsr_area_speed_name = tsr_area_name + "_" + tsr_speed
            for zc_name in get_all_zc():
                is_zc_zcr = get_dc_sys_value(wayside_eqpt_dict[zc_name], DCSYS.Wayside_Eqpt.Function.Zcr)[0] \
                                == YesOrNo.O
                zcr_and_interfaced_with_hmi = is_zc_zcr and tsr_interfaced_with_vhmi
                if _check_obj_msgs(DCSYS.TSR_Area, tsr_area_speed_msg_dict, tsr_area_speed_name,
                                   zcr_and_interfaced_with_hmi, f"message transmitter {zc_name} is a ZCR "
                                   f"and [tsr_interfaced_with_VHMI] = true",
                                   TypeNomLogiqueInfoPASMES.TSR_AREA_SPEED_SUPERVISION, should_be_vital=True,
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
    csv = "TSR_Area;" + ";".join(list_of_speeds) + "\n"
    for tsr_area, speed_dict in missing_speeds_dict.items():
        csv += f"{tsr_area};"
        for is_missing in speed_dict.values():
            csv += f"{'Missing' if is_missing else ''};"
        csv += "\n"
    print(csv)
    if success is True:
        print_log(f"No KO.")


# ------- Common Sub Functions to test flows ------- #
def _check_obj_msgs(obj_type, msg_dict: dict, obj_name: str, condition: bool, condition_str: str,
                    target_msg_types: Union[str, list[str]], should_be_vital: bool,
                    is_flux_pas_mes: bool = True, vital_condition: bool = None, vital_condition_str: str = None,
                    obj_type_str: str = None, zc: str = None, tsr_speed: str = None,
                    tsr_area_missing_speeds: list = None):
    if not isinstance(target_msg_types, list):
        target_msg_types = [target_msg_types]
    if obj_type_str is None:
        obj_type_str = get_sh_name(obj_type)
    is_tsr_area_speed = tsr_area_missing_speeds is not None

    obj_class = DCSYS.Flux_PAS_MES if is_flux_pas_mes else DCSYS.Flux_MES_PAS

    associated_msgs = {msg_name: msg_info for msg_name, msg_info in msg_dict.items()
                       if get_dc_sys_value(msg_info, obj_class.NomObjet) == obj_name
                       and get_dc_sys_value(msg_info, obj_class.NomLogiqueInfo) in target_msg_types}

    if zc is not None:
        # We only check the messages related to this ZC
        associated_msgs = {msg_name: msg_info for msg_name, msg_info in associated_msgs.items()
                           if get_dc_sys_value(msg_info, obj_class.PasUtilisateur1) == zc}

    success = True
    if not condition:
        if associated_msgs:
            for target_msg_type in target_msg_types:
                associated_msg = {msg_name: msg_info for msg_name, msg_info in associated_msgs.items()
                                  if get_dc_sys_value(msg_info, obj_class.NomLogiqueInfo) == target_msg_type}
                if zc is None:
                    _check_message_zc(obj_type, obj_name, associated_msg, obj_type_str, target_msg_type,
                                      condition, condition_str, should_be_vital, is_flux_pas_mes)
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
            if is_tsr_area_speed:
                tsr_area_missing_speeds.append(tsr_speed)
                success = False
                continue
            print_error(f"A flow of type {Color.yellow}{target_msg_type}{Color.reset} should be defined for "
                        f"{obj_type_str} {Color.blue}{obj_name}{Color.reset} "
                        f"as the condition {Color.white}{condition_str.replace(Color.reset, Color.reset + Color.white)}"
                        f"{Color.reset} is met")
            success = False
            continue
        if zc is None:
            if _check_message_zc(obj_type, obj_name, associated_msg, obj_type_str, target_msg_type,
                                 condition, condition_str, should_be_vital, is_flux_pas_mes) is False:
                success = False
        # In ZC Overlay, there would be a message for each ZC
        for associated_msg_name, associated_msg_info in associated_msg.items():
            is_msg_vital = get_dc_sys_value(associated_msg_info, obj_class.TypeInfo) == VitalOrNotType.SECU
            if is_msg_vital != should_be_vital:
                print_error(f"Flow {Color.beige}{associated_msg_name}{Color.reset} "
                            f"for {obj_type_str} {Color.blue}{obj_name}{Color.reset} "
                            f"of type {Color.yellow}{target_msg_type}{Color.reset} "
                            f"should be of type {Color.orange}"
                            f"{VitalOrNotType.SECU if should_be_vital else VitalOrNotType.FONC}{Color.reset} "
                            f"instead of {VitalOrNotType.SECU if is_msg_vital else VitalOrNotType.FONC}\n" +
                            (f"as the condition {Color.light_blue}{vital_condition_str}{Color.reset} is "
                             f"{'not ' if not vital_condition else ''}met\n"
                             if vital_condition is not None else "") +
                            f"(the condition {Color.white}"
                            f"{condition_str.replace(Color.reset, Color.reset + Color.white)}{Color.reset} is met):",
                            end="\n\t\t")
                print(associated_msg_info)
                success = False
    return success


def _check_message_zc(obj_type, obj_name: str, associated_msg, obj_type_str, target_msg_type,
                      condition: bool, condition_str: str, should_be_vital: bool, is_flux_pas_mes: bool):
    obj_class = DCSYS.Flux_PAS_MES if is_flux_pas_mes else DCSYS.Flux_MES_PAS
    success = True
    expected_zc_list = get_zc_of_obj(obj_type, obj_name)
    msg_zc_dict = dict()
    for associated_msg_name, associated_msg_info in associated_msg.items():
        zc_name = get_dc_sys_value(associated_msg_info, obj_class.PasUtilisateur1)
        if zc_name in msg_zc_dict:
            print_error(f"The flow of type {Color.yellow}{target_msg_type}{Color.reset} for "
                        f"{obj_type_str} {Color.blue}{obj_name}{Color.reset} is defined multiple times "
                        f"for the same ZC {zc_name}\n"
                        f"(the condition {Color.white}{condition_str.replace(Color.reset, Color.reset + Color.white)}"
                        f"{Color.reset} is {'not ' if condition else ''}met):")
            print(msg_zc_dict[zc_name])
            print(associated_msg_name)
            success = False
        msg_zc_dict[zc_name] = associated_msg_name
    extra_msg_zc = {zc_name: info for zc_name, info in msg_zc_dict.items() if zc_name not in expected_zc_list}
    missing_zc = [zc_name for zc_name in expected_zc_list if zc_name not in msg_zc_dict]

    if extra_msg_zc:
        print_warning(f"Useless flow(s) to be removed as {obj_type_str} {Color.blue}{obj_name}{Color.reset}"
                      f"is not in the ZC\n(but in {expected_zc_list})")
        for zc, msg in extra_msg_zc.items():
            print(f"\tin {Color.beige}{zc = }{Color.reset}: {msg}")
        success = False
    if missing_zc:
        pass
        # In case of ZC overlay, we often need that only one of the two ZC sends the signal.
        # Don't know when it is required that both sends the signal (maybe it is only when receiving from the IXL).
        # print_error(f"A flow of type {Color.yellow}{target_msg_type}{Color.reset} should be defined for "
        #             f"{obj_type_str} {Color.blue}{obj_name}{Color.reset} "
        #             f"for ZC {Color.pink}{missing_zc}{Color.reset} (object is in {expected_zc_list}).\n"
        #             f"It should be of type {Color.orange}"
        #             f"{VitalOrNotType.SECU if should_be_vital else VitalOrNotType.FONC}{Color.reset}\n"
        #             f"(the condition {Color.white}{condition_str.replace(Color.reset, Color.reset + Color.white)}"
        #             f"{Color.reset} is {'not ' if condition else ''}met).")

    return success
