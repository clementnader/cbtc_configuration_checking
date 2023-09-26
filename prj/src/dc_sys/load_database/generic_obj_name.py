#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...cctool_oo_schema import *


__all__ = ["GENERIC_OBJ_NAME"]


# These sheets do not have a key column, so we use a generic name for the different objects
GENERIC_OBJ_NAME = {
    "Flux_Variant_HF": {"cols": [
        DCSYS.Flux_Variant_HF.Nom,
        DCSYS.Flux_Variant_HF.Troncon,
    ]},
    "Flux_Variant_BF": {"cols": [
        DCSYS.Flux_Variant_BF.Nom,
        DCSYS.Flux_Variant_BF.Troncon,
    ]},
    "Calib": {"cols": [
        DCSYS.Calib.BaliseDeb,
        DCSYS.Calib.BaliseFin,
    ]},
    "ZLPV": {"cols": [
        DCSYS.ZLPV.De.Voie,
        DCSYS.ZLPV.De.Pk,
        DCSYS.ZLPV.De.Seg,
        DCSYS.ZLPV.De.X,
    ]},
    "Profil": {"cols": [
        DCSYS.Profil.Voie,
        DCSYS.Profil.Pk,
        DCSYS.Profil.Seg,
        DCSYS.Profil.X,
    ]},
    "Traction_Profiles": {"cols": [
        DCSYS.Traction_Profiles.TrainType
        if "TrainType" in get_sheet_attributes_columns_dict(DCSYS.Traction_Profiles)
        else DCSYS.Traction_Profiles.TrainConsist,
        DCSYS.Traction_Profiles.Speed,
    ]},
}
