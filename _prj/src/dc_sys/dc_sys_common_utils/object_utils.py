#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from .zc_utils import *
from .dcs_ez_utils import *
from .plt_osp_utils import *


__all__ = ["get_objects_list"]


def get_objects_list(obj_type: str) -> list[str]:
    obj_type = get_sh_name(obj_type)

    if "PAS" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.PAS):
        # ZC can have subsets, the key of the sheet will be the subset names so we cannot directly use the sheet key to
        # have the list of ZCs.
        obj_list = get_all_zc()

    elif "DCS_Elementary_Zones" in get_class_attr_dict(DCSYS) and obj_type == get_sh_name(DCSYS.DCS_Elementary_Zones):
        # DCS EZ can have subsets similarly to ZC.
        obj_list = get_all_dcs_elementary_zones()

    elif ("Sig" in get_class_attr_dict(DCSYS) and "DistPap" in get_class_attr_dict(DCSYS.Sig)
          and obj_type == get_sh_name(DCSYS.Sig.DistPap)):
        # We create a fake type to get signal VSP directly using DCSYS.Sig.DistPap as the object type.
        return get_objects_list(DCSYS.Sig)  # list of VSPs is the list of signals

    elif ("Quai" in get_class_attr_dict(DCSYS) and "PointDArret" in get_class_attr_dict(DCSYS.Quai)
          and obj_type == get_sh_name(DCSYS.Quai.PointDArret)):
        # We create a fake type to get platform OSP directly using DCSYS.Quai.PointDArret as the object type.
        obj_list = get_all_plt_osp()

    else:
        obj_dict = load_sheet(obj_type)
        obj_list = list(obj_dict.keys())

    return obj_list
