#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *
from ...dc_sys_draw_path.dc_sys_get_zones import *


__all__ = ["cf_flr_lvl_1"]


def cf_flr_lvl_1():
    get_whole_object_type_kp_limits(DCSYS.Floor_Levels)
