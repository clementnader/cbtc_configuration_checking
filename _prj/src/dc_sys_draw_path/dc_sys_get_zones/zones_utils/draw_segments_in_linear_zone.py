#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
# from ....dc_sys import *
# from ..get_oriented_limits import *


__all__ = []


LINEAR_ZONE_OBJECTS = {
    "ZLPV": DCSYS.ZLPV if "ZLPV" in get_class_attr_dict(DCSYS) else None,
    "ZLPV_Or": DCSYS.ZLPV_Or if "ZLPV_Or" in get_class_attr_dict(DCSYS) else None,
    "ZSM_CBTC": DCSYS.ZSM_CBTC if "ZSM_CBTC" in get_class_attr_dict(DCSYS) else None,
    "NV_PSR": DCSYS.NV_PSR if "NV_PSR" in get_class_attr_dict(DCSYS) else None,
    "IXL_Overlap": DCSYS.IXL_Overlap if "IXL_Overlap" in get_class_attr_dict(DCSYS) else None,
    "Calib": DCSYS.Calib if "Calib" in get_class_attr_dict(DCSYS) else None,
    # en fait pas besoin de cette liste : il s'agit de toutes les zones de type De/À ou From/To (les PSR),
    # avec aussi ZSM_CBTC avec les 2 Ext ZSM
    # et IXL_Overlap parce que c'est From RP To VSP,
    # et Calib parce que c'est From Start Tag To End Tag,
    # et les Flank Protection Areas (et après il faut faire l'union des zones)
}

# TODO linear zones
