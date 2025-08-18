#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from .cctool_oo_enum_lists import *


__all__ = ["UnknownDirection", "UnknownSwitchPosition", "UnknownOSPType"]


class UnknownDirection(Exception):
    def __init__(self, message):
        super().__init__(message)
        print_error(f"Direction \"{message}\" should be in {get_class_values(Direction)}.")


class UnknownSwitchPosition(Exception):
    def __init__(self, message):
        super().__init__(message)
        print_error(f"Switch Position \"{message}\" should be in {get_class_values(Switch_Position)}.")


class UnknownOSPType(Exception):
    def __init__(self, message):
        super().__init__(message)
        print_error(f"OSP Type \"{message}\" should be in {get_class_values(StoppingPointType)}.")
