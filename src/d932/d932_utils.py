#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import DCSYS
from .check_d932.check_survey_sheets import check_switch, check_platform, check_joints, check_object, check_flood_gate


SURVEY_TYPES_DICT = {
    "SWP":           {"res_sheet": "Switch",     "dcsys_sh": DCSYS.Aig,        "func": check_switch,
                      "tol": "switch_tol",
                      "other_names": ["SWITCH"]},
    "PLATFORM":      {"res_sheet": "Platform",   "dcsys_sh": DCSYS.Quai,       "func": check_platform,
                      "tol": "platform_tol",
                      "other_names": []},
    "TC":            {"res_sheet": "BlockJoint", "dcsys_sh": DCSYS.CDV,        "func": check_joints,
                      "tol": "joint_tol",
                      "other_names": []},
    "SIGNAL":        {"res_sheet": "Signal",     "dcsys_sh": DCSYS.Sig,        "func": check_object,
                      "tol": "signal_tol",
                      "other_names": []},
    "SIGNAL_BUFFER": {"res_sheet": "Buffer",     "dcsys_sh": DCSYS.Sig,        "func": check_object,
                      "tol": "buffer_tol",
                      "other_names": ["BUFFER"]},
    "TAG":           {"res_sheet": "Tag",        "dcsys_sh": DCSYS.Bal,        "func": check_object,
                      "tol": "tag_tol",
                      "other_names": []},
    "FLOOD_GATE":    {"res_sheet": "FloodGate",  "dcsys_sh": DCSYS.Flood_Gate, "func": check_flood_gate,
                      "tol": "flood_gate_tol",
                      "other_names": ["FLOODGATE"]},
}
