#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ..cc_param_utils import *


__all__ = ["get_cc_param_location"]


def get_cc_param_location(input_dir: str):
    """ Return a  dictionary listing for every train unit, every cab and for every cab,
     the corresponding CCParameter.csv path. """
    # input_dir is a C11_D470 directory
    dict_train_units = _get_train_units_dirs(input_dir)  # dictionary containing an empty dictionary for each TU
    for train_dir in dict_train_units:
        # train_dir is equal to TrainUnit_XXX
        for cab_dir in os.listdir(os.path.join(input_dir, train_dir)):  # list every file and directory inside TU dir
            cab_full_path = os.path.join(input_dir, train_dir, cab_dir)
            if os.path.isdir(cab_full_path) and cab_dir.startswith(CAB_DIR_PREFIX):
                # if it is a CabX directory
                cc_param_file_path = os.path.join(cab_full_path, CC_PARAM_DIR, CC_PARAM_FILE)
                # the CCParameter.csv will be inside CCParameter directory inside the CabX directory
                if os.path.exists(cc_param_file_path) and os.path.isfile(cc_param_file_path):
                    # if the CCParameter.csv exists
                    dict_train_units[train_dir][cab_dir] = cc_param_file_path  # store the path for each CabX
                else:
                    print_warning(f"Cab directory {cab_dir} has no {CC_PARAM_FILE} in {CC_PARAM_DIR} directory."
                                  f"{cc_param_file_path}")
    return dict_train_units


def _get_train_units_dirs(input_dir: str):
    """ Return an empty dictionary listing every train unit. """
    # input_dir is a C11_D470 directory
    dict_train_units = dict()
    for train_dir in os.listdir(input_dir):  # list every file and directory inside the C11_D470 directory
        full_path = os.path.join(input_dir, train_dir)
        if os.path.isdir(full_path) and train_dir.startswith(TRAIN_UNIT_PREFIX):
            # if it is a TrainUnit_XXX directory
            dict_train_units[train_dir] = dict()  # initialize an empty dictionary for each train unit
    return sort_dict(dict_train_units)  # sort the result dictionary so that the train units appear in order
