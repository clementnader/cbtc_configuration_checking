#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database.load_xl import load_wb


__all__ = ["get_cctool_oo_name", "get_dc_sys_version", "get_line_name"]


CCTOOL_OO_VERSION_CELL = "A4"
DC_SYS_VERSION_CELL = "B6"
LINE_NAME_CELL = "A3"


def get_cctool_oo_name() -> str:
    ws = open_menu_sheet()
    version = get_xl_cell_value(ws, cell=CCTOOL_OO_VERSION_CELL)
    return version


def get_dc_sys_version() -> str:
    ws = open_menu_sheet()
    version = get_xl_cell_value(ws, cell=DC_SYS_VERSION_CELL)
    return version


def open_menu_sheet():
    wb = load_wb()
    ws = wb.sheet_by_name("!")
    return ws


def get_line_name() -> str:
    ws = open_line_sheet()
    version = get_xl_cell_value(ws, cell=LINE_NAME_CELL)
    return version


def open_line_sheet():
    wb = load_wb()
    ws = wb.sheet_by_name("Ligne")
    return ws
