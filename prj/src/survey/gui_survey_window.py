#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from ..database_location import DATABASE_LOC
from ..utils import *


__all__ = ["survey_window"]


def survey_window():
    # Root window
    window = tkinter.Tk()
    window.title("Survey Verification")
    window.resizable(False, False)
    window.attributes("-topmost", True)
    # window.minsize(550, 250)

    top_frame = tkinter.Frame(window)
    top_frame.grid(column=0, row=0, padx=5, pady=5, sticky="w")
    dc_sys_directory, dc_sys_file_name = add_dc_sys_open_button(top_frame, ref_row=0)

    sep = tkinter.ttk.Separator(window, orient="horizontal")
    sep.grid(column=0, row=4, sticky="we")

    bottom_frame = tkinter.Frame(window)
    bottom_frame.grid(column=0, row=5, padx=5, pady=5, sticky="w")
    survey_loc_dict = add_survey_tab_control(bottom_frame)

    sep_top_right = tkinter.ttk.Separator(window, orient="vertical")
    sep_top_right.grid(column=3, row=0, sticky="ns")
    sep_bottom_right = tkinter.ttk.Separator(window, orient="vertical")
    sep_bottom_right.grid(column=3, row=5, sticky="ns")

    right_frame = tkinter.Frame(window)
    right_frame.grid(column=4, row=5, padx=5, pady=5)
    add_launch_survey_button(window, right_frame, dc_sys_directory, dc_sys_file_name, survey_loc_dict)

    window.mainloop()

    if is_everything_ready(dc_sys_directory, dc_sys_file_name, survey_loc_dict):
        update_database_loc(dc_sys_directory, dc_sys_file_name, survey_loc_dict)
    else:
        print_error("Execution aborted.")
        sys.exit(1)


def update_database_loc(dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                        survey_loc_dict: dict[str, dict[str, tkinter.StringVar]]):

    DATABASE_LOC.dc_sys_addr = os.path.join(dc_sys_directory.get(), dc_sys_file_name.get()).replace("/", os.path.sep)

    DATABASE_LOC.survey_loc.survey_addr = list()
    DATABASE_LOC.survey_loc.survey_sheet = list()
    DATABASE_LOC.survey_loc.start_line = list()
    DATABASE_LOC.survey_loc.ref_col = list()
    DATABASE_LOC.survey_loc.type_col = list()
    DATABASE_LOC.survey_loc.track_col = list()
    DATABASE_LOC.survey_loc.design_kp_col = list()
    DATABASE_LOC.survey_loc.survey_kp_col = list()

    for survey_name, survey_info in survey_loc_dict.items():
        DATABASE_LOC.survey_loc.survey_addr.append(os.path.join(survey_info["survey_directory"].get(),
                                                   survey_info["survey_file_name"].get()).replace("/", os.path.sep))
        DATABASE_LOC.survey_loc.survey_sheet.append(survey_info["survey_sheet"].get())
        DATABASE_LOC.survey_loc.start_line.append(int(survey_info["start_line"].get()))
        DATABASE_LOC.survey_loc.ref_col.append(get_col(survey_info["ref_col"].get()))
        DATABASE_LOC.survey_loc.type_col.append(get_col(survey_info["type_col"].get()))
        DATABASE_LOC.survey_loc.track_col.append(get_col(survey_info["track_col"].get()))
        DATABASE_LOC.survey_loc.design_kp_col.append(get_col(survey_info["design_kp_col"].get()))
        DATABASE_LOC.survey_loc.survey_kp_col.append(get_col(survey_info["survey_kp_col"].get()))


def get_col(val: str):
    try:
        val = int(val)
    except ValueError:
        val = get_xl_column_number(val)
    return val


def add_survey_tab_control(frame: tkinter.Frame) -> dict[str, dict[str, tkinter.StringVar]]:
    notebook_style = tkinter.ttk.Style()
    notebook_style.configure("TNotebook", tabposition="sw")
    tab_control = tkinter.ttk.Notebook(frame)

    tabs = list()
    survey_loc_dict = dict()

    create_new_survey_tab(tab_control, tabs, survey_loc_dict)

    return survey_loc_dict


def create_new_survey_tab(tab_control: tkinter.ttk.Notebook, tabs: list,
                          survey_loc_dict: dict[str, dict[str, tkinter.StringVar]]):
    tab_number = 1 if not tabs else int(tabs[-1].split(" ", 1)[1]) + 1
    tab_name = f"Survey {tab_number}"
    tabs.append(tab_name)

    tab_frame = tkinter.ttk.Frame(tab_control)
    tab_control.add(tab_frame, text=tab_name)
    tab_control.pack(expand=1, fill="both")
    tab_control.select(tab_frame)

    survey_loc_dict[tab_name] = add_survey_open_button(tab_frame, ref_row=3,
                                                       extra_func=lambda: add_another_survey_button(
                                                           tab_control, tab_frame, tabs, survey_loc_dict))
    if tab_number != 1:
        add_delete_tab_button(tab_control, tab_frame, tabs, survey_loc_dict, tab_name)


def add_another_survey_button(tab_control: tkinter.ttk.Notebook, tab_frame: tkinter.Frame, tabs: list,
                              survey_loc_dict: dict[str, dict[str, tkinter.StringVar]]):
    open_button = tkinter.Button(
        tab_frame,
        text="add another survey file",
        command=lambda: create_new_survey_tab(tab_control, tabs, survey_loc_dict),
        wraplength=80,
        background="#A0FFFF",
    )
    open_button.grid(column=0, row=14, rowspan=4)


def add_delete_tab_button(tab_control: tkinter.ttk.Notebook, tab_frame: tkinter.Frame, tabs: list,
                          survey_loc_dict: dict[str, dict[str, tkinter.StringVar]], tab_name: str):
    open_button = tkinter.Button(
        tab_frame,
        text="delete tab",
        command=lambda: delete_tab(tab_control, tab_frame, tabs, survey_loc_dict, tab_name),
        wraplength=80,
        background="#FFFFA0",
    )
    open_button.grid(column=2, row=14, rowspan=4)


def delete_tab(tab_control: tkinter.ttk.Notebook, tab_frame: tkinter.Frame, tabs: list,
               survey_loc_dict: dict[str, dict[str, tkinter.StringVar]], tab_name: str):
    tab_control.forget(tab_frame)
    tabs.remove(tab_name)
    del survey_loc_dict[tab_name]


def add_launch_survey_button(window: tkinter.Tk, frame: tkinter.Frame,
                             dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                             survey_loc_dict: dict[str, dict[str, tkinter.StringVar]]) -> None:
    open_button = tkinter.Button(
        frame,
        text="Launch Survey Verification",
        command=lambda: launch_button(window, dc_sys_directory, dc_sys_file_name, survey_loc_dict),
        wraplength=120,
        background="#A0FFA0",
        font=tkinter.font.Font(size=11, weight="bold")

    )
    open_button.grid(column=4, row=13, rowspan=2)


def launch_button(window: tkinter.Tk, dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
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
                or survey_info["survey_sheet"].get() == "" or survey_info["start_line"].get() == "" \
                or survey_info["ref_col"].get() == "" or survey_info["type_col"].get() == "" \
                or survey_info["track_col"].get() == "" \
                or survey_info["design_kp_col"].get() == "" or survey_info["survey_kp_col"].get() == "":
            test = False

    return test
