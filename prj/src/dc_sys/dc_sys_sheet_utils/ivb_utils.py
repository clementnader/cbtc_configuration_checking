#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_common_utils import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


__all__ = ["get_ivb_in_cbtc_ter", "get_next_ivb_limits_from_point", "get_all_ivb_limits"]


def get_ivb_in_cbtc_ter():
    ivb_dict = load_sheet(DCSYS.IVB)
    within_cbtc_ivb_dict = dict()
    for ivb, ivb_value in ivb_dict.items():
        limits_in_cbtc_ter = list()
        for seg, x in get_dc_sys_zip_values(ivb_value, DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter) and \
                all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter):
            within_cbtc_ivb_dict[ivb] = ivb_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"IVB {ivb} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_ivb_dict[ivb] = ivb_value
    return within_cbtc_ivb_dict


def get_next_ivb_limits_from_point(seg: str, x: float, downstream: bool):
    dict_ivb_limits = get_all_ivb_limits()
    next_ivb_limits = list()

    ivb_limit = _get_next_ivb_limit_on_a_seg(seg, downstream, list(dict_ivb_limits.keys()), start_x=x)
    if ivb_limit is not None:
        next_ivb_limits.append((ivb_limit, dict_ivb_limits[ivb_limit]))
        return next_ivb_limits

    def inner_recurs_seg(current_seg):
        nonlocal next_ivb_limits
        next_segs = get_linked_segs(current_seg, downstream)
        for next_seg in next_segs:
            next_ivb_limit = _get_next_ivb_limit_on_a_seg(next_seg, downstream, list(dict_ivb_limits.keys()))
            if next_ivb_limit is not None:
                next_ivb_limits.append((next_ivb_limit, dict_ivb_limits[next_ivb_limit]))
                return
            inner_recurs_seg(next_seg)

    inner_recurs_seg(seg)
    return next_ivb_limits


def get_all_ivb_limits() -> dict[tuple[str, float], str]:
    dict_ivb_limits = dict()
    ivb_dict = load_sheet(DCSYS.IVB)
    for ivb_name, ivb in ivb_dict.items():
        ivb_limits = list(get_dc_sys_zip_values(ivb, DCSYS.IVB.Limit.Seg, DCSYS.IVB.Limit.X))
        for ivb_limit in ivb_limits:
            _add_limits_to_dict(ivb_name, ivb_limit, dict_ivb_limits)
    return dict_ivb_limits


def _add_limits_to_dict(ivb_name: str, ivb_limit: tuple[str, float], dict_ivb_limits: dict[tuple[str, float], str]) \
        -> None:
    for limit, ivb_names in dict_ivb_limits.items():
        if are_points_matching(limit[0], limit[1], ivb_limit[0], ivb_limit[1]):
            ivb_names += " - " + ivb_name
            dict_ivb_limits[limit] = ivb_names
            return
    dict_ivb_limits[ivb_limit] = ivb_name
    return


def _get_next_ivb_limit_on_a_seg(seg: str, downstream: bool, ivb_limits: list[tuple[str, float]],
                                 start_x: float = None) -> Optional[tuple[str, float]]:
    matching_ivb_limits = list()
    for lim_seg, lim_x in ivb_limits:
        if lim_seg == seg:
            if start_x is None or (downstream and start_x <= lim_x) or (not downstream and start_x >= lim_x):
                matching_ivb_limits.append((lim_seg, lim_x))
    if not matching_ivb_limits:
        return None
    if len(matching_ivb_limits) == 1:
        return matching_ivb_limits[0]
    matching_ivb_limits.sort(key=lambda x: x[1])
    return matching_ivb_limits[0] if downstream else matching_ivb_limits[-1]
