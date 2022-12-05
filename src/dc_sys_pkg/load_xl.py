#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .utils import *
from ..database_loc import *


def load_wb(old: bool = False):
    if old:
        wb = xlrd.open_workbook(DC_SYS_ADDR_OLD)
    else:
        wb = xlrd.open_workbook(DC_SYS_ADDR)
    return wb

