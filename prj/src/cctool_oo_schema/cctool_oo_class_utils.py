#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from .cctool_oo_schema import DCSYS


__all__ = ["get_all_sheet_names", "get_class_attr_dict", "get_sh_name", "get_sheet_attributes_columns_dict",
           "get_sheet_class_from_name", "get_dc_sys_attr_name"]


def get_all_sheet_names() -> list[str]:
    return list(get_class_attr_dict(DCSYS).keys())


def get_class_attr_dict(cl) -> dict[str]:
    if isinstance(cl, type):
        return {key: val for key, val in cl.__dict__.items()
                if not (key.startswith("__") and key.endswith("__"))}
    else:
        return {key: val for key, val in cl.__class__.__dict__.items()
                if not (key.startswith("__") and key.endswith("__"))}


def get_sh_name(sh) -> str:
    if isinstance(sh, str):
        return sh
    return sh.__class__.__name__


def get_dc_sys_attr_name(attr) -> str:
    attr = get_sh_name(attr)
    if "__" in attr:
        return attr.split("__")[-1]
    return attr


def get_sheet_attributes_columns_dict(sh) -> dict[str, Union[int, dict[str, int]]]:
    sh = get_sheet_class_from_name(sh)
    class_attr_dict = get_class_attr_dict(sh)
    res_dict = dict()
    for key, val in class_attr_dict.items():
        if isinstance(val, dict):
            res_dict[key] = val["col"]
        else:
            sub_attr_dict = get_class_attr_dict(val)
            res_dict[key] = {sub_key: sub_val["cols"] for sub_key, sub_val in sub_attr_dict.items()}
    return res_dict


def get_sheet_class_from_name(sh_name: str):
    if isinstance(sh_name, str):
        return get_class_attr_dict(DCSYS)[sh_name]
    return sh_name