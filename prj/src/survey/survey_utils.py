#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *


__all__ = ["check_polarity"]


def check_polarity(dc_sys_kp: Optional[float], surveyed_kp: Optional[float]) -> bool:
    if dc_sys_kp is None or surveyed_kp is None:
        return False
    if abs(dc_sys_kp - surveyed_kp) <= .006 or abs(dc_sys_kp - surveyed_kp) <= abs(abs(dc_sys_kp) - abs(surveyed_kp)):
        return False
    return True
