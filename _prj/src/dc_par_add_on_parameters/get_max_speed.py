#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_par import *
from .get_train_max_speed import get_train_max_speed


__all__ = ["get_max_speed"]


def get_max_speed(variables: dict = None) -> float:
    train_max_speed = get_train_max_speed()
    line_max_speed = get_parameter_value("line_max_speed", variables)
    return min(line_max_speed, train_max_speed)
