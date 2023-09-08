#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ..load_database import *


__all__ = ["VitalOrNotType",
           "TypeClasseObjetVariantHF", "TypeClasseObjetVariantBF",
           "TypeClasseObjetMESPAS", "TypeClasseObjetPASMES",
           "TypeNomLogiqueVariantHF", "TypeNomLogiqueVariantBF",
           "TypeNomLogiqueInfoMESPAS", "TypeNomLogiqueInfoPASMES",
           "get_sub_dict_hf_general_data", "get_sub_dict_lf_general_data",
           "get_sub_dict_ixl_zc_itf", "get_sub_dict_zc_ixl_itf"]


class VitalOrNotType:
    FONC = "FONC"
    SECU = "SECU"


class TypeClasseObjetVariantHF:
    AIGUILLE = "AIGUILLE"
    SIGNAL = "SIGNAL"
    QUAI = "QUAI"
    ZAUM = "ZAUM"
    FLOOD_GATE = "FLOOD_GATE"
    BLOCK = "BLOCK"
    ASR = "ASR"


class TypeClasseObjetVariantBF:
    SIGNAL = "SIGNAL"
    QUAI = "QUAI"
    ZAUM = "ZAUM"
    NV_PSR = "NV_PSR"


class TypeClasseObjetMESPAS:
    AIGUILLE = "AIGUILLE"
    SIGNAL = "SIGNAL"
    DP = "DP"
    CDV = "CDV"
    QUAI = "QUAI"
    SS = "SS"
    IXL_OVERLAP = "IXL_OVERLAP"
    PROTECTION_ZONE = "PROTECTION_ZONE"
    FLOOD_GATE = "FLOOD_GATE"
    IVB = "IVB"
    ASR = "ASR"
    TRAFFIC_STOP = "TRAFFIC_STOP"
    TSR_PREDEFINED_AREA = "TSR_PREDEFINED_AREA"
    PASSAGE_DETECTOR = "PASSAGE_DETECTOR"


class TypeClasseObjetPASMES:
    AIGUILLE = "AIGUILLE"
    SIGNAL = "SIGNAL"
    CDV = "CDV"
    QUAI = "QUAI"
    SS = "SS"
    IVB = "IVB"
    CROSSING_CALLING_AREA = "CROSSING_CALLING_AREA"
    PROTECTION_ZONE = "PROTECTION_ZONE"
    TSR_PREDEFINED_AREA_SPEED = "TSR_PREDEFINED_AREA_SPEED"


class TypeNomLogiqueVariantHF:
    SW_RIGHT_C = "SW_RIGHT_C"
    SW_LEFT_C = "SW_LEFT_C"
    PR_ASPECT = "PR_ASPECT"
    IL_SET = "IL_SET"
    PLATFORM_ACCESS = "PLATFORM_ACCESS"
    ATB_DEP = "ATB_DEP"
    ATB_CAN_DEP = "ATB_CAN_DEP"
    MVT_AUTH = "MVT_AUTH"
    TRACTION_PWR_REGEN_AUTH = "TRACTION_PWR_REGEN_AUTH"
    UTO_MVT_AUTH = "UTO_MVT_AUTH"
    OPEN_AND_LOCKED = "OPEN_AND_LOCKED"
    FUNC_STOP_RQ = "FUNC_STOP_RQ"
    BLOCK_MVT_AUTH = "BLOCK_MVT_AUTH"
    AM_MVT_AUTH = "AM_MVT_AUTH"
    ASR_NOT_APPLIED = "ASR_NOT_APPLIED"


class TypeNomLogiqueVariantBF:
    FAILED_ZONE = "FAILED_ZONE"
    T_ATP_MD_PROHIB_REVERSE_DIR = "T_ATP_MD_PROHIB_REVERSE_DIR"
    T_AD_PROHIB_REVERSE_DIR = "T_AD_PROHIB_REVERSE_DIR"
    T_ATB_PROHIB_REVERSE_DIR = "T_ATB_PROHIB_REVERSE_DIR"
    T_ATP_MD_PROHIB_NORMAL_DIR = "T_ATP_MD_PROHIB_NORMAL_DIR"
    T_AD_PROHIB_NORMAL_DIR = "T_AD_PROHIB_NORMAL_DIR"
    T_ATB_PROHIB_NORMAL_DIR = "T_ATB_PROHIB_NORMAL_DIR"
    PROTECTION_LEVEL = "PROTECTION_LEVEL"
    TRAIN_HOLD_NORMAL_DIR = "TRAIN_HOLD_NORMAL_DIR"
    TRAIN_HOLD_REVERSE_DIR = "TRAIN_HOLD_REVERSE_DIR"
    TRAIN_AHEAD_DEPARTURE = "TRAIN_AHEAD_DEPARTURE"
    SAFETY_RELATED_PLATFORM_HOLD_NORMAL_DIR = "SAFETY_RELATED_PLATFORM_HOLD_NORMAL_DIR"
    SAFETY_RELATED_PLATFORM_HOLD_REVERSE_DIR = "SAFETY_RELATED_PLATFORM_HOLD_REVERSE_DIR"
    SAFETY_RELATED_PLATFORM_SKIP_REVERSE_DIR = "SAFETY_RELATED_PLATFORM_SKIP_REVERSE_DIR"
    SAFETY_RELATED_PLATFORM_SKIP_NORMAL_DIR = "SAFETY_RELATED_PLATFORM_SKIP_NORMAL_DIR"
    NV_PSR_RELAXATION_CONDITION = "NV_PSR_RELAXATION_CONDITION"
    PLATFORM_SKIP_NORMAL_DIR = "PLATFORM_SKIP_NORMAL_DIR"
    PLATFORM_SKIP_REVERSE_DIR = "PLATFORM_SKIP_REVERSE_DIR"


