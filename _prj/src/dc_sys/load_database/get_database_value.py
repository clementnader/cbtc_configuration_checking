#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


__all__ = ["get_database_value"]


def get_database_value(object: dict[str, Any], attribute: dict[str, Any]) -> Any:
    if "column" in attribute:
        return object[attribute["attribute_name"]]
    else:
        list_attributes = object[attribute["attribute_name"]][attribute["sub_attribute_name"]]
        if len(list_attributes) == 1:
            return list_attributes[0]
        list_attributes = [attribute for attribute in list_attributes if attribute is not None]
        return list_attributes
