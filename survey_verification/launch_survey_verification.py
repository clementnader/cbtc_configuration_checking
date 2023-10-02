# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append("..")

from prj.src import *


def main():
    exec_file_full_path = get_full_path(__file__, "_survey_verif.py")
    regen_cctool_oo_schema_wrapper(exec_file_full_path)


if __name__ == "__main__":
    main()
