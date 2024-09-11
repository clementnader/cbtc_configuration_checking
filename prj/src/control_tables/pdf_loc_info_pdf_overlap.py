#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..database_location import *
# import json
# with open(r"C:\Users\naderc\Desktop\test.json", "w") as f:
#     f.write(json.dumps(LOC_DICT, indent=2))


if PROJECT_NAME.startswith("Brussels"):
    LOC_DICT = {
        "Name_Title":                   {"x":  30, "y": 744, "x_tol": 30, "y_tol": 30},
        "Name":                         {"x": 100, "y": 743, "x_tol": 40},
        "[1] Destination Point":        {"x":  36, "y": 670},
        "[2] Destination Point locked": {"x": 220, "y": 684},
        "[3] Incompatibilities":        {"x": 309, "y": 699, "y_tol": 50},
        "[5] Overlap path":             {"x": 233, "y": 587},
        "[6] Flank protections":        {"x": 343, "y": 567, "y_tol": 40},
        "[7]  External Conditions":     {"x": 468, "y": 608},
        "[8]  Overlap path":            {"x": 237, "y": 471},
        "[9]  Flank protections":       {"x": 397, "y": 471},
        "[10] Track Circuit":           {"x": 229, "y": 339},
        "[11] Destination Point":       {"x": 364, "y": 342},
        "[12] Timer":                   {"x": 495, "y": 342},
    }
elif PROJECT_NAME == Projects.Copenhagen:
    LOC_DICT = {
        "Name_Title":                   {"x":  43, "y": 744, "x_tol": 30, "y_tol": 30},
        "Name":                         {"x": 120, "y": 743, "x_tol": 40},
        "[1] Destination Point":        {"x":  36, "y": 669},
        "[2] Destination Point locked": {"x": 221, "y": 683},
        "[3] Incompatibilities":        {"x": 310, "y": 670, "y_tol": 40},
        "[4] Work Zones not activated": {"x": 413, "y": 700},
        "[5] Overlap path":             {"x": 234, "y": 587},
        "[6] Flank protections":        {"x": 344, "y": 587},
        "[7]  External Conditions":     {"x": 469, "y": 608},
        "[8]  Overlap path":            {"x": 237, "y": 471},
        "[9]  Flank protections":       {"x": 398, "y": 471},
        "[10] Track Circuit":           {"x": 229, "y": 340},
        "[11] Timer":                   {"x": 402, "y": 340},
    }
elif PROJECT_NAME.startswith("Glasgow"):
    LOC_DICT = {
        "Name_Title":                   {"x":  39, "y": 744, "x_tol": 30, "y_tol": 30},
        "Name":                         {"x": 128, "y": 743, "x_tol": 40},
        "[1] Destination Point":        {"x":  39, "y": 670},
        "[2] Destination Point locked": {"x": 223, "y": 684},
        "[3] Incompatibilities":        {"x": 312, "y": 699, "y_tol": 50},
        "[5] Overlap path":             {"x": 236, "y": 587},
        "[6] Flank protections":        {"x": 346, "y": 587},
        "[7]  External Conditions":     {"x": 471, "y": 608},
        "[8]  Overlap path":            {"x": 240, "y": 471},
        "[9]  Flank protections":       {"x": 400, "y": 471},
        "[10] Track Circuit":           {"x": 232, "y": 351},
        "[11] Destination Point":       {"x": 367, "y": 350},
        "[12] Timer":                   {"x": 498, "y": 351},
    }
