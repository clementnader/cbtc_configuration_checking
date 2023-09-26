#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
from ..common_utils import *


__all__ = ["tkinter", "add_dir_and_file_open_button", "select_file"]


G_INITIAL_DIRECTORY = DESKTOP_DIRECTORY


def add_dir_and_file_open_button(window: tkinter.Frame, ref_row: int,
                                 directory_string_var: tkinter.StringVar, file_name_string_var: tkinter.StringVar,
                                 title_text: str, open_text: str,
                                 file_types: Union[tuple[str, str], list[tuple[str, str]]],
                                 extra_func: Callable[None, None] = None):

    title_label = tkinter.Label(window, text=title_text, font=tkinter.font.Font(size=11, weight="bold"))
    title_label.grid(column=0, row=ref_row, rowspan=2, sticky="w")

    directory_label = tkinter.Label(window, text="", textvariable=directory_string_var)
    directory_label.grid(column=1, row=ref_row, sticky="w")
    file_name_label = tkinter.Label(window, text="", textvariable=file_name_string_var,
                                    font=tkinter.font.Font(size=9, weight="bold"))
    file_name_label.grid(column=1, row=ref_row+1, sticky="w")

    # Open file button
    open_button = tkinter.Button(
        window,
        text="select",
        command=lambda: select_file(open_text, file_types, directory_string_var, file_name_string_var, extra_func),
        anchor="e"
    )
    open_button.grid(column=2, row=ref_row, rowspan=2)


def select_file(open_text: str, file_types: Union[tuple[str, str], list[tuple[str, str]]],
                directory_string_var: tkinter.StringVar, file_name_string_var: tkinter.StringVar,
                extra_func: Callable[None, None] = None):

    global G_INITIAL_DIRECTORY
    if not isinstance(file_types, list):
        file_types = [file_types]
    file_types = tuple(file_types)

    selected_file_name = tkinter.filedialog.askopenfilename(
        title=open_text,
        initialdir=G_INITIAL_DIRECTORY,
        filetypes=file_types
    )

    directory_string, file_name_string = os.path.split(selected_file_name)
    directory_string_var.set(directory_string)
    file_name_string_var.set(file_name_string)
    G_INITIAL_DIRECTORY = directory_string_var.get()

    if selected_file_name and extra_func is not None:
        extra_func()
