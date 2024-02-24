#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...database_location import *


__all__ = ["load_block_def_wb"]


def load_block_def_wb() -> Optional[Union[xlrd.book.Book, openpyxl.workbook.Workbook]]:
    block_def_addr = DATABASE_LOC.block_def
    if block_def_addr is None:
        return None
    block_def_wb = load_xl_file(block_def_addr)
    return block_def_wb
