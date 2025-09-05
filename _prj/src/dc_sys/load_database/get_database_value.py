#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


__all__ = ["get_database_value"]


def get_database_value(obj: dict[str, Any], attr: dict[str, Any]) -> Any:
    if "col" in attr:
        return obj[attr["attr_name"]]
    else:
        list_attrs = obj[attr["attr_name"]][attr["sub_attr_name"]]
        if len(list_attrs) == 1:
            return list_attrs[0]
        list_attrs = [attr for attr in list_attrs if attr is not None]
        return list_attrs
