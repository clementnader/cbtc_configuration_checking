#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["CONTROL_TABLE_TYPE", "ROUTE_INFORMATION", "OVERLAP_INFORMATION",
           "ROUTE_CONTROL_SIG_CONTROL_TABLE", "ROUTE_SW_CONTROL_TABLE", "ROUTE_PATH_CONTROL_TABLE",
           "OVL_DESTINATION_POINT_CONTROL_TABLE", "OVL_PATH_CONTROL_TABLE", "OVL_SW_CONTROL_TABLE"]


class CONTROL_TABLE_TYPE:
    route = "route"
    overlap = "overlap"


# ROUTE_CONTROL_SIG_CONTROL_TABLE = ["[1]", "[1a]"]
# ROUTE_SW_CONTROL_TABLE = "[9]"
# ROUTE_PATH_CONTROL_TABLE = "[10]"
ROUTE_CONTROL_SIG_CONTROL_TABLE = ["[2]"]
ROUTE_SW_CONTROL_TABLE = "[8]"
ROUTE_PATH_CONTROL_TABLE = "[12]"

OVL_DESTINATION_POINT_CONTROL_TABLE = "[1]"
OVL_PATH_CONTROL_TABLE = "[5]"
OVL_SW_CONTROL_TABLE = "[8]"


# ROUTE_INFORMATION = {
#     "name":
#         {"names": ["Name", "Name[0]", "Name [0]"],
#          "right": True},
#     "origin_signal":
#         {"names": ["[1] Origin Signal", "[1] Controlled Signal", "[1a] Origin Signal", "[1a] Controlled Signal"]
#          },
#     "origin_led_matrix":
#         {"names": ["[1b] Origin LED Matrix"],
#          "optional": True},
#     "incompatibilities":
#         {"names": ["[2] Incompatibilities"],
#          },
#     "wz_route_path":
#         {"names": ["[3] Route Path"],
#          "optional": True},
#     "wz_flank_protections":
#         {"names": ["[4] Flank protections"],
#          "optional": True},
#     "clear_tc_route_path":
#         {"names": ["[5] Route path"],
#          },
#     "clear_tc_flank_protections":
#         {"names": ["[6] Flank protections"],
#          },
#     "route_setting_external_conditions":
#         {"names": ["[7] External Conditions"],
#          },
#     "sw_flank_protections":
#         {"names": ["[8] Flank protections"],
#          },
#     "sw_route_path":
#         {"names": ["[9] Route path"],
#          },
#     "route_path":
#         {"names": ["[10] Route path (T.C. clearance)"],
#          },
#     "functions_not_activated":
#         {"names": ["[11] Functions not activated"],
#          "optional": True},
#     "overlap_set":
#         {"names": ["[12] Overlap set"],
#          },
#     "permanent_replacement_tc":
#         {"names": ["[13] Permanent Replacement T.C."],
#          "optional": True},
#     "approach_area_clearance":
#         {"names": ["[14] Approach Area clearance"],
#          },
#     "route_releasing_external_conditions":
#         {"names": ["[15] External Conditions"],
#          },
#     "points_route_path":
#         {"names": ["[16] Route path (T.C. clearance)"],
#          },
#     "points_flank_protection":
#         {"names": ["[17] Flank protection (T.C. clearance)"],
#          },
#     "destination_point_tc_clearance":
#         {"names": ["[18] Track Circuit clearance"],
#          },
#     "origin_signal_clearing_external_conditions":
#         {"names": ["[19] External Conditions", "[19] External Conditions \\ MAR"],
#          },
#     "downstream_tc":
#         {"names": ["[20] Downstream T.C"],
#          "optional": True},
# }
ROUTE_INFORMATION = {
    "name":
        {"names": ["[1] Name"],
         "right": True},
    "origin_signal":
        {"names": ["[2] Start Signal"],
         "right": True},
    "start_shunt_signal":
        {"names": ["[2a] Start Shunt Signal"],
         "right": True},
    "end_signal":
        {"names": ["[3] End Signal"],
         "right": True},
    "wz_route_path":
        {"names": ["[4] Route Path"],
         },
    "wz_flank_protections":
        {"names": ["[5] Flank Protections"],
         },
    "clear_tc_route_path":
        {"names": ["[6] Route Path"],
         },
    "clear_tc_flank_protections":
        {"names": ["[7] Flank Protections"],
         },
    "sw_route_path":
        {"names": ["[8] Route Path"],
         },
    "sw_flank_protections":
        {"names": ["[9] Flank Protections"],
         },
    "route_setting_external_conditions":
        {"names": ["[10] External Conditions"],
         },
    "incompatibilities":
        {"names": ["[11] Incompatibilities"],
         },
    "route_path":
        {"names": ["[12] Route Path"],
         },
    "overlap_set":
        {"names": ["[13] Overlaps"],
         },
    "maintenance":
        {"names": ["[14] Maintenance areas not activated"],
         },
    "psd":
        {"names": ["[14a] PSDs"],
         },
    "alarms":
        {"names": ["[14b] Alarms"],
         },
    "emergency_stop":
        {"names": ["[14c] Emergency Stop"],
         },
    "traction_power_section":
        {"names": ["[14d] Traction Power section"],
         },
    "external_conditions":
        {"names": ["[14e] External Conditions"],
         },
    "permanent_replacement_ivb":
        {"names": ["[15] Permanent Replacement IVB"],
         },
    "approach_area":
        {"names": ["[16] Approach Area"],
         },
    "route_releasing_external_conditions":
        {"names": ["[17] External Conditions"],
         },
    "points_route_path":
        {"names": ["[18] Route Path (IVB)"],
         },
    "points_flank_protection":
        {"names": ["[19] Flank Protection (IVB)"],
         },
    "downstream_ivb":
        {"names": ["[20] Downstream IVBs"],
         },
    "destination_point_tc_clearance":
        {"names": ["[21] Free IVB"],
         },
}


OVERLAP_INFORMATION = {
    "name":
        {"names": ["Name", "Name[0]", "Name [0]"],
         "right": True},
    "destination_point":
        {"names": ["[1] Destination Point"],
         },
    "dest_point_locked":
        {"names": ["[2] Destination Point locked"],
         },
    "incompatibilities":
        {"names": ["[3] Incompatibilities"],
         },
    "wz_not_activated":
        {"names": ["[4] Work Zones not activated"],
         "optional": True},
    "clear_tc_overlap_path":
        {"names": ["[5] Overlap path"],
         },
    "clear_tc_flank_protections":
        {"names": ["[6] Flank protections"],
         },
    "external_conditions":
        {"names": ["[7] External Conditions"],
         },
    "sw_route_path":
        {"names": ["[8] Overlap path"],
         },
    "sw_flank_protections":
        {"names": ["[9] Flank protections"],
         },
    "clear_tc":
        {"names": ["[10] Track Circuit", "[10] Clear Track Circuits"],
         },
    "ovl_releasing_dest_point":
        {"names": ["[11] Destination Point"],
         "optional": True},
    "timer":
        {"names": ["[11] Timer", "[12] Timer"],
         },
}
