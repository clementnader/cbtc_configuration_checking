#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...database_location import *


__all__ = ["load_dc_sys_wb", "erase_dc_sys_wb", "open_menu_sheet"]


WB = None
WB_OLD = None


def load_dc_sys_wb(old: bool = False) -> xlrd.book.Book:
    if old:
        global WB_OLD
        if not WB_OLD:
            print_log(f"Open DC_SYS file \"{DATABASE_LOC.dc_sys_addr_old}\".")
            WB_OLD = load_xlrd_wb(DATABASE_LOC.dc_sys_addr_old, formatting_info=True)
            print()
        return WB_OLD
    else:
        global WB
        if not WB:
            print_log(f"Open DC_SYS file \"{DATABASE_LOC.dc_sys_addr}\".")
            WB = load_xlrd_wb(DATABASE_LOC.dc_sys_addr, formatting_info=True)
            print()
        return WB


def erase_dc_sys_wb():
    global WB, WB_OLD
    WB = None
    WB_OLD = None


def open_menu_sheet():
    wb = load_dc_sys_wb()
    ws = wb.sheet_by_name("!")
    return ws
