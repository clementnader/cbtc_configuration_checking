#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
from ..utils import *
from ..database_location import *


__all__ = ["generate_cc_parameters_diff_reports"]


def generate_cc_parameters_diff_reports():
    kit_c11 = DATABASE_LOCATION.kit_c11_dir
    kit_c11_sp = DATABASE_LOCATION.kit_c11_sp_dir
    if not kit_c11:
        print_error("C11 kit is not filled.")
        return
    if not kit_c11_sp:
        print_error("C11 Service Pack kit is not filled.")
        return
    _generate_c11_kit_diff(kit_c11, kit_c11_sp)


def _generate_c11_kit_diff(kit_c11: str, kit_c11_sp: str):
    script_file = _generate_bcomp_script(kit_c11, kit_c11_sp)
    _generate_cc_parameter_diff(kit_c11, kit_c11_sp, script_file)


def _generate_bcomp_script(kit_c11: str, kit_c11_sp: str) -> str:
    kit_c11_name = os.path.split(kit_c11)[-1]
    kit_c11_sp_name = os.path.split(kit_c11_sp)[-1]
    script = f"""criteria rules-based
load "%1" "%2"
filter "CCParameter.csv"
expand all
select all
data-report layout:side-by-side &
options:display-mismatches &
title:"Difference Report between {kit_c11_name} and {kit_c11_sp_name} - CCParameter files" &
output-to:printer &
output-options:print-color,print-landscape
"""

    script_file = "beyond_compare_script.txt"
    with open(script_file, "w") as f:
        f.write(script)
    return os.path.realpath(script_file)


def _generate_cc_parameter_diff(kit_c11: str, kit_c11_sp: str, script_file: str):
    if BEYOND_COMPARE_PATH is None:
        print_error(f"\nBeyond Compare 4 is not installed.")
        return

    kit_c11_name = os.path.split(kit_c11)[-1]
    kit_c11_sp_name = os.path.split(kit_c11_sp)[-1]

    print_log(f"Set default printer to save to pdf...")
    cmd = "RUNDLL32 PRINTUI.DLL,PrintUIEntry /y /n \"Microsoft Print to PDF\""
    launch_cmd(cmd)

    print_section_title(f"Launching Beyond Compare 4 Script Comparison between {kit_c11_name} and {kit_c11_sp_name} "
                        f"CCParameter files...")
    subprocess.call(f"{BCOMP_EXE} @\"{script_file}\" \"{kit_c11}\" \"{kit_c11_sp}\"",
                    cwd=BEYOND_COMPARE_PATH, shell=True)

    os.remove(script_file)
