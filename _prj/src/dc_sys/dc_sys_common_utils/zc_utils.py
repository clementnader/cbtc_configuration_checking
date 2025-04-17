#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *


__all__ = ["get_all_zc", "get_zc_value"]


def get_all_zc() -> list[str]:
    zc_dict = load_sheet(DCSYS.PAS)
    list_zc = list()
    for zc_subset in zc_dict.values():
        zc_name = get_dc_sys_value(zc_subset, DCSYS.PAS.Nom)
        if zc_name not in list_zc:
            list_zc.append(zc_name)
    return list_zc


def get_zc_value(zc_name: str) -> dict[str, Any]:
    zc_dict = load_sheet(DCSYS.PAS)
    zc_subset_value = [zc for zc in zc_dict.values()
                       if get_dc_sys_value(zc, DCSYS.PAS.Nom) == zc_name][0]
    # When the ZC is split between multiple ZC subsets for a matter of maximal number of limits reached,
    # the information concerning the ZC is on the first subset.
    return zc_subset_value
