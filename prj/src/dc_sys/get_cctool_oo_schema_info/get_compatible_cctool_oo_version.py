#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...dc_sys.load_database.load_xl import load_wb


__all__ = ["get_cctool_oo_name"]


CCTOOL_OO_VERSION_CELL = "A4"
C_D470_VERSION_CELL = "B6"


def get_cctool_oo_name() -> str:
    ws = open_menu_sheet()
    version = get_xl_cell_value(ws, cell=CCTOOL_OO_VERSION_CELL)
    return version


def open_menu_sheet():
    wb = load_wb()
    ws = wb.sheet_by_name("!")
    return ws
