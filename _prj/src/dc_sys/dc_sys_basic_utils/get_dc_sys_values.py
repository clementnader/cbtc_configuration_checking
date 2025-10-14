#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..load_database import *
from .object_utils import *


__all__ = ["get_dc_sys_value", "get_dc_sys_values", "get_dc_sys_zip_values"]


def get_dc_sys_value(object_value: Union[str, dict[str, Any]], attribute: dict[str, Any],
                     object_sheet: str = None) -> Any:
    if isinstance(object_value, str):
        if object_sheet is None:
            object_sheet = attribute["sheet_name"]
        object_value = get_object_value(object_sheet, object_value)

    return get_database_value(object_value, attribute)


def get_dc_sys_values(object_name: Union[str, dict[str, Any]], *attrs: dict[str, Any],
                      object_sheet: str = None):
    return (get_dc_sys_value(object_name, attribute, object_sheet=object_sheet) for attribute in attrs)


def get_dc_sys_zip_values(object_name: Union[str, dict[str, Any]], *attrs: dict[str, Any],
                          object_sheet: str = None):
    gen = get_dc_sys_values(object_name, *attrs, object_sheet=object_sheet)
    return zip(*gen)
