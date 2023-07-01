#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .load_xl import load_survey_wb


LOADED_SURVEY = dict()

D932_SHEET = "AFS_DEP_ML_AGG_REV_1_12.04.23"

START_LINE = 13

REF_COL = 1
TYPE_COL = 2
TRACK_COL = 3
KP_COL = 4

LIST_OF_TYPES = ["PLATFORM", "SIGNAL", "SIGNAL_BUFFER", "SWP", "TAG", "TC"]


def load_survey() -> dict:
    global LOADED_SURVEY
    if not LOADED_SURVEY:
        wb = load_survey_wb()
        d932_sh = wb.sheet_by_name(D932_SHEET)
        LOADED_SURVEY = get_survey(d932_sh)
    return LOADED_SURVEY


def get_survey(d932_sh: xlrd.sheet) -> dict:
    survey_dict = {type_name: dict() for type_name in LIST_OF_TYPES}
    for line in range(START_LINE, d932_sh.nrows + 1):
        obj_name = get_xlrd_value(d932_sh, line, REF_COL)
        type_name = get_xlrd_value(d932_sh, line, TYPE_COL)
        if obj_name and type_name in LIST_OF_TYPES:
            track = get_xlrd_value(d932_sh, line, TRACK_COL)
            surveyed_kp = get_xlrd_value(d932_sh, line, KP_COL)
            survey_dict[type_name][obj_name] = {"track": track, "surveyed_kp": surveyed_kp}
    return survey_dict
