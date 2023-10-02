#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
from ..common_utils import *
from ..xl_pkg import get_xl_bg_dimmer_color


__all__ = ["tkinter", "gui_add_dir_and_file_open_button", "gui_select_file", "default_gui_bg_color"]


G_INITIAL_DIRECTORY = DESKTOP_DIRECTORY


def gui_add_dir_and_file_open_button(frame: Union[tkinter.Tk, tkinter.Frame], ref_row: int,
                                     directory_string_var: tkinter.StringVar, file_name_string_var: tkinter.StringVar,
                                     title_text: str, open_text: str,
                                     file_types: Union[tuple[str, str], list[tuple[str, str]]],
                                     bg: str = None,
                                     extra_func: Callable[None, None] = None) -> tkinter.Button:
    if bg is None:
        bg = default_gui_bg_color(frame)

    frame.grid_columnconfigure(0, minsize=120)
    title_label = tkinter.Label(frame, text=title_text, font=tkinter.font.Font(size=11, weight="bold"), bg=bg)
    title_label.grid(column=0, row=ref_row, rowspan=2, sticky="w")

    directory_label = tkinter.Label(frame, text="", textvariable=directory_string_var, bg=bg)
    directory_label.grid(column=1, row=ref_row, sticky="w", columnspan=5, padx=(0, 5))

    file_name_label = tkinter.Label(frame, text="", textvariable=file_name_string_var,
                                    font=tkinter.font.Font(size=9, weight="bold"), bg=bg)
    file_name_label.grid(column=1, row=ref_row+1, sticky="w", columnspan=5, padx=(0, 5))

    # Open file button
    button_bg = "#" + get_xl_bg_dimmer_color(bg.removeprefix("#")) if bg.startswith("#") else bg
    open_button = tkinter.Button(
        frame,
        text="select file",
        command=lambda: gui_select_file(open_text, file_types, directory_string_var, file_name_string_var, extra_func),
        bg=button_bg
    )
    open_button.grid(column=6, row=ref_row, rowspan=2, sticky="w", padx=5, pady=5)
    return open_button


def gui_select_file(open_text: str, file_types: Union[tuple[str, str], list[tuple[str, str]]],
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

    if not selected_file_name:
        return

    directory_string, file_name_string = os.path.split(selected_file_name)
    directory_string_var.set(directory_string)
    file_name_string_var.set(file_name_string)
    G_INITIAL_DIRECTORY = directory_string_var.get()

    if extra_func is not None:
        extra_func()


def default_gui_bg_color(frame: tkinter.Frame) -> str:
    return frame.cget("background")
