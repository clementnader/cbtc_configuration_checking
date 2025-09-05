#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *


__all__ = ["get_all_dcs_elementary_zones", "get_dcs_elementary_zone_value"]


def get_all_dcs_elementary_zones() -> list[str]:
    dcs_ez_dict = load_sheet(DCSYS.DCS_Elementary_Zones)
    list_dcs_ez = list()
    for dcs_ez_subset in dcs_ez_dict.values():
        dcs_ez_name = get_database_value(dcs_ez_subset, DCSYS.DCS_Elementary_Zones.Name)
        if dcs_ez_name not in list_dcs_ez:
            list_dcs_ez.append(dcs_ez_name)
    return list_dcs_ez


def get_dcs_elementary_zone_value(dcs_ez_name: str) -> dict[str, Any]:
    dcs_ez_dict = load_sheet(DCSYS.DCS_Elementary_Zones)
    dcs_ez_subset_value = [dcs_ez for dcs_ez in dcs_ez_dict.values()
                           if get_database_value(dcs_ez, DCSYS.DCS_Elementary_Zones.Name) == dcs_ez_name][0]
    # When the DCS Elementary Zone is split between multiple DCS EZ subsets for a matter of maximal number of limits,
    # the information concerning the DCS EZ is on the first subset.
    return dcs_ez_subset_value
