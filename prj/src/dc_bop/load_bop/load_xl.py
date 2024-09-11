#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...database_location import *


__all__ = ["load_dc_bop_wb"]


DC_BOP_WB = None


def load_dc_bop_wb():
    global DC_BOP_WB
    if DC_BOP_WB is None:
        DC_BOP_WB = load_xlrd_wb(DATABASE_LOC.dc_bop_addr)
    return DC_BOP_WB
