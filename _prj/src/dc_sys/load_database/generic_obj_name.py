#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *


__all__ = ["GENERIC_OBJ_NAME"]


# These sheets do not have a key column, so we use a generic name for the different objects
GENERIC_OBJ_NAME = {
    "ZLPV": {"cols": [
        {"attr": DCSYS.ZLPV.De.Voie, "type": str},
        {"attr": DCSYS.ZLPV.De.Pk, "type": float},
        {"attr": DCSYS.ZLPV.De.Seg, "type": str},
        {"attr": DCSYS.ZLPV.De.X, "type": float}
    ]} if "ZLPV" in get_class_attr_dict(DCSYS) else None,

    "ZLPV_Or": {"cols": [
        {"attr": DCSYS.ZLPV_Or.De.Voie, "type": str},
        {"attr": DCSYS.ZLPV_Or.De.Pk, "type": float},
        {"attr": DCSYS.ZLPV_Or.De.Seg, "type": str},
        {"attr": DCSYS.ZLPV_Or.De.X, "type": float},
        {"attr": DCSYS.ZLPV_Or.Sens, "type": str}
    ]} if "ZLPV_Or" in get_class_attr_dict(DCSYS) else None,

    "Profil": {"cols": [
        {"attr": DCSYS.Profil.Voie, "type": str},
        {"attr": DCSYS.Profil.Pk, "type": float},
        {"attr": DCSYS.Profil.Seg, "type": str},
        {"attr": DCSYS.Profil.X, "type": float}
    ]} if "Profil" in get_class_attr_dict(DCSYS) else None,

    "Calib": {"cols": [
        {"attr": DCSYS.Calib.DistanceCalib, "type": float},
        {"attr": DCSYS.Calib.BaliseDeb, "type": str},
        {"attr": DCSYS.Calib.BaliseFin, "type": str}
    ]} if "Calib" in get_class_attr_dict(DCSYS) else None,

    "PAS": {"cols": [
        {"attr": DCSYS.PAS.TrackingAreaSubsetName if "TrackingAreaSubsetName" in get_class_attr_dict(DCSYS.PAS)
         else DCSYS.PAS.Nom, "type": str}
    ]} if "PAS" in get_class_attr_dict(DCSYS) else None,

    "DCS_Elementary_Zones": {"cols": [
        {"attr": DCSYS.DCS_Elementary_Zones.SubsetName if "SubsetName" in get_class_attr_dict(DCSYS.DCS_Elementary_Zones)
         else DCSYS.DCS_Elementary_Zones.Name, "type": str}
    ]} if "DCS_Elementary_Zones" in get_class_attr_dict(DCSYS) else None,

    "Traction_Profiles": {"cols": [
        {"attr": DCSYS.Traction_Profiles.TrainType if "TrainType" in get_class_attr_dict(DCSYS.Traction_Profiles)
         else DCSYS.Traction_Profiles.TrainConsist, "type": str},
        {"attr": DCSYS.Traction_Profiles.Speed, "type": float}
    ]} if "Traction_Profiles" in get_class_attr_dict(DCSYS) else None,

    "Flux_Variant_HF": {"cols": [
        {"attr": DCSYS.Flux_Variant_HF.Nom, "type": str},
        {"attr": DCSYS.Flux_Variant_HF.Troncon, "type": str}
    ]} if "Flux_Variant_HF" in get_class_attr_dict(DCSYS) else None,

    "Flux_Variant_BF": {"cols": [
        {"attr": DCSYS.Flux_Variant_BF.Nom, "type": str},
        {"attr": DCSYS.Flux_Variant_BF.Troncon, "type": str}
    ]} if "Flux_Variant_BF" in get_class_attr_dict(DCSYS) else None,

    "Frontam_General_Data": {"cols": [
        {"attr": DCSYS.Frontam_General_Data.Name, "type": str},
        {"attr": DCSYS.Frontam_General_Data.LineSectionName, "type": str}
    ]} if "Frontam_General_Data" in get_class_attr_dict(DCSYS) else None,

    "AV_Consist_ID": {"cols": [
        {"attr": DCSYS.AV_Consist_ID.Name, "type": str},
        {"attr": DCSYS.AV_Consist_ID.ConsistName, "type": str}
    ]} if "AV_Consist_ID" in get_class_attr_dict(DCSYS) else None,

    "Traffic_Stop": {"cols": [
        {"attr": DCSYS.Traffic_Stop.TrafficStopSubsetName, "type": str}
    ]} if "Traffic_Stop" in get_class_attr_dict(DCSYS) else None,

    "Anchor": {"cols": [
        {"attr": DCSYS.Anchor.TrackName, "type": str},
        {"attr": DCSYS.Anchor.SurveyedKp, "type": float}
    ]} if "Anchor" in get_class_attr_dict(DCSYS) else None,

    "Chainage": {"cols": [
        {"attr": DCSYS.Chainage.TrackName, "type": str},
        {"attr": DCSYS.Chainage.CivilKpStart, "type": str},
        {"attr": DCSYS.Chainage.CivilKpEnd, "type": str},
        {"attr": DCSYS.Chainage.ChainageType, "type": str}
    ]} if "Chainage" in get_class_attr_dict(DCSYS) else None,
}
