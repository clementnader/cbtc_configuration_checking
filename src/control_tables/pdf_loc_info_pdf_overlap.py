#!/usr/bin/env python
# -*- coding: utf-8 -*-

LOC_DICT = {
    "Name": {"x": 118, "x_tol": 40, "y": 743},
    "[1] Destination Point]": {"x": 36, "y": 670},
    "[2] Destination Point locked": {"x": 221, "y": 683},
    "[3] Incompatibilities": {"x": 310, "y": 670, "y_tol": 40},
    "[4] Work Zones not activated": {"x": 413, "y": 700},
    "[5] Overlap path": {"x": 234, "y": 587},
    "[6] Flank protections": {"x": 344, "y": 587},
    "[7]  External Conditions": {"x": 469, "y": 608},
    "[8]  Overlap path": {"x": 237, "y": 471},
    "[9]  Flank protections": {"x": 398, "y": 471},
    "[10] Track Circuit": {"x": 229, "y": 340},
    "[11] Timer": {"x": 402, "y": 340},
}


def loc_info_pdf_overlap():
    loc_dict = LOC_DICT
    return loc_dict
