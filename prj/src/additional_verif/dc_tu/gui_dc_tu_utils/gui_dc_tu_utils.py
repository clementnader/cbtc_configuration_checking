#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *


__all__ = ["launch_function", "is_everything_ready"]


def launch_function(window: tkinter.Tk, c11_d470_directory: tkinter.StringVar):
    if is_everything_ready(c11_d470_directory):
        window.destroy()
    else:
        tkinter.messagebox.showinfo(title="Missing Information", message="Information is missing to launch the tool.")


def is_everything_ready(c11_d470_directory: tkinter.StringVar):
    test = True

    if c11_d470_directory.get() == "":
        test = False

    return test
