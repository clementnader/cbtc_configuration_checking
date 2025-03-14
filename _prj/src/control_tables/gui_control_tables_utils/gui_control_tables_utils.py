#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter.ttk
from ...utils import *


__all__ = ["add_control_table_open_button"]


def add_control_table_open_button(frame: tkinter.Frame, ref_row: int, extra_func: Callable[None, None] = None,
                                  bg: str = None) -> dict[str, tkinter.StringVar]:
    title_text = "Control Table: "
    open_text = "Open Control Table"
    file_types = ("PDF file", "*.pdf")

    control_table_directory = tkinter.StringVar()
    control_table_file_name = tkinter.StringVar()
    page_selection = tkinter.IntVar()
    specific_range_inf = tkinter.StringVar()
    specific_range_sup = tkinter.StringVar()
    specific_page = tkinter.StringVar()

    bottom_frame = tkinter.Frame(frame, bg=bg)
    bottom_frame.grid(column=0, row=2, columnspan=100, sticky="nswe")
    sub_frame = tkinter.Frame(bottom_frame, bg=bg, padx=5, pady=5)
    sub_frame.grid(column=0, row=0, sticky="nswe")

    gui_add_dir_and_file_open_button(frame, ref_row, control_table_directory, control_table_file_name,
                                     title_text, open_text, file_types, bg=bg,
                                     extra_func=lambda: _add_control_table_info(
                                         sub_frame, ref_row, page_selection, specific_range_inf, specific_range_sup,
                                         specific_page, bg=bg, extra_func=extra_func))

    control_table_info = {
        "control_table_directory": control_table_directory,
        "control_table_file_name": control_table_file_name,
        "page_selection": page_selection,
        "specific_range_inf": specific_range_inf,
        "specific_range_sup": specific_range_sup,
        "specific_page": specific_page
    }

    return control_table_info


def _add_control_table_info(frame: tkinter.Frame, ref_row: int,
                            page_selection: tkinter.IntVar,
                            specific_range_inf: tkinter.StringVar,
                            specific_range_sup: tkinter.StringVar,
                            specific_page: tkinter.StringVar,
                            bg: str = None,
                            extra_func: Callable[None, None] = None) -> None:

    def page_selection_click():
        if page_selection.get() == 0:
            all_pages_radiobutton.config(fg="black", font=tkinter.font.Font(size=10, weight="bold"))
            range_selection_radiobutton.config(fg="grey", font=tkinter.font.Font(size=10))
            range_inf_label.config(state=tkinter.DISABLED)
            range_inf_entry.config(state=tkinter.DISABLED)
            range_sup_label.config(state=tkinter.DISABLED)
            range_sup_entry.config(state=tkinter.DISABLED)
            page_selection_radiobutton.config(fg="grey", font=tkinter.font.Font(size=10))
            page_selection_label.config(state=tkinter.DISABLED)
            page_selection_entry.config(state=tkinter.DISABLED)
        elif page_selection.get() == 1:
            all_pages_radiobutton.config(fg="grey", font=tkinter.font.Font(size=10))
            range_selection_radiobutton.config(fg="black", font=tkinter.font.Font(size=10, weight="bold"))
            range_inf_label.config(state=tkinter.NORMAL)
            range_inf_entry.config(state=tkinter.NORMAL)
            range_sup_label.config(state=tkinter.NORMAL)
            range_sup_entry.config(state=tkinter.NORMAL)
            page_selection_radiobutton.config(fg="grey", font=tkinter.font.Font(size=10))
            page_selection_label.config(state=tkinter.DISABLED)
            page_selection_entry.config(state=tkinter.DISABLED)
        elif page_selection.get() == 2:
            all_pages_radiobutton.config(fg="grey", font=tkinter.font.Font(size=10))
            range_selection_radiobutton.config(fg="grey", font=tkinter.font.Font(size=10))
            range_inf_label.config(state=tkinter.DISABLED)
            range_inf_entry.config(state=tkinter.DISABLED)
            range_sup_label.config(state=tkinter.DISABLED)
            range_sup_entry.config(state=tkinter.DISABLED)
            page_selection_radiobutton.config(fg="black", font=tkinter.font.Font(size=10, weight="bold"))
            page_selection_label.config(state=tkinter.NORMAL)
            page_selection_entry.config(state=tkinter.NORMAL)

    if bg is None:
        bg = default_gui_bg_color(frame)

    entry_bg = "white"

    # Page Selection Label
    current_row = ref_row+2
    page_selection_label = tkinter.Label(frame, text="Pages Selection:", font=tkinter.font.Font(size=10, weight="bold"),
                                         bg=bg)
    page_selection_label.grid(column=0, columnspan=2, row=current_row, sticky="w")
    frame.columnconfigure(0, minsize=20)
    frame.columnconfigure(1, minsize=160)

    # Page Selection 0: all pages
    current_row += 1
    all_pages_radiobutton = tkinter.Radiobutton(frame, text="all pages",
                                                font=tkinter.font.Font(size=10, weight="bold"),
                                                variable=page_selection, bg=bg, value=0,
                                                command=page_selection_click)
    all_pages_radiobutton.grid(column=1, row=current_row, sticky="w")

    # Page Selection 1: specific range
    current_row += 1
    range_selection_radiobutton = tkinter.Radiobutton(frame, text="range selection: ",
                                                      font=tkinter.font.Font(size=10),
                                                      variable=page_selection, bg=bg, value=1,
                                                      command=page_selection_click)
    range_selection_radiobutton.grid(column=1, row=current_row, sticky="w")
    range_selection_radiobutton.config(fg="grey")
    range_inf_label = tkinter.Label(frame, text="from: ", font=tkinter.font.Font(size=9, weight="bold"),
                                    bg=bg)
    range_inf_label.grid(column=2, row=current_row, sticky="w")
    range_inf_label.config(state=tkinter.DISABLED)
    range_inf_entry = tkinter.Entry(frame, textvariable=specific_range_inf, bg=entry_bg, width=7)
    range_inf_entry.grid(column=3, row=current_row, sticky="w")
    range_inf_entry.config(state=tkinter.DISABLED)
    range_sup_label = tkinter.Label(frame, text="to: ", font=tkinter.font.Font(size=9, weight="bold"),
                                    bg=bg)
    range_sup_label.grid(column=4, row=current_row, sticky="w")
    range_sup_label.config(state=tkinter.DISABLED)
    range_sup_entry = tkinter.Entry(frame, textvariable=specific_range_sup, bg=entry_bg, width=7)
    range_sup_entry.grid(column=5, row=current_row, sticky="w")
    range_sup_entry.config(state=tkinter.DISABLED)

    # Page Selection 2: specific page
    current_row += 1
    page_selection_radiobutton = tkinter.Radiobutton(frame, text="one-page selection: ",
                                                     font=tkinter.font.Font(size=10),
                                                     variable=page_selection, bg=bg, value=2,
                                                     command=page_selection_click)
    page_selection_radiobutton.grid(column=1, row=current_row, sticky="w")
    page_selection_radiobutton.config(fg="grey")
    page_selection_label = tkinter.Label(frame, text="page: ", font=tkinter.font.Font(size=9, weight="bold"),
                                    bg=bg)
    page_selection_label.grid(column=2, row=current_row, sticky="w")
    page_selection_label.config(state=tkinter.DISABLED)
    page_selection_entry = tkinter.Entry(frame, textvariable=specific_page, bg=entry_bg, width=7)
    page_selection_entry.grid(column=3, row=current_row, sticky="w")
    page_selection_entry.config(state=tkinter.DISABLED)

    if extra_func is not None:
        extra_func()
