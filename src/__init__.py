#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .additional_verif import *
from .cc_param import *
from .cctool_oo_schema import *
from .constraints import *
from .control_tables import *
from .dc_par import *
from .dc_sys import *
from .utils import *
from .zc import *

# Initialization commands
create_cctool_oo_schema_info_file()  # regenerate the CCTOOL-OO Schema Info file to match the current version
