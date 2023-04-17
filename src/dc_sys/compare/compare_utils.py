#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..load_database import load_sheet
from ...utils import compare_dict


def compare_sheets(obj_name):
    dict_old = load_sheet(obj_name, old=True)
    dict_new = load_sheet(obj_name, old=False)
    return compare_dict(dict_old, dict_new, "old", "new")
