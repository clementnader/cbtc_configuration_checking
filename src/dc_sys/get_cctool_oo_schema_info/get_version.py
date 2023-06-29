#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database.load_xl import load_wb
from ...utils import *

CCTOOL_OO_VERSION_CELL = "A4"


def get_version():
    xlrd_line = get_xlrd_line(int(CCTOOL_OO_VERSION_CELL[1]))
    xlrd_col = get_xlrd_column(CCTOOL_OO_VERSION_CELL[0])
    sh = open_menu_sheet()
    version = sh.cell_value(xlrd_line, xlrd_col)
    return version


def open_menu_sheet():
    wb = load_wb()
    sh = wb.sheet_by_name("!")
    return sh
