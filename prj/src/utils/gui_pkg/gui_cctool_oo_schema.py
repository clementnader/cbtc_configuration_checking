#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from ...database_location import DATABASE_LOC
from ..colors_pkg import *
from .gui_open_buttons import *
from .gui_utils import *

__all__ = ["cctool_schema_window"]


def cctool_schema_window():
    # Root window
    window = tkinter.Tk()
    window.title("CCTool-OO Schema")
    window.resizable(False, False)
    window.attributes("-topmost", True)

    top_frame = tkinter.Frame(window)
    top_frame.grid(column=0, row=0, padx=5, pady=5, sticky="w")
    cctool_oo_directory, cctool_oo_file_name = add_cctool_oo_open_button(top_frame, ref_row=0,
                                                                         extra_func=lambda: window.destroy())

    window.mainloop()

    if cctool_oo_directory.get() == "" or cctool_oo_file_name == "":
        print_error("Execution aborted.")
        sys.exit(1)

    DATABASE_LOC.cctool_oo_schema = os.path.join(cctool_oo_directory.get(), cctool_oo_file_name.get())
