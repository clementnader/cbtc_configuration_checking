#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import argparse
from ..utils import *
from ..database_location import *


__all__ = ["verification_of_the_md5_checksum", "checksum_compare_parser"]


ORIGINAL_FILE = "md5sum.txt"
REGEN_FILE = "md5sum_regenerated.txt"
BASH_CMD = f"find -type f -print0 | sort | xargs -r0 md5sum > \"{REGEN_FILE}\""


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


def verification_of_the_md5_checksum():
    kit_c11 = DATABASE_LOC.kit_c11_dir
    compare_checksums(kit_c11)


def checksum_compare_parser():
    parser = argparse.ArgumentParser(
        add_help=True,
        description=f"Regenerate using Git-Bash the MD5 checksum file to compare it to the original checksum file.",
    )
    parser.add_argument("-i", "--input_kit_c11_dir", dest="input_dir", action="store", type=str, required=True,
                        metavar=f"{Color.turquoise}Kit_C11_D470{Color.reset}",
                        help=f"path to the kit C11_D470 folder "
                             f"{Color.dark_grey}(put it between quotes){Color.reset}")
    args = vars(parser.parse_args())
    input_dir = args["input_dir"]
    compare_checksums(input_dir)


def regen_checksum(path_kit_c11):
    if sys.platform == "win32" and "SHELL" not in os.environ.keys():  # For Windows when not using git-bash
        if GIT_PATH is None:
            print_error(f"\nGit is not installed.")
            print(f"The command:\n"
                  f"\t{Color.light_orange}{BASH_CMD}{Color.reset}\n"
                  f"needs to be launched on your side.")
            return
        new_env = {"PATH": os.path.join(GIT_PATH, "usr", "bin")}
    else:
        new_env = None
    print_section_title(f"Generating MD5 checksums in file \"{REGEN_FILE}\"...")
    launch_cmd(BASH_CMD, cwd=path_kit_c11, env=new_env)


def sort_md5_lines(lines: list[str]):
    return sorted(lines, key=lambda x: x.split(" ", 1)[1].casefold())


def order_original_checksum(path_kit_c11):
    print_section_title(f"Reordering the original checksum file to be able to do the comparison...")
    original_file_path = os.path.join(path_kit_c11, ORIGINAL_FILE)
    with open(original_file_path, 'r') as og_file:
        lines = sort_md5_lines(og_file.readlines())
        ordered_original = os.path.join(path_kit_c11, "_ordered".join(os.path.splitext(ORIGINAL_FILE)))
        with open(ordered_original, 'w') as new_file:
            new_file.writelines(lines)
            return ordered_original


def order_regen_checksum(path_kit_c11):
    print_section_title(f"Reordering the regenerated checksum file to be able to do the comparison...")
    regen_file_path = os.path.join(path_kit_c11, REGEN_FILE)
    with open(regen_file_path, 'r') as og_file:
        lines = sort_md5_lines(og_file.readlines())
        for i, line in enumerate(lines):
            lines[i] = line.replace(" *./", "  ./")
        ordered_regen = os.path.join(path_kit_c11, "_ordered".join(os.path.splitext(REGEN_FILE)))
        with open(ordered_regen, 'w') as new_file:
            new_file.writelines(lines)
            return ordered_regen


def launch_beyond_compare(ordered_original, ordered_regen):
    if BEYOND_COMPARE_PATH is None:
        print_error(f"\nBeyond Compare 4 is not installed.")
        return
    print_section_title(f"Launching Beyond Compare 4...")
    subprocess.Popen(f"{BCOMP_EXE} \"{ordered_original}\" \"{ordered_regen}\"", cwd=BEYOND_COMPARE_PATH, shell=True)


def compare_checksums(path_kit_c11):
    print_title(f"Verification of the Delivery Chain MD5 Checksum\n")
    regen_checksum(path_kit_c11)
    ordered_original = order_original_checksum(path_kit_c11)
    if not os.path.exists(os.path.join(path_kit_c11, REGEN_FILE)):
        print_error(f"\nCannot find the regenerated file.")
        return
    ordered_regen = order_regen_checksum(path_kit_c11)
    print(f"\nThe files to compare are located:\n"
          f"\tfor the original file: {Color.light_green}{ordered_original}{Color.reset}\n"
          f"\tand for the regenerated file: {Color.light_green}{ordered_regen}{Color.reset}")
    launch_beyond_compare(ordered_original, ordered_regen)
