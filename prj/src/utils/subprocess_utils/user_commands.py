#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ctypes
from ..colors_pkg import *
# from .subprocess_utils import *


__all__ = ["get_user_full_name"]


# FULL_NAME_ATTRIBUTES = {
#     "fr": "Nom complet",
#     "en": "Full name",
# }


def get_user_full_name() -> str:
    print_log(f"Trying to get user full name to set it as author in Header sheet...")
    if sys.platform != "win32":
        print_log(f"\tPlatform OS is not Windows, unable to find the user name.")
        return ""
    # full_name = None
    # for language, full_name_attr in FULL_NAME_ATTRIBUTES.items():
    #     cmd = cmd_to_get_full_name(full_name_attr)
    #     out = catch_output_cmd(cmd, do_print=True)
    #     if out:
    #         full_name = out
    #         break
    full_name = get_display_name()
    if not full_name:
        print_log(f"\tUnable to find the user name.")
        return ""
    print_log(f"\tFound user name is {Color.default}\"{full_name}\"{Color.reset}.")
    if "(" in full_name:
        full_name = full_name.split("(", 1)[0].strip()
    if "," in full_name:
        full_name = " ".join(reversed(full_name.split(",", 1))).strip()
    return full_name


# def cmd_to_get_full_name(full_name_attr: str) -> str:
#     cmd = (f"FOR /f \"tokens=2*\" %n IN (\'net user \"%USERNAME%\" /domain "
#            f"^| findstr /C:\"{full_name_attr}\"\') DO @echo %o")
#     return cmd


def get_display_name():
    """Get user’s display name using ctypes
    from https://sjohannes.wordpress.com/2010/06/19/win32-python-getting-users-display-name-using-ctypes/"""
    # Function that 'retrieves the name of the user or other security principal associated with the calling thread.'
    # from https://learn.microsoft.com/en-us/windows/win32/api/secext/nf-secext-getusernameexw
    get_user_name_ex = ctypes.windll.secur32.GetUserNameExW
    # Value for the NameDisplay: 'a "friendly" display name (for example, Jeff Smith).'
    # from https://learn.microsoft.com/en-us/windows/win32/api/secext/ne-secext-extended_name_format
    name_display = 3
    # Find the required buffer size
    size = ctypes.pointer(ctypes.c_ulong(0))
    get_user_name_ex(name_display, None, size)
    # Fill the actual buffer
    name_buffer = ctypes.create_unicode_buffer(size.contents.value)
    get_user_name_ex(name_display, name_buffer, size)
    return name_buffer.value
