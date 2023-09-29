#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common_utils import *
from .gui_utils import *


__all__ = ["add_dc_sys_open_button", "add_cctool_oo_open_button", "add_survey_open_button"]


def add_dc_sys_open_button(window: tkinter.Frame, ref_row: int) -> tuple[tkinter.StringVar, tkinter.StringVar]:
    title_text = "DC_SYS: "
    open_text = "Open DC_SYS"
    file_types = ("XLS Excel file", "*.xls")

    dc_sys_directory_string_var = tkinter.StringVar()
    dc_sys_file_name_string_var = tkinter.StringVar()

    add_dir_and_file_open_button(window, ref_row, dc_sys_directory_string_var, dc_sys_file_name_string_var,
                                 title_text, open_text, file_types)

    return dc_sys_directory_string_var, dc_sys_file_name_string_var


def add_cctool_oo_open_button(window: tkinter.Frame, ref_row: int, extra_func: Callable[None, None] = None
                              ) -> tuple[tkinter.StringVar, tkinter.StringVar]:
    title_text = "CCTool-OO Schema: "
    open_text = "Open CCTool-OO Schema"
    file_types = ("XLS Excel file", "*.xls")

    cctool_oo_directory_string_var = tkinter.StringVar()
    cctool_oo_file_name_string_var = tkinter.StringVar()

    add_dir_and_file_open_button(window, ref_row, cctool_oo_directory_string_var, cctool_oo_file_name_string_var,
                                 title_text, open_text, file_types, extra_func=extra_func)

    return cctool_oo_directory_string_var, cctool_oo_file_name_string_var


def add_survey_open_button(window: tkinter.Frame, ref_row: int, extra_func: Callable[None, None] = None
                           ) -> dict[str, tkinter.StringVar]:
    title_text = "Survey: "
    open_text = "Open Survey"
    file_types = ("Excel file", "*.xls*")

    survey_directory = tkinter.StringVar()
    survey_file_name = tkinter.StringVar()
    survey_sheet = tkinter.StringVar()
    start_line = tkinter.StringVar()
    ref_col = tkinter.StringVar()
    type_col = tkinter.StringVar()
    track_col = tkinter.StringVar()
    survey_kp_col = tkinter.StringVar()

    add_dir_and_file_open_button(window, ref_row, survey_directory, survey_file_name,
                                 title_text, open_text, file_types,
                                 extra_func=lambda: add_survey_info(
                                     window, ref_row, survey_sheet, start_line, ref_col, type_col, track_col,
                                     survey_kp_col, extra_func=extra_func))

    survey_info = {
        "survey_directory": survey_directory,
        "survey_file_name": survey_file_name,
        "survey_sheet": survey_sheet,
        "start_line": start_line,
        "ref_col": ref_col,
        "type_col": type_col,
        "track_col": track_col,
        "survey_kp_col": survey_kp_col
    }

    return survey_info


def add_survey_info(window: tkinter.Frame, ref_row: int,
                    survey_sheet: tkinter.StringVar, start_line: tkinter.StringVar,
                    ref_col: tkinter.StringVar, type_col: tkinter.StringVar, track_col: tkinter.StringVar,
                    survey_kp_col: tkinter.StringVar,
                    extra_func: Callable[None, None] = None) -> None:

    label = tkinter.Label(window, text="Survey Sheet: ", font=tkinter.font.Font(size=9, weight="bold"))
    label.grid(column=0, row=ref_row+3, sticky="w")
    survey_sheet_entry = tkinter.Entry(window, textvariable=survey_sheet)
    survey_sheet_entry.grid(column=1, row=ref_row+3, sticky="w")

    label = tkinter.Label(window, text="First Data Line: ", font=tkinter.font.Font(size=9, weight="bold"))
    label.grid(column=0, row=ref_row+4, sticky="w")
    start_line_entry = tkinter.Entry(window, textvariable=start_line)
    start_line_entry.grid(column=1, row=ref_row+4, sticky="w")

    label = tkinter.Label(window, text="Reference Column: ", font=tkinter.font.Font(size=9, weight="bold"))
    label.grid(column=0, row=ref_row+5, sticky="w")
    ref_col_entry = tkinter.Entry(window, textvariable=ref_col)
    ref_col_entry.grid(column=1, row=ref_row+5, sticky="w")

    label = tkinter.Label(window, text="Type Column: ", font=tkinter.font.Font(size=9, weight="bold"))
    label.grid(column=0, row=ref_row+6, sticky="w")
    type_col_entry = tkinter.Entry(window, textvariable=type_col)
    type_col_entry.grid(column=1, row=ref_row+6, sticky="w")

    label = tkinter.Label(window, text="Track Column: ", font=tkinter.font.Font(size=9, weight="bold"))
    label.grid(column=0, row=ref_row+7, sticky="w")
    track_col_entry = tkinter.Entry(window, textvariable=track_col)
    track_col_entry.grid(column=1, row=ref_row+7, sticky="w")

    label = tkinter.Label(window, text="Survey KP Column: ", font=tkinter.font.Font(size=9, weight="bold"))
    label.grid(column=0, row=ref_row+8, sticky="w")
    survey_kp_col_entry = tkinter.Entry(window, textvariable=survey_kp_col)
    survey_kp_col_entry.grid(column=1, row=ref_row+8, sticky="w")

    if extra_func is not None:
        extra_func()
