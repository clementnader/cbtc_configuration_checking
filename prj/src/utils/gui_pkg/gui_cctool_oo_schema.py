#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from ...database_location import DATABASE_LOC
from ..colors_pkg import *
from ..xl_pkg import XlBgColor
from .gui_open_buttons import *
from .gui_utils import *

__all__ = ["cctool_schema_window"]


def cctool_schema_window():
    # Root window
    window = create_window("CCTool-OO Schema")

    bg = f"#{XlBgColor.light_blue}"
    window.configure(bg=bg)
    sub_frame = tkinter.Frame(window, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")

    cctool_oo_directory, cctool_oo_file_name = (
        add_cctool_oo_open_button(sub_frame, ref_row=0, extra_func=lambda: window.destroy()))

    window.mainloop()

    if cctool_oo_directory.get() == "" or cctool_oo_file_name.get() == "":
        print_error("Execution aborted.")
        sys.exit(1)

    DATABASE_LOC.cctool_oo_schema = os.path.join(cctool_oo_directory.get(), cctool_oo_file_name.get()
                                                 ).replace("/", os.path.sep)
