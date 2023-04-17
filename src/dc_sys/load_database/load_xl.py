#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...database_loc import *

WB = None
WB_OLD = None


def load_wb(old: bool = False):
    if old:
        global WB_OLD
        if not WB_OLD:
            WB_OLD = xlrd.open_workbook(DC_SYS_ADDR_OLD)
        return WB_OLD
    else:
        global WB
        if not WB:
            WB = xlrd.open_workbook(DC_SYS_ADDR)
        return WB
