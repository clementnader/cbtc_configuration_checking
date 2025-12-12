#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import *
from ..dc_sys import *
from ..database_location import DATABASE_LOCATION
from .gui_control_tables_utils import *


__all__ = ["control_tables_window"]


def control_tables_window() -> None:
    ga_version = get_ga_version_text()
    print_title(f"Route and Overlap Verification", color=Color.mint_green)
    print(f"{Color.light_green}Select the Control Tables and the DC_SYS "
          f"{Color.cyan}{Color.underline}compatible with CCTool-OO Schema {ga_version}{Color.no_underline}"
          f"{Color.light_green}.{Color.reset}\n")

    DATABASE_LOCATION.reset()  # reset database location information
    # Root window
    window_title = f"Control Table Verification (CCTool-OO Schema {ga_version})"
    window = create_window(window_title)

    # Top 2 Frame
    bg = f"#{XlBgColor.light_orange}"
    top2_left_frame = tkinter.Frame(window, bg=bg)
    top2_left_frame.grid(column=0, row=1, sticky="nswe")
    sub_frame = tkinter.Frame(top2_left_frame, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    control_tables_config_ini_file = add_control_tables_config_ini_frame(sub_frame, ref_row=0)

    # Center Frame
    bg = f"#{XlBgColor.light_green}"
    center_left_frame = tkinter.Frame(window, bg=bg)
    center_left_frame.grid(column=0, row=5, sticky="nswe")
    control_tables_loc_dict = add_tab_control(center_left_frame, type_name="control table",
                                              add_open_button_func=add_control_table_open_button,
                                              tab_bg= XlBgColor.green)

    control_table_type = tkinter.StringVar()
    control_table_type.set("")

    # Top Right Frame
    bg = f"#{XlBgColor.light_blue}"
    top_right_frame = tkinter.Frame(window, bg=bg)
    top_right_frame.grid(column=10, row=0, rowspan=20, sticky="nswe")
    sub_frame = tkinter.Frame(top_right_frame, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    launch_translation_button = add_translation_button(window, sub_frame,
                                                       control_tables_config_ini_file,
                                                       control_tables_loc_dict, control_table_type)

    # Bottom Frame
    bg = f"#{XlBgColor.light_yellow}"
    bottom_left_frame = tkinter.Frame(window, bg=bg)
    bottom_left_frame.grid(column=0, row=20, sticky="nswe")
    sub_frame = tkinter.Frame(bottom_left_frame, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    dc_sys_directory, dc_sys_file_name = add_dc_sys_open_button(sub_frame, ref_row=0, ga_version=ga_version)

    # Bottom Frame 2
    bg = f"#{XlBgColor.light_yellow}"
    bottom_left_frame2 = tkinter.Frame(window, bg=bg)
    bottom_left_frame2.grid(column=0, row=25, sticky="nswe")
    sub_frame = tkinter.Frame(bottom_left_frame2, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    dc_bop_directory, dc_bop_file_name = add_dc_bop_open_button(sub_frame, ref_row=0)

    # Bottom Right Frame
    bg = f"#{XlBgColor.light_blue}"
    bottom_right_frame = tkinter.Frame(window, bg=bg)
    bottom_right_frame.grid(column=10, row=20, rowspan=10, sticky="nswe")
    sub_frame = tkinter.Frame(bottom_right_frame, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    launch_button = add_launch_button(window, sub_frame, dc_sys_directory, dc_sys_file_name,
                                      dc_bop_directory, dc_bop_file_name,
                                      control_tables_config_ini_file,
                                      control_tables_loc_dict, control_table_type)

    # Top Frame
    bg = f"#{XlBgColor.light_orange}"
    top_left_frame = tkinter.Frame(window, bg=bg)
    top_left_frame.grid(column=0, row=0, sticky="nswe")
    top_left_frame.columnconfigure(0, minsize=400)
    sub_frame = tkinter.Frame(top_left_frame, bg=bg, padx=10, pady=10)
    sub_frame.grid(column=0, row=0, sticky="nswe")
    add_control_table_type_frame(sub_frame, control_table_type, window, window_title, launch_translation_button,
                                 launch_button, ref_row=0, bg=bg)

    # Separators
    sep_top_top = tkinter.ttk.Separator(window, orient="horizontal")
    sep_top_top.grid(column=0, row=4, sticky="we")
    sep_top_bottom = tkinter.ttk.Separator(window, orient="horizontal")
    sep_top_bottom.grid(column=0, row=19, sticky="we")

    sep_top_right = tkinter.ttk.Separator(window, orient="vertical")
    sep_top_right.grid(column=9, row=0, sticky="ns")
    sep_top_right2 = tkinter.ttk.Separator(window, orient="vertical")
    sep_top_right2.grid(column=9, row=1, sticky="ns")
    sep_top_right3 = tkinter.ttk.Separator(window, orient="vertical")
    sep_top_right3.grid(column=9, row=5, sticky="ns")
    sep_bottom_right = tkinter.ttk.Separator(window, orient="vertical")
    sep_bottom_right.grid(column=9, row=20, sticky="ns")
    sep_bottom_right2 = tkinter.ttk.Separator(window, orient="vertical")
    sep_bottom_right2.grid(column=9, row=25, sticky="ns")

    window.mainloop()

    print_log(f"\nRoute and Overlap Verification Window was closed.")
    return


def add_translation_button(window: tkinter.Tk, frame: tkinter.Frame,
                           control_tables_config_ini_file: tkinter.StringVar,
                           control_tables_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                           control_table_type: tkinter.StringVar) -> tkinter.Button:
    launch_translation_button = tkinter.Button(
        frame,
        text="Launch\nControl Table Translation",
        command=lambda: launch_translation_function(window, control_tables_config_ini_file,
                                                    control_tables_loc_dict, control_table_type),
        wraplength=120,
        background=f"#{XlBgColor.blue}",
        font=tkinter.font.Font(size=11, weight="bold"),
        width=13
    )
    launch_translation_button.grid(column=0, row=0, padx=5, pady=(80, 0))
    return launch_translation_button



def add_launch_button(window: tkinter.Tk, frame: tkinter.Frame,
                      dc_sys_directory: tkinter.StringVar, dc_sys_file_name: tkinter.StringVar,
                      dc_bop_directory: tkinter.StringVar, dc_bop_file_name: tkinter.StringVar,
                      control_tables_config_ini_file: tkinter.StringVar,
                      control_tables_loc_dict: dict[str, dict[str, tkinter.StringVar]],
                      control_table_type: tkinter.StringVar) -> tkinter.Button:
    launch_button = tkinter.Button(
        frame,
        text="Launch\nControl Table Verification",
        command=lambda: launch_function(window, dc_sys_directory, dc_sys_file_name, dc_bop_directory, dc_bop_file_name,
                                        control_tables_config_ini_file,
                                        control_tables_loc_dict, control_table_type),
        wraplength=120,
        background=f"#{XlBgColor.blue}",
        font=tkinter.font.Font(size=11, weight="bold"),
        width=13
    )
    launch_button.grid(column=0, row=0, padx=5, pady=5)
    return launch_button
