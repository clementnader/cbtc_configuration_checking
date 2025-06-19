#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...database_location import *


__all__ = ["load_dc_par_wb"]


DC_PAR_WB = None


def load_dc_par_wb():
    global DC_PAR_WB
    if DC_PAR_WB is None:
        print_log(f"Open DC_PAR file {Color.default}\"{DATABASE_LOC.dc_par_addr}\"{Color.reset}.")
        DC_PAR_WB = load_xlrd_wb(DATABASE_LOC.dc_par_addr)
    return DC_PAR_WB
