#!/usr/bin/env python
# -*- coding: utf-8 -*-


import openpyxl.utils as xl_ut  # for column_index_from_string and get_column_letter
import xlrd


def get_xlrd_column(col: str) -> int:
    return xl_ut.column_index_from_string(col) - 1


def get_xlrd_line(line: int) -> int:
    return line - 1
