#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


__all__ = ["load_survey_wb"]


SURVEY_WB = dict()


def load_survey_wb(d932_addr):
    global SURVEY_WB
    if d932_addr not in SURVEY_WB:
        SURVEY_WB[d932_addr] = load_xl_file(d932_addr)
    return SURVEY_WB[d932_addr]
