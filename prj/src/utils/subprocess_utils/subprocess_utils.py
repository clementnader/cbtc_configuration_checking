#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from ..colors_pkg import *


__all__ = ["open_file_app", "open_excel_file", "launch_cmd", "catch_output_cmd"]


G_ENCODING = None


def open_file_app(file_path: str) -> None:
    os.startfile(file_path)


def open_excel_file(file_path: str) -> None:
    os.system(f"start excel.exe /x \"{file_path}\"")


def launch_cmd(cmd: str, shell: bool = True, cwd: str = None, env: dict[str] = None) -> None:
    print_log(f" > {cmd}\n")
    subprocess.call(cmd, shell=shell, cwd=cwd, env=env)


def catch_output_cmd(cmd: str) -> str:
    global G_ENCODING
    if G_ENCODING is None:
        get_language_encoding()
    print_log(f" > {cmd}")
    instance = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, encoding=G_ENCODING, universal_newlines=True)
    res = instance.stdout.read().strip()
    print(f"{Color.dark_grey}{res}{Color.reset}\n")
    return res


def get_language_encoding():
    global G_ENCODING
    if sys.platform == "win32":
        cmd = "chcp"
        print_log(f" > {cmd}")
        instance = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out = instance.stdout.read().strip().decode(errors="ignore")
        print(f"{Color.dark_grey}{out}{Color.reset}\n")
        active_code_page = out.split()[-1]
        encoding = f"CP{active_code_page}"
    else:
        encoding = "utf-8"
    print_log(f"Set the stdout encoding to {encoding}.\n")
    G_ENCODING = encoding
