#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common_utils import *
from ..xl_pkg import *
from .gui_utils import *


__all__ = ["add_tab_control"]


def add_tab_control(frame: tkinter.Frame, type_name: str, add_open_button_func: Callable[None, None],
                    tab_bg: str = XlBgColor.green, bg: str = None
                    ) -> dict[str, dict[str, tkinter.StringVar]]:
    notebook_style = tkinter.ttk.Style()
    notebook_style.theme_create("custom_theme", settings={
        "TNotebook": {
            "layout": [],
            "configure": {"tabposition": "nw",
                          "background": "white",  # background color of the tabs bar
                          "tabmargins": [0, 0, 10, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1]},
            "map": {"background": [("selected", f"#{tab_bg}"),  # tab color when active
                                   ("!active", "gray75")]}}  # tab color when not active
    })
    notebook_style.theme_use("custom_theme")

    tab_control = tkinter.ttk.Notebook(frame)

    if bg is None:
        bg = default_gui_bg_color(frame)

    tabs = list()
    buttons_dict = dict()
    tab_dict = dict()

    _create_new_tab(type_name, add_open_button_func, tab_control, tabs, buttons_dict, tab_dict, bg)

    return tab_dict


def _create_new_tab(type_name: str, add_open_button_func: Callable[None, None],
                    tab_control: tkinter.ttk.Notebook, tabs: list[tkinter.ttk.Frame],
                    delete_buttons_dict: dict[str, tkinter.Button],
                    tab_dict: dict[str, dict[str, tkinter.StringVar]], bg: str) -> None:

    tab_number = 1 if not tabs else int(tab_control.tab(tabs[-1], "text").split()[-1]) + 1
    tab_name = f"{type_name.title()} {tab_number}"

    tab_frame = tkinter.Frame(tab_control, bg=bg, padx=10, pady=10)
    tab_control.add(tab_frame, text=tab_name)
    tab_control.pack(expand=1, anchor="sw", fill="both")
    tab_control.select(tab_frame)
    tabs.append(tab_frame)

    tab_dict[tab_name] = add_open_button_func(
        tab_frame, ref_row=0, extra_func=lambda: _add_another_tab_button(type_name, add_open_button_func, tab_control,
                                                                         tab_frame, tabs, delete_buttons_dict, tab_dict,
                                                                         bg), bg=bg)

    if tab_number != 1:  # if there is only one tab, no delete button
        delete_buttons_dict[tab_name] = (
            _add_delete_tab_button(tab_control, tab_frame, tabs, delete_buttons_dict, tab_dict))
    if len(tabs) == 2:  # if there are more than one tab, add the delete button on the first tab
        delete_buttons_dict[tab_control.tab(tabs[0], "text")] = (
            _add_delete_tab_button(tab_control, tabs[0], tabs, delete_buttons_dict, tab_dict))


def _add_another_tab_button(type_name: str, add_open_button_func: Callable[None, None],
                            tab_control: tkinter.ttk.Notebook, tab_frame: tkinter.Frame, tabs: list,
                            delete_buttons_dict: dict[str, tkinter.Button],
                            tab_dict: dict[str, dict[str, tkinter.StringVar]], bg: str) -> tkinter.Button:

    text = f"add another {type_name} file"
    new_tab_button = tkinter.Button(
        tab_frame,
        text=text,
        command=lambda: _create_new_tab(type_name, add_open_button_func, tab_control, tabs, delete_buttons_dict,
                                        tab_dict, bg),
        wraplength=3.5*len(text),
        background="#FFFF77"
    )
    new_tab_button.grid(column=0, row=9, rowspan=4, sticky="sw", padx=5, pady=5)
    return new_tab_button


def _add_delete_tab_button(tab_control: tkinter.ttk.Notebook, tab_frame: tkinter.Frame, tabs: list,
                           buttons_dict: dict[str, tkinter.Button],
                           tab_dict: dict[str, dict[str, tkinter.StringVar]]) -> tkinter.Button:

    delete_button = tkinter.Button(
        tab_frame,
        text="delete tab",
        command=lambda: _delete_tab(tab_control, tab_frame, tabs, buttons_dict, tab_dict),
        wraplength=80,
        background="#FFA0A0",
    )
    delete_button.grid(column=6, row=9, rowspan=4, sticky="se", padx=5, pady=5)
    return delete_button


def _delete_tab(tab_control: tkinter.ttk.Notebook, tab_frame: tkinter.Frame, tabs: list,
                buttons_dict: dict[str, tkinter.Button],
                tab_dict: dict[str, dict[str, tkinter.StringVar]]):

    tab_name = tab_control.tab(tab_frame, "text")
    tab_control.forget(tab_frame)
    tabs.remove(tab_frame)
    del buttons_dict[tab_name]
    del tab_dict[tab_name]

    if len(tabs) == 1:  # if there is only one tab left, remove the delete button
        left_tab_name = tab_control.tab(tabs[0], "text")
        buttons_dict[left_tab_name].destroy()
