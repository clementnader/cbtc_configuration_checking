#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..database_location import DATABASE_LOC

__all__ = ["ixl_apz_definition_file", "get_approach_area_ivb_from_excel_file"]


LOADED_DB = dict()


def ixl_apz_definition_file() -> bool:
    return DATABASE_LOC.ixl_apz.ixl_apz_file is not None


def get_approach_area_ivb_from_excel_file(sig_name: str) -> Optional[list[str]]:
    if DATABASE_LOC.ixl_apz.ixl_apz_file is None:
        return None
    if not LOADED_DB:
        wb = load_xlsx_wb(DATABASE_LOC.ixl_apz.ixl_apz_file)
        ws = get_xl_sheet_by_name(wb, DATABASE_LOC.ixl_apz.ixl_apz_sheet_name)
        for row in range(DATABASE_LOC.ixl_apz.start_line, get_xl_number_of_rows(ws) + 1):
            sig = get_xl_cell_value(ws, row=row, column=DATABASE_LOC.ixl_apz.sig_column)
            if sig is None:
                continue
            apz_ivb_list = list()
            for column in range(DATABASE_LOC.ixl_apz.apz_start_column,
                                DATABASE_LOC.ixl_apz.apz_start_column + DATABASE_LOC.ixl_apz.apz_nb_columns):
                ivb = get_xl_cell_value(ws, row=row, column=column)
                if ivb is not None:
                    apz_ivb_list.append(ivb)
            LOADED_DB[sig] = apz_ivb_list
    return LOADED_DB.get(sig_name)
