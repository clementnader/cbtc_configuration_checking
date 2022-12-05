#!/usr/bin/env python
# -*- coding: utf-8 -*-

SHEETS_INFO = {
    "zsm": {"sh_name": "ZSM_CBTC", "cols": ['D', 'E', 'H', 'I']},
    "seg": {"sh_name": "Seg", "cols": ['G', 'H', 'I', 'J', 'K']},
    "sw": {"sh_name": "Aig", "cols": ['B', 'C', 'D']},
    "plt": {"sh_name": "Quai", "cols": ['I', 'J', 'Q', 'R', 'Y', 'AA', 'AB', 'AD', 'AI', 'AK', 'AL', 'AN',
                                        'AS', 'AU', 'AV', 'AX']},
    "tag": {"sh_name": "Bal", "cols": ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']},
    "tag_gr": {"sh_name": "StaticTag_Group", "lim_start_col": 'C', "nb_max_limits": 10, "delta_between_limits": 1},
    "sig": {"sh_name": "Sig", "cols": ['B', 'C', 'D', 'E', 'I', 'S', 'Z']},
    "cbtc_ter": {"sh_name": "CBTC_TER", "cols": ['B'],
                 "lim_start_col": 'I', "nb_max_limits": 15, "delta_between_limits": 3},
    "vb": {"sh_name": "CV", "lim_start_col": 'B', "nb_max_limits": 3, "delta_between_limits": 2},
    "zc_area": {"sh_name": "PAS", "lim_start_col": 'D', "nb_max_limits": 30, "delta_between_limits": 6},
    "slope": {"sh_name": "Profil", "cols": ['A', 'B', 'C', 'D', 'E'], "name_col": 'F'},
    "zlpv": {"sh_name": "ZLPV", "cols": ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'], "name_col": 'L'},
    "calib": {"sh_name": "Calib", "cols": ['A', 'B', 'C', 'D'], "name_col": 'E'},
    "hf_data": {"sh_name": "Flux_Variant_HF", "cols": ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']},
    "lf_data": {"sh_name": "Flux_Variant_BF", "cols": ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']},
}
