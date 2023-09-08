#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["get_dc_sys_value", "get_dc_sys_values", "get_dc_sys_zip_values"]


def get_dc_sys_value(obj: dict[str], attr: dict[str]):
    if "col" in attr:
        return obj[attr["attr_name"]]
    else:
        list_attrs = obj[attr["attr_name"]][attr["sub_attr_name"]]
        list_attrs = [attr for attr in list_attrs if attr is not None]
        return list_attrs


def get_dc_sys_values(obj: dict[str], *attrs):
    return (get_dc_sys_value(obj, attr) for attr in attrs)


def get_dc_sys_zip_values(obj: dict[str], *attrs):
    gen = get_dc_sys_values(obj, *attrs)
    return zip(*gen)
