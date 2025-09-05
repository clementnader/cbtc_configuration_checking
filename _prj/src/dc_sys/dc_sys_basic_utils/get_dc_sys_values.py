#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database import *
from .object_utils import *


__all__ = ["get_dc_sys_value", "get_dc_sys_values", "get_dc_sys_zip_values"]


def get_dc_sys_value(obj: Union[str, dict[str, Any]], attr: dict[str, Any], obj_sheet: str = None) -> Any:
    if isinstance(obj, str):
        if obj_sheet is None:
            obj_sheet = attr["sh_name"]
        obj = get_object_value(obj_sheet, obj)

    return get_database_value(obj, attr)


def get_dc_sys_values(obj: Union[str, dict[str, Any]], *attrs: dict[str, Any], obj_sheet: str = None):
    return (get_dc_sys_value(obj, attr, obj_sheet=obj_sheet) for attr in attrs)


def get_dc_sys_zip_values(obj: Union[str, dict[str, Any]], *attrs: dict[str, Any], obj_sheet: str = None):
    gen = get_dc_sys_values(obj, *attrs, obj_sheet=obj_sheet)
    return zip(*gen)
