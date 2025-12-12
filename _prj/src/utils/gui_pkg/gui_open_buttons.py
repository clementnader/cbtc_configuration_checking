#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common_utils import *
from .gui_utils import *


__all__ = ["add_dc_sys_open_button", "add_cctool_oo_open_button", "add_dc_par_open_button", "add_dc_bop_open_button",
           "add_c11_open_button"]


def add_dc_sys_open_button(frame: tkinter.Frame, ref_row: int, bg: str = None, ga_version: str = None
                           ) -> tuple[tkinter.StringVar, tkinter.StringVar]:
    title_text = "DC_SYS: "
    open_text = "Open DC_SYS" + (f" compatible with CCTool-OO Schema {ga_version}" if ga_version is not None else "")
    file_types = ("DC_SYS", "*.xls *.xlsm")

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
    file_types = ("CCTool-OO Schema.xls", "*.xls")

    cctool_oo_directory_string_var = tkinter.StringVar()
    cctool_oo_file_name_string_var = tkinter.StringVar()

    gui_add_dir_and_file_open_button(frame, ref_row, cctool_oo_directory_string_var, cctool_oo_file_name_string_var,
                                     title_text, open_text, file_types, bg=bg, extra_func=extra_func)

    return cctool_oo_directory_string_var, cctool_oo_file_name_string_var


def add_dc_par_open_button(frame: tkinter.Frame, ref_row: int, bg: str = None
                           ) -> tuple[tkinter.StringVar, tkinter.StringVar]:
    title_text = "DC_PAR: "
    open_text = "Open DC_PAR"
    file_types = ("DC_PAR", "*.xls *.xlsm")

    dc_par_directory_string_var = tkinter.StringVar()
    dc_par_file_name_string_var = tkinter.StringVar()

    gui_add_dir_and_file_open_button(frame, ref_row, dc_par_directory_string_var, dc_par_file_name_string_var,
                                     title_text, open_text, file_types, bg=bg)

    return dc_par_directory_string_var, dc_par_file_name_string_var


def add_dc_bop_open_button(frame: tkinter.Frame, ref_row: int, bg: str = None
                           ) -> tuple[tkinter.StringVar, tkinter.StringVar]:
    title_text = "DC_BOP: "
    open_text = "Open DC_BOP"
    file_types = ("DC_BOP.xls", "*.xls")

    dc_bop_directory_string_var = tkinter.StringVar()
    dc_bop_file_name_string_var = tkinter.StringVar()

    gui_add_dir_and_file_open_button(frame, ref_row, dc_bop_directory_string_var, dc_bop_file_name_string_var,
                                     title_text, open_text, file_types, bg=bg)

    return dc_bop_directory_string_var, dc_bop_file_name_string_var


def add_c11_open_button(frame: tkinter.Frame, ref_row: int,
                        bg: str = None) -> tkinter.StringVar:
    title_text = "C11_D470: "
    open_text = "Open C11_D470"

    c11_d470_directory_string_var = tkinter.StringVar()

    gui_add_dir_open_button(frame, ref_row, c11_d470_directory_string_var, title_text, open_text, bg=bg)

    return c11_d470_directory_string_var
