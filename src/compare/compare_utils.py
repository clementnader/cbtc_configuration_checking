#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_sys import *
from ..utils import *


def compare_sheets(obj_name):
    dict_new = load_sheet(obj_name, old=False)
    dict_old = load_sheet(obj_name, old=True)
    return compare_dict(dict_new, dict_old, "new", "old")
