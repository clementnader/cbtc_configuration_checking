#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl
import openpyxl.utils as xl_ut
import xlrd


def get_xlrd_column(col: str) -> int:
    return xl_ut.column_index_from_string(col) - 1


def get_xlrd_line(line: int) -> int:
    return line - 1


def load_xlsx_wb(path: str) -> openpyxl.workbook.Workbook:
    return openpyxl.load_workbook(path)


def get_xl_column(col: int) -> str:
    return xl_ut.get_column_letter(col + 1)


def get_xl_line(line: int) -> int:
    return line + 1


def read_cell(sh: xlrd.sheet, i: int, j: int):
    value = sh.cell_value(i, j)
    if value in ("", None):
        return None
    if isinstance(value, str):
        try:
            value = float(value.replace(",", "."))
        except ValueError:
            pass
    return value


def get_xlrd_value(sh: xlrd.sheet, line: int, col: str) -> str:
    xlrd_line = get_xlrd_line(line)
    xlrd_col = get_xlrd_column(col)
    try:
        cell_value = sh.cell_value(xlrd_line, xlrd_col)
    except IndexError:
        cell_value = None
    return cell_value
