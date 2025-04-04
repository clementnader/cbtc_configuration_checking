#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from .load_xl import *
from .get_sheet_dict import *
from .generic_obj_name import *


__all__ = ["load_sheet", "clean_loaded_dc_sys", "check_dc_sys_global_definition"]


LOADED_SHEETS: dict[str, Optional[dict[str, dict[str, Any]]]] = {ws: None for ws in get_all_sheet_names()}
LOADED_SHEETS_OLD: dict[str, Optional[dict[str, dict[str, Any]]]] = {ws: None for ws in get_all_sheet_names()}


def clean_loaded_dc_sys():
    erase_dc_sys_wb()
    global LOADED_SHEETS, LOADED_SHEETS_OLD
    LOADED_SHEETS = {ws: None for ws in get_all_sheet_names()}
    LOADED_SHEETS_OLD = {ws: None for ws in get_all_sheet_names()}


def load_sheet(ws, old: bool = False) -> dict[str, dict[str, Any]]:
    sh_name = get_sh_name(ws)
    if old:
        global LOADED_SHEETS_OLD
        if not LOADED_SHEETS_OLD[sh_name]:
            wb_old = load_dc_sys_wb(old=True)
            LOADED_SHEETS_OLD[sh_name] = get_sheet(wb_old, sh_name)
        return LOADED_SHEETS_OLD[sh_name]

    else:
        global LOADED_SHEETS
        if not LOADED_SHEETS[sh_name]:
            wb = load_dc_sys_wb()
            LOADED_SHEETS[sh_name] = get_sheet(wb, sh_name)
        return LOADED_SHEETS[sh_name]


def get_sheet(wb: xlrd.Book, sh_name: str) -> dict[str, dict]:
    if sh_name not in get_xl_sheet_names(wb):
        print_error(f"Sheet {Color.orange}\"{sh_name}\"{Color.reset} is not present in DC_SYS.")
        return {}
    ws = wb.sheet_by_name(sh_name)
    columns_dict = get_sheet_attributes_columns_dict(sh_name)
    generic_obj_name = GENERIC_OBJ_NAME.get(sh_name, None)
    sh_dict = get_sh_dict(ws, columns_dict, generic_obj_name)
    return sh_dict


ALREADY_ALL_READ = False

def check_dc_sys_global_definition():
    global ALREADY_ALL_READ
    if ALREADY_ALL_READ:
        return
    ALREADY_ALL_READ = True
    print_title(f"Read every sheet in the DC_SYS to verify the global good definition of the different objects")
    # Try to read every sheet
    for sheet_name in get_all_sheet_names():
        load_sheet(sheet_name)
