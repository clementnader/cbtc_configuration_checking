#!/usr/bin/env python
# -*- coding: utf-8 -*-

# class SheetsInfo:
#     seg = {"sh_name": "Seg", "cols": ['G', 'H', 'I', 'J', 'K']}
#     sw = {"sh_name": "Aig", "cols": ['B', 'C', 'D']}
#     tag = {"sh_name": "Bal", "cols": ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']}
#     calib = {"sh_name": "Calib", "cols": ['A', 'B', 'C', 'D'], "generic_obj_name": True}
#     zlpv = {"sh_name": "ZLPV", "cols": ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
#             "generic_obj_name": True}
#     plt = {"sh_name": "Quai", "cols": ['I', 'J', 'Q', 'R', 'Y', 'AA', 'AB', 'AD', 'AI', 'AK', 'AL', 'AN',
#                                         'AS', 'AU', 'AV', 'AX']}
#     block = {"sh_name": "CDV", "lim_start_col": 'N', "nb_max_limits": 15, "delta_between_limits": 2}
#     vb = {"sh_name": "CV", "lim_start_col": 'B', "nb_max_limits": 3, "delta_between_limits": 2}
#     sig = {"sh_name": "Sig", "cols": ['B', 'C', 'D', 'E', 'I', 'S', 'Z']}
#     slope = {"sh_name": "Profil", "cols": ['A', 'B', 'C', 'D', 'E'], "generic_obj_name": True}
#     cbtc_ter = {"sh_name": "CBTC_TER", "cols": ['B'],
#                 "lim_start_col": 'I', "nb_max_limits": 15, "delta_between_limits": 3}
#     zc_area = {"sh_name": "PAS", "lim_start_col": 'D', "nb_max_limits": 30, "delta_between_limits": 6}
#     zsm = {"sh_name": "ZSM_CBTC", "cols": ['D', 'E', 'H', 'I']}
#     hf_data = {"sh_name": "Flux_Variant_HF", "cols": ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']}
#     lf_data = {"sh_name": "Flux_Variant_BF", "cols": ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']}
#     tag_gr = {"sh_name": "StaticTag_Group", "lim_start_col": 'C', "nb_max_limits": 10, "delta_between_limits": 1}


SHEETS_INFO = {
    "seg": {"sh_name": "Seg", "cols": ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']},
    "sw": {"sh_name": "Aig", "cols": ['B', 'C', 'D']},
    "tag": {"sh_name": "Bal", "cols": ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']},
    "calib": {"sh_name": "Calib", "cols": ['A', 'B', 'C', 'D'], "generic_obj_name": True},
    "zlpv": {"sh_name": "ZLPV", "cols": ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
             "generic_obj_name": True},
    "plt": {"sh_name": "Quai", "cols": ['I', 'J', 'Q', 'R', 'Y', 'AA', 'AB', 'AD', 'AI', 'AK', 'AL', 'AN',
                                        'AS', 'AU', 'AV', 'AX']},
    "block": {"sh_name": "CDV", "lim_start_col": 'N', "nb_max_limits": 15, "delta_between_limits": 2},
    "vb": {"sh_name": "CV", "lim_start_col": 'B', "nb_max_limits": 3, "delta_between_limits": 2},
    "sig": {"sh_name": "Sig", "cols": ['B', 'C', 'D', 'E', 'I', 'S', 'Z']},
    "slope": {"sh_name": "Profil", "cols": ['A', 'B', 'C', 'D', 'E'], "generic_obj_name": True},
    "cbtc_ter": {"sh_name": "CBTC_TER", "cols": ['B'],
                 "lim_start_col": 'I', "nb_max_limits": 15, "delta_between_limits": 3},
    "zc_area": {"sh_name": "PAS", "lim_start_col": 'D', "nb_max_limits": 30, "delta_between_limits": 6},
    "zsm": {"sh_name": "ZSM_CBTC", "cols": ['D', 'E', 'H', 'I']},
    "hf_data": {"sh_name": "Flux_Variant_HF", "cols": ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']},
    "lf_data": {"sh_name": "Flux_Variant_BF", "cols": ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']},
    "tag_gr": {"sh_name": "StaticTag_Group", "lim_start_col": 'C', "nb_max_limits": 10, "delta_between_limits": 1},
}


# TODO get these infos from CCTOOL-OO Schema
# et changer l'utilisation des numéros de colonnes par les objets de la FDS en repassant par le CCTOOL-OO Schema
