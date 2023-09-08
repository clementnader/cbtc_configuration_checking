#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database.load_xl import load_wb
from ...utils import *


__all__ = ["get_cctool_oo_version", "get_ga_version", "get_major_and_middle_version", "get_c_d470_version"]


CCTOOL_OO_VERSION_CELL = "A4"
C_D470_VERSION_CELL = "B6"


def get_major_and_middle_version() -> float:
    version = get_ga_version()
    split_version = version.split(".")
    return float(f"{split_version[0]}.{split_version[1]}")


def get_ga_version() -> str:
    version = get_cctool_oo_version()
    version = version.removeprefix("CCTool-OO-")
    return ".".join([info.removeprefix("0") for info in version.split("_")])


def get_cctool_oo_version() -> str:
    sh = open_menu_sheet()
    version = get_xl_cell_value(sh, cell=CCTOOL_OO_VERSION_CELL)
    return version


def get_c_d470_version() -> str:
    sh = open_menu_sheet()
    version = get_xl_cell_value(sh, cell=C_D470_VERSION_CELL)
    return version


def open_menu_sheet():
    wb = load_wb()
    sh = wb.sheet_by_name("!")
    return sh
