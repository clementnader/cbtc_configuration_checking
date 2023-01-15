#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import argparse
from ..colors_pkg import *

ORIGINAL_FILE = "md5sum.txt"
REGEN_FILE = "Appendix C_MD5 Checksum of the files analysed.txt"

BASH_CMD = f"find . | sort | xargs md5sum > \"{REGEN_FILE}\""


def get_software_location(sw):
    software_paths = {
        "local_app_data": os.path.join(os.getenv("LocalAppData"), sw),
        "local_app_data_programs": os.path.join(os.getenv("LocalAppData"), "Programs", sw),
        "program_files": os.path.join(os.getenv("ProgramFiles"), sw),
        "program_files_x86": os.path.join(os.getenv("ProgramFiles(x86)"), sw),
    }

    for sw_path in software_paths.values():
        if os.path.exists(sw_path):
            return sw_path
    return None


GIT_PATH = get_software_location("Git")
BEYOND_COMPARE_PATH = get_software_location("Beyond Compare 4")
BCOMP_EXE = "BCompare.exe"


def checksum_compare_parser():
    parser = argparse.ArgumentParser(
        add_help=True,
        description=f"Regenerate using Git-Bash the MD5 checksum file to compare it to the original checksum file.",
    )
    parser.add_argument("-i", "--input_kit_c11_dir", dest="input_dir", action="store", type=str, required=True,
                        metavar=f"{Color.blue}Kit_C11_D470{Color.reset}",
                        help=f"path to the kit C11_D470 folder "
                             f"{Color.dark_grey}(put it between quotes){Color.reset}")
    args = vars(parser.parse_args())
    input_dir = args["input_dir"]
    compare_checksums(input_dir)


def regen_checksum(path_kit_c11):
    if sys.platform == "win32" and "SHELL" not in os.environ.keys():  # For Windows when not using git-bash
        if GIT_PATH is None:
            print(f"\n{Color.red}Git is not installed{Color.reset}")
            print(f"The command:\n"
                  f"\t{Color.dark_yellow}{BASH_CMD}{Color.reset}\n"
                  f"needs to be launched on your side.")
            return
        new_env = {"PATH": os.path.join(GIT_PATH, 'usr', 'bin')}
    else:
        new_env = None
    print(f"\n{Color.blue}Generating MD5 checksums in file {REGEN_FILE}{Color.reset}")
    print(f"\t> {Color.dark_yellow}{BASH_CMD}{Color.reset}")
    subprocess.call(BASH_CMD, cwd=path_kit_c11, env=new_env, shell=True)


def order_original_checksum(path_kit_c11):
    print(f"\n{Color.blue}Reordering the original checksum file to be able to do the comparison{Color.reset}")
    original_file_path = os.path.join(path_kit_c11, ORIGINAL_FILE)
    with open(original_file_path, 'r') as og_file:
        lines = og_file.readlines()
        lines.sort(key=lambda x: x.split(" ", 1)[1])
        ordered_original = os.path.join(path_kit_c11, "_ordered".join(os.path.splitext(ORIGINAL_FILE)))
        with open(ordered_original, 'w') as new_file:
            new_file.writelines(lines)
            return ordered_original


def order_regen_checksum(path_kit_c11):
    print(f"\n{Color.blue}Reordering the regenerated checksum file to be able to do the comparison{Color.reset}")
    regen_file_path = os.path.join(path_kit_c11, REGEN_FILE)
    with open(regen_file_path, 'r') as og_file:
        lines = og_file.readlines()
        lines.sort(key=lambda x: x.split(" ", 1)[1])
        for i, line in enumerate(lines):
            lines[i] = line.replace(" *./", "  ./")
        ordered_regen = os.path.join(path_kit_c11, "_ordered".join(os.path.splitext(REGEN_FILE)))
        with open(ordered_regen, 'w') as new_file:
            new_file.writelines(lines)
            return ordered_regen


def launch_beyond_compare(ordered_original, ordered_regen):
    if BEYOND_COMPARE_PATH is None:
        print(f"\n{Color.red}Beyond Compare 4 is not installed{Color.reset}")
        return
    print(f"\n{Color.blue}Launching Beyond Compare 4...{Color.reset}")
    subprocess.Popen(f"{BCOMP_EXE} \"{ordered_original}\" \"{ordered_regen}\"", cwd=BEYOND_COMPARE_PATH, shell=True)


def compare_checksums(path_kit_c11):
    print(f"{Color.dark_cyan}{Color.underline}"
          f"Regenerating the MD5 checksum file to compare it to the original checksum file "
          f"to create Appendix C of the OnBoard DPSR{Color.reset}")
    regen_checksum(path_kit_c11)
    ordered_original = order_original_checksum(path_kit_c11)
    if not os.path.exists(os.path.join(path_kit_c11, REGEN_FILE)):
        print(f"\n{Color.red}Cannot find the regenerated file{Color.reset}")
        return
    ordered_regen = order_regen_checksum(path_kit_c11)
    print(f"\nThe files to compare are located:\n"
          f"\tfor the original file: {Color.green}{ordered_original}{Color.reset}\n"
          f"\tand for the regenerated file: {Color.green}{ordered_regen}{Color.reset}")
    launch_beyond_compare(ordered_original, ordered_regen)
