#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *


__all__ = ["get_reverse_direction", "UnknownDirection", "UnknownSwitchPosition"]


def get_reverse_direction(direction: str) -> Optional[str]:
    if direction == Direction.CROISSANT:
        return Direction.DECROISSANT
    if direction == Direction.DECROISSANT:
        return Direction.CROISSANT
    raise UnknownDirection(direction)


class UnknownDirection(Exception):
    def __init__(self, message):
        super().__init__(message)
        print_error(f"Direction \"{message}\" should be in {get_class_values(Direction)}.")


class UnknownSwitchPosition(Exception):
    def __init__(self, message):
        super().__init__(message)
        print_error(f"Switch Position \"{message}\" should be in {get_class_values(Switch_Position)}.")
