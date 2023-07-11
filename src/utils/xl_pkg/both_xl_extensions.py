#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import typing
from ..colors_pkg import *
from .xl_utils import *


def load_xl_file(addr):
    ext = os.path.splitext(addr)[1]
    if ext == ".xls":
        wb = xlrd.open_workbook(addr)
        return wb
    elif ext == ".xlsx" or ext == ".xlsm":
        wb = openpyxl.load_workbook(addr, data_only=True)
        return wb
    else:
        print_error(f"{addr} is not an Excel file: extension is {ext=}.")
        return None


def get_sheets(wb):
    if isinstance(wb, xlrd.book.Book):
        return wb.sheet_names()
    elif isinstance(wb, openpyxl.workbook.workbook.Workbook):
        return wb.sheetnames


def get_xl_sheet(wb, sheet_name: str):
    if isinstance(wb, xlrd.book.Book):
        sh = wb.sheet_by_name(sheet_name)
        return sh
    elif isinstance(wb, openpyxl.workbook.workbook.Workbook):
        sh = wb.get_sheet_by_name(sheet_name)
        return sh


def get_xl_cell_value(sh, cell: str = None, line: int = None, col: typing.Union[str, int] = None):
    line, col = get_cell_line_col(cell, line, col)
    if isinstance(sh, xlrd.sheet.Sheet):
        return get_xlrd_value(sh, line, col)
    elif isinstance(sh, openpyxl.worksheet.worksheet.Worksheet):
        return get_xlsx_value(sh, line, col)


def get_xl_float_value(sh, cell: str = None, line: int = None, col: typing.Union[str, int] = None):
    value = get_xl_cell_value(sh, cell, line, col)
    if isinstance(value, str):
        try:
            value = float(value.replace(",", "."))
        except ValueError:
            pass
    return value


def get_sh_nb_rows(sh):
    if isinstance(sh, xlrd.sheet.Sheet):
        return sh.nrows
    elif isinstance(sh, openpyxl.worksheet.worksheet.Worksheet):
        return sh.max_row
