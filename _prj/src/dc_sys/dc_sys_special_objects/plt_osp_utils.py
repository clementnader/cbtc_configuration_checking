#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..load_database import *


__all__ = ["get_all_plt_osp", "get_plt_osp_value"]


def get_all_plt_osp() -> list[str]:
    plt_dict = load_sheet(DCSYS.Quai)
    list_plt_osp = list()
    for plt_value in plt_dict.values():
        for osp_name in get_database_value(plt_value, DCSYS.Quai.PointDArret.Name):
            list_plt_osp.append(osp_name)
    return list_plt_osp


def get_plt_osp_value(plt_osp_name: str) -> dict[str, Any]:
    plt_dict = load_sheet(DCSYS.Quai)
    plt_value = [plt for plt in plt_dict.values()
                 if plt_osp_name in get_database_value(plt, DCSYS.Quai.PointDArret.Name)][0]
    return plt_value
