#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from .cctool_oo_schema import *


__all__ = ["is_ga_octys"]


def is_ga_octys() -> bool:
    if ("CbtcVersionKey" in get_class_attributes_dict(DCSYS.Ligne)
            and "CbtcVersionRelease" in get_class_attributes_dict(DCSYS.Ligne)):
        # These attributes don't exist for OCTYS and exist for other CBTC GAs
        return False
    return True
