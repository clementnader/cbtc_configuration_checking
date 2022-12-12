#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl
import openpyxl.utils as xl_ut
import xlrd


def get_xlrd_column(col: str) -> int:
    return xl_ut.column_index_from_string(col) - 1


def get_xlrd_line(line: int) -> int:
    return line - 1


def load_xlsx_wb(path) -> openpyxl.workbook.Workbook:
    return openpyxl.load_workbook(path)
