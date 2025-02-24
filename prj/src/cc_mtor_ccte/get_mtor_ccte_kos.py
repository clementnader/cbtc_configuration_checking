#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..utils import *


__all__ = ["get_mtor_ccte_ko"]


# MTOR_CCTE_PATH = r"C:\Users\naderc\Desktop\Riyadh\Verification of MTOR and CCTE Plugs"
# MTOR_CCTE_PATH = r"C:\Users\naderc\Desktop\Glasgow\Verification of MTOR and CCTE Plugs"
MTOR_CCTE_PATH = r"C:\Users\naderc\Desktop\results ml4 mtor ccte"
# MTOR_CCTE_PATH = r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\Verification of MTOR and CCTE Plugs"


RES_SHEETS = {
    "ccte": "RESULT_CCTE",
    "mtor": "RESULT_MTOR",
}


def get_mtor_ccte_ko():
    list_of_files = [file for file in os.listdir(MTOR_CCTE_PATH)
                     if os.path.splitext(file)[1] == ".xls" or os.path.splitext(file)[1] == ".xlsx"]
    nb_files = len(list_of_files)
    dict_of_kos = {"ccte": dict(), "mtor": dict()}
    progress_bar(1, 1, end=True)  # reset progress_bar
    for i, file in enumerate(list_of_files):
        first_ko = True
        print_log_progress_bar(i, nb_files, f"analyzing {file}")
        temp_dict, mtor = _analyze_mtor_ccte_file(file)
        if temp_dict is None:
            continue
        sub_dict_name = "ccte" if not mtor else "mtor"
        for key, val in temp_dict.items():
            if key not in dict_of_kos[sub_dict_name]:
                if first_ko:
                    first_ko = False
                    print()
                print(f"New KO: on key {Color.blue}{key}{Color.reset}, KO is {Color.yellow}\"{val}\"{Color.reset}")
                dict_of_kos[sub_dict_name][key] = val
            else:
                if val != dict_of_kos[sub_dict_name][key]:
                    if first_ko:
                        first_ko = False
                        print()
                    print(f"A different KO is seen on key {Color.blue}{key}{Color.reset}, "
                          f"old KO is {Color.light_yellow}\"{dict_of_kos[sub_dict_name][key]}\"{Color.reset}, "
                          f"new KO is {Color.yellow}\"{val}\"{Color.reset}\".")
    print_log_progress_bar(nb_files, nb_files, "analysis of all MTOR and CCTE Plugs Verification files is done",
                           end=True)


def _analyze_mtor_ccte_file(file):
    full_path = os.path.join(MTOR_CCTE_PATH, file)
    if os.path.splitext(file)[1] == ".xls":
        os.rename(full_path, full_path + "x")
        full_path += "x"
    wb = load_xl_file(full_path)
    list_of_sheets = get_xl_sheet_names(wb)
    if RES_SHEETS["ccte"] in list_of_sheets:
        ws = get_xl_sheet_by_name(wb, RES_SHEETS["ccte"])
        mtor = False
    elif RES_SHEETS["mtor"] in list_of_sheets:
        ws = get_xl_sheet_by_name(wb, RES_SHEETS["mtor"])
        mtor = True
    else:
        return None, None
    dict_of_kos = _get_kos_res_sheet(ws)
    return dict_of_kos, mtor


def _get_kos_res_sheet(ws):
    dict_of_kos = dict()
    first_row = 2
    param_id_column = "A"
    verification_column = "J"
    for row in range(first_row, get_xl_number_of_rows(ws) + 1):
        verif_res = get_xl_cell_value(ws, row=row, column=verification_column)
        if verif_res is None:
            continue
        param_id_name = get_xl_cell_value(ws, row=row, column=param_id_column)
        if not _check_if_verif_is_ok(verif_res):
            dict_of_kos[param_id_name] = verif_res
    return dict_of_kos


def _check_if_verif_is_ok(verif_res: str) -> bool:
    verif_res = verif_res.strip()
    if '+' in verif_res:
        value_res, sacem_res = verif_res.split('+', 1)
        value_res = value_res.strip()
        sacem_res = sacem_res.strip().removeprefix("code SACEM :").lstrip()
        if sacem_res == "KO":
            return False
        if value_res == "OK" or value_res == "NA":
            return True
        else:
            return False
    else:
        if verif_res == "OK" or verif_res == "NA":
            return True
        elif verif_res.removeprefix("code SACEM :").lstrip() == "OK":
            return True
        else:
            return False
