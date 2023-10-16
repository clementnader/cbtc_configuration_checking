#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


__all__ = ["load_survey_wb"]


SURVEY_WB = dict()


def load_survey_wb(survey_addr):
    global SURVEY_WB
    if survey_addr not in SURVEY_WB:
        SURVEY_WB[survey_addr] = load_xl_file(survey_addr)
    return SURVEY_WB[survey_addr]
