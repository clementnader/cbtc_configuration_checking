#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *
from ..dc_sys_common_utils import *
from .cbtc_territory_utils import is_point_in_cbtc_ter


__all__ = ["get_maz_in_cbtc_ter", "get_segs_within_maz", "is_point_in_maz",
           "get_maz_of_point", "get_maz_of_extremities"]


MAZ_SEGMENTS = dict()
MAZ_LIMITS = dict()


def get_maz_in_cbtc_ter():
    maz_dict = load_sheet(DCSYS.Zaum)
    within_cbtc_maz_dict = dict()
    for maz_name, maz_value in maz_dict.items():
        limits_in_cbtc_ter: list[bool] = list()
        for seg, x in get_dc_sys_zip_values(maz_value, DCSYS.Zaum.Extremite.Seg, DCSYS.Zaum.Extremite.X):
            limits_in_cbtc_ter.append(is_point_in_cbtc_ter(seg, x))
        if all(lim_in_cbtc_ter is not False for lim_in_cbtc_ter in limits_in_cbtc_ter):
            within_cbtc_maz_dict[maz_name] = maz_value
        elif any(lim_in_cbtc_ter is True for lim_in_cbtc_ter in limits_in_cbtc_ter):
            print_warning(f"MAZ {maz_name} is both inside and outside CBTC Territory. "
                          f"It is still taken into account.")
            within_cbtc_maz_dict[maz_name] = maz_value
    return within_cbtc_maz_dict


def get_all_maz():
    maz_dict = load_sheet(DCSYS.Zaum)
    return list(maz_dict.keys())


def get_segs_within_maz(maz_name: str) -> set[str]:
    global MAZ_SEGMENTS
    if not MAZ_SEGMENTS:
        update_segs_within_maz()
    return set([seg for seg, _ in MAZ_SEGMENTS[maz_name]])


def get_all_segs_in_maz(maz_name: str) -> set[str]:
    maz_segments = get_segs_within_maz(maz_name)
    maz_limits = get_maz_limits(maz_name)
    return maz_segments.union([seg for seg, _, _ in maz_limits])


def get_maz_limits(maz_name: str) -> list[tuple[str, float, bool]]:
    global MAZ_LIMITS
    if not MAZ_LIMITS:
        update_segs_within_maz()
    return MAZ_LIMITS[maz_name]


def update_segs_within_maz() -> None:
    global MAZ_SEGMENTS
    if MAZ_SEGMENTS:
        return

    maz_dict = load_sheet(DCSYS.Zaum)
    for maz_name, maz_info in maz_dict.items():
        MAZ_SEGMENTS[maz_name] = list()
        maz_limits = get_start_and_end_limits_maz(maz_info)
        for start_lim in maz_limits:
            start_seg, start_x, start_direction = start_lim
            get_next_segments(maz_name, start_seg, start_x, start_direction, maz_limits)
        update_maz_limits(maz_name, maz_limits)


def get_start_and_end_limits_maz(maz_info: dict[str]) -> list[tuple[str, float, bool]]:
    maz_limits = list()

    for seg, x, direction in get_dc_sys_zip_values(maz_info, DCSYS.Zaum.Extremite.Seg,
                                                   DCSYS.Zaum.Extremite.X, DCSYS.Zaum.Extremite.Sens):
        maz_limits.append((seg, x, (direction == Direction.CROISSANT)))

    return maz_limits


def get_next_segments(maz_name: str, start_seg: str, start_x: float, downstream: bool,
                      maz_limits: list[tuple[str, float, bool]]) -> None:
    global MAZ_SEGMENTS

    if is_first_seg_on_another_limit(start_seg, start_x, downstream, maz_limits):
        return

    def inner_recurs_next_seg(seg: str, inner_downstream: bool):
        global MAZ_SEGMENTS
        for next_seg in get_linked_segs(seg, inner_downstream):
            if is_seg_depolarized(next_seg) and seg in get_associated_depol(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            if is_seg_end_limit(next_seg, next_inner_downstream, maz_limits):
                continue
            if (next_seg, next_inner_downstream) in MAZ_SEGMENTS[maz_name]:
                continue
            MAZ_SEGMENTS[maz_name].append((next_seg, next_inner_downstream))
            inner_recurs_next_seg(next_seg, next_inner_downstream)

    inner_recurs_next_seg(start_seg, downstream)


def is_first_seg_on_another_limit(start_seg: str, start_x: float, downstream: bool,
                                  maz_limits: list[tuple[str, float, bool]]) -> bool:
    for limit_seg, limit_x, limit_downstream in maz_limits:
        if start_seg == limit_seg:
            if (downstream and start_x < limit_x) or (not downstream and start_x > limit_x):
                if not downstream == limit_downstream:
                    return True
                print_warning("Reach a MAZ limit but with a different direction.")
                print(f"{start_seg = }, {start_x = }, {downstream = }")
                print((limit_seg, limit_x, limit_downstream))
                return True
    return False


def is_seg_end_limit(seg: str, downstream: bool, maz_limits: list[tuple[str, float, bool]]) -> bool:
    if (seg, not downstream) in [(limit_seg, limit_downstream) for limit_seg, _, limit_downstream in maz_limits]:
        return True
    if seg in [limit_seg for limit_seg, _, _ in maz_limits]:
        print_warning("Reach a MAZ limit but with a different direction.")
        print(f"{seg = }, {downstream = }")
        print([limit_seg for limit_seg, _, _ in maz_limits if seg == limit_seg])
        return True
    return False


def update_maz_limits(maz_name: str, maz_limits: list[tuple[str, float, bool]]) -> None:
    global MAZ_LIMITS
    MAZ_LIMITS[maz_name] = list()
    for lim in maz_limits:
        MAZ_LIMITS[maz_name].append(lim)


def is_point_in_maz(seg: str, x: float, maz_name: str, direction: str = None) -> Optional[bool]:
    x = float(x)
    maz_segments = get_segs_within_maz(maz_name)
    maz_limits = get_maz_limits(maz_name)
    if seg in maz_segments:
        return True
    limits_on_seg = [(lim_seg, lim_x, lim_downstream) for lim_seg, lim_x, lim_downstream in maz_limits
                     if lim_seg == seg]
    if not limits_on_seg:
        return False
    closest_limit = sorted(limits_on_seg, key=lambda a: abs(a[1] - x))[0]
    lim_seg, lim_x, lim_downstream = closest_limit
    if x == lim_x:  # limit point
        if direction is not None:
            if lim_downstream == (direction == Direction.CROISSANT):
                return True
            else:
                return False
        return None
    if (lim_downstream and x > lim_x) or (not lim_downstream and x < lim_x):
        return True
    return False


def get_maz_of_point(seg: str, x: float, direction: str = None) -> Optional[str]:
    list_maz = list()
    for maz_name in get_all_maz():
        if is_point_in_maz(seg, x, maz_name, direction) is True:
            list_maz.append(maz_name)
        # if direction is None and is_point_in_maz(seg, x, maz_name) is None:
        #     print(f"Point {(seg, x)} is at limit of {maz_name}.")
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
