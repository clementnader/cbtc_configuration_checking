#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .load_dc_tu_information import *
from .analyze_dc_tu import *
from .dc_tu_result_file import *

__all__ = ["dc_tu_verification"]


def dc_tu_verification():
    dc_tu_dict = load_dc_tu_information()
    ip_address_dict, ssh_key_dict = get_ip_address_and_ssh_key(dc_tu_dict)
    res_file_path = create_dc_tu_verif_file(ip_address_dict, ssh_key_dict)
    open_excel_file(res_file_path)
