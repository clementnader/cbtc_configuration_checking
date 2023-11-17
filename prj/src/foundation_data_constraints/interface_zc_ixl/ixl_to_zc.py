#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_par import *
from .common_functions import *


__all__ = ["r_mes_pas_itf_1"]


LIST_OF_TSR_SPEEDS = ["Speed_0", "Speed_5", "Speed_10",
                      "Speed_20", "Speed_25", "Speed_30", "Speed_35", "Speed_40", "Speed_45",
                      "Speed_50", "Speed_55", "Speed_60", "Speed_65", "Speed_70", "Speed_75", "Speed_80"]


def r_mes_pas_itf_1(in_cbtc: bool = False):
    # IXL -> ZC Interface
    print_title(f"Verification of R_MES_PAS_ITF_1\nIXL -> ZC Interface", color=Color.mint_green)
    _rule_1_check_plt(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.QUAI), in_cbtc)
    _rule_1_check_signal(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.SIGNAL), in_cbtc)
    _rule_1_check_switch(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.AIGUILLE), in_cbtc)
    _rule_1_check_block(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.CDV), in_cbtc)
    _rule_1_check_ivb(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.IVB), in_cbtc)
    _rule_1_check_dd(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.DP), in_cbtc)
    if "PASSAGE_DETECTOR" in get_class_attr_dict(TypeClasseObjetMESPAS):
        _rule_1_check_passage_detector(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.PASSAGE_DETECTOR), in_cbtc)
    _rule_1_check_tpz(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.SS), in_cbtc)
    if "Isolation_Switch_Area" in get_class_attr_dict(DCSYS):
        if load_sheet(DCSYS.Isolation_Switch_Area):
            print_error(f"Isolation_Switch_Area sheet is not empty.")
    _rule_1_check_ovl(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.IXL_OVERLAP), in_cbtc)
    if "GES" in get_class_attr_dict(TypeClasseObjetMESPAS):
        _rule_1_check_ges(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.GES), in_cbtc)
    if "PROTECTION_ZONE" in get_class_attr_dict(TypeClasseObjetMESPAS):
        _rule_1_check_protection_zone(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.PROTECTION_ZONE), in_cbtc)
    _rule_1_check_flood_gate(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.FLOOD_GATE), in_cbtc)
    _rule_1_check_traffic_stop(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.TRAFFIC_STOP), in_cbtc)
    _rule_1_check_asr(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.ASR), in_cbtc)
    if "TSR_PREDEFINED_AREA" in get_class_attr_dict(TypeClasseObjetMESPAS):
        _rule_1_check_tsr_area(get_sub_dict_ixl_zc_itf(TypeClasseObjetMESPAS.TSR_PREDEFINED_AREA), in_cbtc)


