#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from .survey_verification.check_survey_sheets import *


__all__ = ["SURVEY_TYPES_DICT"]


def _add_other_spaces_names(names_list: list[str]) -> list[str]:
    res_list = names_list
    for name in names_list:
        if "_" in name:
            res_list.append(name.replace("_", " "))
            res_list.append(name.replace("_", ""))
    for name in res_list:
        if "Xth" in name:
            res_list.remove(name)
            res_list.append(name.replace("Xth", "1ST"))
            res_list.append(name.replace("Xth", "2ND"))
            for n in range(3, 13):
                res_list.append(name.replace("Xth", f"{n}TH"))
    return res_list


SURVEY_TYPES_DICT = {
    "SWP":               {"res_sheet": "Switch",
                          "dcsys_sheet": DCSYS.Aig,
                          "func": check_switch,
                          "tol": ("switches", "switch_tolerance", 0.006),
                          "survey_type_names": _add_other_spaces_names([
                              "SWP", "SWITCH", "SWITCH_POINT",
                          ]),
                          "display_name": "Switches",
                          },
    "PLATFORM":          {"res_sheet": "Platform",
                          "dcsys_sheet": DCSYS.Quai,
                          "func": check_platform,
                          "tol": {
                              ((get_sheet_name(DCSYS.Quai),), "PLATFORM"):
                                  ("platform ends", "platform_end_tolerance", 0.006),
                              ((get_sheet_name(DCSYS.Quai.PointDArret),
                                get_sheet_name(DCSYS.PtA)), "OSP"):
                                  ("OSPs", "osp_tolerance", 0.006)},
                          "survey_type_names": _add_other_spaces_names([
                              "PLATFORM", "PLATFORM_END", "PLATFORM_EXTREMITY", "BOARDING_PLATFORM",
                          ]),
                          "multiple_dc_sys_objets": [get_sheet_name(DCSYS.Quai),
                                                     get_sheet_name(DCSYS.Quai.PointDArret),
                                                     get_sheet_name(DCSYS.PtA)],
                          "multiple_survey_objets": ["PLATFORM",
                                                     "OSP",
                                                     "MIDDLE_PLATFORM",],
                          "display_name": "Platform ends and OSPs",
                          "dc_sys_display_names": [((get_sheet_name(DCSYS.Quai),), "Platform ends"),
                                                   ((get_sheet_name(DCSYS.Quai.PointDArret),
                                                     get_sheet_name(DCSYS.PtA)), "OSPs")],
                          "survey_display_names": [(("PLATFORM",), "Platform ends"),
                                                   (("OSP",), "OSPs")],
                          "extra_defined_name":  ("Length of the platforms:", "platform_length", None,
                                                  "Used to compute platform extremity position from middle platform."),
                          },
    "MIDDLE_PLATFORM":   {"res_sheet": None,
                          "survey_type_names": _add_other_spaces_names([
                              "MPLATFORM", "PLATFORM_CENTER", "PFC",
                          ]),
                          },
    "OSP":               {"res_sheet": None,
                          "survey_type_names": _add_other_spaces_names([
                              "OSP", "PAE", "PLATFORM_OSP", "PSD_Xth_DOOR_CENTER",
                              "OUT_PLATFORM_OSP", "OSP_OUTP",
                          ]),
                          },
    "BLOCK":             {"res_sheet": "Block",
                          "dcsys_sheet": DCSYS.CDV,
                          "func": check_joint,
                          "tol": ("joints", "joint_tolerance", 0.006),
                          "survey_type_names": _add_other_spaces_names([
                              "BLOCK", "TC", "TRACK_CIRCUIT", "TRACK_CIRCUITS_JOINT", "TRACK_CIRCUIT_JOINT",
                              "AXC", "AXLE_COUNTER", "IJ", "INSULATED_JOINT", "AXLE_COUNTER_DP",
                          ]),
                          "multiple_survey_objets": ["BLOCK",
                                                     "BUFFER",
                                                     ("SIGNAL", "PERMANENT_RED")],
                          "display_name": "Blocks",
                          },
    "SIGNAL":            {"res_sheet": "Signal",
                          "dcsys_sheet": DCSYS.Sig,
                          "func": check_signal,
                          "tol": {
                              ((get_sheet_name(DCSYS.Sig) + f"__{SignalType.MANOEUVRE}",
                                get_sheet_name(DCSYS.Sig) + f"__{SignalType.PERMANENT_ARRET}",
                                get_sheet_name(DCSYS.Sig) + f"__{SignalType.ESPACEMENT}"), "SIGNAL"):
                                    ("signals", "signal_tolerance", 0.006),
                              ((get_sheet_name(DCSYS.Sig) + f"__{SignalType.HEURTOIR}",), "BUFFER"):
                                    ("buffers", "buffer_tolerance", 0.006)},
                          "survey_type_names": _add_other_spaces_names([
                              "SIG", "SIGNAL", "SIGN",
                          ]),
                          "multiple_dc_sys_objets": [get_sheet_name(DCSYS.Sig) + f"__{SignalType.MANOEUVRE}",
                                                     get_sheet_name(DCSYS.Sig) + f"__{SignalType.PERMANENT_ARRET}",
                                                     get_sheet_name(DCSYS.Sig) + f"__{SignalType.ESPACEMENT}",
                                                     get_sheet_name(DCSYS.Sig) + f"__{SignalType.HEURTOIR}"],
                          "multiple_survey_objets": ["SIGNAL",
                                                     "BUFFER",
                                                     "PERMANENT_RED"],
                          "display_name": "Signals and Buffers",
                          "dc_sys_display_names": [((get_sheet_name(DCSYS.Sig) + f"__{SignalType.MANOEUVRE}",
                                                    get_sheet_name(DCSYS.Sig) + f"__{SignalType.PERMANENT_ARRET}",
                                                    get_sheet_name(DCSYS.Sig) + f"__{SignalType.ESPACEMENT}"),
                                                    "Signals"),
                                                   ((get_sheet_name(DCSYS.Sig) + f"__{SignalType.HEURTOIR}",),
                                                    "Buffers")],
                          "survey_display_names": [(("SIGNAL", "PERMANENT_RED"), "Signals"),
                                                   (("BUFFER",), "Buffers")],
                          },
    "PERMANENT_RED":     {"res_sheet": None,
                          "survey_type_names": _add_other_spaces_names([
                              "PERMANENT_RED", "BUFFER_RED_SIGNAL",
                          ]),
                          },
    "BUFFER":            {"res_sheet": None,
                          "survey_type_names": _add_other_spaces_names([
                              "BUFFER", "SIGNAL_BUFFER", "BS", "BUFFER_STOP", "BUFFER_STOP_SIGNAL",
                          ]),
                          },
    "TAG":               {"res_sheet": "Tag",
                          "dcsys_sheet": [DCSYS.Bal, DCSYS.IATPM_tags, DCSYS.IATPM_Version_Tags],
                          "func": check_tag,
                          "tol": ("tags", "tag_tolerance", 0.006),
                          "survey_type_names": _add_other_spaces_names([
                              "BAL", "BALISE", "TAG", "TAGS",
                              "FIXED_BAL", "FIXED_BALISE",
                              "FIXED_TAG", "FIXED_TAGS",
                          ]),
                          "multiple_dc_sys_objets": [get_sheet_name(DCSYS.Bal),
                                                     get_sheet_name(DCSYS.IATPM_tags),
                                                     get_sheet_name(DCSYS.IATPM_Version_Tags)],
                          "multiple_survey_objets": ["TAG",
                                                     "DYNAMIC_TAG",
                                                     "VERSION_TAG"],
                          "display_name": "Localization and Dynamic Tags",
                          "dc_sys_display_names": [((get_sheet_name(DCSYS.Bal),), "Localization Tags"),
                                                   ((get_sheet_name(DCSYS.IATPM_tags),), "Dynamic Tags")],
                          },
    "DYNAMIC_TAG":       {"res_sheet": None,
                          "survey_type_names": _add_other_spaces_names([
                              "IATPM_BAL", "IATPM_BALISE", "IATP_BAL", "IATP_BALISE",
                              "IATPM_TAG", "IATPM_TAGS", "IATP_TAG", "IATP_TAGS",
                          ]),
                          },
    "VERSION_TAG":       {"res_sheet": None,
                          "survey_type_names": _add_other_spaces_names([
                              "VERSION_TAG", "VERSION_TAGS",
                              "IATPM_VERSION_TAG", "IATPM_VERSION_TAGS",
                              "IATP_VERSION_TAG", "IATP_VERSION_TAGS",
                              "IATPM_VERSION", "IATP_VERSION",
                          ]),
                          },
    "FLOOD_GATE":        {"res_sheet": "FloodGate",
                          "dcsys_sheet": DCSYS.Flood_Gate,
                          "func": check_flood_gate,
                          "tol": ("flood gates", "flood_gate_tolerance", 0.006),
                          "survey_type_names": _add_other_spaces_names([
                              "FLOOD_GATE", "FLOOD_GATES",
                          ]),
                          "display_name": "Flood Gates",
                          },
}
