#!/usr/bin/env python
# -*- coding: utf-8 -*-


TRAIN_UNIT_PREFIX = r"TrainUnit_"
CAB_DIR_PREFIX = r"Cab"
CC_PARAM_DIR = r"CCParameter"
CC_PARAM_FILE = r"CCParameter.csv"

RANK_COLUMN = 0
ID_COLUMN = 1
VALUE_COLUMN = 2
INFO_COLUMN = 5

RANK_TITLE = "RANK"
ID_TITLE = "ID"
VALUE_TITLE = "VALUE"
UNITS_TITLE = "UNITS"
CONVERSION_TITLE = "CONVERSION"
INFO_TITLE = "INFO"


def get_num_train(train: str) -> int:
    return int(train.split(TRAIN_UNIT_PREFIX)[1])


def get_type_of_train(train_num: int, types_of_train: list[str], list_train_num_limits: list[str]):
    for type_of_train, train_num_lim in zip(types_of_train, list_train_num_limits):
        inf = int(train_num_lim.split("-")[0])
        sup = int(train_num_lim.split("-")[1])
        if inf <= train_num <= sup:
            return type_of_train
    return None
