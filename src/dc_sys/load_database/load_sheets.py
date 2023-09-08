#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from .load_xl import *
from .get_sheet_dict import *
from .generic_obj_name import *


__all__ = ["load_sheet"]


LOADED_SHEETS = {sh: None for sh in get_all_sheet_names()}
LOADED_SHEETS_OLD = {sh: None for sh in get_all_sheet_names()}


def load_sheet(sh, old: bool = False) -> dict:
    sh_name = get_sh_name(sh)
    if old:
        global LOADED_SHEETS_OLD
        if not LOADED_SHEETS_OLD[sh_name]:
            wb_old = load_wb(old)
            LOADED_SHEETS_OLD[sh_name] = get_sheet(wb_old, sh_name)
        return LOADED_SHEETS_OLD[sh_name]
    else:
        global LOADED_SHEETS
        if not LOADED_SHEETS[sh_name]:
            wb = load_wb(old)
            LOADED_SHEETS[sh_name] = get_sheet(wb, sh_name)
        return LOADED_SHEETS[sh_name]


def get_sheet(wb: xlrd.Book, sh_name: str):
    sh = wb.sheet_by_name(sh_name)
    columns_dict = get_sheet_attributes_columns_dict(sh_name)
    generic_obj_name = GENERIC_OBJ_NAME.get(sh_name, None)
    sh_dict = get_sh_dict(sh, columns_dict, generic_obj_name)
    return sh_dict
