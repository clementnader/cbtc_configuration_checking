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
    window = create_window(f"Survey Verification (System Referential {ga_version})")

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
    survey_loc_dict = add_tab_control(bottom_left_frame, type_name="survey",
                                      add_open_button_func=add_survey_open_button,
                                      tab_bg= XlBgColor.green)

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
