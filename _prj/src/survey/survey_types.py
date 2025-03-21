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
    return res_list


SURVEY_TYPES_DICT = {
    "SWP":               {"res_sheet": "Switch",
                          "dcsys_sh": DCSYS.Aig,
                          "func": check_switch,
                          "tol": ("switches", "switch_tolerance", 0.006),
                          "survey_type_names": _add_other_spaces_names([
                              "SWP", "SWITCH", "SWITCH_POINT",
                          ]),
                          "display_name": "Switches",
                          },
    "PLATFORM":          {"res_sheet": "Platform",
                          "dcsys_sh": DCSYS.Quai,
                          "func": check_platform,
                          "tol": {
                              ((get_sh_name(DCSYS.Quai),), "PLATFORM"):
                                  ("platform ends", "platform_end_tolerance", 0.006),
                              ((get_sh_name(DCSYS.Quai.PointDArret),
                                get_sh_name(DCSYS.PtA)), "OSP"):
                                  ("OSPs", "osp_tolerance", 0.006)},
                          "survey_type_names": _add_other_spaces_names([
                              "PLATFORM", "PLATFORM_END", "PLATFORM_EXTREMITY", "MPLATFORM",
                          ]),
                          "multiple_dc_sys_objets": [get_sh_name(DCSYS.Quai),
                                                     get_sh_name(DCSYS.Quai.PointDArret),
                                                     get_sh_name(DCSYS.PtA)],
                          "multiple_survey_objets": ["PLATFORM",
                                                     "OSP"],
                          "display_name": "Platform ends and OSPs",
                          "dc_sys_display_names": [((get_sh_name(DCSYS.Quai),), "Platform ends"),
                                                   ((get_sh_name(DCSYS.Quai.PointDArret),
                                                     get_sh_name(DCSYS.PtA)), "OSPs")],
                          "survey_display_names": [(("PLATFORM",), "Platform ends"),
                                                   (("OSP",), "OSPs")],
                          },
    "OSP":               {"res_sheet": None,
                          "survey_type_names": _add_other_spaces_names([
                              "OSP", "PAE", "PLATFORM_OSP",
                          ]),
                          },
    "BLOCK":             {"res_sheet": "Block",
                          "dcsys_sh": DCSYS.CDV,
                          "func": check_joint,
                          "tol": ("joints", "joint_tolerance", 0.006),
                          "survey_type_names": _add_other_spaces_names([
                              "BLOCK", "TC", "TRACK_CIRCUIT", "TRACK_CIRCUITS_JOINT", "TRACK_CIRCUIT_JOINT",
                              "AXC", "AXLE_COUNTER", "IJ", "INSULATED_JOINT",
                          ]),
                          "multiple_survey_objets": ["BLOCK",
                                                     "BUFFER"],
                          "display_name": "Blocks",
                          },
    "SIGNAL":            {"res_sheet": "Signal",
                          "dcsys_sh": DCSYS.Sig,
                          "func": check_signal,
                          "tol": {
                              ((get_sh_name(DCSYS.Sig) + f"__{SignalType.MANOEUVRE}",
                                get_sh_name(DCSYS.Sig) + f"__{SignalType.PERMANENT_ARRET}",
                                get_sh_name(DCSYS.Sig) + f"__{SignalType.ESPACEMENT}"), "SIGNAL"):
                                    ("signals", "signal_tolerance", 0.006),
                              ((get_sh_name(DCSYS.Sig) + f"__{SignalType.HEURTOIR}",), "BUFFER"):
                                    ("buffers", "buffer_tolerance", 0.006)},
                          "survey_type_names": _add_other_spaces_names([
                              "SIG", "SIGNAL", "SIGN",
                          ]),
                          "multiple_dc_sys_objets": [get_sh_name(DCSYS.Sig) + f"__{SignalType.MANOEUVRE}",
                                                     get_sh_name(DCSYS.Sig) + f"__{SignalType.PERMANENT_ARRET}",
                                                     get_sh_name(DCSYS.Sig) + f"__{SignalType.ESPACEMENT}",
                                                     get_sh_name(DCSYS.Sig) + f"__{SignalType.HEURTOIR}"],
                          "multiple_survey_objets": ["SIGNAL",
                                                     "BUFFER"],
                          "display_name": "Signals and Buffers",
                          "dc_sys_display_names": [((get_sh_name(DCSYS.Sig) + f"__{SignalType.MANOEUVRE}",
                                                    get_sh_name(DCSYS.Sig) + f"__{SignalType.PERMANENT_ARRET}",
                                                    get_sh_name(DCSYS.Sig) + f"__{SignalType.ESPACEMENT}"), "Signals"),
                                                   ((get_sh_name(DCSYS.Sig) + f"__{SignalType.HEURTOIR}",), "Buffers")],
                          "survey_display_names": [(("SIGNAL",), "Signals"),
                                                   (("BUFFER",), "Buffers")],
                          },
    "BUFFER":            {"res_sheet": None,
                          "survey_type_names": _add_other_spaces_names([
                              "BUFFER", "SIGNAL_BUFFER", "BS",
                          ]),
                          },
    "TAG":               {"res_sheet": "Tag",
                          "dcsys_sh": [DCSYS.Bal, DCSYS.IATPM_tags, DCSYS.IATPM_Version_Tags],
                          "func": check_tag,
                          "tol": ("tags", "tag_tolerance", 0.006),
                          "survey_type_names": _add_other_spaces_names([
                              "BAL", "BALISE", "TAG", "TAGS",
                              "FIXED_BAL", "FIXED_BALISE",
                              "FIXED_TAG", "FIXED_TAGS",
                          ]),
                          "multiple_dc_sys_objets": [get_sh_name(DCSYS.Bal),
                                                     get_sh_name(DCSYS.IATPM_tags),
                                                     get_sh_name(DCSYS.IATPM_Version_Tags)],
                          "multiple_survey_objets": ["TAG",
                                                     "DYNAMIC_TAG",
                                                     "VERSION_TAG"],
                          "display_name": "Localization and Dynamic Tags",
                          "dc_sys_display_names": [((get_sh_name(DCSYS.Bal),), "Localization Tags"),
                                                   ((get_sh_name(DCSYS.IATPM_tags),), "Dynamic Tags")],
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
                          "dcsys_sh": DCSYS.Flood_Gate,
                          "func": check_flood_gate,
                          "tol": ("flood gates", "flood_gate_tolerance", 0.006),
                          "survey_type_names": _add_other_spaces_names([
                              "FLOOD_GATE", "FLOOD_GATES",
                          ]),
                          "display_name": "Flood Gates",
                          },
    # "WALKWAY":           {"res_sheet": "Walkway",
    #                       "dcsys_sh": DCSYS.Walkways_Area,
    #                       "func": check_walkway,
    #                       "tol": ("walkway ends", "walkway_tolerance", 0.006),
    #                       "survey_type_names": _add_other_spaces_names([
    #                           "WALKWAY", "WALKWAYS", "WALKWAYS_AREA",
    #                       ]),
    #                       "multiple_survey_objets": ["WALKWAY",
    #                                                  "PLATFORM",
    #                                                  "TURNBACK_PLATFORM"],
    #                       "display_name": "Walkways",
    #                       },
    # "TURNBACK_PLATFORM": {"res_sheet": None,
    #                       "survey_type_names": _add_other_spaces_names([
    #                           "TURNBACK_PLATFORM",
    #                       ]),
    #                       },
}
