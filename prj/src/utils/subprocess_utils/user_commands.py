#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from ..colors_pkg import *
from .subprocess_utils import *


__all__ = ["get_user_full_name"]


FULL_NAME_ATTRIBUTES = {
    "fr": "Nom complet",
    "en": "Full name",
}


def get_user_full_name() -> str:
    if sys.platform != "win32":
        print_log(f"Platform OS is not Windows, unable to find the user name.")
        return ""
    full_name = None
    for language, full_name_attr in FULL_NAME_ATTRIBUTES.items():
        cmd = cmd_to_get_full_name(full_name_attr)
        out = catch_output_cmd(cmd)
        if out:
            full_name = out
            break
    if full_name is None:
        print_log(f"Unable to find the user name.")
        return ""
    if "(" in full_name:
        full_name = full_name.split("(", 1)[0].strip()
    if "," in full_name:
        full_name = " ".join(reversed(full_name.split(",", 1))).strip()
    return full_name


def cmd_to_get_full_name(full_name_attr: str) -> str:
    cmd = (f"@echo off && FOR /f \"tokens=2*\" %n IN (\'net user \"%USERNAME%\" /domain^"
           f"|findstr /C:\"{full_name_attr}\"\') DO echo %o")
    return cmd
