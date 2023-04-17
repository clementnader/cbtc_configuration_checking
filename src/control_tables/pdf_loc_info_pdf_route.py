#!/usr/bin/env python
# -*- coding: utf-8 -*-

LOC_DICT = {
    "Name": {"x": 129.0, "x_tol": 40, "y": 750.3},
    "[1] Controlled Signal": {"x": 43.3, "y": 675.8},
    "[2] Incompatibilities": {"x": 217.6, "y": 703.6},
    "[3] Route Path": {"x": 339.5, "y": 672.7},
    "[4] Flank protections": {"x": 451.2, "y": 672.2},
    "[5] Route path": {"x": 221.4, "y": 550.0},
    "[6] Flank protections": {"x": 300.8, "y": 551.1},
    "[7] External Conditions": {"x": 421.1, "y": 573.4},
    "[8] Flank protections": {"x": 383.9, "y": 421.6},
    "[9] Route path": {"x": 225.6, "y": 423.1},
    "[10] Route path (T.C. clearance)": {"x": 47.0, "y": 575.4, "y_tol": 20},
    "[11] Functions not activated": {"x": 47.8, "y": 486.9, "y_tol": 20},
    "[12] Overlap set": {"x": 47.8, "y": 425.8, "y_tol": 20},
    "[13] Permanent Replacement T.C.": {"x": 227.8, "y": 279.2},
    "[14] Approach Area clearance": {"x": 360.2, "y": 282.9},
    "[15] External Conditions": {"x": 450.0, "y": 309.4},
    "[16] Route path (T.C. clearance)": {"x": 224.9, "y": 196.4},
    "[17] Flank protection (T.C. clearance)": {"x": 343.2, "y": 191.7},
    "[18] Track Circuit clearance": {"x": 475.4, "y": 183.7},
    "[19] External Conditions \\ MAR": {"x": 46.7, "y": 367.2, "y_tol": 20},
}


def loc_info_pdf_route():
    loc_dict = LOC_DICT
    return loc_dict
