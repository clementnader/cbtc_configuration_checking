#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from ...database_location import *
from ..cc_param_utils import *
from .get_cc_param_location import *


__all__ = ["get_cc_params"]


CC_PARAMS = dict()


def get_cc_params():
    """ Return the information contained in the csv for each CCParameter.csv file (inside each Cab inside each TU). """
    # We use a global variable to store the info and avoid re-reading each time all the CCParameters.
    global CC_PARAMS
    if not CC_PARAMS:
        _open_all_cc_parameter_files()
    return CC_PARAMS


def _open_all_cc_parameter_files() -> None:
    """ Store inside the global variable, for each CCParameter.csv file (inside each Cab inside each TU),
     the information contained in the csv. """
    global CC_PARAMS
    dict_train_units = get_cc_parameter_location(DATABASE_LOCATION.kit_c11_dir)  # dictionary containing a sub-dict by TU
    # containing a sub-dict by Cab
    for train_cab in dict_train_units.values():  # Cab sub-dict for each TU
        for cc_parameter_path in train_cab.values():  # CCParameter.csv path for each Cab
            CC_PARAMS[cc_parameter_path] = _open_cc_parameter_file(cc_parameter_path)


def _open_cc_parameter_file(cc_parameter_path: str):
    """ Open the CCParameter.csv file and return a dictionary with all CCParameter and their related information. """
    cc_parameter_dict = dict()
    with open(cc_parameter_path, "r") as csv_file:  # open CCParameter.csv file
        lines = csv.reader(csv_file, delimiter=";")
        header_line = lines.__next__()  # store the header line information
        for line in lines:  # start after the header line
            parameter_id = line[ID_COLUMN].lower()
            cc_parameter_dict[parameter_id] = dict()
            for title, value in zip(header_line, line):
                cc_parameter_dict[parameter_id][title] = value
    return cc_parameter_dict
