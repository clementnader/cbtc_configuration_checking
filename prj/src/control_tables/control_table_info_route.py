#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


__all__ = ["ROUTE_INFORMATION"]


ROUTE_INFORMATION = {
    "name": {"names": ["Name", "Name[0]", "Name [0]"],
             "info_format": re.compile(r"[A-Za-z0-9]+-[A-Za-z0-9]+"),
             "right": True, "next_line": True, "first": True},
    "origin_signal": {"names": ["[1] Origin Signal", "[1] Controlled Signal", "[1a] Origin Signal",
                                "[1a] Controlled Signal"],
                      "next_line": True, "first": True},
    "origin_led_matrix": {"names": ["[1b] Origin LED Matrix"],
                          "next_line": True, "first": True, "multiple_lines": True, "optional": True},
    "incompatibilities": {"names": ["[2] Incompatibilities"],
                          "next_line": True, "multiple_lines": True, "negative_tol": 150},
    "wz_route_path": {"names": ["[3] Route Path"],
                      "next_line": True, "multiple_lines": True, "optional": True},
    "wz_flank_protections": {"names": ["[4] Flank protections"],
                             "next_line": True, "multiple_lines": True, "optional": True},
    "clear_tc_route_path": {"names": ["[5] Route path"],
                            "next_line": True, "multiple_lines": True},
    "clear_tc_flank_protections": {"names": ["[6] Flank protections"],
                                   "next_line": True, "multiple_lines": True},
    "route_setting_external_conditions": {"names": ["[7] External Conditions"],
                                          "next_line": True, "multiple_lines": True, "negative_tol": 40},
    "sw_flank_protections": {"names": ["[8] Flank protections"],
                             "next_line": True, "multiple_lines": True, "negative_tol": 80},
    "sw_route_path": {"names": ["[9] Route path"],
                      "next_line": True, "multiple_lines": True, "negative_tol": 80},
    "route_path": {"names": ["[10] Route path (T.C. clearance)"],
                   "next_line": True, "multiple_lines": True, "first": True},
    "functions_not_activated": {"names": ["[11] Functions not activated"],
                                "next_line": True, "multiple_lines": True, "first": True, "optional": True},
    "overlap_set": {"names": ["[12] Overlap set"],
                    "next_line": True, "multiple_lines": True, "first": True},
    "permanent_replacement_tc": {"names": ["[13] Permanent Replacement T.C."],
                                 "next_line": True, "multiple_lines": True, "negative_tol": 40, "optional": True},
    "approach_area_clearance": {"names": ["[14] Approach Area clearance"],
                                "next_line": True, "multiple_lines": True, "negative_tol": 60},
    "route_releasing_external_conditions": {"names": ["[15] External Conditions"],
                                            "next_line": True, "multiple_lines": True},
    "points_route_path": {"names": ["[16] Route path (T.C. clearance)"],
                          "next_line": True, "multiple_lines": True},
    "points_flank_protection": {"names": ["[17] Flank protection (T.C. clearance)"],
                                "next_line": True, "multiple_lines": True},
    "destination_point_tc_clearance": {"names": ["[18] Track Circuit clearance"],
                                       "next_line": True, "multiple_lines": True},
    "origin_signal_clearing_external_conditions": {"names": ["[19] External Conditions",
                                                             "[19] External Conditions \\ MAR"],
                                                   "next_line": True, "multiple_lines": True, "first": True},
    "downstream_tc": {"names": ["[20] Downstream T.C"],
                      "next_line": True, "multiple_lines": True, "optional": True},
}
