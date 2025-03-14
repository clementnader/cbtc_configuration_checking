#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
from ..common_utils import *
from ..xl_pkg import get_xl_bg_dimmer_color


__all__ = ["tkinter", "default_gui_bg_color", "disable_frame", "enable_frame",
           "gui_add_dir_and_file_open_button", "gui_add_dir_open_button",
           "create_window",
           "get_gui_initial_directory", "set_gui_initial_directory"]


G_INITIAL_DIRECTORY = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                   "..", "..", "..", "..", ".."))  # root directory of the tool


def create_window(window_title: str, min_width: Optional[int] = 300, min_height: Optional[int] = 100) -> tkinter.Tk:
    window = tkinter.Tk()
    # Set title
    window.title(window_title)
    # Define window icon
    logo_name = "logo_hitachi_rail.png"
    photo = tkinter.PhotoImage(file=os.path.join(TEMPLATE_DIRECTORY, logo_name))
    window.wm_iconphoto(False, photo)
    # Set properties
    window.resizable(False, False)  # not resizable
    window.attributes("-topmost", True)  # always at top
    # Set window default position, it is set at the top left with a margin of 1/4 of the width screen from the edge
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"+{screen_width // 4}+{screen_height // 4}")
    # Set minimal window size
    window.minsize(min_width, min_height)
    return window


def disable_frame(frame: Union[tkinter.Tk, tkinter.Frame]):
    for child in frame.winfo_children():
        wtype = child.winfo_class()
        if wtype in ("Frame", "Labelframe", "TFrame", "TLabelframe"):  # child is a frame
            disable_frame(child)  # recursive call
        else:
            child.configure(state=tkinter.DISABLED)


def enable_frame(frame: Union[tkinter.Tk, tkinter.Frame]):
    for child in frame.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ("Frame", "Labelframe", "TFrame", "TLabelframe"):
            child.configure(state=tkinter.NORMAL)
        else:  # child is a frame
            enable_frame(child)  # recursive call


def gui_add_dir_and_file_open_button(frame: Union[tkinter.Tk, tkinter.Frame], ref_row: int,
                                     directory_string_var: tkinter.StringVar, file_name_string_var: tkinter.StringVar,
                                     title_text: str, open_text: str,
                                     file_types: Union[tuple[str, str], list[tuple[str, str]]],
                                     bg: str = None, size: int = 11,
                                     extra_func: Callable[None, None] = None,
                                     specific_directory: str = None) -> tkinter.Button:
    if bg is None:
        bg = default_gui_bg_color(frame)

    frame.grid_columnconfigure(0, minsize=80)
    title_label = tkinter.Label(frame, text=title_text, font=tkinter.font.Font(size=size, weight="bold"), bg=bg)
    title_label.grid(column=0, row=ref_row, rowspan=2, sticky="w")

    directory_label = tkinter.Label(frame, text="", textvariable=directory_string_var,
                                    font=tkinter.font.Font(size=size-2), bg=bg)
    directory_label.grid(column=1, row=ref_row, sticky="w", padx=(0, 5))

    file_name_label = tkinter.Label(frame, text="", textvariable=file_name_string_var,
                                    font=tkinter.font.Font(size=size-2, weight="bold"), bg=bg)
    file_name_label.grid(column=1, row=ref_row+1, sticky="w", padx=(0, 5))

    # Open file button
    button_bg = "#" + get_xl_bg_dimmer_color(bg.removeprefix("#")) if bg.startswith("#") else bg
    open_button = tkinter.Button(
        frame,
        text="select file",
        command=lambda: gui_select_file(open_text, file_types, directory_string_var, file_name_string_var, extra_func,
                                        specific_directory),
        bg=button_bg,
        font=tkinter.font.Font(size=size-2)
    )
    open_button.grid(column=6, row=ref_row, rowspan=2, sticky="w", padx=5, pady=5)
    return open_button


def gui_select_file(open_text: str, file_types: Union[tuple[str, str], list[tuple[str, str]]],
                    directory_string_var: tkinter.StringVar, file_name_string_var: tkinter.StringVar,
                    extra_func: Callable[None, None] = None,
                    specific_directory: str = None):

    global G_INITIAL_DIRECTORY
    initial_directory = specific_directory if specific_directory is not None else G_INITIAL_DIRECTORY

    if not isinstance(file_types, list):
        file_types = [file_types]
    file_types = tuple(file_types)

    selected_file_name = tkinter.filedialog.askopenfilename(
        title=open_text,
        initialdir=initial_directory,
        filetypes=file_types
    )

    if not selected_file_name:
        return

    directory_string, file_name_string = os.path.split(selected_file_name)
    directory_string_var.set(directory_string)
    file_name_string_var.set(file_name_string)

    if specific_directory is None:
        G_INITIAL_DIRECTORY = directory_string_var.get()

    if extra_func is not None:
        extra_func()


def gui_add_dir_open_button(frame: Union[tkinter.Tk, tkinter.Frame], ref_row: int,
                            directory_string_var: tkinter.StringVar,
                            title_text: str, open_text: str,
                            bg: str = None,
                            extra_func: Callable[None, None] = None) -> tkinter.Button:
    if bg is None:
        bg = default_gui_bg_color(frame)

    frame.grid_columnconfigure(0, minsize=120)
    title_label = tkinter.Label(frame, text=title_text, font=tkinter.font.Font(size=11, weight="bold"), bg=bg)
    title_label.grid(column=0, row=ref_row, rowspan=2, sticky="w")

    directory_label = tkinter.Label(frame, text="", textvariable=directory_string_var, bg=bg)
    directory_label.grid(column=1, row=ref_row, rowspan=2, sticky="w", columnspan=5, padx=(0, 5))

    # Open file button
    button_bg = "#" + get_xl_bg_dimmer_color(bg.removeprefix("#")) if bg.startswith("#") else bg
    open_button = tkinter.Button(
        frame,
        text="select directory",
        command=lambda: gui_select_directory(open_text, directory_string_var, extra_func),
        bg=button_bg
    )
    open_button.grid(column=6, row=ref_row, rowspan=2, sticky="w", padx=5, pady=5)
    return open_button


def gui_select_directory(open_text: str, directory_string_var: tkinter.StringVar,
                         extra_func: Callable[None, None] = None):

    global G_INITIAL_DIRECTORY

    directory_string = tkinter.filedialog.askdirectory(
        title=open_text,
        initialdir=G_INITIAL_DIRECTORY,
    )

    if not directory_string:
        return

    directory_string_var.set(directory_string)
    G_INITIAL_DIRECTORY = directory_string_var.get()

    if extra_func is not None:
        extra_func()


def default_gui_bg_color(frame: tkinter.Frame) -> str:
    return frame.cget("background")


def get_gui_initial_directory() -> str:
    global G_INITIAL_DIRECTORY
    return G_INITIAL_DIRECTORY


def set_gui_initial_directory(initial_directory: str) -> None:
    global G_INITIAL_DIRECTORY
    G_INITIAL_DIRECTORY = initial_directory
