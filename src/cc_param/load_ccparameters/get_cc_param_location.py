#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ..cc_param_utils import *


__all__ = ["get_cc_param_location"]


def get_cc_param_location(input_dir):
    dict_train_units = get_train_units_dirs(input_dir)
    for train_dir in dict_train_units:
        for cab_dir in os.listdir(os.path.join(input_dir, train_dir)):
            cab_full_path = os.path.join(input_dir, train_dir, cab_dir)
            if os.path.isdir(cab_full_path) and cab_dir.startswith(CAB_DIR_PREFIX):
                cc_param_file_path = os.path.join(cab_full_path, CC_PARAM_DIR, CC_PARAM_FILE)
                if os.path.exists(cc_param_file_path) and os.path.isfile(cc_param_file_path):
                    dict_train_units[train_dir][cab_dir] = cc_param_file_path
                else:
                    print_warning(f"Cab directory {cab_dir} has no {CC_PARAM_FILE} in {CC_PARAM_DIR} directory."
                                  f"{cc_param_file_path}")
    return dict_train_units


def get_train_units_dirs(input_dir):
    dict_train_units = dict()
    for train_dir in os.listdir(input_dir):
        full_path = os.path.join(input_dir, train_dir)
        if os.path.isdir(full_path) and train_dir.startswith(TRAIN_UNIT_PREFIX):
            dict_train_units[train_dir] = dict()
    return sort_dict(dict_train_units)
