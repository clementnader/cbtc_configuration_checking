#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..dc_sys import *
from ..cctool_oo_schema import *
from ..dc_sys_sheet_utils.train_utils import get_train_length


__all__ = ["get_max_train_len_at_plt_osp"]


def get_max_train_len_at_plt_osp(osp_name: str) -> float:
    consist_osp_dict = load_sheet(DCSYS.Consist_OSP)
    train_consist_list = get_dc_sys_value(consist_osp_dict[osp_name], DCSYS.Consist_OSP.AuthorisedConsist.ConsistName)
    max_len = max(get_train_length(train_consist) for train_consist in train_consist_list)
    return max_len
