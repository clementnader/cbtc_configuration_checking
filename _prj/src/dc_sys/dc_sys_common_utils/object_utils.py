#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .zc_utils import *
from .dcs_ez_utils import *


__all__ = ["get_objects_list"]


def get_objects_list(obj_type: str) -> list[str]:
    obj_type = get_sh_name(obj_type)

    if "PAS" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.PAS):
        obj_list = get_all_zc()
    elif "DCS_Elementary_Zones" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.DCS_Elementary_Zones):
        obj_list = get_all_dcs_elementary_zones()
    elif ("Sig" in get_class_attr_dict(DCSYS) and "DistPap" in get_class_attr_dict(DCSYS.Sig)
          and obj_type == get_sh_name(DCSYS.Sig.DistPap)):
        # list of VSPs is the list of signals
        return get_objects_list(DCSYS.Sig)
    else:
        obj_dict = load_sheet(obj_type)
        obj_list = list(obj_dict.keys())

    return obj_list
