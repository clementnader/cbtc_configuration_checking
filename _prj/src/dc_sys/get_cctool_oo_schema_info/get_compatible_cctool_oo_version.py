#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database import open_menu_sheet


__all__ = ["get_cctool_oo_name", "get_cctool_oo_version"]


CCTOOL_OO_NAME_CELL = "A3"
CCTOOL_OO_VERSION_CELL = "A4"


def get_cctool_oo_name() -> str:
    ws = open_menu_sheet()
    cctool_oo_name = get_xl_cell_value(ws, cell=CCTOOL_OO_NAME_CELL)
    if cctool_oo_name.startswith("ADONF"):
        return "ADONF"
    if cctool_oo_name.startswith("CCTool-OO"):
        return "CCTool-OO"
    return cctool_oo_name


def get_cctool_oo_version() -> str:
    ws = open_menu_sheet()
    cctool_oo_version = get_xl_cell_value(ws, cell=CCTOOL_OO_VERSION_CELL)
    return cctool_oo_version
