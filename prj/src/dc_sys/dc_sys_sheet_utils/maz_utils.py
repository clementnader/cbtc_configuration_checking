#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_get_zones import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


__all__ = ["get_maz_in_cbtc_ter", "get_maz_of_point", "get_maz_of_extremities"]


def get_maz_in_cbtc_ter():
    maz_dict = load_sheet(DCSYS.Zaum)
    within_cbtc_maz_dict = dict()
    for maz_name, maz_value in maz_dict.items():
        limits_in_cbtc_ter: list[bool] = list()
        for seg, x in get_dc_sys_zip_values(maz_value, DCSYS.Zaum.Extremite.Seg, DCSYS.Zaum.Extremite.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter) and \
                all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter):
            within_cbtc_maz_dict[maz_name] = maz_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"MAZ {maz_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_maz_dict[maz_name] = maz_value
    return within_cbtc_maz_dict


def get_maz_of_point(seg: str, x: float, direction: str = None) -> Optional[str]:
    list_maz = get_zones_on_point(DCSYS.Zaum, seg, x, direction)
    if not list_maz:
        print_warning(f"No MAZ has been found covering {(seg, x)}.")
        return None
    if len(list_maz) > 1:
        print_warning(f"{(seg, x)} is covered by multiple MAZ: {list_maz}.")
    return list_maz[0]


def get_maz_of_extremities(limits: Union[list[tuple[str, float]], list[tuple[str, float, str]]]) -> list[str]:
    list_maz = list()
    for lim in limits:
        seg, x = lim[0], lim[1]
        if len(lim) > 2:
            direction = lim[2]
        else:
            direction = None
        maz = get_maz_of_point(seg, x, direction)
        if maz not in list_maz:
            list_maz.append(maz)
    return list_maz
