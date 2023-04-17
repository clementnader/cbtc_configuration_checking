#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from ...database_loc import KIT_C11_DIR
from ..cc_param_utils import *
from .get_cc_param_location import get_cc_param_location


CC_PARAMS = dict()


def get_cc_params():
    if not CC_PARAMS:
        open_all_cc_param_files()
    return CC_PARAMS


def open_cc_param_file(path):
    cc_param_dict = dict()
    with open(path, 'r') as csv_file:
        lines = csv.reader(csv_file, delimiter=';')
        first_line = lines.__next__()
        for line in lines:
            param_id = line[ID_COLUMN].lower()
            cc_param_dict[param_id] = dict()
            for title, value in zip(first_line, line):
                cc_param_dict[param_id][title] = value
    return cc_param_dict


def open_all_cc_param_files():
    dict_train_units = get_cc_param_location(KIT_C11_DIR)
    for train_cab in dict_train_units.values():
        for path in train_cab.values():
            CC_PARAMS[path] = open_cc_param_file(path)
