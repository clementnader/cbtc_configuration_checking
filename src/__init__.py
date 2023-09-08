#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .additional_verif import *
from .cc_mtor_ccte import *
from .cc_param import *
from .cctool_oo_schema import *
from .control_tables import *
from .dc_bop import *
from .dc_par import *
from .dc_sys import *
from .foundation_data_constraints import *
from .parameters_constraints import *
from .survey import *
from .utils import *
from .zc import *
from .database_location import *


# Initialization commands
print_title(f"The working project is {Color.green2}{PROJECT_NAME}{Color.reset}\n"
            f"{Color.cyan}{get_c_d470_version()}{Color.reset}\n"
            f"with CCTool-OO Core CBTC version {Color.pale_green}{get_ga_version()}{Color.reset}.")
create_cctool_oo_schema_info_file()  # regenerate the CCTOOL-OO Schema Info file to match the current version
