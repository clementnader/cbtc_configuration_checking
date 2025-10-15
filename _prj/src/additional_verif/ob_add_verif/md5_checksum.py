#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from ...utils import *
from ...database_location import *


__all__ = ["verification_of_the_cc_kit_md5_checksum"]


def _checksum_bash_cmd(checksum: str, regen_file: str):
    return f"find -type f | sort -f | xargs -d \"\\n\" {checksum} -t > \"{regen_file}\""
# The command lists every file, sorts the list, and for each one of them executes the md5sum command.
# "-type f" option in the find lists all files inside the current directory (including at deeper levels).
# "-f" option in the sort allows the sort to be case-insensitive.
# '-d "\n"' option in the xargs specifies the delimiter to be a line feed \n, else it will split at all spaces
# and not work when a file possesses spaces in its name.
# "-t" option in the md5sum is to read in text mode (and not in binary mode).


def _sort_bash_cmd(original_file: str, ordered_original_file: str):
    return f"sort -k2f \"{original_file}\" > \"{ordered_original_file}\""
# The command sorts the file the same way so that we can compare the original md5sum file and the re-generated one.
# "-k2" option is to sort according to the second argument (after the space symbol separating the checksum
# and the file name) so that we sort according to the file name.
# "-f" option allows the sort to be case-insensitive.


def verification_of_the_cc_kit_md5_checksum(sha256: bool = False):
    checksum_type = "SHA256" if sha256 else "MD5"
    checksum = "sha256sum" if sha256 else "md5sum"
    path_kit_c11 = DATABASE_LOCATION.kit_c11_dir
    print_title(f"Verification of the Delivery Chain {checksum_type} Checksum of CC kit"
                f"\n{Color.cyan}{path_kit_c11}{Color.reset}")

    original_file = f"{checksum}.txt"
    ordered_original_file = f"{checksum}_ordered.txt"
    regen_file = f"RAMS{checksum}.txt"

    _regen_checksum_and_sort_old(path_kit_c11, checksum_type, checksum, original_file, ordered_original_file,
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


def _regen_checksum_and_sort_old(path_kit_c11: str, checksum_type: str, checksum: str, original_file: str,
                                 ordered_original_file: str, regen_file: str) -> None:
    checksum_bash_cmd = _checksum_bash_cmd(checksum, regen_file)
    sort_bash_cmd = _sort_bash_cmd(original_file, ordered_original_file)

    if sys.platform == "win32" and "SHELL" not in os.environ.keys():  # for Windows when not using git-bash
        # We add to the path Git/usr/bin so to be able to use the UNIX commands.
        if GIT_PATH is None:
            print_error(f"\nGit is not installed.")
            print(f"The command:\n"
                  f"\t{Color.light_orange}{checksum_bash_cmd}{Color.reset}\n"
                  f"needs to be launched on your side.")
            return
        new_env = {"PATH": os.path.join(GIT_PATH, "usr", "bin"), "LC_ALL": "C"}

    else: # already a UNIX environment
        new_env = {"LC_ALL": "C"}
    # LC_ALL defines the value for all language categories.
    # LC_ALL=C allows to have the same sorting behavior on every computer (whatever OS and language they are in).
    # In the C locale (or POSIX locale), characters are single bytes and the sorting order is based on the byte values.

    print_section_title(f"Generating {checksum_type} checksums in file \"{regen_file}\"...")
    launch_cmd(checksum_bash_cmd, cwd=path_kit_c11, env=new_env)
    print_section_title(f"Sorting existing {checksum_type} checksum \"{original_file}\" into file "
                        f"\"{ordered_original_file}\" to do the comparison...")
    launch_cmd(sort_bash_cmd, cwd=path_kit_c11, env=new_env)


def _launch_beyond_compare(ordered_original: str, regen_file: str) -> None:
    if BEYOND_COMPARE_PATH is None:
        print_error(f"\nBeyond Compare 4 is not installed.")
        return
    print_section_title(f"Launching Beyond Compare 4...")
    subprocess.Popen(f"{BCOMP_EXE} \"{ordered_original}\" \"{regen_file}\"", cwd=BEYOND_COMPARE_PATH, shell=True)
