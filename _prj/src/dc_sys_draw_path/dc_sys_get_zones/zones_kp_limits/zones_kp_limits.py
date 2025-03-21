#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ..zones_utils import get_segments_within_zone, get_zone_limits
from .result_file import *


__all__ = ["get_zones_kp_limits"]


def get_zones_kp_limits(sheet_name: str):
    sheet_name = get_sh_name(sheet_name)
    res_dict = dict()
    sheet_dict = load_sheet(sheet_name)
    for obj_name in sheet_dict.keys():
        res_dict[obj_name] = _get_limits_on_every_track(sheet_name, obj_name)

    res_file_path = create_verif_file(sheet_name, res_dict)
    open_excel_file(res_file_path)


def _get_limits_on_every_track(obj_type, obj_name: str) -> Optional[dict[str, list[tuple[float, float]]]]:
    segs_in_zone = get_segments_within_zone(obj_type, obj_name)
    zone_limits = get_zone_limits(obj_type, obj_name)
    if segs_in_zone is None or zone_limits is None:
        return None

    min_max_kp_dict = _get_track_dict_for_within_zone_segs(segs_in_zone)
    min_max_kp_dict = _update_kp_track_dict(min_max_kp_dict, _get_track_dict_for_limits(zone_limits))

    res_dict = dict()

    for track in sorted(min_max_kp_dict):
        list_min_max_kp = min_max_kp_dict[track]
        res_dict[track] = remove_common_min_max_kp(list_min_max_kp)

    return res_dict


def _update_kp_track_dict(min_max_kp_dict, limits_kp_dict):
    for track, list_min_max_kp in limits_kp_dict.items():
        if track not in min_max_kp_dict:
            min_max_kp_dict[track] = list_min_max_kp
        else:
            min_max_kp_dict[track].extend(list_min_max_kp)
    return min_max_kp_dict


def _get_track_dict_for_within_zone_segs(segs_in_zone: set[str]):
    res_dict = dict()
    seg_dict = load_sheet(DCSYS.Seg)
    for seg in segs_in_zone:
        seg_val = seg_dict[seg]
        track = get_dc_sys_value(seg_val, DCSYS.Seg.Voie)
        start_kp, end_kp = get_dc_sys_values(seg_val, DCSYS.Seg.Origine, DCSYS.Seg.Fin)
        if track not in res_dict:
            res_dict[track] = list()
        res_dict[track].append((start_kp, end_kp))

    return res_dict


def _get_track_dict_for_limits(zone_limits: list[tuple[str, float, bool]]):
    res_dict = dict()
    seg_dict = load_sheet(DCSYS.Seg)
    for (seg, x, downstream) in zone_limits:
        track, kp = from_seg_offset_to_kp(seg, x)
        if track not in res_dict:
            res_dict[track] = list()

        other_limit_offset_on_seg = _get_other_limit_on_seg(seg, x, downstream, zone_limits)

        if other_limit_offset_on_seg is not None:
            _, other_kp = from_seg_offset_to_kp(seg, other_limit_offset_on_seg)
            if (kp, other_kp) in res_dict[track] or (other_kp, kp) in res_dict[track]:
                # Already inside the dictionary due to the other limit on segment, don't duplicate it.
                continue

            if downstream:
                res_dict[track].append((kp, other_kp))
            else:
                res_dict[track].append((other_kp, kp))

        else:
            seg_val = seg_dict[seg]
            start_kp, end_kp = get_dc_sys_values(seg_val, DCSYS.Seg.Origine, DCSYS.Seg.Fin)
            if downstream:
                res_dict[track].append((kp, end_kp))
            else:
                res_dict[track].append((start_kp, kp))

    return res_dict


def _get_other_limit_on_seg(start_seg: str, start_x: float, downstream: bool,
                            zone_limits: list[tuple[str, float, bool]]) -> Optional[float]:

    for limit_seg, limit_x, limit_downstream in zone_limits:
        if (limit_seg, limit_x, limit_downstream) == (start_seg, start_x, downstream):
            # the limit corresponding to the start point
            continue
        if (limit_seg, limit_x, limit_downstream) == (start_seg, start_x, not downstream):
            # limit corresponding to the start point in opposite direction
            return limit_x

        if start_seg == limit_seg:
            if (downstream and start_x <= limit_x) or (not downstream and start_x >= limit_x):
                if not downstream == limit_downstream:
                    return limit_x
    return None
