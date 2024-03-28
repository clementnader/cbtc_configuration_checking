#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..dc_sys import *
from .gui_survey_utils import *


__all__ = ["survey_window"]


def survey_window() -> None:
    ga_version = get_ga_version_text()
    print_title(f"Survey Verification", color=Color.mint_green)
    print(f"{Color.light_green}Select the DC_SYS "
          f"{Color.cyan}{Color.underline}compatible with System Referential {ga_version}{Color.no_underline}"
          f"{Color.light_green} and the Survey information to verify.{Color.reset}\n")
    # Root window
    window = tkinter.Tk()
    window.title(f"Survey Verification (System Referential {ga_version})")
    window.resizable(False, False)
    window.attributes("-topmost", True)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"+{screen_width//4}+{screen_height//4}")

    # Top Frame
    bg = f"#{XlBgColor.light_yellow}"
    top_left_frame = tkinter.Frame(window, bg=bg)
    top_left_frame.grid(column=0, row=0, sticky="nswe")
    sub_frame = tkinter.Frame(top_left_frame, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    dc_sys_directory, dc_sys_file_name = add_dc_sys_open_button(sub_frame, ref_row=0, ga_version=ga_version)

    # Top Frame 2
    bg = f"#{XlBgColor.light_yellow}"
    top_left_frame2 = tkinter.Frame(window, bg=bg)
    top_left_frame2.grid(column=0, row=5, sticky="nswe")
    sub_frame = tkinter.Frame(top_left_frame2, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    automatic_names, block_def_directory, block_def_file_name = add_block_joint_def_frame(sub_frame, ref_row=0, bg=bg)

    # Bottom Frame
    bg = f"#{XlBgColor.light_green}"
    bottom_left_frame = tkinter.Frame(window, bg=bg)
    bottom_left_frame.grid(column=0, row=20, sticky="nswe")
    survey_loc_dict = add_survey_tab_control(bottom_left_frame)

    # Right Frame
    bg = f"#{XlBgColor.light_blue}"
    right_frame = tkinter.Frame(window, bg=bg)
    right_frame.grid(column=10, row=0, rowspan=40, sticky="nswe")
    sub_frame = tkinter.Frame(right_frame, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    add_launch_survey_button(window, sub_frame, dc_sys_directory, dc_sys_file_name, survey_loc_dict,
                             automatic_names, block_def_directory, block_def_file_name)

    # Separators
    sep_top_top2 = tkinter.ttk.Separator(window, orient="horizontal")
    sep_top_top2.grid(column=0, row=4, sticky="we")
    sep_top_bottom = tkinter.ttk.Separator(window, orient="horizontal")
    sep_top_bottom.grid(column=0, row=19, sticky="we")

    sep_top_right = tkinter.ttk.Separator(window, orient="vertical")
    sep_top_right.grid(column=9, row=0, sticky="ns")
    sep_top_right2 = tkinter.ttk.Separator(window, orient="vertical")
    sep_top_right2.grid(column=9, row=5, sticky="ns")
    sep_bottom_right = tkinter.ttk.Separator(window, orient="vertical")
    sep_bottom_right.grid(column=9, row=20, sticky="ns")

    window.mainloop()

    print_log(f"Survey Verification Window was closed.")
    return


def add_survey_tab_control(frame: tkinter.Frame, bg: str = None) -> dict[str, dict[str, tkinter.StringVar]]:
    notebook_style = tkinter.ttk.Style()
    notebook_style.theme_create("custom_theme", settings={
        "TNotebook": {
            "layout": [],
            "configure": {"tabposition": "nw",
                          "background": "white",  # background color of the tabs bar
                          "tabmargins": [0, 0, 10, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1]},
            "map": {"background": [("selected", f"#{XlBgColor.green}"),  # tab color when active
                                   ("!active", "gray75")]}}  # tab color when not active
    })
    notebook_style.theme_use("custom_theme")

    tab_control = tkinter.ttk.Notebook(frame)

    if bg is None:
        bg = default_gui_bg_color(frame)

    tabs = list()
    buttons_dict = dict()
    survey_loc_dict = dict()

    create_new_survey_tab(tab_control, tabs, buttons_dict, survey_loc_dict, bg)

    return survey_loc_dict


def create_new_survey_tab(tab_control: tkinter.ttk.Notebook, tabs: list[tkinter.ttk.Frame],
                          delete_buttons_dict: dict[str, tkinter.Button],
                          survey_loc_dict: dict[str, dict[str, tkinter.StringVar]], bg: str) -> None:

    tab_number = 1 if not tabs else int(tab_control.tab(tabs[-1], "text").split(" ", 1)[1]) + 1
    tab_name = f"Survey {tab_number}"

    tab_frame = tkinter.Frame(tab_control, bg=bg, padx=10, pady=10)
    tab_control.add(tab_frame, text=tab_name)
    tab_control.pack(expand=1, anchor="sw", fill="both")
    tab_control.select(tab_frame)
    tabs.append(tab_frame)

    survey_loc_dict[tab_name] = add_survey_open_button(
        tab_frame, ref_row=0, extra_func=lambda: add_another_survey_button(
            tab_control, tab_frame, tabs, delete_buttons_dict, survey_loc_dict, bg), bg=bg)

    if tab_number != 1:  # if there is only one tab, no delete button
        delete_buttons_dict[tab_name] = (
            add_delete_tab_button(tab_control, tab_frame, tabs, delete_buttons_dict, survey_loc_dict))
    if len(tabs) == 2:  # if there are more than one tab, add the delete button on the first tab
        delete_buttons_dict[tab_control.tab(tabs[0], "text")] = (
            add_delete_tab_button(tab_control, tabs[0], tabs, delete_buttons_dict, survey_loc_dict))


def add_another_survey_button(tab_control: tkinter.ttk.Notebook, tab_frame: tkinter.Frame, tabs: list,
                              delete_buttons_dict: dict[str, tkinter.Button],
                              survey_loc_dict: dict[str, dict[str, tkinter.StringVar]], bg: str) -> tkinter.Button:
    new_tab_button = tkinter.Button(
        tab_frame,
        text="add another survey file",
        command=lambda: create_new_survey_tab(tab_control, tabs, delete_buttons_dict, survey_loc_dict, bg),
        wraplength=80,
        background="#FFFF77"
    )
    new_tab_button.grid(column=0, row=9, rowspan=4, sticky="sw", padx=5, pady=5)
    return new_tab_button


def add_delete_tab_button(tab_control: tkinter.ttk.Notebook, tab_frame: tkinter.Frame, tabs: list,
                          buttons_dict: dict[str, tkinter.Button],
                          survey_loc_dict: dict[str, dict[str, tkinter.StringVar]]) -> tkinter.Button:
    delete_button = tkinter.Button(
        tab_frame,
        text="delete tab",
        command=lambda: delete_tab(tab_control, tab_frame, tabs, buttons_dict, survey_loc_dict),
        wraplength=80,
        background="#FFA0A0",
    )
    delete_button.grid(column=6, row=9, rowspan=4, sticky="se", padx=5, pady=5)
    return delete_button


def add_launch_survey_button(window: tkinter.Tk, frame: tkinter.Frame,
                             dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                             survey_loc_dict: dict[str, dict[str, Union[tkinter.StringVar, tkinter.BooleanVar]]],
                             automatic_names: tkinter.BooleanVar,
                             block_def_directory: tkinter.StringVar, block_def_file_name: tkinter.StringVar) -> None:
    launch_button = tkinter.Button(
        frame,
        text="Launch Survey Verification",
        command=lambda: launch_function(window, dc_sys_directory, dc_sys_file_name, survey_loc_dict,
                                        automatic_names, block_def_directory, block_def_file_name),
        wraplength=120,
        background=f"#{XlBgColor.blue}",
        font=tkinter.font.Font(size=11, weight="bold")
    )
    launch_button.grid(column=0, row=0, padx=5, pady=(146, 5))
