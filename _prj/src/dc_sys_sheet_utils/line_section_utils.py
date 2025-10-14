#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_line_section_of_object"]


def get_line_section_of_object(object_type, object_name: str, plt_end: str = None) -> Optional[list[str]]:
    if not object_name:
        return None

    if get_sheet_name(object_type) == get_sheet_name(DCSYS.Aig):  # a dedicated function for switches
        return _get_line_section_of_switch(object_name)
    if get_sheet_name(object_type) == get_sheet_name(DCSYS.Quai) and plt_end in ["normal", "reverse"]:
        # a dedicated function for platform ends
        return [_get_line_section_of_plt_end(object_name, plt_end)]

    dedicated_ls = _get_dedicated_line_section_of_object(object_type, object_name)
    if dedicated_ls is not None:
        return [dedicated_ls]

    position = get_object_position(object_type, object_name)
    if isinstance(position, tuple):
        return [get_line_section_of_seg(position[0])]
    if isinstance(position, list):
        return get_line_section_of_extremities(position)
    return None


def get_line_section_of_seg(seg: str) -> str:
    seg_dict = load_sheet(DCSYS.Seg)
    ls = get_dc_sys_value(seg_dict[seg], DCSYS.Seg.Troncon)
    return ls


def get_line_section_of_extremities(limits: list[tuple[str, float]]) -> list[str]:
    list_ls = list()
    for lim in limits:
        seg = lim[0]
        ls = get_line_section_of_seg(seg)
        if ls not in list_ls:
            list_ls.append(ls)
    return list_ls


def _get_dedicated_line_section_of_object(object_type, object_name: str) -> Optional[str]:
    object_dict = load_sheet(object_type)
    object_value = object_dict[object_name]
    object_sheet = get_sheet_class_from_name(object_type)
    sheet_attributes = get_class_attributes_dict(object_sheet).keys()

    if "TronconPreferentiel" in sheet_attributes:
        return get_dc_sys_value(object_value, object_sheet.TronconPreferentiel)
    if "DedicatedLineSection" in sheet_attributes:
        return get_dc_sys_value(object_value, object_sheet.DedicatedLineSection)
    return None


def _get_line_section_of_switch(object_name: str) -> list[str]:
    list_ls = list()
    sw_dict = load_sheet(DCSYS.Aig)
    for seg in get_dc_sys_values(sw_dict[object_name], DCSYS.Aig.SegmentPointe, DCSYS.Aig.SegmentTd, DCSYS.Aig.SegmentTg):
        ls = get_line_section_of_seg(seg)
        if ls not in list_ls:
            list_ls.append(ls)
    return list_ls


def _get_line_section_of_plt_end(object_name: str, plt_end: str) -> str:
    assert plt_end in ["normal", "reverse"]
    plt_dict = load_sheet(DCSYS.Quai)
    if plt_end == "normal":
        plt_end_dir = LineRelatedDirection.SENS_LIGNE
    else:
        plt_end_dir = LineRelatedDirection.SENS_OPPOSE
    plt_end_seg = [seg for (seg, direction) in get_dc_sys_zip_values(plt_dict[object_name],
                   DCSYS.Quai.ExtremiteDuQuai.Seg, DCSYS.Quai.ExtremiteDuQuai.SensExt)
                   if direction == plt_end_dir][0]
    ls = get_line_section_of_seg(plt_end_seg)
    return ls
