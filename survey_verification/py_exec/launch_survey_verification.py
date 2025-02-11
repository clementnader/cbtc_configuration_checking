# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join("..", ".."))

from prj.src import *


def main():
    log_file_name = f"survey_log_{get_timestamp()}.log"
    file_to_launch_full_address = get_full_path(__file__, "_survey_verif.py")
    with open(os.path.join("..", log_file_name), "w", encoding="utf-8") as log_file:
        sys.stdout = Logger(log_file)
        regen_cctool_oo_schema_wrapper(file_to_launch_full_address, log_file_instance=log_file,
                                       log_file_name=log_file_name)


if __name__ == "__main__":
    main()
