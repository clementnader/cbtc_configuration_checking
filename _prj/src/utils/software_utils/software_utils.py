#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


__all__ = ["get_software_location", "GIT_PATH", "BEYOND_COMPARE_PATH", "BCOMP_EXE"]


def get_software_location(sw):
    software_paths = {
        "local_app_data": os.path.join(os.getenv("LocalAppData"), sw),
        "local_app_data_programs": os.path.join(os.getenv("LocalAppData"), "Programs", sw),
        "program_files": os.path.join(os.getenv("ProgramFiles"), sw),
        "program_files_x86": os.path.join(os.getenv("ProgramFiles(x86)"), sw),
    }

    for sw_path in software_paths.values():
        if os.path.exists(sw_path):
            return sw_path
    return None


GIT_PATH = get_software_location("Git")
BEYOND_COMPARE_PATH = get_software_location("Beyond Compare 4")
BCOMP_EXE = "BCompare.exe"
