#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...dc_sys import *


__all__ = ["add_block_joint_def_frame"]


def add_block_joint_def_frame(frame: tkinter.Frame, ref_row: int, bg: str = None
                              ) -> tuple[tkinter.BooleanVar, tkinter.StringVar, tkinter.StringVar]:

    title_label = tkinter.Label(frame, text="Block Joint Name Definition:",
                                font=tkinter.font.Font(size=11, weight="bold"), bg=bg)
    title_label.grid(column=0, row=ref_row, columnspan=6, sticky="w")

    # Left Frame
    left_frame = tkinter.Frame(frame, bg=bg)
    left_frame.grid(column=0, row=1, sticky="nswe")

    # Right Frame
    right_frame = tkinter.Frame(frame, bg=bg)
    right_frame.grid(column=3, row=1, rowspan=20, sticky="nswe")

    # Separators
    sep = tkinter.ttk.Separator(frame, orient="vertical")
    sep.grid(column=2, row=1, sticky="ns")

    # Left Frame
    sub_frame = tkinter.Frame(left_frame, bg=bg, padx=5, pady=5)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    automatic_names_bool_var = _add_automatic_names_button(sub_frame, 0, right_frame, bg=bg)

    # Right Frame
    sub_frame = tkinter.Frame(right_frame, bg=bg, padx=5, pady=5)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    block_def_label = tkinter.Label(sub_frame, text="Dedicated Block Definition File",
                                    font=tkinter.font.Font(size=10), bg=bg)
    block_def_label.grid(column=0, row=0, columnspan=10, sticky="w")
    block_def_directory_string_var, block_def_file_name_string_var = _add_block_def_button(sub_frame, 2, bg=bg)
    disable_frame(right_frame)  # default state

    return automatic_names_bool_var, block_def_directory_string_var, block_def_file_name_string_var


def _add_block_def_button(frame: tkinter.Frame, ref_row: int, bg: str = None
                          ) -> tuple[tkinter.StringVar, tkinter.StringVar]:
    title_text = "Block Def.: "
    open_text = "Open Block Definition file"
    file_types = ("Excel file", "*.xls*")

    block_def_directory_string_var = tkinter.StringVar()
    block_def_file_name_string_var = tkinter.StringVar()

    gui_add_dir_and_file_open_button(frame, ref_row, block_def_directory_string_var, block_def_file_name_string_var,
                                     title_text, open_text, file_types, bg=bg, size=10)

    return block_def_directory_string_var, block_def_file_name_string_var


def _add_automatic_names_button(frame: tkinter.Frame, ref_row: int, other_frame: tkinter.Frame, bg: str = None
                                ) -> tkinter.BooleanVar:
    def automatic_names_click():
        if automatic_names.get():
            disable_frame(other_frame)
            automatic_names_comment.config(state=tkinter.NORMAL)
        else:
            enable_frame(other_frame)
            automatic_names_comment.config(state=tkinter.DISABLED)

    if bg is None:
        bg = default_gui_bg_color(frame)

    automatic_names_comment = tkinter.Label(frame, text="Let the tool generate the joint names",
                                            font=tkinter.font.Font(size=10), bg=bg)
    automatic_names_comment.grid(column=0, row=ref_row, columnspan=3, sticky="w")

    frame.grid_rowconfigure(ref_row+1, minsize=40)
    automatic_names = tkinter.BooleanVar()
    automatic_names.set(True)
    automatic_names_checkbutton = tkinter.Checkbutton(frame, text="automatic joint names",
                                                      font=tkinter.font.Font(size=9, weight="bold"),
                                                      variable=automatic_names, bg=bg,
                                                      command=automatic_names_click)
    automatic_names_checkbutton.grid(column=0, row=ref_row+1, columnspan=3, sticky="w")

    return automatic_names
