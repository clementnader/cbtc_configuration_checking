# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join("..", ".."))

from prj.src import *


def main():
    file_to_launch_full_address = get_full_path(__file__, "_survey_verif.py")
    regen_cctool_oo_schema_wrapper(file_to_launch_full_address)


if __name__ == "__main__":
    main()
