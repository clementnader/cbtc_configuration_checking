#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *


__all__ = ["GENERIC_OBJ_NAME"]


# These sheets do not have a key column, so we use a generic name for the different objects
GENERIC_OBJ_NAME = {
    "Flux_Variant_HF": {"cols": [
        {"attr": DCSYS.Flux_Variant_HF.Nom, "type": str},
        {"attr": DCSYS.Flux_Variant_HF.Troncon, "type": str}
    ]},
    "Flux_Variant_BF": {"cols": [
        {"attr": DCSYS.Flux_Variant_BF.Nom, "type": str},
        {"attr": DCSYS.Flux_Variant_BF.Troncon, "type": str}
    ]},
    "Calib": {"cols": [
        {"attr": DCSYS.Calib.DistanceCalib, "type": float},
        {"attr": DCSYS.Calib.BaliseDeb, "type": str},
        {"attr": DCSYS.Calib.BaliseFin, "type": str}
    ]},
    "ZLPV": {"cols": [
        {"attr": DCSYS.ZLPV.De.Voie, "type": str},
        {"attr": DCSYS.ZLPV.De.Pk, "type": float},
        {"attr": DCSYS.ZLPV.De.Seg, "type": str},
        {"attr": DCSYS.ZLPV.De.X, "type": float}
    ]},
    "Profil": {"cols": [
        {"attr": DCSYS.Profil.Voie, "type": str},
        {"attr": DCSYS.Profil.Pk, "type": float},
        {"attr": DCSYS.Profil.Seg, "type": str},
        {"attr": DCSYS.Profil.X, "type": float}
    ]},
    "Traction_Profiles": {"cols": [
        {"attr": DCSYS.Traction_Profiles.TrainType if "TrainType" in get_class_attr_dict(DCSYS.Traction_Profiles)
         else DCSYS.Traction_Profiles.TrainConsist,
         "type": str},
        {"attr": DCSYS.Traction_Profiles.Speed, "type": float}
    ]},
    "PAS": {"cols": [
        {"attr": DCSYS.PAS.TrackingAreaSubsetName, "type": str}
    ]},
    "Traffic_Stop": {"cols": [
        {"attr": DCSYS.Traffic_Stop.TrafficStopSubsetName, "type": str}
    ]},
}
