#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
from .colors_pkg import *


__all__ = ["open_file_app", "open_excel_file", "launch_cmd"]


def open_file_app(file_path: str):
    os.startfile(file_path)


def open_excel_file(file_path: str):
    os.system(f"start excel.exe /x \"{file_path}\"")


def launch_cmd(cmd: str):
    print_log(f" > {cmd}")
    subprocess.call(cmd, shell=True)
