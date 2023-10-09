#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..utils import *


# MTOR_CCTE_PATH = r"C:\Users\naderc\Desktop\Riyadh\Verification of MTOR and CCTE Plugs"
MTOR_CCTE_PATH = r"C:\Users\naderc\Desktop\Glasgow\Verification of MTOR and CCTE Plugs"
# MTOR_CCTE_PATH = r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\Verification of MTOR and CCTE Plugs"


HEADER_SHEET = "Header"

CELLS_TO_PATCH = {
    "company":            {"cell": "A7",  "text": "Hitachi Rail STS France"},
    "title":              {"cell": "B13", "text": "Verification of MTOR and CCTE Plugs"},
    "author_title":       {"cell": "C23", "text": "Author"},
    "verifier_title":     {"cell": "D23", "text": "Verifier"},
    "approver_title":     {"cell": "E23", "text": "Approver"},
    "author":             {"cell": "C24", "text": "Clément NADER"},
    "verifier":           {"cell": "D24", "text": "Ouassim MAHIA"},
    "approver":           {"cell": "E24", "text": "Gian Marco DE ROSA"},
    # "c11_d470_version":   {"cell": "D28", "text": "RL3_C11_D470_06_06_01_V00"},
    "std_c11_cc_version": {"cell": "D29", "text": "STD_CC_C11_V_6_6_1"},
}


def patch_cc_mtor_ccte():
    list_of_files = [file for file in os.listdir(MTOR_CCTE_PATH)
                     if os.path.splitext(file)[1] == ".xls" or os.path.splitext(file)[1] == ".xlsx"]
    nb_files = len(list_of_files)
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, file in enumerate(list_of_files):
        print_log(f"\r{progress_bar(i, nb_files)} patching {file}...", end="")
        try:
            _patch_file(file)
        except KeyboardInterrupt:
            _patch_file(file)
            raise KeyboardInterrupt
    print_log(f"\r{progress_bar(nb_files, nb_files, end=True)} patching of "
              f"all MTOR and CCTE Plugs Verification files is done.")


def _patch_file(file):
    full_path = os.path.join(MTOR_CCTE_PATH, file)
    if os.path.splitext(file)[1] == ".xls":
        os.rename(full_path, full_path + "x")
        full_path += "x"
    wb = load_xl_file(full_path)
    sheet = get_xl_sheet_by_name(wb, HEADER_SHEET)
    for val in CELLS_TO_PATCH.values():
        cell = val["cell"]
        text = val["text"]
        sheet[cell] = text
    wb.save(os.path.join(full_path))
