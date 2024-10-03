#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tkinter.ttk
import traceback
import logging
from ...utils import *


__all__ = ["add_survey_open_button"]


def add_survey_open_button(frame: tkinter.Frame, ref_row: int, extra_func: Callable[None, None] = None,
                           bg: str = None) -> dict[str, tkinter.StringVar]:
    title_text = "Survey: "
    open_text = "Open Survey"
    file_types = ("Excel file", "*.xls*")

    survey_directory = tkinter.StringVar()
    survey_file_name = tkinter.StringVar()
    survey_sheet = tkinter.StringVar()
    all_sheets = tkinter.BooleanVar()
    start_row = tkinter.StringVar()
    ref_col = tkinter.StringVar()
    type_col = tkinter.StringVar()
    track_col = tkinter.StringVar()
    survey_kp_col = tkinter.StringVar()

    bottom_frame = tkinter.Frame(frame, bg=bg)
    bottom_frame.grid(column=0, row=2, columnspan=100, sticky="nswe")
    sub_frame = tkinter.Frame(bottom_frame, bg=bg, padx=5, pady=5)
    sub_frame.grid(column=0, row=0, sticky="nswe")

    gui_add_dir_and_file_open_button(frame, ref_row, survey_directory, survey_file_name, title_text, open_text,
                                     file_types, bg=bg,
                                     extra_func=lambda: _add_survey_info(os.path.join(survey_directory.get(),
                                                                                      survey_file_name.get()
                                                                                      ).replace("/", os.path.sep),
                                                                         sub_frame, ref_row, survey_sheet, all_sheets,
                                                                         start_row, ref_col, type_col, track_col,
                                                                         survey_kp_col, bg=bg, extra_func=extra_func))

    survey_info = {
        "survey_directory": survey_directory,
        "survey_file_name": survey_file_name,
        "survey_sheet": survey_sheet,
        "all_sheets": all_sheets,
        "start_row": start_row,
        "ref_col": ref_col,
        "type_col": type_col,
        "track_col": track_col,
        "survey_kp_col": survey_kp_col
    }

    return survey_info


