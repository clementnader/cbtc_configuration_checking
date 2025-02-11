#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from ...utils import *
from ..load_database.load_xl import load_dc_sys_wb


__all__ = ["get_cctool_oo_name", "get_dc_sys_version", "get_line_name", "get_current_version"]


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
    wb = load_dc_sys_wb()
    ws = wb.sheet_by_name("!")
    return ws


def get_line_name() -> str:
    ws = open_line_sheet()
    version = get_xl_cell_value(ws, cell=LINE_NAME_CELL)
    return version


def open_line_sheet():
    wb = load_dc_sys_wb()
    ws = wb.sheet_by_name("Ligne")
    return ws


def get_current_version() -> str:
    c_d470 = get_c_d470_version()
    if c_d470:
        if "_C_D470_" in c_d470.upper():
            return c_d470
        dc_sys_version = get_dc_sys_version()
        if "_C_D470_" in dc_sys_version.upper():
            return dc_sys_version
        for directory in get_dc_sys_folder().split(os.sep):  # check at any upper levels in DC_SYS folder
            if "_C_D470_" in directory.upper():
                return directory
        return get_line_name()

    c11_d470 = get_c11_d470_version()
    if c11_d470:
        return c11_d470

    c121_d470 = get_c121_d470_version()
    if c121_d470:
        return c121_d470

    return "PRJ"