class TypeNomLogiqueInfoMESPAS:
    BLOCK = "BLOCK"
    SW_RIGHT_C = "SW_RIGHT_C"
    SW_LEFT_C = "SW_LEFT_C"
    IL_SET = "IL_SET"
    B_ESS = "B_ESS"
    PR_ASPECT = "PR_ASPECT"
    AP_CAN_RQ = "AP_CAN_RQ"
    B_TH = "B_TH"
    B_TAD = "B_TAD"
    DEPARTURE_AUTH = "DEPARTURE_AUTH"
    BLOCK_NORMAL_DIRECTION_L = "BLOCK_NORMAL_DIRECTION_L"
    BLOCK_REVERSE_DIRECTION_L = "BLOCK_REVERSE_DIRECTION_L"
    DD = "DD"
    TRACTION_PWR_REGEN_AUTH = "TRACTION_PWR_REGEN_AUTH"
    PROTECTION_LEVEL = "PROTECTION_LEVEL"
    B_ATB = "B_ATB"
    OLZ_OVERLAP_LK = "OLZ_OVERLAP_LK"
    MVT_AUTH = "MVT_AUTH"
    OPEN_AND_LOCKED = "OPEN_AND_LOCKED"
    FUNC_STOP_RQ = "FUNC_STOP_RQ"
    ASR_NOT_APPLIED = "ASR_NOT_APPLIED"
    UTO_MVT_AUTH = "UTO_MVT_AUTH"
    BLOCK_INIT_STATUS = "BLOCK_INIT_STATUS"
    STOP = "STOP"
    BLOCK_NOT_HELD = "BLOCK_NOT_HELD"
    TSR_AREA_SPEED_SET_CMD = "TSR_AREA_SPEED_SET_CMD"
    TSR_AREA_SPEED_REMOVE_CMD = "TSR_AREA_SPEED_REMOVE_CMD"
    NO_PASSAGE = "NO_PASSAGE"


class TypeNomLogiqueInfoPASMES:
    ZC_BLOCK = "ZC_BLOCK"
    TRAIN_PASS_HS = "TRAIN_PASS_HS"
    CBTC_APZ = "CBTC_APZ"
    STOP_ASSURE = "STOP_ASSURE"
    X_RQ = "X_RQ"
    TRAIN_AT_PLATFORM = "TRAIN_AT_PLATFORM"
    OPEN_CMD_L = "OPEN_CMD_L"
    OPEN_CMD_R = "OPEN_CMD_R"
    CLOSE_CMD_L = "CLOSE_CMD_L"
    CLOSE_CMD_R = "CLOSE_CMD_R"
    CBTC_OLZ = "CBTC_OLZ"
    TRAIN_IN_BERTH = "TRAIN_IN_BERTH"
    IXL_VIRTUAL_BLOCK = "IXL_VIRTUAL_BLOCK"
    BLOCK_FREED = "BLOCK_FREED"
    AUTHORIZED_NORMAL = "AUTHORIZED_NORMAL"
    AUTHORIZED_REVERSE = "AUTHORIZED_REVERSE"
    FUNC_STOP_ACCEPT = "FUNC_STOP_ACCEPT"
    FUNC_STOP_REJECT = "FUNC_STOP_REJECT"
    UNLOCK_DL_NORMAL = "UNLOCK_DL_NORMAL"
    UNLOCK_DL_REVERSE = "UNLOCK_DL_REVERSE"
    CBTC_FREE_TO_MOVE = "CBTC_FREE_TO_MOVE"
    CBTC_TRAIN_IN_APPROACH = "CBTC_TRAIN_IN_APPROACH"
    MOVEMENT_AUTHORIZED = "MOVEMENT_AUTHORIZED"
    POWER_AUTHORIZED = "POWER_AUTHORIZED"
    CROSSING_AUTH_REQUEST = "CROSSING_AUTH_REQUEST"
    TSR_AREA_SPEED_SUPERVISION = "TSR_AREA_SPEED_SUPERVISION"


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
