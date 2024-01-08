#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common_utils import *
from .gui_utils import *


__all__ = ["add_dc_sys_open_button", "add_cctool_oo_open_button"]


def add_dc_sys_open_button(frame: tkinter.Frame, ref_row: int, bg: str = None, ga_version: str = None
                           ) -> tuple[tkinter.StringVar, tkinter.StringVar]:
    title_text = "DC_SYS: "
    open_text = "Open DC_SYS" + (f" compatible with System Referential {ga_version}" if ga_version is not None else "")
    file_types = ("XLS Excel file", "*.xls")

    dc_sys_directory_string_var = tkinter.StringVar()
    dc_sys_file_name_string_var = tkinter.StringVar()

    gui_add_dir_and_file_open_button(frame, ref_row, dc_sys_directory_string_var, dc_sys_file_name_string_var,
                                     title_text, open_text, file_types, bg=bg)

    return dc_sys_directory_string_var, dc_sys_file_name_string_var


def add_cctool_oo_open_button(frame: Union[tkinter.Tk, tkinter.Frame], ref_row: int,
                              extra_func: Callable[None, None] = None,
                              bg: str = None) -> tuple[tkinter.StringVar, tkinter.StringVar]:
    title_text = "CCTool-OO Schema: "
    open_text = "Open CCTool-OO Schema"
    file_types = ("XLS Excel file", "*.xls")

    cctool_oo_directory_string_var = tkinter.StringVar()
    cctool_oo_file_name_string_var = tkinter.StringVar()

    gui_add_dir_and_file_open_button(frame, ref_row, cctool_oo_directory_string_var, cctool_oo_file_name_string_var,
                                     title_text, open_text, file_types, bg=bg, extra_func=extra_func)

    return cctool_oo_directory_string_var, cctool_oo_file_name_string_var
