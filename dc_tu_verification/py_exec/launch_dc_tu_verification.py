#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join("..", ".."))

from prj.src import *


def main():
    log_file_name = f"dc_tu_log_{get_timestamp()}.log"
    with open(os.path.join("..", log_file_name), "w", encoding="utf-8") as log_file:
        sys.stdout = Logger(log_file)
        os.chdir("..")
        dc_tu_window()


if __name__ == "__main__":
    main()
