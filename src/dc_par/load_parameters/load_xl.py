#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...database_loc import *

DC_PAR_WB = None


def load_dc_par_wb():
    global DC_PAR_WB
    if DC_PAR_WB is None:
        DC_PAR_WB = xlrd.open_workbook(DC_PAR_ADDR)
    return DC_PAR_WB
