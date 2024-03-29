#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...database_location import *


__all__ = ["load_dc_sys_wb", "erase_dc_sys_wb"]


WB = None
WB_OLD = None


def load_dc_sys_wb(old: bool = False):
    if old:
        global WB_OLD
        if not WB_OLD:
            WB_OLD = xlrd.open_workbook(DATABASE_LOC.dc_sys_addr_old)
        return WB_OLD
    else:
        global WB
        if not WB:
            WB = xlrd.open_workbook(DATABASE_LOC.dc_sys_addr)
        return WB


def erase_dc_sys_wb():
    global WB, WB_OLD
    WB = None
    WB_OLD = None
