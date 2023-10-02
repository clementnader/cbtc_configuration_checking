#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..common_utils import *
from ..colors_pkg import *
from .xl_utils import *


__all__ = ["load_xl_file", "get_xl_sheet_by_name", "get_xl_number_of_rows", "get_xl_sheet_names",
           "get_xl_cell_value", "get_xl_float_value"]


def load_xl_file(xl_file_address: str) -> Optional[Union[xlrd.book.Book, openpyxl.workbook.Workbook]]:
    ext = os.path.splitext(xl_file_address)[1]
    if ext == ".xls":
        wb = xlrd.open_workbook(xl_file_address)
        return wb
    elif ext == ".xlsx" or ext == ".xlsm" or ext == ".xlsb":
        wb = openpyxl.load_workbook(xl_file_address, data_only=True)
        return wb
    else:
        print_error(f"{xl_file_address} is not an Excel file: extension is {ext=}.")
        return None


def get_xl_sheet_names(wb: Union[xlrd.book.Book, openpyxl.workbook.Workbook]) -> list[str]:
    if isinstance(wb, xlrd.book.Book):
        return wb.sheet_names()
    elif isinstance(wb, openpyxl.workbook.Workbook):
        return wb.sheetnames


def get_xl_sheet_by_name(wb: Union[xlrd.book.Book, openpyxl.workbook.Workbook], sheet_name: str
                         ) -> Union[xlrd.sheet.Sheet, xl_ws.Worksheet]:
    if isinstance(wb, xlrd.book.Book):
        ws = wb.sheet_by_name(sheet_name)
        return ws
    elif isinstance(wb, openpyxl.workbook.Workbook):
        ws = wb.get_sheet_by_name(sheet_name)
        return ws


def get_xl_number_of_rows(ws: Union[xlrd.sheet.Sheet, xl_ws.Worksheet]) -> int:
    if isinstance(ws, xlrd.sheet.Sheet):
        return ws.nrows
    elif isinstance(ws, xl_ws.Worksheet):
        return ws.max_row


def get_xl_cell_value(ws: Union[xlrd.sheet.Sheet, xl_ws.Worksheet],
                      cell: str = None, row: int = None, column: Union[str, int] = None
                      ) -> Optional[str]:
    row, column = get_row_and_column_from_cell(cell, row, column)
    if isinstance(ws, xlrd.sheet.Sheet):
        return get_xlrd_value(ws, row, column)
    elif isinstance(ws, xl_ws.Worksheet):
        return get_xlsx_value(ws, row, column)


def get_xl_float_value(ws: Union[xlrd.sheet.Sheet, xl_ws.Worksheet],
                       cell: str = None, row: int = None, column: Union[str, int] = None
                       ) -> Optional[Union[float, str]]:
    value = get_xl_cell_value(ws, cell, row, column)
    if isinstance(value, str):
        try:
            value = float(value.replace(",", "."))
        except ValueError:
            pass
    return value
