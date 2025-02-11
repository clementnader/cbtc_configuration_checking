#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join("..", ".."))

from prj.src import *


def main():
    log_file_name = get_log_file_sub_python()
    with open(os.path.join("..", log_file_name), "a", encoding="utf-8") as log_file:
        sys.stdout = Logger(log_file)
        os.chdir("..")
        survey_window()


if __name__ == "__main__":
    main()
