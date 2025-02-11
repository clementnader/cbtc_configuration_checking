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
ORDERED_ORIGINAL_FILE = "_ordered".join(os.path.splitext(ORIGINAL_FILE))
REGEN_FILE = "RAMSmd5sum.txt"
BASH_CMD = f"find -type f | sort -f | xargs -d \"\\n\" md5sum -t > \"{REGEN_FILE}\""
SORT_BASH_CMD = f"sort -k2f \"{ORIGINAL_FILE}\" > \"{ORDERED_ORIGINAL_FILE}\""


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


def regen_checksum_and_sort_old(path_kit_c11):
    if sys.platform == "win32" and "SHELL" not in os.environ.keys():  # For Windows when not using git-bash
        if GIT_PATH is None:
            print_error(f"\nGit is not installed.")
            print(f"The command:\n"
                  f"\t{Color.light_orange}{BASH_CMD}{Color.reset}\n"
                  f"needs to be launched on your side.")
            return
        new_env = {"PATH": os.path.join(GIT_PATH, "usr", "bin"), "LC_ALL": "C"}
    else:
        new_env = {"LC_ALL": "C"}
    print_section_title(f"Generating MD5 checksums in file \"{REGEN_FILE}\"...")
    launch_cmd(BASH_CMD, cwd=path_kit_c11, env=new_env)
    print_section_title(f"Sorting existing MD5 checksum \"{ORIGINAL_FILE}\" into file \"{ORDERED_ORIGINAL_FILE}\" "
                        f"to do the comparison...")
    launch_cmd(SORT_BASH_CMD, cwd=path_kit_c11, env=new_env)


def launch_beyond_compare(ordered_original, ordered_regen):
    if BEYOND_COMPARE_PATH is None:
        print_error(f"\nBeyond Compare 4 is not installed.")
        return
    print_section_title(f"Launching Beyond Compare 4...")
    subprocess.Popen(f"{BCOMP_EXE} \"{ordered_original}\" \"{ordered_regen}\"", cwd=BEYOND_COMPARE_PATH, shell=True)


def compare_checksums(path_kit_c11):
    print_title(f"Verification of the Delivery Chain MD5 Checksum\n")
    regen_checksum_and_sort_old(path_kit_c11)
    ordered_original = os.path.join(path_kit_c11, ORDERED_ORIGINAL_FILE)
    if not os.path.exists(os.path.join(path_kit_c11, REGEN_FILE)):
        print_error(f"\nCannot find the regenerated file.")
        return
    ordered_regen = os.path.join(path_kit_c11, REGEN_FILE)
    print(f"\nThe files to compare are located:\n"
          f"\tfor the original file: {Color.light_green}{ordered_original}{Color.reset}\n"
          f"\tand for the regenerated file: {Color.light_green}{ordered_regen}{Color.reset}")
    launch_beyond_compare(ordered_original, ordered_regen)
