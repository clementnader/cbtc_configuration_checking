#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .additional_verif import *
from .cc_param import *
from .cctool_oo_schema import *
from .constraints import *
from .control_tables import *
from .d932 import *
from .dc_par import *
from .dc_sys import *
from .patch_cc_mtor_ccte import *
from .utils import *
from .zc import *
from .database_loc import PROJECT_NAME

# Initialization commands
print_title(f"The working project is {Color.vivid_green}{PROJECT_NAME}{Color.reset}\n"
            f"with CCTool-OO Core CBTC version {Color.beige}{get_version()}{Color.reset}.")
create_cctool_oo_schema_info_file()  # regenerate the CCTOOL-OO Schema Info file to match the current version