elif PROJECT_NAME == Projects.Milan:
    LOC_DICT = {
        "Name_Title":                   {"x":  43, "y": 744, "x_tol": 30, "y_tol": 30},
        "Name":                         {"x": 118, "y": 743, "x_tol": 40},
        "[1] Destination Point":        {"x":  36, "y": 670},
        "[2] Destination Point locked": {"x": 221, "y": 683},
        "[3] Incompatibilities":        {"x": 310, "y": 675, "y_tol": 40},
        "[4] Work Zones not activated": {"x": 413, "y": 700},
        "[5] Overlap path":             {"x": 234, "y": 587},
        "[6] Flank protections":        {"x": 344, "y": 560, "y_tol": 40},
        "[7]  External Conditions":     {"x": 468, "y": 607},
        "[8]  Overlap path":            {"x": 237, "y": 471},
        "[9]  Flank protections":       {"x": 398, "y": 471},
        "[10] Track Circuit":           {"x": 229, "y": 340},
        "[11] Timer":                   {"x": 401, "y": 340},
    }
elif PROJECT_NAME == Projects.Riyadh:
    LOC_DICT = {
        "Name_Title":                   {"x":  36, "y": 744, "x_tol": 30, "y_tol": 30},
        "Name":                         {"x": 108, "y": 745, "x_tol": 40},
        "[1] Destination Point":        {"x":  36, "y": 669},
        "[2] Destination Point locked": {"x": 221, "y": 683},
        "[3] Incompatibilities":        {"x": 310, "y": 675, "y_tol": 30},
        "[4] Work Zones not activated": {"x": 413, "y": 700},
        "[5] Overlap path":             {"x": 234, "y": 587},
        "[6] Flank protections":        {"x": 344, "y": 587},
        "[7]  External Conditions":     {"x": 468, "y": 607},
        "[8]  Overlap path":            {"x": 237, "y": 471},
        "[9]  Flank protections":       {"x": 398, "y": 471},
        "[10] Track Circuit":           {"x": 229, "y": 350},
        "[11] Destination Point":       {"x": 364, "y": 350},
        "[12] Timer":                   {"x": 496, "y": 350},
    }
elif PROJECT_NAME == Projects.Thessaloniki:
    LOC_DICT = {
        "Name_Title":                   {"x":  36, "y": 744, "x_tol": 30, "y_tol": 30},
        "Name":                         {"x": 122, "y": 743, "x_tol": 40},
        "[1] Destination Point":        {"x":  36, "y": 669},
        "[2] Destination Point locked": {"x": 221, "y": 683},
        "[3] Incompatibilities":        {"x": 310, "y": 670, "y_tol": 30},
        "[4] Work Zones not activated": {"x": 413, "y": 700},
        "[5] Overlap path":             {"x": 234, "y": 587},
        "[6] Flank protections":        {"x": 344, "y": 587},
        "[7]  External Conditions":     {"x": 469, "y": 608},
        "[8]  Overlap path":            {"x": 237, "y": 471},
        "[9]  Flank protections":       {"x": 398, "y": 471},
        "[10] Clear Track Circuits":    {"x": 229, "y": 350},
        "[11] Destination Point":       {"x": 364, "y": 350},
        "[12] Timer":                   {"x": 496, "y": 350},
    }
else:  # default
    LOC_DICT = {
        "Name_Title":                   {"x":  39, "y": 744, "x_tol": 30, "y_tol": 30},
        "Name":                         {"x": 128, "y": 743, "x_tol": 40},
        "[1] Destination Point":        {"x":  39, "y": 670},
        "[2] Destination Point locked": {"x": 223, "y": 684},
        "[3] Incompatibilities":        {"x": 312, "y": 699, "y_tol": 50},
        "[5] Overlap path":             {"x": 236, "y": 587},
        "[6] Flank protections":        {"x": 346, "y": 587},
        "[7]  External Conditions":     {"x": 471, "y": 608},
        "[8]  Overlap path":            {"x": 240, "y": 471},
        "[9]  Flank protections":       {"x": 400, "y": 471},
        "[10] Track Circuit":           {"x": 232, "y": 351},
        "[11] Destination Point":       {"x": 367, "y": 350},
        "[12] Timer":                   {"x": 498, "y": 351},
    }


def loc_info_pdf_overlap():
    loc_dict = LOC_DICT
    return loc_dict
