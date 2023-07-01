#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...database_loc import DATABASE_LOC


SURVEY_WB = None


def load_survey_wb():
    global SURVEY_WB
    if SURVEY_WB is None:
        SURVEY_WB = xlrd.open_workbook(DATABASE_LOC.d932_addr)
    return SURVEY_WB