def _add_survey_info(survey_file_name: str, frame: tkinter.Frame, ref_row: int,
                     survey_sheet: tkinter.StringVar, all_sheets: tkinter.BooleanVar,
                     start_row: tkinter.StringVar, ref_col: tkinter.StringVar,
                     type_col: tkinter.StringVar, track_col: tkinter.StringVar,
                     survey_kp_col: tkinter.StringVar, bg: str = None,
                     extra_func: Callable[None, None] = None) -> None:

    try:
        print_log(f"Loading Survey File {Color.default}\"{os.path.split(survey_file_name)[-1]}\"{Color.reset} "
                  f"to get the sheet names...")
        survey_sheets = get_xl_sheet_names_preload(survey_file_name)
    except Exception as error:
        logging.error(traceback.format_exc())
        print(error)
        print_error("Error during the loading of the Excel survey file.")
        tkinter.messagebox.showerror(title="Error",
                                     message="Error during the loading of the Excel survey file.\n"
                                             "Check the cmd window for more information.")
        return

    if survey_sheets is None:
        print_error("File format is not expected.")
        tkinter.messagebox.showerror(title="Error",
                                     message="File format is not expected.\n"
                                             "Check the cmd window for more information.")
        return

    memorized_sheet = ""

    def all_sheets_click():
        nonlocal memorized_sheet
        if all_sheets.get():
            memorized_sheet = survey_sheet_combobox.get()
            survey_sheet_combobox.set("")
            survey_sheet_combobox.config(state=tkinter.DISABLED)
            survey_sheet_comment.config(state=tkinter.DISABLED)
            all_sheets_comment.config(state=tkinter.NORMAL)
        else:
            survey_sheet_combobox.set(memorized_sheet)
            survey_sheet_combobox.config(state="readonly")
            survey_sheet_comment.config(state=tkinter.NORMAL)
            all_sheets_comment.config(state=tkinter.DISABLED)

    if bg is None:
        bg = default_gui_bg_color(frame)

    entry_bg = "white"

    # Survey Sheet
    current_row = ref_row+2
    survey_sheet_label = tkinter.Label(frame, text="Survey Sheet: ", font=tkinter.font.Font(size=9, weight="bold"),
                                       bg=bg)
    survey_sheet_label.grid(column=0, row=current_row, sticky="w")
    # A Combobox allows to select one value in a set of values
    survey_sheet_combobox = tkinter.ttk.Combobox(frame, textvariable=survey_sheet)
    survey_sheet_combobox["values"] = survey_sheets
    survey_sheet_combobox["state"] = "readonly"  # prevent typing a value
    survey_sheet_combobox.grid(column=1, row=current_row, columnspan=3, sticky="w")
    survey_sheet_comment = tkinter.Label(frame, text="(name of the D932 result sheet)",
                                         font=tkinter.font.Font(size=8), bg=bg)
    survey_sheet_comment.grid(column=4, row=current_row, columnspan=1, sticky="w")
    survey_sheet_combobox.set("")

    # All Sheets Checkbox
    current_row += 1
    all_sheets_checkbutton = tkinter.Checkbutton(frame, text="use all sheets",
                                                 font=tkinter.font.Font(size=9, weight="bold"),
                                                 variable=all_sheets, bg=bg,
                                                 command=all_sheets_click)
    all_sheets_checkbutton.grid(column=1, row=current_row, columnspan=2, sticky="w")
    all_sheets_comment = tkinter.Label(frame, text="(use all the sheets of the survey file)",
                                       font=tkinter.font.Font(size=8), bg=bg)
    all_sheets_comment.grid(column=3, row=current_row, columnspan=2, sticky="w")
    all_sheets_comment.config(state=tkinter.DISABLED)

    # First Data Row
    current_row += 1
    start_row_label = tkinter.Label(frame, text="First Data Row: ", font=tkinter.font.Font(size=9, weight="bold"),
                                    bg=bg)
    start_row_label.grid(column=0, row=current_row, sticky="w")
    start_row_entry = tkinter.Entry(frame, textvariable=start_row, bg=entry_bg, width=7)
    start_row_entry.grid(column=1, row=current_row, sticky="w")
    start_row_comment = tkinter.Label(frame, text="(number of the first row with survey information)",
                                      font=tkinter.font.Font(size=8), bg=bg)
    start_row_comment.grid(column=2, row=current_row, columnspan=7, sticky="w")
    start_row.set("")

    # Reference Column
    current_row += 1
    ref_col_label = tkinter.Label(frame, text="Reference Column: ", font=tkinter.font.Font(size=9, weight="bold"),
                                  bg=bg)
    ref_col_label.grid(column=0, row=current_row, sticky="w")
    ref_col_entry = tkinter.Entry(frame, textvariable=ref_col, bg=entry_bg, width=7)
    ref_col_entry.grid(column=1, row=current_row, sticky="w")
    ref_col_comment = tkinter.Label(frame, text="(letter or number of the column containing "
                                                "the objects name)",
                                    font=tkinter.font.Font(size=8), bg=bg)
    ref_col_comment.grid(column=2, row=current_row, columnspan=7, sticky="w")
    ref_col.set("")

    # Type Column
    current_row += 1
    type_col_label = tkinter.Label(frame, text="Type Column: ", font=tkinter.font.Font(size=9, weight="bold"), bg=bg)
    type_col_label.grid(column=0, row=current_row, sticky="w")
    type_col_entry = tkinter.Entry(frame, textvariable=type_col, bg=entry_bg, width=7)
    type_col_entry.grid(column=1, row=current_row, sticky="w")
    type_col_comment = tkinter.Label(frame, text="(letter or number of the column containing "
                                                 "the objects type (e.g. SWP, TC, TAG...))",
                                     font=tkinter.font.Font(size=8), bg=bg)
    type_col_comment.grid(column=2, row=current_row, columnspan=7, sticky="w")
    type_col.set("")

    # Track Column
    current_row += 1
    track_col_label = tkinter.Label(frame, text="Track Column: ", font=tkinter.font.Font(size=9, weight="bold"), bg=bg)
    track_col_label.grid(column=0, row=current_row, sticky="w")
    track_col_entry = tkinter.Entry(frame, textvariable=track_col, bg=entry_bg, width=7)
    track_col_entry.grid(column=1, row=current_row, sticky="w")
    track_col_comment = tkinter.Label(frame, text="(letter or number of the column containing "
                                                  "the objects track)",
                                      font=tkinter.font.Font(size=8), bg=bg)
    track_col_comment.grid(column=2, row=current_row, columnspan=7, sticky="w")
    track_col.set("")

    # Surveyed KP Column
    current_row += 1
    survey_kp_col_label = tkinter.Label(frame, text="Surveyed KP Column: ",
                                        font=tkinter.font.Font(size=9, weight="bold"), bg=bg)
    survey_kp_col_label.grid(column=0, row=current_row, sticky="w")
    survey_kp_col_entry = tkinter.Entry(frame, textvariable=survey_kp_col, bg=entry_bg, width=7)
    survey_kp_col_entry.grid(column=1, row=current_row, sticky="w")
    survey_kp_col_comment = tkinter.Label(frame, text="(letter or number of the column containing "
                                                      "the objects surveyed KP)",
                                          font=tkinter.font.Font(size=8), bg=bg)
    survey_kp_col_comment.grid(column=2, row=current_row, columnspan=7, sticky="w")
    survey_kp_col.set("")

    if extra_func is not None:
        extra_func()
