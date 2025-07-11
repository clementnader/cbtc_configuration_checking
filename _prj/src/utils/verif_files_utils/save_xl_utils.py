#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..xl_pkg import *
from ..colors_pkg import *
from ..exception_utils import *


__all__ = ["save_xl_file"]


def save_xl_file(wb: openpyxl.workbook.Workbook, result_file_path: str):
    result_file_path = os.path.realpath(result_file_path)
    if os.path.isfile(result_file_path):
        print_error(f"result_file_path = \"{result_file_path}\" already exists.")
        if not ask_question_yes_or_no("Do you want to overwrite it?"):
            print_error("Execution aborted.")
            raise UnableToSaveFileException
    try:
        wb.save(result_file_path)
    except PermissionError:
        print_error(f"Permission denied to write at \"{result_file_path}\"."
                    f"\nYou have to close it if you want it to be overwritten.")
        if not ask_question_yes_or_no("Do you want to retry?"):
            print_error("Execution aborted.")
            raise UnableToSaveFileException
        wb.save(result_file_path)