# ------- Rule 1 (IXL -> ZC) Sub Functions ------- #
def _rule_1_check_plt(plt_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.QUAI}...")
    if not in_cbtc:
        plt_dict = load_sheet(DCSYS.Quai)
    else:
        plt_dict = get_platforms_in_cbtc_ter()
    success = True
    ws_eqpt_dict = load_sheet(DCSYS.Wayside_Eqpt)
    for plt_name, plt in plt_dict.items():
        related_ws_eqpt = get_dc_sys_value(plt, DCSYS.Quai.RelatedWaysideEquip)
        related_ws_eqpt_is_a_zc = (related_ws_eqpt is not None
                                   and get_dc_sys_value(ws_eqpt_dict[related_ws_eqpt],
                                                        DCSYS.Wayside_Eqpt.Function.Zc) == YesOrNo.O)

        if ("GIDS_LVL1_INTRUSION" in get_class_attr_dict(TypeNomLogiqueInfoMESPAS)
                and "GIDS_LVL2_INTRUSION" in get_class_attr_dict(TypeNomLogiqueInfoMESPAS)
                and "GIDS_NOT_ISOLATED" in get_class_attr_dict(TypeNomLogiqueInfoMESPAS)):
            with_gids = (get_dc_sys_value(plt, DCSYS.Quai.AvecSqv) and related_ws_eqpt_is_a_zc)
            if check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, with_gids,
                              f"flag [With GIDS] set to 'Y' and [Related Wayside Equip] {related_ws_eqpt} is a ZC",
                              TypeNomLogiqueInfoMESPAS.B_ATB, shall_be_vital=True, is_flux_pas_mes=False) is False:
                success = False

        atb_zones = [atb[0] for atb in get_atb_zone_related_to_plt(plt_name)]
        origin_atb_mvt = True if atb_zones else False
        if check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, origin_atb_mvt,
                          f"platform is origin of an ATB movement {atb_zones}", TypeNomLogiqueInfoMESPAS.B_ATB,
                          shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False

        with_ess = (get_dc_sys_value(plt, DCSYS.Quai.WithEss) == YesOrNo.O and related_ws_eqpt_is_a_zc)
        if check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, with_ess,
                          f"flag [With ESS] set to 'Y' and [Related Wayside Equip] {related_ws_eqpt} is a ZC",
                          TypeNomLogiqueInfoMESPAS.B_ESS, shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False

        with_th = get_dc_sys_value(plt, DCSYS.Quai.WithTh) == YesOrNo.O
        if check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, with_th, f"flag [With TH] set to 'Y'",
                          TypeNomLogiqueInfoMESPAS.B_TH, shall_be_vital=False, is_flux_pas_mes=False) is False:
            success = False

        with_tad = get_dc_sys_value(plt, DCSYS.Quai.WithTad) == YesOrNo.O
        if check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, with_tad, f"flag [With TAD] set to 'Y'",
                          TypeNomLogiqueInfoMESPAS.B_TAD, shall_be_vital=False, is_flux_pas_mes=False) is False:
            success = False

        if "PSD_ALARM" in get_class_attr_dict(TypeNomLogiqueInfoMESPAS):
            if check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, related_ws_eqpt_is_a_zc,
                              f"[Related Wayside Equip] {related_ws_eqpt} is a ZC", TypeNomLogiqueInfoMESPAS.PSD_ALARM,
                              shall_be_vital=True, is_flux_pas_mes=False) is False:
                success = False

        psd_msg_routed = get_dc_sys_value(plt, DCSYS.Quai.PsdMessagesRouted) == YesOrNo.O
        if check_obj_msgs(DCSYS.Quai, plt_msg_dict, plt_name, psd_msg_routed, f"flag [PSD Messages Routed] set to 'Y'",
                          TypeNomLogiqueInfoMESPAS.DEPARTURE_AUTH, shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_signal(sig_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.SIGNAL}...")
    if not in_cbtc:
        sig_dict = load_sheet(DCSYS.Sig)
    else:
        sig_dict = get_sigs_in_cbtc_ter()
    success = True
    for sig_name, sig in sig_dict.items():
        is_not_buffer_or_pr = get_dc_sys_value(sig, DCSYS.Sig.Type) not in [SignalType.HEURTOIR,
                                                                            SignalType.PERMANENT_ARRET]

        cbtc_terr_exit_or_with_iatp = (get_dc_sys_value(sig, DCSYS.Sig.SortieTerritoireCbtc) == YesOrNo.O
                                       or get_dc_sys_value(sig, DCSYS.Sig.WithIatpDepCheck) == YesOrNo.O)
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, is_not_buffer_or_pr,
                          "shall exist for all Signals (excluding buffers and permanent reds)",
                          TypeNomLogiqueInfoMESPAS.PR_ASPECT, shall_be_vital=cbtc_terr_exit_or_with_iatp,
                          is_flux_pas_mes=False, vital_condition=cbtc_terr_exit_or_with_iatp,
                          vital_condition_str="flag [CBTC Territory exit] set to 'Y' "
                                              "or flag [With IATP dep check] set to 'Y'") is False:
            success = False

        with_sa = is_not_buffer_or_pr and (get_dc_sys_value(sig, DCSYS.Sig.Du_Assistee) == YesOrNo.O)
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, with_sa, "flag [With SA] set to 'Y'",
                          TypeNomLogiqueInfoMESPAS.AP_CAN_RQ, shall_be_vital=False, is_flux_pas_mes=False) is False:
            success = False

        is_home_signal = get_dc_sys_value(sig, DCSYS.Sig.Type) == SignalType.MANOEUVRE
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, is_home_signal, "shall exist for all Home Signals",
                          TypeNomLogiqueInfoMESPAS.IL_SET, shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False

        func_stop = is_not_buffer_or_pr and (get_dc_sys_value(sig, DCSYS.Sig.WithFunc_Stop) == YesOrNo.O)
        if check_obj_msgs(DCSYS.Sig, sig_msg_dict, sig_name, func_stop, "flag [With Func Stop] set to 'Y'",
                          TypeNomLogiqueInfoMESPAS.FUNC_STOP_RQ, shall_be_vital=False, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_switch(sw_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.AIGUILLE}...")
    if not in_cbtc:
        sw_dict = load_sheet(DCSYS.Aig)
    else:
        sw_dict = get_switches_in_cbtc_ter()
    success = True
    for sw_name, sw in sw_dict.items():
        if check_obj_msgs(DCSYS.Aig, sw_msg_dict, sw_name, True, "shall exist for all switches",
                          [TypeNomLogiqueInfoMESPAS.SW_RIGHT_C,
                           TypeNomLogiqueInfoMESPAS.SW_LEFT_C], shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_block(block_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.CDV}...")
    if not in_cbtc:
        block_dict = load_sheet(DCSYS.CDV)
    else:
        block_dict = get_blocks_in_cbtc_ter()
    success = True
    for block_name, block in block_dict.items():
        if check_obj_msgs(DCSYS.CDV, block_msg_dict, block_name, True,
                          "shall exist for all CDV",
                          TypeNomLogiqueInfoMESPAS.BLOCK,
                          shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False

        block_not_held = get_dc_sys_value(block, DCSYS.CDV.IxlGivesNotHeldStatus) == YesOrNo.O
        if check_obj_msgs(DCSYS.CDV, block_msg_dict, block_name, block_not_held,
                          "flag [Block Not Held] set to 'Y'",
                          TypeNomLogiqueInfoMESPAS.BLOCK_NOT_HELD,
                          shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False

        block_init_status = get_dc_sys_value(block, DCSYS.CDV.IxlGivesBlockInitStatus) == YesOrNo.O
        if check_obj_msgs(DCSYS.CDV, block_msg_dict, block_name, block_init_status,
                          "flag [With Block Init Status Exchanged] set to 'Y'",
                          TypeNomLogiqueInfoMESPAS.BLOCK_INIT_STATUS,
                          shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_ivb(ivb_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.IVB}...")
    if not in_cbtc:
        ivb_dict = load_sheet(DCSYS.IVB)
    else:
        ivb_dict = get_ivb_in_cbtc_ter()
    success = True
    for ivb_name, ivb in ivb_dict.items():
        direction_locking_block = get_dc_sys_value(ivb, DCSYS.IVB.DirectionLockingBlock) == YesOrNo.O
        if check_obj_msgs(DCSYS.IVB, ivb_msg_dict, ivb_name, direction_locking_block,
                          "flag [Direction Locking Block] set to 'Y'",
                          [TypeNomLogiqueInfoMESPAS.BLOCK_NORMAL_DIRECTION_L,
                           TypeNomLogiqueInfoMESPAS.BLOCK_REVERSE_DIRECTION_L],
                          shall_be_vital=True,
                          is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_dd(dd_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.DP}...")
    if not in_cbtc:
        dd_dict = load_sheet(DCSYS.DP)
    else:
        dd_dict = get_dd_in_cbtc_ter()
    success = True
    for dd_name, dd in dd_dict.items():
        if check_obj_msgs(DCSYS.DP, dd_msg_dict, dd_name, True, "shall exist for all Discrete Detectors",
                          TypeNomLogiqueInfoMESPAS.DD, shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_passage_detector(pass_det_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.PASSAGE_DETECTOR}...")
    if not in_cbtc:
        pass_det_dict = load_sheet(DCSYS.Passage_Detector)
    else:
        pass_det_dict = get_passage_detectors_in_cbtc_ter()
    success = True
    for pass_det_name, pass_det in pass_det_dict.items():
        if check_obj_msgs(DCSYS.Passage_Detector, pass_det_msg_dict, pass_det_name, True,
                          "shall exist for all Passage Detectors", TypeNomLogiqueInfoMESPAS.NO_PASSAGE,
                          shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_tpz(tpz_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.SS}...")
    if not in_cbtc:
        tpz_dict = load_sheet(DCSYS.SS)
    else:
        tpz_dict = get_traction_power_zones_in_cbtc_ter()
    success = True
    target_msg_types = (TypeNomLogiqueInfoMESPAS.TRACTION_PWR_REGEN_AUTH
                        if ("MVT_AUTH" not in get_class_attr_dict(TypeNomLogiqueInfoMESPAS)
                            or "UTO_MVT_AUTH" not in get_class_attr_dict(TypeNomLogiqueInfoMESPAS)
                            or "PROTECTION_LEVEL" not in get_class_attr_dict(TypeNomLogiqueInfoMESPAS))
                        else [TypeNomLogiqueInfoMESPAS.TRACTION_PWR_REGEN_AUTH,
                              TypeNomLogiqueInfoMESPAS.MVT_AUTH,
                              TypeNomLogiqueInfoMESPAS.UTO_MVT_AUTH,
                              TypeNomLogiqueInfoMESPAS.PROTECTION_LEVEL])
    for tpz_name, tpz in tpz_dict.items():
        if check_obj_msgs(DCSYS.SS, tpz_msg_dict, tpz_name, True, "shall exist for all Traction Power Zones",
                          target_msg_types, shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_ovl(ovl_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.IXL_OVERLAP}...")
    if not in_cbtc:
        ovl_dict = load_sheet(DCSYS.IXL_Overlap)
    else:
        ovl_dict = get_overlaps_in_cbtc_ter()
    sig_dict = load_sheet(DCSYS.Sig)
    success = True
    for ovl_name, ovl in ovl_dict.items():
        related_sig = get_dc_sys_value(ovl, DCSYS.IXL_Overlap.DestinationSignal)
        with_overlap = (get_dc_sys_value(sig_dict[related_sig], DCSYS.Sig.Enc_Dep) == YesOrNo.O
                        and get_dc_sys_value(sig_dict[related_sig], DCSYS.Sig.OverlapType) == Edep_Type.NO_CBTC_REQUEST)
        if check_obj_msgs(DCSYS.IXL_Overlap, ovl_msg_dict, ovl_name, with_overlap,
                          f"signal upstream the overlap ({related_sig}) has flag [With overlap] set to 'Y' "
                          f"and [Overlap Type] = 'NO_CBTC_REQUEST'", TypeNomLogiqueInfoMESPAS.OLZ_OVERLAP_LK,
                          shall_be_vital=True, only_one_zc=True, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_ges(ges_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.GES}...")
    if not in_cbtc:
        ges_dict = load_sheet(DCSYS.GES)
    else:
        ges_dict = get_ges_in_cbtc_ter()
    success = True
    for ges_name, ges in ges_dict.items():
        if check_obj_msgs(DCSYS.GES, ges_msg_dict, ges_name, True, "shall exist for all GES",
                          TypeNomLogiqueInfoMESPAS.GES, shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_protection_zone(pz_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.PROTECTION_ZONE}...")
    if not in_cbtc:
        pz_dict = load_sheet(DCSYS.Protection_Zone)
    else:
        pz_dict = get_protection_zones_in_cbtc_ter()
    success = True
    for pz_name, pz in pz_dict.items():
        if check_obj_msgs(DCSYS.Protection_Zone, pz_msg_dict, pz_name, True,
                          "shall exist for all Protection Zones",
                          TypeNomLogiqueInfoMESPAS.MVT_AUTH,
                          shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_flood_gate(fg_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.FLOOD_GATE}...")
    if not in_cbtc:
        fg_dict = load_sheet(DCSYS.Flood_Gate)
    else:
        fg_dict = get_flood_gates_in_cbtc_ter()
    success = True
    for fg_name, fg in fg_dict.items():
        if check_obj_msgs(DCSYS.Flood_Gate, fg_msg_dict, fg_name, True,
                          "shall exist for all Flood Gates",
                          TypeNomLogiqueInfoMESPAS.OPEN_AND_LOCKED,
                          shall_be_vital=True, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_traffic_stop(stop_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.TRAFFIC_STOP}...")
    if not in_cbtc:
        stop_dict = load_sheet(DCSYS.Traffic_Stop)
    else:
        stop_dict = get_traffic_stops_in_cbtc_ter()
    success = True
    for stop_name, stop in stop_dict.items():
        if check_obj_msgs(DCSYS.Traffic_Stop, stop_msg_dict, stop_name, True,
                          "shall exist for all Traffic Stops",
                          TypeNomLogiqueInfoMESPAS.STOP,
                          shall_be_vital=False, is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_asr(asr_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.ASR}...")
    if not in_cbtc:
        asr_dict = load_sheet(DCSYS.ASR)
    else:
        asr_dict = get_asr_in_cbtc_ter()
    success = True
    for asr_name, asr in asr_dict.items():
        if check_obj_msgs(DCSYS.ASR, asr_msg_dict, asr_name, True,
                          "shall exist for all ASR",
                          TypeNomLogiqueInfoMESPAS.ASR_NOT_APPLIED,
                          shall_be_vital=True,
                          is_flux_pas_mes=False) is False:
            success = False
    if success is True:
        print_log(f"No KO.")


def _rule_1_check_tsr_area(tsr_area_msg_dict: dict, in_cbtc: bool):
    print_section_title(f"\nChecking {TypeClasseObjetMESPAS.TSR_PREDEFINED_AREA}...")
    tsr_interfaced_with_vhmi = get_param_value("tsr_interfaced_with_VHMI")
    if not in_cbtc:
        tsr_area_dict = load_sheet(DCSYS.TSR_Area)
    else:
        tsr_area_dict = get_tsr_area_in_cbtc_ter()
    missing_speeds_dict = {key: {speed: False for speed in LIST_OF_TSR_SPEEDS} for key in tsr_area_dict}
    tsr_speed_dict = load_sheet(DCSYS.TSR_Possible_Speeds)
    wayside_eqpt_dict = load_sheet(DCSYS.Wayside_Eqpt)
    success = True
    for tsr_area_name, tsr_area in tsr_area_dict.items():
        tsr_area_missing_speeds_for_set_cmd = list()
        tsr_area_missing_speeds_for_remove_cmd = list()
        for tsr_speed in tsr_speed_dict.keys():
            tsr_area_speed_name = tsr_area_name + "_" + tsr_speed
            for zc_name in get_all_zc():
                is_zc_zcr = get_dc_sys_value(wayside_eqpt_dict[zc_name], DCSYS.Wayside_Eqpt.Function.Zcr) == YesOrNo.O
                zcr_and_interfaced_with_hmi = is_zc_zcr and tsr_interfaced_with_vhmi

                if check_obj_msgs(DCSYS.TSR_Area, tsr_area_msg_dict, tsr_area_speed_name, zcr_and_interfaced_with_hmi,
                                  f"message transmitter {zc_name} is a ZCR "
                                  f"and [tsr_interfaced_with_VHMI] = true",
                                  TypeNomLogiqueInfoMESPAS.TSR_AREA_SPEED_SET_CMD,
                                  shall_be_vital=False,
                                  is_flux_pas_mes=False,
                                  obj_type_str="TSR_Area_Possible_Speeds",
                                  zc=zc_name,
                                  tsr_speed=tsr_speed,
                                  tsr_area_missing_speeds=tsr_area_missing_speeds_for_set_cmd) is False:
                    success = False

                if check_obj_msgs(DCSYS.TSR_Area, tsr_area_msg_dict, tsr_area_speed_name, zcr_and_interfaced_with_hmi,
                                  f"message transmitter {zc_name} is a ZCR "
                                  f"and [tsr_interfaced_with_VHMI] = true",
                                  TypeNomLogiqueInfoMESPAS.TSR_AREA_SPEED_REMOVE_CMD,
                                  shall_be_vital=True,
                                  is_flux_pas_mes=False,
                                  obj_type_str="TSR_Area_Possible_Speeds",
                                  zc=zc_name,
                                  tsr_speed=tsr_speed,
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
    csv = "TSR_Area;" + ";".join(LIST_OF_TSR_SPEEDS) + "\n"
    for tsr_area, speed_dict in missing_speeds_dict.items():
        csv += f"{tsr_area};"
        for is_missing in speed_dict.values():
            csv += f"{'Missing' if is_missing else ''};"
        csv += "\n"
    print(csv)
    if success is True:
        print_log(f"No KO.")
