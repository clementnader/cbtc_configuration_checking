# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from src import *


def main():
    exec_file_full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_survey_verif.py")
    regen_cctool_oo_schema_wrapper(exec_file_full_path)


if __name__ == "__main__":
    main()
