#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *


__all__ = ["get_reverse_direction"]


def get_reverse_direction(direction: str) -> Optional[str]:
    if direction == Direction.CROISSANT:
        return Direction.DECROISSANT
    if direction == Direction.DECROISSANT:
        return Direction.CROISSANT
    return None
