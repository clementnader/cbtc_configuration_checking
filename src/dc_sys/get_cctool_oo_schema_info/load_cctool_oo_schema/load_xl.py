#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["load_cctool_oo_schema_wb"]


CCTOOL_OO_SCHEMA_WB = None


def load_cctool_oo_schema_wb(addr):
    global CCTOOL_OO_SCHEMA_WB
    if CCTOOL_OO_SCHEMA_WB is None:
        CCTOOL_OO_SCHEMA_WB = xlrd.open_workbook(addr)
    return CCTOOL_OO_SCHEMA_WB
