#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .compare_utils import *


# ------------ Compare Limits of sheets ------------ #

def compare_limits_zc_area():
    compare_limits_sheets(sh_name="PAS", line_ref=3, col_ref='D', nb_max_limits=30, delta_between_limits=6)


def compare_limits_zsm_cbtc():
    compare_limits_sheets(sh_name="ZSM_CBTC", line_ref=3, col_ref='D', nb_max_limits=2, delta_between_limits=4)


# ------------ Compare sheets ------------ #

def compare_slopes():
    return compare_sheets(sh_name="Profil", line_ref=3, cols_ref=['A', 'B', 'C', 'D', 'E'], name_col='F')


def compare_zlpv():
    return compare_sheets(sh_name="ZLPV", line_ref=3, cols_ref=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
                          name_col='L')


def compare_bal():
    return compare_sheets(sh_name="Bal", line_ref=3, cols_ref=['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])


def compare_calib():
    return compare_sheets(sh_name="Calib", line_ref=3, cols_ref=['A', 'B', 'C', 'D'], name_col='E')


def compare_hf_data():
    return compare_sheets(sh_name="Flux_Variant_HF", line_ref=3, cols_ref=['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])


def compare_lf_data():
    return compare_sheets(sh_name="Flux_Variant_BF", line_ref=3, cols_ref=['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
