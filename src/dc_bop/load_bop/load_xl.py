#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...database_loc import DATABASE_LOC

DC_BOP_WB = None


def load_dc_bop_wb():
    global DC_BOP_WB
    if DC_BOP_WB is None:
        DC_BOP_WB = xlrd.open_workbook(DATABASE_LOC.dc_bop_addr)
    return DC_BOP_WB
