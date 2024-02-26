#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from .survey_verification.check_survey_sheets import *


__all__ = ["SURVEY_TYPES_DICT"]


SURVEY_TYPES_DICT = {
    "SWP":           {"res_sheet": "Switch",
                      "dcsys_sh": DCSYS.Aig,
                      "func": check_switch,
                      "tol": "switch_tolerance",
                      "survey_type_names": ["SWP", "SWITCH", "SWITCH POINT"]},

    "PLATFORM":      {"res_sheet": "Platform",
                      "dcsys_sh": DCSYS.Quai,
                      "func": check_platform,
                      "tol": {get_sh_name(DCSYS.Quai): "platform_end_tolerance",
                              get_sh_name(DCSYS.Quai.PointDArret): "platform_osp_tolerance"},
                      "survey_type_names": ["PLATFORM", "PLATFORM END", "PLATFORM EXTREMITY", "MPLATFORM"],
                      "multiple_dc_sys_objets": [get_sh_name(DCSYS.Quai), get_sh_name(DCSYS.Quai.PointDArret)],
                      "multiple_survey_objets": [("PLATFORM", None, None), ("OSP", None, None)]},

    "OSP":           {"res_sheet": None,
                      "survey_type_names": ["OSP", "PAE", "PLATFORM_OSP"]},

    "TC":            {"res_sheet": "Block_Joint",
                      "dcsys_sh": DCSYS.CDV,
                      "func": check_joint,
                      "tol": "joint_tolerance",
                      "survey_type_names": ["TC", "TRACK CIRCUIT", "TRACK CIRCUITS JOINT",
                                            "AXLE COUNTER", "INSULATED JOINT"],
                      "multiple_survey_objets": [("TC", None, None), ("SIGNAL_BUFFER", None, None)]},

    "SIGNAL":        {"res_sheet": "Signal",
                      "dcsys_sh": DCSYS.Sig,
                      "func": check_object,
                      "tol": "signal_tolerance",
                      "survey_type_names": ["SIGNAL"]},

    "SIGNAL_BUFFER": {"res_sheet": "Buffer",
                      "dcsys_sh": DCSYS.Sig,
                      "func": check_object,
                      "tol": "buffer_tolerance",
                      "survey_type_names": ["SIGNAL_BUFFER", "BUFFER", "BS"]},

    "TAG":           {"res_sheet": "Tag",
                      "dcsys_sh": [DCSYS.Bal, DCSYS.IATPM_tags],
                      "func": check_tag,
                      "tol": "tag_tolerance",
                      "survey_type_names": ["TAG", "BAL", "BALISE", "TAGS", "FIXED BAL",
                                            "IATPM_TAG", "IATPM TAG", "IATPM TAGS", "IATP BAL"],
                      "multiple_dc_sys_objets": [get_sh_name(DCSYS.Bal), get_sh_name(DCSYS.IATPM_tags),
                                                 get_sh_name(DCSYS.IATPM_Version_Tags)],
                      "multiple_survey_objets": [("TAG", None, 5), ("TAG", 5, None), ("VERSION TAG", None, None)]},

    "VERSION TAG":   {"res_sheet": None,
                      "survey_type_names": ["VERSION TAG", "VERSION TAGS", "IATPM VERSION TAG", "IATPM VERSION TAGS",
                                            "IATP VERSION TAG", "IATP VERSION TAGS", "IATP VERSION"]},

    "FLOOD_GATE":    {"res_sheet": "FloodGate",
                      "dcsys_sh": DCSYS.Flood_Gate,
                      "func": check_flood_gate,
                      "tol": "flood_gate_tolerance",
                      "survey_type_names": ["FLOOD_GATE", "FLOODGATE", "FLOOD GATE"]},
}
