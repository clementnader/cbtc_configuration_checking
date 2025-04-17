#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .load_sheets import *


__all__ = ["get_dc_sys_value", "get_dc_sys_values", "get_dc_sys_zip_values"]


def get_dc_sys_value(obj: Union[str, dict[str, Any]], attr: dict[str, Any]) -> Any:
    if isinstance(obj, str):
        obj_sheet = attr["sh_name"]
        obj_dict = load_sheet(obj_sheet)
        obj = obj_dict[obj]

    if "col" in attr:
        return obj[attr["attr_name"]]
    else:
        list_attrs = obj[attr["attr_name"]][attr["sub_attr_name"]]
        if len(list_attrs) == 1:
            return list_attrs[0]
        list_attrs = [attr for attr in list_attrs if attr is not None]
        return list_attrs


def get_dc_sys_values(obj: Union[str, dict[str, Any]], *attrs: dict[str, Any]):
    return (get_dc_sys_value(obj, attr) for attr in attrs)


def get_dc_sys_zip_values(obj: Union[str, dict[str, Any]], *attrs: dict[str, Any]):
    gen = get_dc_sys_values(obj, *attrs)
    return zip(*gen)
