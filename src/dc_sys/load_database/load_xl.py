#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...database_loc import DATABASE_LOC

WB = None
WB_OLD = None


def load_wb(old: bool = False):
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
