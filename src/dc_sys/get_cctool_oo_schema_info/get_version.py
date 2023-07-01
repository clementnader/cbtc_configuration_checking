#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database.load_xl import load_wb
from ...utils import *


CCTOOL_OO_VERSION_LINE = 4
CCTOOL_OO_VERSION_COLUMN = 1


def get_major_and_middle_version() -> float:
    version = get_version()
    split_version = version.split(".")
    return float(f"{split_version[0]}.{split_version[1]}")


def get_version() -> str:
    version = get_cctool_oo_version()
    version = version.removeprefix("CCTool-OO-")
    return ".".join([info.removeprefix("0") for info in version.split("_")])


def get_cctool_oo_version() -> str:
    xlrd_line = get_xlrd_line(CCTOOL_OO_VERSION_LINE)
    xlrd_col = get_xlrd_column(CCTOOL_OO_VERSION_COLUMN)
    sh = open_menu_sheet()
    version = sh.cell_value(xlrd_line, xlrd_col)
    return version


def open_menu_sheet():
    wb = load_wb()
    sh = wb.sheet_by_name("!")
    return sh
