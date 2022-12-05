#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .compare_utils import *


def compare_zc_area():
    compare_sheets("zc_area")


def compare_zsm_cbtc():
    compare_sheets("zsm_cbtc")


def compare_slope():
    return compare_sheets("slope")


def compare_zlpv():
    return compare_sheets("zlpv")


def compare_tag():
    return compare_sheets("tag")


def compare_calib():
    return compare_sheets("calib")


def compare_hf_data():
    return compare_sheets("hf_data")


def compare_lf_data():
    return compare_sheets("lf_data")
