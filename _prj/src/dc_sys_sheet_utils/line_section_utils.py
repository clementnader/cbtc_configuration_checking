#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..cctool_oo_schema import *
from ..dc_sys import *


__all__ = ["get_line_section_of_obj"]


def get_line_section_of_obj(obj_type, obj_name: str, plt_end: str = None) -> Optional[list[str]]:
    if not obj_name:
        return None

    if get_sh_name(obj_type) == get_sh_name(DCSYS.Aig):  # a dedicated function for switches
        return _get_line_section_of_switch(obj_name)
    if get_sh_name(obj_type) == get_sh_name(DCSYS.Quai) and plt_end in ["normal", "reverse"]:
        # a dedicated function for platform ends
        return [_get_line_section_of_plt_end(obj_name, plt_end)]

    dedicated_ls = _get_dedicated_line_section_of_obj(obj_type, obj_name)
    if dedicated_ls is not None:
        return [dedicated_ls]

    position = get_obj_position(obj_type, obj_name)
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


def _get_dedicated_line_section_of_obj(obj_type, obj_name: str) -> Optional[str]:
    obj_dict = load_sheet(obj_type)
    obj_val = obj_dict[obj_name]
    obj_sh = get_sheet_class_from_name(obj_type)
    sh_attrs = get_class_attr_dict(obj_sh).keys()

    if "TronconPreferentiel" in sh_attrs:
        return get_dc_sys_value(obj_val, obj_sh.TronconPreferentiel)
    if "DedicatedLineSection" in sh_attrs:
        return get_dc_sys_value(obj_val, obj_sh.DedicatedLineSection)
    return None


def _get_line_section_of_switch(obj_name: str) -> list[str]:
    list_ls = list()
    sw_dict = load_sheet(DCSYS.Aig)
    for seg in get_dc_sys_values(sw_dict[obj_name], DCSYS.Aig.SegmentPointe, DCSYS.Aig.SegmentTd, DCSYS.Aig.SegmentTg):
        ls = get_line_section_of_seg(seg)
        if ls not in list_ls:
            list_ls.append(ls)
    return list_ls


def _get_line_section_of_plt_end(obj_name: str, plt_end: str) -> str:
    assert plt_end in ["normal", "reverse"]
    plt_dict = load_sheet(DCSYS.Quai)
    if plt_end == "normal":
        plt_end_dir = LineRelatedDirection.SENS_LIGNE
    else:
        plt_end_dir = LineRelatedDirection.SENS_OPPOSE
    plt_end_seg = [seg for (seg, direction) in get_dc_sys_zip_values(plt_dict[obj_name],
                   DCSYS.Quai.ExtremiteDuQuai.Seg, DCSYS.Quai.ExtremiteDuQuai.SensExt)
                   if direction == plt_end_dir][0]
    ls = get_line_section_of_seg(plt_end_seg)
    return ls
