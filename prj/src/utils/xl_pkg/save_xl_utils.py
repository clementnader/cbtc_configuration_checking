#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from .xl_utils import *
from ..colors_pkg import *


__all__ = ["save_xl_file"]


def save_xl_file(wb: openpyxl.workbook.Workbook, res_file_path: str):
    if os.path.isfile(res_file_path):
        print_error(f"{res_file_path = } already exists.")
        if input(f"Do you want to overwrite it? (Y/N) ").upper() not in ["Y", "YES"]:
            print_error("Execution aborted.")
            sys.exit(1)
    try:
        wb.save(res_file_path)
    except PermissionError:
        print_error(f"Permission denied to write at {res_file_path = }."
                    f"\nYou have to close it if you want it to be overwritten.")
        if input(f"Do you want to retry? (Y/N) ").upper() not in ["Y", "YES"]:
            print_error("Execution aborted.")
            sys.exit(1)
        wb.save(res_file_path)
