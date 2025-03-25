#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....dc_sys import *
from ....cctool_oo_schema import *
from ....dc_sys_draw_path.dc_sys_get_zones import *
from ....dc_sys_sheet_utils import *


__all__ = ["check_pz_ze"]


def check_pz_ze():
    print(get_zones_intersecting_zone(DCSYS.Zaum, DCSYS.CBTC_Protection_Zone, "PZ_SCOL"))

    list_zc = get_all_zc()
    results = {zc_name: dict() for zc_name in list_zc}
    pz_dict = load_sheet(DCSYS.CBTC_Protection_Zone)
    pz_per_zc = {zc_name: sorted([pz_name for pz_name in pz_dict
                                  if zc_name in get_zc_of_obj(DCSYS.CBTC_Protection_Zone, pz_name)])
                 for zc_name in list_zc}

    for zc_name in list_zc:
        for pz_name in pz_per_zc[zc_name]:
            list_maz_intersecting_pz = get_zones_intersecting_zone(DCSYS.Zaum, DCSYS.CBTC_Protection_Zone, pz_name)
            list_ze_intersecting_pz = [f"ZE_{maz_name}" for maz_name in list_maz_intersecting_pz]
            results[zc_name][pz_name] = list_ze_intersecting_pz

    pretty_print_dict(results)
    return
