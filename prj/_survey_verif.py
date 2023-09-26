#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from src import *


def main():
    print_title(f"Survey Verification", color=Color.mint_green)
    print(f"{Color.light_green}Select the DC_SYS and the Survey information to verify.{Color.reset}\n")
    survey_window()
    print_title(f"Analyzing the survey information for "
                f"{Color.cyan}{os.path.split(os.path.split(DATABASE_LOC.dc_sys_addr)[0])[-1]}{Color.reset}.")
    check_survey()


if __name__ == "__main__":
    main()
