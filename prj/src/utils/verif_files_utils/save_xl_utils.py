#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..xl_pkg import *
from ..colors_pkg import *
from ..exception_utils import *


__all__ = ["save_xl_file"]


def save_xl_file(wb: openpyxl.workbook.Workbook, res_file_path: str):
    res_file_path = os.path.abspath(res_file_path)
    if os.path.isfile(res_file_path):
        print_error(f"res_file_path = \"{res_file_path}\" already exists.")
        if not ask_question_yes_or_no("Do you want to overwrite it?"):
            print_error("Execution aborted.")
            raise UnableToSaveFileException
    try:
        wb.save(res_file_path)
    except PermissionError:
        print_error(f"Permission denied to write at \"{res_file_path}\"."
                    f"\nYou have to close it if you want it to be overwritten.")
        if not ask_question_yes_or_no("Do you want to retry?"):
            print_error("Execution aborted.")
            raise UnableToSaveFileException
        wb.save(res_file_path)
