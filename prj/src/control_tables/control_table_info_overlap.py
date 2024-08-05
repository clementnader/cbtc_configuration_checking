#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


__all__ = ["OVERLAP_INFORMATION"]


OVERLAP_INFORMATION = {
    "name": {"names": ["Name", "Name[0]", "Name [0]"],
             "info_format": re.compile(r"[A-Za-z0-9]+-[A-Za-z0-9]+"),
             "right": True, "next_line": True, "first": True},
    "destination_point": {"names": ["[1] Destination Point"],
                          "next_line": True, "first": True},
    "dest_point_locked": {"names": ["[2] Destination Point locked"],
                          "next_line": True, "multiple_lines": True},
    "incompatibilities": {"names": ["[3] Incompatibilities"],
                          "next_line": True, "multiple_lines": True, "negative_tol": 150},
    "wz_not_activated": {"names": ["[4] Work Zones not activated"],
                         "next_line": True, "multiple_lines": True, "negative_tol": 40, "optional": True},
    "clear_tc_overlap_path": {"names": ["[5] Overlap path"],
                              "next_line": True, "multiple_lines": True},
    "clear_tc_flank_protections": {"names": ["[6] Flank protections"],
                                   "next_line": True, "multiple_lines": True},
    "external_conditions": {"names": ["[7] External Conditions"],
                            "next_line": True, "multiple_lines": True, "negative_tol": 40},
    "sw_route_path": {"names": ["[8] Overlap path"],
                      "next_line": True, "multiple_lines": True, "negative_tol": 100},
    "sw_flank_protections": {"names": ["[9] Flank protections"],
                             "next_line": True, "multiple_lines": True, "negative_tol": 80},
    "clear_tc": {"names": ["[10] Track Circuit", "[10] Clear Track Circuits"],
                 "next_line": True, "multiple_lines": True, "negative_tol": 80},
    "timer": {"names": ["[12] Timer", "[11] Timer"],
              "next_line": True, "multiple_lines": True, "negative_tol": 80},
    "ovl_releasing_dest_point": {"names": ["[11] Destination Point"],
                                 "next_line": True, "multiple_lines": True, "negative_tol": 40, "optional": True},
}
