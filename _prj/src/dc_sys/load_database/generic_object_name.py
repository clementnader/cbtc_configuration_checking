#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *


__all__ = ["GENERIC_OBJ_NAME"]


# These sheets do not have a key column, so we use a generic name for the different objects
GENERIC_OBJ_NAME = {
    "ZLPV": {"columns": [
        {"attribute": DCSYS.ZLPV.De.Voie, "type": str},
        {"attribute": DCSYS.ZLPV.De.Pk, "type": float},
        {"attribute": DCSYS.ZLPV.De.Seg, "type": str},
        {"attribute": DCSYS.ZLPV.De.X, "type": float}
    ]} if "ZLPV" in get_class_attributes_dict(DCSYS) else None,

    "ZLPV_Or": {"columns": [
        {"attribute": DCSYS.ZLPV_Or.De.Voie, "type": str},
        {"attribute": DCSYS.ZLPV_Or.De.Pk, "type": float},
        {"attribute": DCSYS.ZLPV_Or.De.Seg, "type": str},
        {"attribute": DCSYS.ZLPV_Or.De.X, "type": float},
        {"attribute": DCSYS.ZLPV_Or.Sens, "type": str}
    ]} if "ZLPV_Or" in get_class_attributes_dict(DCSYS) else None,

    "Profil": {"columns": [
        {"attribute": DCSYS.Profil.Voie, "type": str},
        {"attribute": DCSYS.Profil.Pk, "type": float},
        {"attribute": DCSYS.Profil.Seg, "type": str},
        {"attribute": DCSYS.Profil.X, "type": float}
    ]} if "Profil" in get_class_attributes_dict(DCSYS) else None,

    "Calib": {"columns": [
        {"attribute": DCSYS.Calib.DistanceCalib, "type": float},
        {"attribute": DCSYS.Calib.BaliseDeb, "type": str},
        {"attribute": DCSYS.Calib.BaliseFin, "type": str}
    ]} if "Calib" in get_class_attributes_dict(DCSYS) else None,

    "PAS": {"columns": [
        {"attribute": DCSYS.PAS.TrackingAreaSubsetName if "TrackingAreaSubsetName" in get_class_attributes_dict(DCSYS.PAS)
         else DCSYS.PAS.Nom, "type": str}
    ]} if "PAS" in get_class_attributes_dict(DCSYS) else None,

    "DCS_Elementary_Zones": {"columns": [
        {"attribute": DCSYS.DCS_Elementary_Zones.SubsetName if "SubsetName" in get_class_attributes_dict(DCSYS.DCS_Elementary_Zones)
         else DCSYS.DCS_Elementary_Zones.Name, "type": str}
    ]} if "DCS_Elementary_Zones" in get_class_attributes_dict(DCSYS) else None,

    "Traction_Profiles": {"columns": [
        {"attribute": DCSYS.Traction_Profiles.TrainType if "TrainType" in get_class_attributes_dict(DCSYS.Traction_Profiles)
         else DCSYS.Traction_Profiles.TrainConsist, "type": str},
        {"attribute": DCSYS.Traction_Profiles.Speed, "type": float}
    ]} if "Traction_Profiles" in get_class_attributes_dict(DCSYS) else None,

    "Flux_Variant_HF": {"columns": [
        {"attribute": DCSYS.Flux_Variant_HF.Nom, "type": str},
        {"attribute": DCSYS.Flux_Variant_HF.Troncon, "type": str}
    ]} if "Flux_Variant_HF" in get_class_attributes_dict(DCSYS) else None,

    "Flux_Variant_BF": {"columns": [
        {"attribute": DCSYS.Flux_Variant_BF.Nom, "type": str},
        {"attribute": DCSYS.Flux_Variant_BF.Troncon, "type": str}
    ]} if "Flux_Variant_BF" in get_class_attributes_dict(DCSYS) else None,

    "Frontam_General_Data": {"columns": [
        {"attribute": DCSYS.Frontam_General_Data.Name, "type": str},
        {"attribute": DCSYS.Frontam_General_Data.LineSectionName, "type": str}
    ]} if "Frontam_General_Data" in get_class_attributes_dict(DCSYS) else None,

    "AV_Consist_ID": {"columns": [
        {"attribute": DCSYS.AV_Consist_ID.Name, "type": str},
        {"attribute": DCSYS.AV_Consist_ID.ConsistName, "type": str}
    ]} if "AV_Consist_ID" in get_class_attributes_dict(DCSYS) else None,

    "Traffic_Stop": {"columns": [
        {"attribute": DCSYS.Traffic_Stop.TrafficStopSubsetName, "type": str}
    ]} if "Traffic_Stop" in get_class_attributes_dict(DCSYS) else None,

    "Anchor": {"columns": [
        {"attribute": DCSYS.Anchor.TrackName, "type": str},
        {"attribute": DCSYS.Anchor.SurveyedKp, "type": float}
    ]} if "Anchor" in get_class_attributes_dict(DCSYS) else None,

    "Chainage": {"columns": [
        {"attribute": DCSYS.Chainage.TrackName, "type": str},
        {"attribute": DCSYS.Chainage.CivilKpStart, "type": str},
        {"attribute": DCSYS.Chainage.CivilKpEnd, "type": str},
        {"attribute": DCSYS.Chainage.ChainageType, "type": str}
    ]} if "Chainage" in get_class_attributes_dict(DCSYS) else None,
}
