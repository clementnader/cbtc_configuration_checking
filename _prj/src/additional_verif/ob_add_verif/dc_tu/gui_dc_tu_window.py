#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from ....utils import *
from .gui_dc_tu_utils import *
from .dc_tu_verification import *


__all__ = ["dc_tu_window"]


def dc_tu_window():
    print_title(f"DC_TU Verification{Color.no_underline} ({DC_TU_CHECKING_VERSION}){Color.reset}",
                color=Color.mint_green)
    print(f"{Color.light_green}Select the C11_D470.{Color.reset}\n")

    # Root window
    window = create_window("DC_TU Verification")

    # Left Frame
    bg = f"#{XlBgColor.light_yellow}"
    left_frame = tkinter.Frame(window, bg=bg)
    left_frame.grid(column=0, row=0, sticky="nswe")
    sub_frame = tkinter.Frame(left_frame, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    c11_d470_directory = add_c11_open_button(sub_frame, ref_row=0)

    # Right Frame
    bg = f"#{XlBgColor.light_green}"
    right_frame = tkinter.Frame(window, bg=bg)
    right_frame.grid(column=5, row=0, sticky="nswe")
    sub_frame = tkinter.Frame(right_frame, bg=bg, padx=10, pady=25)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    add_launch_dc_tu_button(window, sub_frame, c11_d470_directory)

    # Separators
    sep_right = tkinter.ttk.Separator(window, orient="vertical")
    sep_right.grid(column=4, row=0, sticky="ns")

    window.mainloop()

    if is_everything_ready(c11_d470_directory):
        update_database_loc(c11_d470_directory)
        dc_tu_verification()
    else:
        print_error("Execution aborted.")
        sys.exit(1)


def add_launch_dc_tu_button(window: tkinter.Tk, frame: tkinter.Frame, c11_d470_directory: tkinter.StringVar) -> None:
    launch_button = tkinter.Button(
        frame,
        text="Launch DC_TU Verification",
        command=lambda: launch_function(window, c11_d470_directory),
        wraplength=120,
        background="#A0FFA0",
        font=tkinter.font.Font(size=11, weight="bold")
    )
    launch_button.grid(column=0, row=0, padx=5, pady=0)
