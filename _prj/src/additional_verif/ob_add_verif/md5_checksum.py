#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from ...utils import *
from ...database_location import *


__all__ = ["verification_of_the_md5_checksum"]


ORIGINAL_FILE = "md5sum.txt"
ORIGINAL_FILE2 = "sha256sum.txt"
ORDERED_ORIGINAL_FILE = "_ordered".join(os.path.splitext(ORIGINAL_FILE))
ORDERED_ORIGINAL_FILE2 = "_ordered".join(os.path.splitext(ORIGINAL_FILE2))
REGEN_FILE = "RAMSmd5sum.txt"
REGEN_FILE2 = "RAMSsha256sum.txt"
BASH_CMD = f"find -type f | sort -f | xargs -d \"\\n\" md5sum -t > \"{REGEN_FILE}\""
BASH_CMD2 = f"find -type f | sort -f | xargs -d \"\\n\" sha256sum -t > \"{REGEN_FILE2}\""
# The command lists every file, sorts the list, and for each one of them executes the md5sum command.
# "-type f" option in the find lists all files inside the current directory (including at deeper levels).
# "-f" option in the sort allows the sort to be case-insensitive.
# '-d "\n"' option in the xargs specifies the delimiter to be a line feed \n, else it will split at all spaces
# and not work when a file possesses spaces in its name.
# "-t" option in the md5sum is to read in text mode (and not in binary mode).
SORT_BASH_CMD = f"sort -k2f \"{ORIGINAL_FILE}\" > \"{ORDERED_ORIGINAL_FILE}\""
SORT_BASH_CMD2 = f"sort -k2f \"{ORIGINAL_FILE2}\" > \"{ORDERED_ORIGINAL_FILE2}\""
# The command sorts the file the same way so that we can compare the original md5sum file and the re-generated one.
# "-k2" option is to sort according to the second argument (after the space symbol separating the checksum
# and the file name) so that we sort according to the file name.
# "-f" option allows the sort to be case-insensitive.


def verification_of_the_md5_checksum(sha256: bool = False):
    path_kit_c11 = DATABASE_LOC.kit_c11_dir
    print_title(f"Verification of the Delivery Chain {'SHA256' if sha256 else 'MD5'} Checksum\n")

    bash_cmd = BASH_CMD2 if sha256 else BASH_CMD
    sort_bash_cmd = SORT_BASH_CMD2 if sha256 else SORT_BASH_CMD
    original_file = ORIGINAL_FILE2 if sha256 else ORIGINAL_FILE
    ordered_original_file = ORDERED_ORIGINAL_FILE2 if sha256 else ORDERED_ORIGINAL_FILE
    regen_file = REGEN_FILE2 if sha256 else REGEN_FILE

    _regen_checksum_and_sort_old(path_kit_c11, bash_cmd, sort_bash_cmd, original_file, ordered_original_file,
                                 regen_file)
    ordered_original = os.path.join(path_kit_c11, ordered_original_file)
    regen_file = os.path.join(path_kit_c11, regen_file)
    if not os.path.exists(regen_file):
        print_error(f"\nCannot find the regenerated file.")
        return
    print(f"\nThe files to compare are located:\n"
          f"\tfor the ordered original file: {Color.light_green}{ordered_original}{Color.reset}\n"
          f"\tand for the regenerated file: {Color.light_green}{regen_file}{Color.reset}")
    _launch_beyond_compare(ordered_original, regen_file)


def _regen_checksum_and_sort_old(path_kit_c11: str, bash_cmd: str, sort_bash_cmd: str, original_file: str,
                                 ordered_original_file: str, regen_file: str) -> None:
    if sys.platform == "win32" and "SHELL" not in os.environ.keys():  # for Windows when not using git-bash
        # We add to the path Git/usr/bin so to be able to use the UNIX commands.
        if GIT_PATH is None:
            print_error(f"\nGit is not installed.")
            print(f"The command:\n"
                  f"\t{Color.light_orange}{bash_cmd}{Color.reset}\n"
                  f"needs to be launched on your side.")
            return
        new_env = {"PATH": os.path.join(GIT_PATH, "usr", "bin"), "LC_ALL": "C"}
    else: # already a UNIX environment
        new_env = {"LC_ALL": "C"}
    # LC_ALL defines the value for all language categories.
    # LC_ALL=C allows to have the same sorting behavior on every computer (whatever OS and language they are in).
    # In the C locale (or POSIX locale), characters are single bytes and the sorting order is based on the byte values.

    print_section_title(f"Generating SHA256 checksums in file \"{regen_file}\"...")
    launch_cmd(bash_cmd, cwd=path_kit_c11, env=new_env)
    print_section_title(f"Sorting existing SHA256 checksum \"{original_file}\" into file \"{ordered_original_file}\" "
                        f"to do the comparison...")
    launch_cmd(sort_bash_cmd, cwd=path_kit_c11, env=new_env)


def _launch_beyond_compare(ordered_original: str, regen_file: str) -> None:
    if BEYOND_COMPARE_PATH is None:
        print_error(f"\nBeyond Compare 4 is not installed.")
        return
    print_section_title(f"Launching Beyond Compare 4...")
    subprocess.Popen(f"{BCOMP_EXE} \"{ordered_original}\" \"{regen_file}\"", cwd=BEYOND_COMPARE_PATH, shell=True)
