#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from ..utils import *
from ..database_location import *


__all__ = ["verification_of_the_md5_checksum"]


ORIGINAL_FILE = "md5sum.txt"
ORDERED_ORIGINAL_FILE = "_ordered".join(os.path.splitext(ORIGINAL_FILE))
REGEN_FILE = "RAMSmd5sum.txt"
BASH_CMD = f"find -type f | sort -f | xargs -d \"\\n\" md5sum -t > \"{REGEN_FILE}\""
# The command lists every file, sorts the list, and for each one of them executes the md5sum command.
# "-type f" option in the find lists all files inside the current directory (including at deeper levels).
# "-f" option in the sort allows the sort to be case-insensitive.
# '-d "\n"' option in the xargs specifies the delimiter to be a line feed \n, else it will split at all spaces
# and not work when a file possesses spaces in its name.
# "-t" option in the md5sum is to read in text mode (and not in binary mode).
SORT_BASH_CMD = f"sort -k2f \"{ORIGINAL_FILE}\" > \"{ORDERED_ORIGINAL_FILE}\""
# The command sorts the file the same way so that we can compare the original md5sum file and the re-generated one.
# "-k2" option is to sort according to the second argument (after the space symbol separating the checksum
# and the file name) so that we sort according to the file name.
# "-f" option allows the sort to be case-insensitive.


def verification_of_the_md5_checksum():
    path_kit_c11 = DATABASE_LOC.kit_c11_dir
    print_title(f"Verification of the Delivery Chain MD5 Checksum\n")

    _regen_checksum_and_sort_old(path_kit_c11)
    ordered_original = os.path.join(path_kit_c11, ORDERED_ORIGINAL_FILE)
    if not os.path.exists(os.path.join(path_kit_c11, REGEN_FILE)):
        print_error(f"\nCannot find the regenerated file.")
        return
    regen_file = os.path.join(path_kit_c11, REGEN_FILE)
    print(f"\nThe files to compare are located:\n"
          f"\tfor the original file: {Color.light_green}{ordered_original}{Color.reset}\n"
          f"\tand for the regenerated file: {Color.light_green}{regen_file}{Color.reset}")
    _launch_beyond_compare(ordered_original, regen_file)


def _regen_checksum_and_sort_old(path_kit_c11: str):
    if sys.platform == "win32" and "SHELL" not in os.environ.keys():  # for Windows when not using git-bash
        # We add to the path Git/usr/bin so to be able to use the UNIX commands.
        if GIT_PATH is None:
            print_error(f"\nGit is not installed.")
            print(f"The command:\n"
                  f"\t{Color.light_orange}{BASH_CMD}{Color.reset}\n"
                  f"needs to be launched on your side.")
            return
        new_env = {"PATH": os.path.join(GIT_PATH, "usr", "bin"), "LC_ALL": "C"}
    else: # already a UNIX environment
        new_env = {"LC_ALL": "C"}
    # LC_ALL defines the value for all language categories.
    # LC_ALL=C allows to have the same sorting behavior on every computer (whatever OS and language they are in).
    # In the C locale (or POSIX locale), characters are single bytes and the sorting order is based on the byte values.

    print_section_title(f"Generating MD5 checksums in file \"{REGEN_FILE}\"...")
    launch_cmd(BASH_CMD, cwd=path_kit_c11, env=new_env)
    print_section_title(f"Sorting existing MD5 checksum \"{ORIGINAL_FILE}\" into file \"{ORDERED_ORIGINAL_FILE}\" "
                        f"to do the comparison...")
    launch_cmd(SORT_BASH_CMD, cwd=path_kit_c11, env=new_env)


def _launch_beyond_compare(ordered_original: str, regen_file: str):
    if BEYOND_COMPARE_PATH is None:
        print_error(f"\nBeyond Compare 4 is not installed.")
        return
    print_section_title(f"Launching Beyond Compare 4...")
    subprocess.Popen(f"{BCOMP_EXE} \"{ordered_original}\" \"{regen_file}\"", cwd=BEYOND_COMPARE_PATH, shell=True)
