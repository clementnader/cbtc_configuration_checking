#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from ....cctool_oo_schema import *
from ....dc_sys import *
from ..zones_kp_limits import *
from .verif_file import *


__all__ = ["get_whole_object_type_kp_limits"]


def get_whole_object_type_kp_limits(sheet_name):
    sheet_name = get_sh_name(sheet_name)
    object_type_min_max_kp_dict = _get_dict_of_tracks_covered_by_object_type(sheet_name)

    res_file_path = create_verif_file(sheet_name, object_type_min_max_kp_dict)
    open_excel_file(res_file_path)


def _get_dict_of_tracks_covered_by_object_type(sheet_name: str):
    objects_zones_kp_dict = get_dict_of_zones_kp_limits(sheet_name)

    object_type_min_max_kp_dict = dict()

    for object_name, min_max_kp_dict in objects_zones_kp_dict.items():
        for track, list_min_max_kp in min_max_kp_dict.items():
            if track not in object_type_min_max_kp_dict:
                object_type_min_max_kp_dict[track] = list_min_max_kp
            else:
                object_type_min_max_kp_dict[track].extend(list_min_max_kp)

    res_dict = dict()
    for track in get_sorted_track_list():
        if track not in object_type_min_max_kp_dict:
            res_dict[track] = [("-", "-")]
            continue
        list_min_max_kp = object_type_min_max_kp_dict[track]
        res_dict[track] = remove_common_min_max_kp(list_min_max_kp)

    return res_dict
