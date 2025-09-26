#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_draw_path.dc_sys_get_zones import *


__all__ = ["cf_flr_lvl_1"]


def cf_flr_lvl_1():
    print_title(f"Verification of CF_FLR_LVL_1", color=Color.mint_green)
    if not get_objects_list(DCSYS.Floor_Levels):
        print(f"Sheet \"Floor_Levels\" is empty in DC_SYS.")
        return
    get_whole_object_type_kp_limits(DCSYS.Floor_Levels)
