#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..utils import *
from ..database_loc import DATABASE_LOC


IF_VERIF_TEMPLATE_RELATIVE_PATH = os.path.join("..", "templates", "template_if_results.xlsx")
FILE_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))
IF_VERIF_TEMPLATE = os.path.join(FILE_DIRECTORY_PATH, IF_VERIF_TEMPLATE_RELATIVE_PATH)

OUTPUT_DIRECTORY = os.path.join(os.getenv("UserProfile"), r"Desktop")

START_LINE = 3
OBJECT_COL = "A"
IF_COL = "B"

HEADER_SHEET_NAME = "Header"
HEADER_TITLE_CELL = "B13"
VERIF_SHEET_NAME = "IF - XXX"

IF = {
    "SCADE": {"dir_name": "GenPar", "header_line": 3, "rams_if_analysis_file": DATABASE_LOC.rams_if_analysis.scade},
    "APPLI": {"dir_name": "Appli", "header_line": 1, "rams_if_analysis_file": DATABASE_LOC.rams_if_analysis.appli},
    "ARCHI": {"dir_name": "Archi", "header_line": 1, "rams_if_analysis_file": DATABASE_LOC.rams_if_analysis.archi},
}

ZC_01_COLUMN = "E"
DELTA_BETWEEN_ZC = 3
NB_MAX_ZC = 7


def create_if_files():
    for layer, val in IF.items():
        if layer != "ARCHI":
            continue
        dir_name = val["dir_name"]
        header_line = val["header_line"]
        try:
            _create_if_layer_file(layer, dir_name, header_line)
        except KeyboardInterrupt:
            _create_if_layer_file(layer, dir_name, header_line)
            raise KeyboardInterrupt


def _create_if_layer_file(layer: str, dir_name: str, header_line: int):
    wb = load_xlsx_wb(IF_VERIF_TEMPLATE)
    _update_header_sheet(wb, layer)
    _update_verif_sheet(wb, layer, dir_name, header_line)
    wb.save(os.path.join(OUTPUT_DIRECTORY, f"ZC IF {layer} Verification.xlsx"))


def _update_header_sheet(wb: openpyxl.Workbook, layer: str):
    sh = wb.get_sheet_by_name(HEADER_SHEET_NAME)
    sh[HEADER_TITLE_CELL] = f"ZC IF {layer} Verification"


def _update_verif_sheet(wb: openpyxl.Workbook, layer: str, dir_name: str, header_line: int):
    sh = wb.get_sheet_by_name(VERIF_SHEET_NAME)
    sh.title = f"IF - {layer}"
    list_zc_export, res_dict = _get_info_export(dir_name, layer, header_line)
    res_dict = _update_info_with_rams_analysis(layer, res_dict)
    _hide_columns(sh, list_zc_export)
    _add_if(sh, res_dict, layer)


def _hide_columns(sh, list_zc_export: list[list[str]]):
    last_zc = len(list_zc_export)
    first_col_to_hide = xl_ut.get_column_letter(xl_ut.column_index_from_string(ZC_01_COLUMN)
                                                + DELTA_BETWEEN_ZC * last_zc)
    last_col_to_hide = xl_ut.get_column_letter(xl_ut.column_index_from_string(ZC_01_COLUMN)
                                               + DELTA_BETWEEN_ZC * NB_MAX_ZC - 1)
    for col in columns_from_to(first_col_to_hide, last_col_to_hide):
        sh.column_dimensions[col].hidden = True

    # Rename useful columns with the name of the ZC in the export
    for num_zc, zc in enumerate(list_zc_export):
        col = xl_ut.get_column_letter(xl_ut.column_index_from_string(ZC_01_COLUMN) + DELTA_BETWEEN_ZC * num_zc)
        sh[f"{col}2"] = zc[0]


def _get_info_export(dir_name: str, layer: str, header_line: int) -> tuple[list[list[str]], dict[str, list]]:
    list_zc_export = list()
    export_dir = os.path.join(DATABASE_LOC.kit_c121_d470_dir, "Project_ZC_GENPAR", "ZCGenPar", dir_name)
    for export_file in os.listdir(export_dir):
        full_path_file = os.path.join(export_dir, export_file)
        export_file_name, sep = os.path.splitext(export_file)
        if sep == ".xls":
            _, _, export_name_in_file, zc, zc_num = export_file_name.split("_")
            if export_name_in_file == f"Export{dir_name}" and zc == "ZC":
                list_zc_export.append([f"ZC_{zc_num}", full_path_file])
    return list_zc_export, _get_info_in_file(list_zc_export, layer, header_line)


def _get_info_in_file(list_zc_export: list[list[str]], layer: str, header_line: int) -> dict[str, list]:
    if not list_zc_export:
        return dict()
    res_dict = dict()
    excel_file = list_zc_export[0][1]
    wb = xlrd.open_workbook(excel_file)
    for sh in wb.sheets():
        if not(layer == "ARCHI" and sh.name.startswith("PARAMETRES_")):
            res_dict.update(_get_info_in_sheet(sh, header_line))
    return res_dict


def _get_info_in_sheet(sh: xlrd.sheet.Sheet, header_line: int) -> dict[str, list]:
    if_list = list()
    for column in range(1, sh.ncols + 1):
        cell = get_xlrd_float_value(sh, header_line, column)
        if cell:
            cell = cell.replace("Ã©", "e")
            if_list.append(cell)
    return {sh.name: if_list}


def _add_if(sh, res_dict: dict[str, list], layer: str):
    if layer == "ARCHI":
        sh["D1"].value = "Manual Check"
    current_line = START_LINE
    for obj, if_list in res_dict.items():
        for if_name in if_list:
            sh[f"{OBJECT_COL}{current_line}"].value = str(obj)
            sh[f"{IF_COL}{current_line}"].value = str(if_name)
            current_line += 1


def _update_info_with_rams_analysis(layer: str, res_dict: dict[str, list]) -> dict[str, list]:
    rams_if_analysis_file = IF[layer]["rams_if_analysis_file"]
    wb = xlrd.open_workbook(rams_if_analysis_file)
    if layer == "ARCHI":
        res_dict = analyze_rams_sheet_archi(wb, res_dict)
    return res_dict


RAMS_START_LINE = 2
RAMS_IF_COL = "A"
RAMS_S_NS_COL = "G"
RAMS_CONSTRAINT_COL = "M"


def analyze_rams_sheet_archi(wb: xlrd.Book, res_dict: dict[str, list]) -> dict[str, list]:
    sheet_names_list = [sh.name for sh in wb.sheets()]
    extra_names_in_rams = [key for key in sheet_names_list if key not in res_dict]
    extra_names_in_eng = [key for key in res_dict if key not in sheet_names_list]
    if extra_names_in_rams != ["General"] or extra_names_in_eng != []:
        print_warning("An info exists in one side and is missing in the other one:")
        print(f"{extra_names_in_rams = }"
              f"\n{extra_names_in_eng = }")
    for key, val in res_dict.items():
        ...  # TODO
    return res_dict
