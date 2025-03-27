#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ...utils import *
from ..control_tables_utils import *


__all__ = ["add_control_table_type_frame", "add_control_tables_config_ini_frame"]


def add_control_table_type_frame(frame: tkinter.Frame, control_table_type_var: tkinter.StringVar,
                                 window: tkinter.Tk, window_title: str,
                                 launch_translation_button: tkinter.Button, launch_button: tkinter.Button,
                                 ref_row: int, bg: str = None):

    title_label = tkinter.Label(frame, text="Control Table Type:",
                                font=tkinter.font.Font(size=11, weight="bold"), bg=bg)
    title_label.grid(column=0, row=ref_row, sticky="w")

    # Frame
    sub_frame = tkinter.Frame(frame, bg=bg, padx=5, pady=5)
    sub_frame.grid(column=0, row=1, sticky="nswe")
    _add_control_table_type_buttons(sub_frame, control_table_type_var, window, window_title, launch_translation_button,
                                    launch_button, 0, bg=bg)


def _add_control_table_type_buttons(frame: tkinter.Frame, control_table_type_var: tkinter.StringVar,
                                    window: tkinter.Tk, window_title: str,
                                    launch_translation_button: tkinter.Button, launch_button: tkinter.Button,
                                    ref_row: int, bg: str = None) -> tkinter.StringVar:
    def table_type_click():
        window.title(f"{control_table_type_var.get().title()} {window_title}")
        launch_translation_button.config(text=f"Launch {control_table_type_var.get().title()} "
                                                f"Control Table Translation")
        launch_button.config(text=f"Launch {control_table_type_var.get().title()} "
                                  f"Control Table Verification")
        if control_table_type_var.get() == CONTROL_TABLE_TYPE.route:
            route_control_table_radiobutton.config(fg="black", font=tkinter.font.Font(size=11, weight="bold"))
            overlap_control_table_radiobutton.config(fg="grey", font=tkinter.font.Font(size=11, weight="normal"))
        else:
            route_control_table_radiobutton.config(fg="grey", font=tkinter.font.Font(size=11, weight="normal"))
            overlap_control_table_radiobutton.config(fg="black", font=tkinter.font.Font(size=11, weight="bold"))

    if bg is None:
        bg = default_gui_bg_color(frame)

    frame.columnconfigure(0, minsize=50)
    frame.columnconfigure(1, minsize=100)

    # Route Radio Button
    route_control_table_radiobutton = tkinter.Radiobutton(frame, text="Route",
                                                          font=tkinter.font.Font(size=11, weight="normal"),
                                                          variable=control_table_type_var, bg=bg,
                                                          value=CONTROL_TABLE_TYPE.route,
                                                          command=table_type_click,
                                                          tristatevalue="dummy")  # the tri state value default is "",
                                                          # so the radio button was appearing in tri-state with
                                                          # the initialization of control_table_type_var
    route_control_table_radiobutton.grid(column=1, row=ref_row+1, sticky="w")

    # Overlap Radio Button
    overlap_control_table_radiobutton = tkinter.Radiobutton(frame, text="Overlap",
                                                            font=tkinter.font.Font(size=11, weight="normal"),
                                                            variable=control_table_type_var, bg=bg,
                                                            value=CONTROL_TABLE_TYPE.overlap,
                                                            command=table_type_click,
                                                            tristatevalue="dummy")  # the tri state value default is "",
                                                            # so the radio button was appearing in tri-state with
                                                            # the initialization of control_table_type_var
    overlap_control_table_radiobutton.grid(column=2, row=ref_row+1, sticky="w")

    return control_table_type_var


def add_control_tables_config_ini_frame(frame: tkinter.Frame, ref_row: int, bg: str = None) -> tkinter.StringVar:
    title_text = "Control Tables Configuration .ini file: "
    open_text = "Open control_tables_configuration.ini"
    file_types = ("control_tables_configuration.ini", "*.ini")

    config_ini_directory = os.path.join(ROOT_DIRECTORY, "control_tables_configuration")
    control_tables_config_ini_directory = tkinter.StringVar()
    control_tables_config_ini_file = tkinter.StringVar()

    gui_add_dir_and_file_open_button(frame, ref_row,
                                     control_tables_config_ini_directory, control_tables_config_ini_file,
                                     title_text, open_text, file_types, bg=bg, specific_directory=config_ini_directory)

    return control_tables_config_ini_file
