#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from .cctool_oo_schema import DCSYS


__all__ = ["get_all_sheet_names", "get_sheet_name", "get_sheet_attributes_columns_dict",
           "get_sheet_class_from_name", "get_dc_sys_attribute_name"]


def get_all_sheet_names() -> list[str]:
    return list(get_class_attributes_dict(DCSYS).keys())


def get_sheet_name(ws: Union[str, dict, Any]) -> str:
    if isinstance(ws, str):
        return ws
    if isinstance(ws, dict):
        if "sub_attribute_name" in ws:
            return f"{ws['sheet_name']}__{ws['attribute_name']}__{ws['sub_attribute_name']}"
        else:
            return f"{ws['sheet_name']}__{ws['attribute_name']}"
    return ws.__class__.__name__


def get_dc_sys_attribute_name(attribute: Union[str, dict, Any]) -> str:
    attribute = get_sheet_name(attribute)
    if "__" in attribute:
        return attribute.split("__")[-1]
    return attribute


def get_sheet_attributes_columns_dict(ws: Union[str, Any]) -> dict[str, Union[int, dict[str, int]]]:
    ws = get_sheet_class_from_name(ws)
    class_attributes_dict = get_class_attributes_dict(ws)
    res_dict = dict()
    for key, val in class_attributes_dict.items():
        if isinstance(val, dict):
            res_dict[key] = val["column"]
        else:
            sub_attr_dict = get_class_attributes_dict(val)
            res_dict[key] = {sub_key: sub_value["columns"] for sub_key, sub_value in sub_attr_dict.items()}
    return res_dict


def get_sheet_class_from_name(sheet_name: Union[str, Any]):
    if isinstance(sheet_name, str):
        return get_class_attributes_dict(DCSYS)[sheet_name]
    return sheet_name
