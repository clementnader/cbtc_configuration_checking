#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *


__all__ = ["add_survey_open_button", "launch_function", "is_everything_ready", "delete_tab"]


def add_survey_open_button(frame: tkinter.Frame, ref_row: int, extra_func: Callable[None, None] = None,
                           bg: str = None) -> dict[str, tkinter.StringVar]:
    title_text = "Survey: "
    open_text = "Open Survey"
    file_types = ("Excel file", "*.xls*")

    survey_directory = tkinter.StringVar()
    survey_file_name = tkinter.StringVar()
    survey_sheet = tkinter.StringVar()
    start_row = tkinter.StringVar()
    ref_col = tkinter.StringVar()
    type_col = tkinter.StringVar()
    track_col = tkinter.StringVar()
    survey_kp_col = tkinter.StringVar()

    gui_add_dir_and_file_open_button(frame, ref_row, survey_directory, survey_file_name, title_text, open_text,
                                     file_types, bg=bg,
                                     extra_func=lambda: add_survey_info(frame, ref_row, survey_sheet, start_row,
                                                                        ref_col, type_col, track_col, survey_kp_col,
                                                                        bg=bg, extra_func=extra_func))

    survey_info = {
        "survey_directory": survey_directory,
        "survey_file_name": survey_file_name,
        "survey_sheet": survey_sheet,
        "start_row": start_row,
        "ref_col": ref_col,
        "type_col": type_col,
        "track_col": track_col,
        "survey_kp_col": survey_kp_col
    }

    return survey_info


def add_survey_info(frame: tkinter.Frame, ref_row: int,
                    survey_sheet: tkinter.StringVar, start_row: tkinter.StringVar,
                    ref_col: tkinter.StringVar, type_col: tkinter.StringVar, track_col: tkinter.StringVar,
                    survey_kp_col: tkinter.StringVar, bg: str = None,
                    extra_func: Callable[None, None] = None) -> None:
    if bg is None:
        bg = default_gui_bg_color(frame)
    entry_bg = "white"
    # Survey Sheet
    current_row = ref_row+2
    label = tkinter.Label(frame, text="Survey Sheet: ", font=tkinter.font.Font(size=9, weight="bold"), bg=bg)
    label.grid(column=0, row=current_row, sticky="w")
    survey_sheet_entry = tkinter.Entry(frame, textvariable=survey_sheet, bg=entry_bg)
    survey_sheet_entry.grid(column=1, row=current_row, sticky="w")
    comment = tkinter.Label(frame, text="(name of the sheet)", font=tkinter.font.Font(size=8), bg=bg)
    comment.grid(column=2, row=current_row, sticky="w")
    # First Data Row
    current_row += 1
    label = tkinter.Label(frame, text="First Data Row: ", font=tkinter.font.Font(size=9, weight="bold"), bg=bg)
    label.grid(column=0, row=current_row, sticky="w")
    start_row_entry = tkinter.Entry(frame, textvariable=start_row, bg=entry_bg)
    start_row_entry.grid(column=1, row=current_row, sticky="w")
    comment = tkinter.Label(frame, text="(number of the row)", font=tkinter.font.Font(size=8), bg=bg)
    comment.grid(column=2, row=current_row, sticky="w")
    # Reference Column
    current_row += 1
    label = tkinter.Label(frame, text="Reference Column: ", font=tkinter.font.Font(size=9, weight="bold"), bg=bg)
    label.grid(column=0, row=current_row, sticky="w")
    ref_col_entry = tkinter.Entry(frame, textvariable=ref_col, bg=entry_bg)
    ref_col_entry.grid(column=1, row=current_row, sticky="w")
    comment = tkinter.Label(frame, text="(letter or number of the column)", font=tkinter.font.Font(size=8), bg=bg)
    comment.grid(column=2, row=current_row, sticky="w")
    # Type Column
    current_row += 1
    label = tkinter.Label(frame, text="Type Column: ", font=tkinter.font.Font(size=9, weight="bold"), bg=bg)
    label.grid(column=0, row=current_row, sticky="w")
    type_col_entry = tkinter.Entry(frame, textvariable=type_col, bg=entry_bg)
    type_col_entry.grid(column=1, row=current_row, sticky="w")
    comment = tkinter.Label(frame, text="(letter or number of the column)", font=tkinter.font.Font(size=8), bg=bg)
    comment.grid(column=2, row=current_row, sticky="w")
    # Track Column
    current_row += 1
    label = tkinter.Label(frame, text="Track Column: ", font=tkinter.font.Font(size=9, weight="bold"), bg=bg)
    label.grid(column=0, row=current_row, sticky="w")
    track_col_entry = tkinter.Entry(frame, textvariable=track_col, bg=entry_bg)
    track_col_entry.grid(column=1, row=current_row, sticky="w")
    comment = tkinter.Label(frame, text="(letter or number of the column)", font=tkinter.font.Font(size=8), bg=bg)
    comment.grid(column=2, row=current_row, sticky="w")
    # Survey KP Column
    current_row += 1
    label = tkinter.Label(frame, text="Survey KP Column: ", font=tkinter.font.Font(size=9, weight="bold"), bg=bg)
    label.grid(column=0, row=current_row, sticky="w")
    survey_kp_col_entry = tkinter.Entry(frame, textvariable=survey_kp_col, bg=entry_bg)
    survey_kp_col_entry.grid(column=1, row=current_row, sticky="w")
    comment = tkinter.Label(frame, text="(letter or number of the column)", font=tkinter.font.Font(size=8), bg=bg)
    comment.grid(column=2, row=current_row, sticky="w")

    if extra_func is not None:
        extra_func()


def delete_tab(tab_control: tkinter.ttk.Notebook, tab_frame: tkinter.Frame, tabs: list,
               buttons_dict: dict[str, tkinter.Button],
               survey_loc_dict: dict[str, dict[str, tkinter.StringVar]]):
    tab_name = tab_control.tab(tab_frame, "text")
    tab_control.forget(tab_frame)
    tabs.remove(tab_frame)
    del buttons_dict[tab_name]
    del survey_loc_dict[tab_name]
    if len(tabs) == 1:  # if there is only one tab left, remove the delete button
        left_tab_name = tab_control.tab(tabs[0], "text")
        buttons_dict[left_tab_name].destroy()


def launch_function(window: tkinter.Tk, dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                    survey_loc_dict: dict[str, dict[str, tkinter.StringVar]]):
    if is_everything_ready(dc_sys_directory, dc_sys_file_name, survey_loc_dict):
        window.destroy()
    else:
        tkinter.messagebox.showinfo(title="Missing Information", message="Information is missing to launch the tool.")


def is_everything_ready(dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                        survey_loc_dict: dict[str, dict[str, tkinter.StringVar]]):
    test = True

    if dc_sys_directory.get() == "" or dc_sys_file_name.get() == "":
        test = False

    for survey_name, survey_info in survey_loc_dict.items():
        if survey_info["survey_directory"].get() == "" or survey_info["survey_file_name"].get() == "" \
                or survey_info["survey_sheet"].get() == "" or survey_info["start_row"].get() == "" \
                or survey_info["ref_col"].get() == "" or survey_info["type_col"].get() == "" \
                or survey_info["track_col"].get() == "" or survey_info["survey_kp_col"].get() == "":
            test = False

    return test
