#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from .survey_verification.check_survey_sheets import *


__all__ = ["SURVEY_TYPES_DICT"]


SURVEY_TYPES_DICT = {
    "SWP":           {"res_sheet": "Switch",
                      "dcsys_sh": DCSYS.Aig,
                      "func": check_switch,
                      "tol": "switch_tol",
                      "other_names": ["SWITCH", "SWITCH POINT"]},
    "PLATFORM":      {"res_sheet": "Platform",
                      "dcsys_sh": DCSYS.Quai,
                      "func": check_platform,
                      "tol": {get_sh_name(DCSYS.Quai): "platform_tol",
                              get_sh_name(DCSYS.Quai.PointDArret): "platform_osp_tol"},
                      "other_names": ["PLATFORM END", "PLATFORM EXTREMITY", "MPLATFORM"]},
    "OSP":           {"res_sheet": None,
                      "other_names": ["PAE", "PLATFORM_OSP"]},
    "TC":            {"res_sheet": "Block_Joint",
                      "dcsys_sh": DCSYS.CDV,
                      "func": check_joint,
                      "tol": "joint_tol",
                      "other_names": ["TRACK CIRCUIT", "TRACK CIRCUITS JOINT", "AXLE COUNTER", "INSULATED JOINT"]},
    "SIGNAL":        {"res_sheet": "Signal",
                      "dcsys_sh": DCSYS.Sig,
                      "func": check_object,
                      "tol": "signal_tol",
                      "other_names": []},
    "SIGNAL_BUFFER": {"res_sheet": "Buffer",
                      "dcsys_sh": DCSYS.Sig,
                      "func": check_object,
                      "tol": "buffer_tol",
                      "other_names": ["BUFFER", "BS"]},
    "TAG":           {"res_sheet": "Tag",
                      "dcsys_sh": [DCSYS.Bal, DCSYS.IATPM_tags],
                      "func": check_tag,
                      "tol": "tag_tol",
                      "other_names": ["BAL", "BALISE", "TAGS", "FIXED BAL",
                                      "IATPM_TAG", "IATPM TAG", "IATPM TAGS", "IATP BAL"]},
    "VERSION TAG":   {"res_sheet": None,
                      "other_names": ["VERSION TAGS", "IATPM VERSION TAG", "IATPM VERSION TAGS",
                                      "IATP VERSION TAG", "IATP VERSION TAGS", "IATP VERSION"]},
    "FLOOD_GATE":    {"res_sheet": "FloodGate",
                      "dcsys_sh": DCSYS.Flood_Gate,
                      "func": check_flood_gate,
                      "tol": "flood_gate_tol",
                      "other_names": ["FLOODGATE", "FLOOD GATE"]},
}
