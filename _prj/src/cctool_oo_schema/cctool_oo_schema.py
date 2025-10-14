#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------------------------ #
# Automatically generated Python file defining a DCSYS class containing the column information of  #
# sheets and attributes from the CCTool-OO Schema sheet of the CCTool-OO Schema file.              #
# ------------------------------------------------------------------------------------------------ #
# Revision: 08/03/01/00                                                                            #
# Comments: Compliant with Ref Sys 08-03-01-00                                                     #
# ------------------------------------------------------------------------------------------------ #

__all__ = ["DCSYS"]


class Ligne__SegmentsDepolarises:
    Cell = {'sheet_name': 'Ligne', 'attribute_name': 'SegmentsDepolarises', 'sub_attribute_name': 'Cell', 'columns': [7, 8, 9, 10, 11, 12, 13, 14]}


class Ligne__LoopbackSegments:
    Cell = {'sheet_name': 'Ligne', 'attribute_name': 'LoopbackSegments', 'sub_attribute_name': 'Cell', 'columns': [18, 19, 20, 21, 22, 23, 24, 25]}


class Ligne:
    Nom = {'sheet_name': 'Ligne', 'attribute_name': 'Nom', 'column': 1}
    Numero = {'sheet_name': 'Ligne', 'attribute_name': 'Numero', 'column': 2}
    Referentiel = {'sheet_name': 'Ligne', 'attribute_name': 'Referentiel', 'column': 3}
    SegmentReference = {'sheet_name': 'Ligne', 'attribute_name': 'SegmentReference', 'column': 4}
    OrientationGauche = {'sheet_name': 'Ligne', 'attribute_name': 'OrientationGauche', 'column': 5}
    OrientationDroite = {'sheet_name': 'Ligne', 'attribute_name': 'OrientationDroite', 'column': 6}
    SegmentsDepolarises = Ligne__SegmentsDepolarises()
    Version = {'sheet_name': 'Ligne', 'attribute_name': 'Version', 'column': 15}
    CbtcVersionKey = {'sheet_name': 'Ligne', 'attribute_name': 'CbtcVersionKey', 'column': 16}
    CbtcVersionRelease = {'sheet_name': 'Ligne', 'attribute_name': 'CbtcVersionRelease', 'column': 17}
    LoopbackSegments = Ligne__LoopbackSegments()


class Voie:
    Nom = {'sheet_name': 'Voie', 'attribute_name': 'Nom', 'column': 1}
    Ligne = {'sheet_name': 'Voie', 'attribute_name': 'Ligne', 'column': 2}
    NumeroSurLigne = {'sheet_name': 'Voie', 'attribute_name': 'NumeroSurLigne', 'column': 3}
    NomPcc = {'sheet_name': 'Voie', 'attribute_name': 'NomPcc', 'column': 4}
    Type = {'sheet_name': 'Voie', 'attribute_name': 'Type', 'column': 5}
    SensNominal = {'sheet_name': 'Voie', 'attribute_name': 'SensNominal', 'column': 6}
    PkDebut = {'sheet_name': 'Voie', 'attribute_name': 'PkDebut', 'column': 7}
    PkFin = {'sheet_name': 'Voie', 'attribute_name': 'PkFin', 'column': 8}


class Troncon__ExtremiteSurVoie:
    Voie = {'sheet_name': 'Troncon', 'attribute_name': 'ExtremiteSurVoie', 'sub_attribute_name': 'Voie', 'columns': [9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66]}
    PkDebut = {'sheet_name': 'Troncon', 'attribute_name': 'ExtremiteSurVoie', 'sub_attribute_name': 'PkDebut', 'columns': [10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67]}
    PkFin = {'sheet_name': 'Troncon', 'attribute_name': 'ExtremiteSurVoie', 'sub_attribute_name': 'PkFin', 'columns': [11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68]}


class Troncon:
    Nom = {'sheet_name': 'Troncon', 'attribute_name': 'Nom', 'column': 1}
    Ligne = {'sheet_name': 'Troncon', 'attribute_name': 'Ligne', 'column': 2}
    NumeroTronconLigne = {'sheet_name': 'Troncon', 'attribute_name': 'NumeroTronconLigne', 'column': 3}
    NumVersion = {'sheet_name': 'Troncon', 'attribute_name': 'NumVersion', 'column': 4}
    TronconUtile1 = {'sheet_name': 'Troncon', 'attribute_name': 'TronconUtile1', 'column': 5}
    TronconUtile2 = {'sheet_name': 'Troncon', 'attribute_name': 'TronconUtile2', 'column': 6}
    TronconUtile3 = {'sheet_name': 'Troncon', 'attribute_name': 'TronconUtile3', 'column': 7}
    TronconUtile4 = {'sheet_name': 'Troncon', 'attribute_name': 'TronconUtile4', 'column': 8}
    ExtremiteSurVoie = Troncon__ExtremiteSurVoie()


class Seg__SegmentsVoisins:
    Amont = {'sheet_name': 'Seg', 'attribute_name': 'SegmentsVoisins', 'sub_attribute_name': 'Amont', 'columns': [8, 9]}
    Aval = {'sheet_name': 'Seg', 'attribute_name': 'SegmentsVoisins', 'sub_attribute_name': 'Aval', 'columns': [10, 11]}


class Seg:
    Nom = {'sheet_name': 'Seg', 'attribute_name': 'Nom', 'column': 1}
    Troncon = {'sheet_name': 'Seg', 'attribute_name': 'Troncon', 'column': 2}
    NumSegmentTroncon = {'sheet_name': 'Seg', 'attribute_name': 'NumSegmentTroncon', 'column': 3}
    Voie = {'sheet_name': 'Seg', 'attribute_name': 'Voie', 'column': 4}
    Origine = {'sheet_name': 'Seg', 'attribute_name': 'Origine', 'column': 5}
    Fin = {'sheet_name': 'Seg', 'attribute_name': 'Fin', 'column': 6}
    Longueur = {'sheet_name': 'Seg', 'attribute_name': 'Longueur', 'column': 7}
    SegmentsVoisins = Seg__SegmentsVoisins()
    SensLigne = {'sheet_name': 'Seg', 'attribute_name': 'SensLigne', 'column': 12}
    RingSegment = {'sheet_name': 'Seg', 'attribute_name': 'RingSegment', 'column': 13}
    RejectionDistance = {'sheet_name': 'Seg', 'attribute_name': 'RejectionDistance', 'column': 14}


class Aig__SwitchBlockLockingArea:
    Ivb = {'sheet_name': 'Aig', 'attribute_name': 'SwitchBlockLockingArea', 'sub_attribute_name': 'Ivb', 'columns': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}


class Aig__CbtcProtectingSwitchArea:
    Ivb = {'sheet_name': 'Aig', 'attribute_name': 'CbtcProtectingSwitchArea', 'sub_attribute_name': 'Ivb', 'columns': [18, 19, 20, 21, 22, 23, 24, 25, 26, 27]}


class Aig__AreaRightPositionFlank:
    BeginSeg = {'sheet_name': 'Aig', 'attribute_name': 'AreaRightPositionFlank', 'sub_attribute_name': 'BeginSeg', 'columns': [28, 33, 38, 43]}
    BeginX = {'sheet_name': 'Aig', 'attribute_name': 'AreaRightPositionFlank', 'sub_attribute_name': 'BeginX', 'columns': [29, 34, 39, 44]}
    EndSeg = {'sheet_name': 'Aig', 'attribute_name': 'AreaRightPositionFlank', 'sub_attribute_name': 'EndSeg', 'columns': [30, 35, 40, 45]}
    EndX = {'sheet_name': 'Aig', 'attribute_name': 'AreaRightPositionFlank', 'sub_attribute_name': 'EndX', 'columns': [31, 36, 41, 46]}
    Direction = {'sheet_name': 'Aig', 'attribute_name': 'AreaRightPositionFlank', 'sub_attribute_name': 'Direction', 'columns': [32, 37, 42, 47]}


class Aig__AreaLeftPositionFlank:
    BeginSeg = {'sheet_name': 'Aig', 'attribute_name': 'AreaLeftPositionFlank', 'sub_attribute_name': 'BeginSeg', 'columns': [48, 53, 58, 63]}
    BeginX = {'sheet_name': 'Aig', 'attribute_name': 'AreaLeftPositionFlank', 'sub_attribute_name': 'BeginX', 'columns': [49, 54, 59, 64]}
    EndSeg = {'sheet_name': 'Aig', 'attribute_name': 'AreaLeftPositionFlank', 'sub_attribute_name': 'EndSeg', 'columns': [50, 55, 60, 65]}
    EndX = {'sheet_name': 'Aig', 'attribute_name': 'AreaLeftPositionFlank', 'sub_attribute_name': 'EndX', 'columns': [51, 56, 61, 66]}
    Direction = {'sheet_name': 'Aig', 'attribute_name': 'AreaLeftPositionFlank', 'sub_attribute_name': 'Direction', 'columns': [52, 57, 62, 67]}


class Aig:
    Nom = {'sheet_name': 'Aig', 'attribute_name': 'Nom', 'column': 1}
    SegmentPointe = {'sheet_name': 'Aig', 'attribute_name': 'SegmentPointe', 'column': 2}
    SegmentTd = {'sheet_name': 'Aig', 'attribute_name': 'SegmentTd', 'column': 3}
    SegmentTg = {'sheet_name': 'Aig', 'attribute_name': 'SegmentTg', 'column': 4}
    NumeroPcc = {'sheet_name': 'Aig', 'attribute_name': 'NumeroPcc', 'column': 5}
    SwitchBlockLockingArea = Aig__SwitchBlockLockingArea()
    FreeToMove = {'sheet_name': 'Aig', 'attribute_name': 'FreeToMove', 'column': 16}
    Trailable = {'sheet_name': 'Aig', 'attribute_name': 'Trailable', 'column': 17}
    CbtcProtectingSwitchArea = Aig__CbtcProtectingSwitchArea()
    AreaRightPositionFlank = Aig__AreaRightPositionFlank()
    AreaLeftPositionFlank = Aig__AreaLeftPositionFlank()


class Quai__Station:
    Nom = {'sheet_name': 'Quai', 'attribute_name': 'Station', 'sub_attribute_name': 'Nom', 'columns': [3]}
    Abreviation = {'sheet_name': 'Quai', 'attribute_name': 'Station', 'sub_attribute_name': 'Abreviation', 'columns': [4]}
    NumStationLigne = {'sheet_name': 'Quai', 'attribute_name': 'Station', 'sub_attribute_name': 'NumStationLigne', 'columns': [5]}


class Quai__ExtremiteDuQuai:
    Seg = {'sheet_name': 'Quai', 'attribute_name': 'ExtremiteDuQuai', 'sub_attribute_name': 'Seg', 'columns': [9, 17]}
    X = {'sheet_name': 'Quai', 'attribute_name': 'ExtremiteDuQuai', 'sub_attribute_name': 'X', 'columns': [10, 18]}
    CoteOuvPortes = {'sheet_name': 'Quai', 'attribute_name': 'ExtremiteDuQuai', 'sub_attribute_name': 'CoteOuvPortes', 'columns': [11, 19]}
    SensExt = {'sheet_name': 'Quai', 'attribute_name': 'ExtremiteDuQuai', 'sub_attribute_name': 'SensExt', 'columns': [12, 20]}
    Voie = {'sheet_name': 'Quai', 'attribute_name': 'ExtremiteDuQuai', 'sub_attribute_name': 'Voie', 'columns': [13, 21]}
    Pk = {'sheet_name': 'Quai', 'attribute_name': 'ExtremiteDuQuai', 'sub_attribute_name': 'Pk', 'columns': [14, 22]}
    CvspDistance = {'sheet_name': 'Quai', 'attribute_name': 'ExtremiteDuQuai', 'sub_attribute_name': 'CvspDistance', 'columns': [15, 23]}
    TerminalStation = {'sheet_name': 'Quai', 'attribute_name': 'ExtremiteDuQuai', 'sub_attribute_name': 'TerminalStation', 'columns': [16, 24]}


class Quai__PointDArret:
    Name = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'Name', 'columns': [25, 37, 49, 61]}
    Number = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'Number', 'columns': [26, 38, 50, 62]}
    Seg = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'Seg', 'columns': [27, 39, 51, 63]}
    X = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'X', 'columns': [28, 40, 52, 64]}
    SensAssocie = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'SensAssocie', 'columns': [29, 41, 53, 65]}
    SensApproche = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'SensApproche', 'columns': [30, 42, 54, 66]}
    StoppingPointDistance = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'StoppingPointDistance', 'columns': [31, 43, 55, 67]}
    TypePtArretQuai = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'TypePtArretQuai', 'columns': [32, 44, 56, 68]}
    StaticTest = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'StaticTest', 'columns': [33, 45, 57, 69]}
    TractionCutOffWhenApproachingOsp = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'TractionCutOffWhenApproachingOsp', 'columns': [34, 46, 58, 70]}
    Voie = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'Voie', 'columns': [35, 47, 59, 71]}
    Pk = {'sheet_name': 'Quai', 'attribute_name': 'PointDArret', 'sub_attribute_name': 'Pk', 'columns': [36, 48, 60, 72]}


class Quai__PointDEntree:
    Seg = {'sheet_name': 'Quai', 'attribute_name': 'PointDEntree', 'sub_attribute_name': 'Seg', 'columns': [73, 77, 81, 85, 89, 93]}
    X = {'sheet_name': 'Quai', 'attribute_name': 'PointDEntree', 'sub_attribute_name': 'X', 'columns': [74, 78, 82, 86, 90, 94]}
    Voie = {'sheet_name': 'Quai', 'attribute_name': 'PointDEntree', 'sub_attribute_name': 'Voie', 'columns': [75, 79, 83, 87, 91, 95]}
    Pk = {'sheet_name': 'Quai', 'attribute_name': 'PointDEntree', 'sub_attribute_name': 'Pk', 'columns': [76, 80, 84, 88, 92, 96]}


class Quai__FacadesDeQuai:
    EqptCfq = {'sheet_name': 'Quai', 'attribute_name': 'FacadesDeQuai', 'sub_attribute_name': 'EqptCfq', 'columns': [107]}
    CoteFq = {'sheet_name': 'Quai', 'attribute_name': 'FacadesDeQuai', 'sub_attribute_name': 'CoteFq', 'columns': [108]}


class Quai:
    Nom = {'sheet_name': 'Quai', 'attribute_name': 'Nom', 'column': 1}
    NumQuaiStation = {'sheet_name': 'Quai', 'attribute_name': 'NumQuaiStation', 'column': 2}
    Station = Quai__Station()
    InhibAccessibilite = {'sheet_name': 'Quai', 'attribute_name': 'InhibAccessibilite', 'column': 6}
    CheckBrakes = {'sheet_name': 'Quai', 'attribute_name': 'CheckBrakes', 'column': 7}
    AllowAccelerometersCalibration = {'sheet_name': 'Quai', 'attribute_name': 'AllowAccelerometersCalibration', 'column': 8}
    ExtremiteDuQuai = Quai__ExtremiteDuQuai()
    PointDArret = Quai__PointDArret()
    PointDEntree = Quai__PointDEntree()
    AvecPassagers = {'sheet_name': 'Quai', 'attribute_name': 'AvecPassagers', 'column': 97}
    AvecFq = {'sheet_name': 'Quai', 'attribute_name': 'AvecFq', 'column': 98}
    PsdNumber = {'sheet_name': 'Quai', 'attribute_name': 'PsdNumber', 'column': 99}
    PsdNumbering = {'sheet_name': 'Quai', 'attribute_name': 'PsdNumbering', 'column': 100}
    AvecPrecPtArret = {'sheet_name': 'Quai', 'attribute_name': 'AvecPrecPtArret', 'column': 101}
    RightSideOpeningTime = {'sheet_name': 'Quai', 'attribute_name': 'RightSideOpeningTime', 'column': 102}
    LeftSideOpeningTime = {'sheet_name': 'Quai', 'attribute_name': 'LeftSideOpeningTime', 'column': 103}
    DoublePlatformOpeningDelay = {'sheet_name': 'Quai', 'attribute_name': 'DoublePlatformOpeningDelay', 'column': 104}
    DisableAutomaticDoorClosing = {'sheet_name': 'Quai', 'attribute_name': 'DisableAutomaticDoorClosing', 'column': 105}
    RelatedWaysideEquip = {'sheet_name': 'Quai', 'attribute_name': 'RelatedWaysideEquip', 'column': 106}
    FacadesDeQuai = Quai__FacadesDeQuai()
    NumeroPccQuai = {'sheet_name': 'Quai', 'attribute_name': 'NumeroPccQuai', 'column': 109}
    NumeroPccStation = {'sheet_name': 'Quai', 'attribute_name': 'NumeroPccStation', 'column': 110}
    WithEss = {'sheet_name': 'Quai', 'attribute_name': 'WithEss', 'column': 111}
    WithTh = {'sheet_name': 'Quai', 'attribute_name': 'WithTh', 'column': 112}
    WithTad = {'sheet_name': 'Quai', 'attribute_name': 'WithTad', 'column': 113}
    PsdMessagesRouted = {'sheet_name': 'Quai', 'attribute_name': 'PsdMessagesRouted', 'column': 114}
    Router = {'sheet_name': 'Quai', 'attribute_name': 'Router', 'column': 115}


class PtA:
    Nom = {'sheet_name': 'PtA', 'attribute_name': 'Nom', 'column': 1}
    NumPtAtoSegment = {'sheet_name': 'PtA', 'attribute_name': 'NumPtAtoSegment', 'column': 2}
    Seg = {'sheet_name': 'PtA', 'attribute_name': 'Seg', 'column': 3}
    X = {'sheet_name': 'PtA', 'attribute_name': 'X', 'column': 4}
    SensAssocie = {'sheet_name': 'PtA', 'attribute_name': 'SensAssocie', 'column': 5}
    SensApproche = {'sheet_name': 'PtA', 'attribute_name': 'SensApproche', 'column': 6}
    Voie = {'sheet_name': 'PtA', 'attribute_name': 'Voie', 'column': 7}
    Pk = {'sheet_name': 'PtA', 'attribute_name': 'Pk', 'column': 8}
    TypePtAto = {'sheet_name': 'PtA', 'attribute_name': 'TypePtAto', 'column': 9}
    ArretPermanentCpa = {'sheet_name': 'PtA', 'attribute_name': 'ArretPermanentCpa', 'column': 10}
    ParkingPosition = {'sheet_name': 'PtA', 'attribute_name': 'ParkingPosition', 'column': 11}
    StaticTestAllowed = {'sheet_name': 'PtA', 'attribute_name': 'StaticTestAllowed', 'column': 12}
    TrainDoorsOpeningSide = {'sheet_name': 'PtA', 'attribute_name': 'TrainDoorsOpeningSide', 'column': 13}
    WashingOsp = {'sheet_name': 'PtA', 'attribute_name': 'WashingOsp', 'column': 14}
    OspProxDist = {'sheet_name': 'PtA', 'attribute_name': 'OspProxDist', 'column': 15}
    AllowAccelerometersCalibration = {'sheet_name': 'PtA', 'attribute_name': 'AllowAccelerometersCalibration', 'column': 16}


class OSP_ATS_Id:
    Name = {'sheet_name': 'OSP_ATS_Id', 'attribute_name': 'Name', 'column': 1}
    Type = {'sheet_name': 'OSP_ATS_Id', 'attribute_name': 'Type', 'column': 2}
    AtsId = {'sheet_name': 'OSP_ATS_Id', 'attribute_name': 'AtsId', 'column': 3}


class CDV__Extremite:
    Seg = {'sheet_name': 'CDV', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41]}
    X = {'sheet_name': 'CDV', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42]}
    Voie = {'sheet_name': 'CDV', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71]}
    Pk = {'sheet_name': 'CDV', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72]}


class CDV:
    Nom = {'sheet_name': 'CDV', 'attribute_name': 'Nom', 'column': 1}
    DetectArb = {'sheet_name': 'CDV', 'attribute_name': 'DetectArb', 'column': 2}
    DetectNcArb = {'sheet_name': 'CDV', 'attribute_name': 'DetectNcArb', 'column': 3}
    DetectNrb = {'sheet_name': 'CDV', 'attribute_name': 'DetectNrb', 'column': 4}
    DetectNcNrb = {'sheet_name': 'CDV', 'attribute_name': 'DetectNcNrb', 'column': 5}
    ExtendedSievingAllowed = {'sheet_name': 'CDV', 'attribute_name': 'ExtendedSievingAllowed', 'column': 6}
    RailRoadEntrance = {'sheet_name': 'CDV', 'attribute_name': 'RailRoadEntrance', 'column': 7}
    BrokenRailDetection = {'sheet_name': 'CDV', 'attribute_name': 'BrokenRailDetection', 'column': 8}
    DedicatedLineSection = {'sheet_name': 'CDV', 'attribute_name': 'DedicatedLineSection', 'column': 9}
    ReachBlockAllowed = {'sheet_name': 'CDV', 'attribute_name': 'ReachBlockAllowed', 'column': 10}
    IxlGivesBlockInitStatus = {'sheet_name': 'CDV', 'attribute_name': 'IxlGivesBlockInitStatus', 'column': 11}
    IxlGivesNotHeldStatus = {'sheet_name': 'CDV', 'attribute_name': 'IxlGivesNotHeldStatus', 'column': 12}
    Extremite = CDV__Extremite()
    AtsBlockId = {'sheet_name': 'CDV', 'attribute_name': 'AtsBlockId', 'column': 73}
    DisplayableName = {'sheet_name': 'CDV', 'attribute_name': 'DisplayableName', 'column': 74}


class IVB__Limit:
    Seg = {'sheet_name': 'IVB', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38]}
    X = {'sheet_name': 'IVB', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39]}
    Track = {'sheet_name': 'IVB', 'attribute_name': 'Limit', 'sub_attribute_name': 'Track', 'columns': [40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68]}
    Kp = {'sheet_name': 'IVB', 'attribute_name': 'Limit', 'sub_attribute_name': 'Kp', 'columns': [41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69]}


class IVB__DiamondCrossingSwitches:
    SwitchName = {'sheet_name': 'IVB', 'attribute_name': 'DiamondCrossingSwitches', 'sub_attribute_name': 'SwitchName', 'columns': [71, 72, 73, 74]}


class IVB:
    Name = {'sheet_name': 'IVB', 'attribute_name': 'Name', 'column': 1}
    Id = {'sheet_name': 'IVB', 'attribute_name': 'Id', 'column': 2}
    SentToIxl = {'sheet_name': 'IVB', 'attribute_name': 'SentToIxl', 'column': 3}
    UsedByIxl = {'sheet_name': 'IVB', 'attribute_name': 'UsedByIxl', 'column': 4}
    BlockFreed = {'sheet_name': 'IVB', 'attribute_name': 'BlockFreed', 'column': 5}
    ZcName = {'sheet_name': 'IVB', 'attribute_name': 'ZcName', 'column': 6}
    DirectionLockingBlock = {'sheet_name': 'IVB', 'attribute_name': 'DirectionLockingBlock', 'column': 7}
    UnlockNormal = {'sheet_name': 'IVB', 'attribute_name': 'UnlockNormal', 'column': 8}
    UnlockReverse = {'sheet_name': 'IVB', 'attribute_name': 'UnlockReverse', 'column': 9}
    Limit = IVB__Limit()
    DiamondCrossing = {'sheet_name': 'IVB', 'attribute_name': 'DiamondCrossing', 'column': 70}
    DiamondCrossingSwitches = IVB__DiamondCrossingSwitches()
    RelatedBlock = {'sheet_name': 'IVB', 'attribute_name': 'RelatedBlock', 'column': 75}


class CV__Extremite:
    Seg = {'sheet_name': 'CV', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [2, 4, 6]}
    X = {'sheet_name': 'CV', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [3, 5, 7]}
    Voie = {'sheet_name': 'CV', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [8, 10, 12]}
    Pk = {'sheet_name': 'CV', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [9, 11, 13]}


class CV:
    Nom = {'sheet_name': 'CV', 'attribute_name': 'Nom', 'column': 1}
    Extremite = CV__Extremite()
    IsEndOfTrack = {'sheet_name': 'CV', 'attribute_name': 'IsEndOfTrack', 'column': 14}


class Sig__IvbJoint:
    UpstreamIvb = {'sheet_name': 'Sig', 'attribute_name': 'IvbJoint', 'sub_attribute_name': 'UpstreamIvb', 'columns': [12]}
    DownstreamIvb = {'sheet_name': 'Sig', 'attribute_name': 'IvbJoint', 'sub_attribute_name': 'DownstreamIvb', 'columns': [13]}


class Sig:
    Nom = {'sheet_name': 'Sig', 'attribute_name': 'Nom', 'column': 1}
    Type = {'sheet_name': 'Sig', 'attribute_name': 'Type', 'column': 2}
    Seg = {'sheet_name': 'Sig', 'attribute_name': 'Seg', 'column': 3}
    X = {'sheet_name': 'Sig', 'attribute_name': 'X', 'column': 4}
    Sens = {'sheet_name': 'Sig', 'attribute_name': 'Sens', 'column': 5}
    Voie = {'sheet_name': 'Sig', 'attribute_name': 'Voie', 'column': 6}
    Pk = {'sheet_name': 'Sig', 'attribute_name': 'Pk', 'column': 7}
    R_Cli = {'sheet_name': 'Sig', 'attribute_name': 'R_Cli', 'column': 8}
    DistPap = {'sheet_name': 'Sig', 'attribute_name': 'DistPap', 'column': 9}
    VspType = {'sheet_name': 'Sig', 'attribute_name': 'VspType', 'column': 10}
    DelayedLtDistance = {'sheet_name': 'Sig', 'attribute_name': 'DelayedLtDistance', 'column': 11}
    IvbJoint = Sig__IvbJoint()
    Da_Passage = {'sheet_name': 'Sig', 'attribute_name': 'Da_Passage', 'column': 14}
    D_Echap = {'sheet_name': 'Sig', 'attribute_name': 'D_Echap', 'column': 15}
    Du_Assistee = {'sheet_name': 'Sig', 'attribute_name': 'Du_Assistee', 'column': 16}
    D_Libre = {'sheet_name': 'Sig', 'attribute_name': 'D_Libre', 'column': 17}
    Enc_Dep = {'sheet_name': 'Sig', 'attribute_name': 'Enc_Dep', 'column': 18}
    OverlapType = {'sheet_name': 'Sig', 'attribute_name': 'OverlapType', 'column': 19}
    Annulable = {'sheet_name': 'Sig', 'attribute_name': 'Annulable', 'column': 20}
    WithFunc_Stop = {'sheet_name': 'Sig', 'attribute_name': 'WithFunc_Stop', 'column': 21}
    CbtcTrainAppProvided = {'sheet_name': 'Sig', 'attribute_name': 'CbtcTrainAppProvided', 'column': 22}
    NumeroPcc = {'sheet_name': 'Sig', 'attribute_name': 'NumeroPcc', 'column': 23}
    PositionForcee = {'sheet_name': 'Sig', 'attribute_name': 'PositionForcee', 'column': 24}
    SortieTerritoireCbtc = {'sheet_name': 'Sig', 'attribute_name': 'SortieTerritoireCbtc', 'column': 25}
    PresenceDynamicTag = {'sheet_name': 'Sig', 'attribute_name': 'PresenceDynamicTag', 'column': 26}
    WithIatpDepCheck = {'sheet_name': 'Sig', 'attribute_name': 'WithIatpDepCheck', 'column': 27}
    RelatedTag1 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag1', 'column': 28}
    RelatedTag2 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag2', 'column': 29}
    RelatedTag3 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag3', 'column': 30}
    RelatedTag4 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag4', 'column': 31}
    RelatedTag5 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag5', 'column': 32}
    RelatedTag6 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag6', 'column': 33}
    RelatedTag7 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag7', 'column': 34}
    RelatedTag8 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag8', 'column': 35}
    RelatedTag9 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag9', 'column': 36}
    RelatedTag10 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag10', 'column': 37}
    RelatedTag11 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag11', 'column': 38}
    RelatedTag12 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag12', 'column': 39}
    RelatedTag13 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag13', 'column': 40}
    RelatedTag14 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag14', 'column': 41}
    RelatedTag15 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag15', 'column': 42}
    RelatedTag16 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag16', 'column': 43}
    RelatedTag17 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag17', 'column': 44}
    RelatedTag18 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag18', 'column': 45}
    RelatedTag19 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag19', 'column': 46}
    RelatedTag20 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag20', 'column': 47}
    RelatedTag21 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag21', 'column': 48}
    RelatedTag22 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag22', 'column': 49}
    RelatedTag23 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag23', 'column': 50}
    RelatedTag24 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag24', 'column': 51}
    RelatedTag25 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag25', 'column': 52}
    RelatedTag26 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag26', 'column': 53}
    RelatedTag27 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag27', 'column': 54}
    RelatedTag28 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag28', 'column': 55}
    RelatedTag29 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag29', 'column': 56}
    RelatedTag30 = {'sheet_name': 'Sig', 'attribute_name': 'RelatedTag30', 'column': 57}


class Sig_Zone__ExtremitesZoneArmementDa:
    Seg = {'sheet_name': 'Sig_Zone', 'attribute_name': 'ExtremitesZoneArmementDa', 'sub_attribute_name': 'Seg', 'columns': [2, 6, 10, 14, 18, 22]}
    X = {'sheet_name': 'Sig_Zone', 'attribute_name': 'ExtremitesZoneArmementDa', 'sub_attribute_name': 'X', 'columns': [3, 7, 11, 15, 19, 23]}
    Voie = {'sheet_name': 'Sig_Zone', 'attribute_name': 'ExtremitesZoneArmementDa', 'sub_attribute_name': 'Voie', 'columns': [4, 8, 12, 16, 20, 24]}
    Pk = {'sheet_name': 'Sig_Zone', 'attribute_name': 'ExtremitesZoneArmementDa', 'sub_attribute_name': 'Pk', 'columns': [5, 9, 13, 17, 21, 25]}


class Sig_Zone__PointsDEntreeZoneDApproche:
    Seg = {'sheet_name': 'Sig_Zone', 'attribute_name': 'PointsDEntreeZoneDApproche', 'sub_attribute_name': 'Seg', 'columns': [26, 30, 34, 38, 42, 46]}
    X = {'sheet_name': 'Sig_Zone', 'attribute_name': 'PointsDEntreeZoneDApproche', 'sub_attribute_name': 'X', 'columns': [27, 31, 35, 39, 43, 47]}
    Voie = {'sheet_name': 'Sig_Zone', 'attribute_name': 'PointsDEntreeZoneDApproche', 'sub_attribute_name': 'Voie', 'columns': [28, 32, 36, 40, 44, 48]}
    Pk = {'sheet_name': 'Sig_Zone', 'attribute_name': 'PointsDEntreeZoneDApproche', 'sub_attribute_name': 'Pk', 'columns': [29, 33, 37, 41, 45, 49]}


class Sig_Zone__PointsDEntreeZoneEnclDepass:
    Seg = {'sheet_name': 'Sig_Zone', 'attribute_name': 'PointsDEntreeZoneEnclDepass', 'sub_attribute_name': 'Seg', 'columns': [50, 54, 58, 62, 66, 70]}
    X = {'sheet_name': 'Sig_Zone', 'attribute_name': 'PointsDEntreeZoneEnclDepass', 'sub_attribute_name': 'X', 'columns': [51, 55, 59, 63, 67, 71]}
    Voie = {'sheet_name': 'Sig_Zone', 'attribute_name': 'PointsDEntreeZoneEnclDepass', 'sub_attribute_name': 'Voie', 'columns': [52, 56, 60, 64, 68, 72]}
    Pk = {'sheet_name': 'Sig_Zone', 'attribute_name': 'PointsDEntreeZoneEnclDepass', 'sub_attribute_name': 'Pk', 'columns': [53, 57, 61, 65, 69, 73]}


class Sig_Zone__ItiInterdictionAnnulation:
    Iti = {'sheet_name': 'Sig_Zone', 'attribute_name': 'ItiInterdictionAnnulation', 'sub_attribute_name': 'Iti', 'columns': [74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93]}


class Sig_Zone__ConcealBlocksList:
    Block = {'sheet_name': 'Sig_Zone', 'attribute_name': 'ConcealBlocksList', 'sub_attribute_name': 'Block', 'columns': [94, 95, 96, 97, 98, 99, 100, 101, 102, 103]}


class Sig_Zone:
    NomDuSignal = {'sheet_name': 'Sig_Zone', 'attribute_name': 'NomDuSignal', 'column': 1}
    ExtremitesZoneArmementDa = Sig_Zone__ExtremitesZoneArmementDa()
    PointsDEntreeZoneDApproche = Sig_Zone__PointsDEntreeZoneDApproche()
    PointsDEntreeZoneEnclDepass = Sig_Zone__PointsDEntreeZoneEnclDepass()
    ItiInterdictionAnnulation = Sig_Zone__ItiInterdictionAnnulation()
    ConcealBlocksList = Sig_Zone__ConcealBlocksList()


class Profil:
    Pente = {'sheet_name': 'Profil', 'attribute_name': 'Pente', 'column': 1}
    Seg = {'sheet_name': 'Profil', 'attribute_name': 'Seg', 'column': 2}
    X = {'sheet_name': 'Profil', 'attribute_name': 'X', 'column': 3}
    Voie = {'sheet_name': 'Profil', 'attribute_name': 'Voie', 'column': 4}
    Pk = {'sheet_name': 'Profil', 'attribute_name': 'Pk', 'column': 5}


class Bal:
    Nom = {'sheet_name': 'Bal', 'attribute_name': 'Nom', 'column': 1}
    BaliseName = {'sheet_name': 'Bal', 'attribute_name': 'BaliseName', 'column': 2}
    NumBaliseSeg = {'sheet_name': 'Bal', 'attribute_name': 'NumBaliseSeg', 'column': 3}
    Seg = {'sheet_name': 'Bal', 'attribute_name': 'Seg', 'column': 4}
    X = {'sheet_name': 'Bal', 'attribute_name': 'X', 'column': 5}
    Voie = {'sheet_name': 'Bal', 'attribute_name': 'Voie', 'column': 6}
    Pk = {'sheet_name': 'Bal', 'attribute_name': 'Pk', 'column': 7}
    TypePose = {'sheet_name': 'Bal', 'attribute_name': 'TypePose', 'column': 8}
    NumeroPcc = {'sheet_name': 'Bal', 'attribute_name': 'NumeroPcc', 'column': 9}
    ReadingOccurrence = {'sheet_name': 'Bal', 'attribute_name': 'ReadingOccurrence', 'column': 10}


class Coasting_Profiles__CoastingZone:
    TriggerSpeed = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CoastingZone', 'sub_attribute_name': 'TriggerSpeed', 'columns': [8, 43, 78]}
    StartTrack = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CoastingZone', 'sub_attribute_name': 'StartTrack', 'columns': [9, 44, 79]}
    StartKp = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CoastingZone', 'sub_attribute_name': 'StartKp', 'columns': [10, 45, 80]}
    EndTrack = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CoastingZone', 'sub_attribute_name': 'EndTrack', 'columns': [11, 46, 81]}
    EndKp = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CoastingZone', 'sub_attribute_name': 'EndKp', 'columns': [12, 47, 82]}
    Seg = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CoastingZone', 'sub_attribute_name': 'Seg', 'columns': [13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 83, 86, 89, 92, 95, 98, 101, 104, 107, 110]}
    X = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CoastingZone', 'sub_attribute_name': 'X', 'columns': [14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 84, 87, 90, 93, 96, 99, 102, 105, 108, 111]}
    Direction = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CoastingZone', 'sub_attribute_name': 'Direction', 'columns': [15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 85, 88, 91, 94, 97, 100, 103, 106, 109, 112]}


class Coasting_Profiles:
    CoastingProfileName = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CoastingProfileName', 'column': 1}
    Origin = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'Origin', 'column': 2}
    Destination = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'Destination', 'column': 3}
    CoastingProfileLevel = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CoastingProfileLevel', 'column': 4}
    TheoreticalRuntime = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'TheoreticalRuntime', 'column': 5}
    CruisingSpeed = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CruisingSpeed', 'column': 6}
    CruisingZoneName = {'sheet_name': 'Coasting_Profiles', 'attribute_name': 'CruisingZoneName', 'column': 7}
    CoastingZone = Coasting_Profiles__CoastingZone()


class CELL__Wcc:
    Nom = {'sheet_name': 'CELL', 'attribute_name': 'Wcc', 'sub_attribute_name': 'Nom', 'columns': [3]}


class CELL__PasCellule:
    Cell = {'sheet_name': 'CELL', 'attribute_name': 'PasCellule', 'sub_attribute_name': 'Cell', 'columns': [4, 5, 6, 7, 8]}


class CELL__TronconsPropres:
    Cell = {'sheet_name': 'CELL', 'attribute_name': 'TronconsPropres', 'sub_attribute_name': 'Cell', 'columns': [9, 10, 11, 12]}


class CELL__TronconsAnticipes:
    Cell = {'sheet_name': 'CELL', 'attribute_name': 'TronconsAnticipes', 'sub_attribute_name': 'Cell', 'columns': [13, 14, 15, 16]}


class CELL__Extremite:
    Seg = {'sheet_name': 'CELL', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60]}
    X = {'sheet_name': 'CELL', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61]}
    Sens = {'sheet_name': 'CELL', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Sens', 'columns': [20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62]}
    Voie = {'sheet_name': 'CELL', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91]}
    Pk = {'sheet_name': 'CELL', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92]}


class CELL:
    Nom = {'sheet_name': 'CELL', 'attribute_name': 'Nom', 'column': 1}
    NumCellule = {'sheet_name': 'CELL', 'attribute_name': 'NumCellule', 'column': 2}
    Wcc = CELL__Wcc()
    PasCellule = CELL__PasCellule()
    TronconsPropres = CELL__TronconsPropres()
    TronconsAnticipes = CELL__TronconsAnticipes()
    ServeurDInvariants = {'sheet_name': 'CELL', 'attribute_name': 'ServeurDInvariants', 'column': 17}
    Extremite = CELL__Extremite()


class ZA_EFF_T__Extremite:
    Seg = {'sheet_name': 'ZA_EFF_T', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}
    X = {'sheet_name': 'ZA_EFF_T', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}
    Sens = {'sheet_name': 'ZA_EFF_T', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Sens', 'columns': [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]}
    Voie = {'sheet_name': 'ZA_EFF_T', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [35, 37, 39, 41, 43, 45, 47, 49, 51, 53]}
    Pk = {'sheet_name': 'ZA_EFF_T', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [36, 38, 40, 42, 44, 46, 48, 50, 52, 54]}


class ZA_EFF_T:
    Nom = {'sheet_name': 'ZA_EFF_T', 'attribute_name': 'Nom', 'column': 1}
    Type = {'sheet_name': 'ZA_EFF_T', 'attribute_name': 'Type', 'column': 2}
    TriggerCondition = {'sheet_name': 'ZA_EFF_T', 'attribute_name': 'TriggerCondition', 'column': 3}
    MaximumTractionEffort = {'sheet_name': 'ZA_EFF_T', 'attribute_name': 'MaximumTractionEffort', 'column': 4}
    Extremite = ZA_EFF_T__Extremite()


class SP:
    Nom = {'sheet_name': 'SP', 'attribute_name': 'Nom', 'column': 1}
    TerminusOuSp = {'sheet_name': 'SP', 'attribute_name': 'TerminusOuSp', 'column': 2}
    QuaiArrivee = {'sheet_name': 'SP', 'attribute_name': 'QuaiArrivee', 'column': 3}
    SensExtArrivee = {'sheet_name': 'SP', 'attribute_name': 'SensExtArrivee', 'column': 4}
    QuaiDepart = {'sheet_name': 'SP', 'attribute_name': 'QuaiDepart', 'column': 5}
    SensExtDepart = {'sheet_name': 'SP', 'attribute_name': 'SensExtDepart', 'column': 6}
    RetournementSp = {'sheet_name': 'SP', 'attribute_name': 'RetournementSp', 'column': 7}
    TypeSigSp = {'sheet_name': 'SP', 'attribute_name': 'TypeSigSp', 'column': 8}
    SignalSortieQuai = {'sheet_name': 'SP', 'attribute_name': 'SignalSortieQuai', 'column': 9}
    PointArretAto = {'sheet_name': 'SP', 'attribute_name': 'PointArretAto', 'column': 10}


class Iti__RouteIvb:
    Ivb = {'sheet_name': 'Iti', 'attribute_name': 'RouteIvb', 'sub_attribute_name': 'Ivb', 'columns': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]}


class Iti__Aiguille:
    Nom = {'sheet_name': 'Iti', 'attribute_name': 'Aiguille', 'sub_attribute_name': 'Nom', 'columns': [26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54]}
    Position = {'sheet_name': 'Iti', 'attribute_name': 'Aiguille', 'sub_attribute_name': 'Position', 'columns': [27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55]}


class Iti:
    Nom = {'sheet_name': 'Iti', 'attribute_name': 'Nom', 'column': 1}
    SignalOrig = {'sheet_name': 'Iti', 'attribute_name': 'SignalOrig', 'column': 2}
    OriginIvb = {'sheet_name': 'Iti', 'attribute_name': 'OriginIvb', 'column': 3}
    RouteIvb = Iti__RouteIvb()
    DestinationIvb = {'sheet_name': 'Iti', 'attribute_name': 'DestinationIvb', 'column': 24}
    CdvDestEchap = {'sheet_name': 'Iti', 'attribute_name': 'CdvDestEchap', 'column': 25}
    Aiguille = Iti__Aiguille()


class CBTC_TER__Extremite:
    Seg = {'sheet_name': 'CBTC_TER', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51]}
    X = {'sheet_name': 'CBTC_TER', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52]}
    Sens = {'sheet_name': 'CBTC_TER', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Sens', 'columns': [11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53]}


class CBTC_TER__ItinerairesDeSortie:
    Iti = {'sheet_name': 'CBTC_TER', 'attribute_name': 'ItinerairesDeSortie', 'sub_attribute_name': 'Iti', 'columns': [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]}


class CBTC_TER__PointEntreeTerritoireCbtc:
    Seg = {'sheet_name': 'CBTC_TER', 'attribute_name': 'PointEntreeTerritoireCbtc', 'sub_attribute_name': 'Seg', 'columns': [74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122]}
    X = {'sheet_name': 'CBTC_TER', 'attribute_name': 'PointEntreeTerritoireCbtc', 'sub_attribute_name': 'X', 'columns': [75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123]}


class CBTC_TER:
    Nom = {'sheet_name': 'CBTC_TER', 'attribute_name': 'Nom', 'column': 1}
    TypeTerritoireCbtc = {'sheet_name': 'CBTC_TER', 'attribute_name': 'TypeTerritoireCbtc', 'column': 2}
    AtcOffAllowed = {'sheet_name': 'CBTC_TER', 'attribute_name': 'AtcOffAllowed', 'column': 3}
    EvacuationInhibition = {'sheet_name': 'CBTC_TER', 'attribute_name': 'EvacuationInhibition', 'column': 4}
    WaysideDelocAlarmInhibition = {'sheet_name': 'CBTC_TER', 'attribute_name': 'WaysideDelocAlarmInhibition', 'column': 5}
    SleepingOrLocMemorizationAllowed = {'sheet_name': 'CBTC_TER', 'attribute_name': 'SleepingOrLocMemorizationAllowed', 'column': 6}
    RadioCoverageType = {'sheet_name': 'CBTC_TER', 'attribute_name': 'RadioCoverageType', 'column': 7}
    RearSievingRequired = {'sheet_name': 'CBTC_TER', 'attribute_name': 'RearSievingRequired', 'column': 8}
    Extremite = CBTC_TER__Extremite()
    ItinerairesDeSortie = CBTC_TER__ItinerairesDeSortie()
    PointEntreeTerritoireCbtc = CBTC_TER__PointEntreeTerritoireCbtc()


class PAS__ExtremiteSuivi:
    Seg = {'sheet_name': 'PAS', 'attribute_name': 'ExtremiteSuivi', 'sub_attribute_name': 'Seg', 'columns': [5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95, 101, 107, 113, 119, 125, 131, 137, 143, 149, 155, 161, 167, 173, 179]}
    X = {'sheet_name': 'PAS', 'attribute_name': 'ExtremiteSuivi', 'sub_attribute_name': 'X', 'columns': [6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96, 102, 108, 114, 120, 126, 132, 138, 144, 150, 156, 162, 168, 174, 180]}
    Sens = {'sheet_name': 'PAS', 'attribute_name': 'ExtremiteSuivi', 'sub_attribute_name': 'Sens', 'columns': [7, 13, 19, 25, 31, 37, 43, 49, 55, 61, 67, 73, 79, 85, 91, 97, 103, 109, 115, 121, 127, 133, 139, 145, 151, 157, 163, 169, 175, 181]}
    Voie = {'sheet_name': 'PAS', 'attribute_name': 'ExtremiteSuivi', 'sub_attribute_name': 'Voie', 'columns': [8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86, 92, 98, 104, 110, 116, 122, 128, 134, 140, 146, 152, 158, 164, 170, 176, 182]}
    Pk = {'sheet_name': 'PAS', 'attribute_name': 'ExtremiteSuivi', 'sub_attribute_name': 'Pk', 'columns': [9, 15, 21, 27, 33, 39, 45, 51, 57, 63, 69, 75, 81, 87, 93, 99, 105, 111, 117, 123, 129, 135, 141, 147, 153, 159, 165, 171, 177, 183]}
    MaxDist = {'sheet_name': 'PAS', 'attribute_name': 'ExtremiteSuivi', 'sub_attribute_name': 'MaxDist', 'columns': [10, 16, 22, 28, 34, 40, 46, 52, 58, 64, 70, 76, 82, 88, 94, 100, 106, 112, 118, 124, 130, 136, 142, 148, 154, 160, 166, 172, 178, 184]}


class PAS__TronconsGeresParLePas:
    Troncon = {'sheet_name': 'PAS', 'attribute_name': 'TronconsGeresParLePas', 'sub_attribute_name': 'Troncon', 'columns': [185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204]}


class PAS:
    Nom = {'sheet_name': 'PAS', 'attribute_name': 'Nom', 'column': 1}
    TrackingAreaSubsetName = {'sheet_name': 'PAS', 'attribute_name': 'TrackingAreaSubsetName', 'column': 2}
    AtsZcId = {'sheet_name': 'PAS', 'attribute_name': 'AtsZcId', 'column': 3}
    DisplayableName = {'sheet_name': 'PAS', 'attribute_name': 'DisplayableName', 'column': 4}
    ExtremiteSuivi = PAS__ExtremiteSuivi()
    TronconsGeresParLePas = PAS__TronconsGeresParLePas()
    ConcealmentType = {'sheet_name': 'PAS', 'attribute_name': 'ConcealmentType', 'column': 205}
    TracksMultiConsists = {'sheet_name': 'PAS', 'attribute_name': 'TracksMultiConsists', 'column': 206}
    DynamicSievingEnabled = {'sheet_name': 'PAS', 'attribute_name': 'DynamicSievingEnabled', 'column': 207}


class Sas_ZSM_CBTC:
    Nom = {'sheet_name': 'Sas_ZSM_CBTC', 'attribute_name': 'Nom', 'column': 1}
    PasEmetteur = {'sheet_name': 'Sas_ZSM_CBTC', 'attribute_name': 'PasEmetteur', 'column': 2}
    ZsmCbtc = {'sheet_name': 'Sas_ZSM_CBTC', 'attribute_name': 'ZsmCbtc', 'column': 3}
    Rang = {'sheet_name': 'Sas_ZSM_CBTC', 'attribute_name': 'Rang', 'column': 4}
    PasRecepteur1 = {'sheet_name': 'Sas_ZSM_CBTC', 'attribute_name': 'PasRecepteur1', 'column': 5}
    PasRecepteur2 = {'sheet_name': 'Sas_ZSM_CBTC', 'attribute_name': 'PasRecepteur2', 'column': 6}
    PasRecepteur3 = {'sheet_name': 'Sas_ZSM_CBTC', 'attribute_name': 'PasRecepteur3', 'column': 7}
    PasRecepteur4 = {'sheet_name': 'Sas_ZSM_CBTC', 'attribute_name': 'PasRecepteur4', 'column': 8}


class DP:
    Nom = {'sheet_name': 'DP', 'attribute_name': 'Nom', 'column': 1}
    Type = {'sheet_name': 'DP', 'attribute_name': 'Type', 'column': 2}
    Seg = {'sheet_name': 'DP', 'attribute_name': 'Seg', 'column': 3}
    X = {'sheet_name': 'DP', 'attribute_name': 'X', 'column': 4}
    Voie = {'sheet_name': 'DP', 'attribute_name': 'Voie', 'column': 5}
    Pk = {'sheet_name': 'DP', 'attribute_name': 'Pk', 'column': 6}
    NumeroPcc = {'sheet_name': 'DP', 'attribute_name': 'NumeroPcc', 'column': 7}


class Sieving_Limit:
    Name = {'sheet_name': 'Sieving_Limit', 'attribute_name': 'Name', 'column': 1}
    Type = {'sheet_name': 'Sieving_Limit', 'attribute_name': 'Type', 'column': 2}
    RelatedBlock = {'sheet_name': 'Sieving_Limit', 'attribute_name': 'RelatedBlock', 'column': 3}
    Seg = {'sheet_name': 'Sieving_Limit', 'attribute_name': 'Seg', 'column': 4}
    X = {'sheet_name': 'Sieving_Limit', 'attribute_name': 'X', 'column': 5}
    Voie = {'sheet_name': 'Sieving_Limit', 'attribute_name': 'Voie', 'column': 6}
    Pk = {'sheet_name': 'Sieving_Limit', 'attribute_name': 'Pk', 'column': 7}
    Direction = {'sheet_name': 'Sieving_Limit', 'attribute_name': 'Direction', 'column': 8}


class ZSM_CBTC__SignauxZsm:
    Sigman = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'SignauxZsm', 'sub_attribute_name': 'Sigman', 'columns': [2, 3]}


class ZSM_CBTC__ExtZsm:
    Seg = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'ExtZsm', 'sub_attribute_name': 'Seg', 'columns': [4, 8]}
    X = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'ExtZsm', 'sub_attribute_name': 'X', 'columns': [5, 9]}
    Voie = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'ExtZsm', 'sub_attribute_name': 'Voie', 'columns': [6, 10]}
    Pk = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'ExtZsm', 'sub_attribute_name': 'Pk', 'columns': [7, 11]}


class ZSM_CBTC:
    Nom = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'Nom', 'column': 1}
    SignauxZsm = ZSM_CBTC__SignauxZsm()
    ExtZsm = ZSM_CBTC__ExtZsm()
    SegReference = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'SegReference', 'column': 12}
    SensAutorise = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'SensAutorise', 'column': 13}
    SensDefaut = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'SensDefaut', 'column': 14}
    InterlockingVirtualBlock = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'InterlockingVirtualBlock', 'column': 15}
    DefaultIxlDirection = {'sheet_name': 'ZSM_CBTC', 'attribute_name': 'DefaultIxlDirection', 'column': 16}


class SE__Extremite:
    Seg = {'sheet_name': 'SE', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}
    X = {'sheet_name': 'SE', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]}
    Sens = {'sheet_name': 'SE', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Sens', 'columns': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48]}
    Voie = {'sheet_name': 'SE', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77]}
    Pk = {'sheet_name': 'SE', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78]}


class SE:
    Nom = {'sheet_name': 'SE', 'attribute_name': 'Nom', 'column': 1}
    Type = {'sheet_name': 'SE', 'attribute_name': 'Type', 'column': 2}
    Ss = {'sheet_name': 'SE', 'attribute_name': 'Ss', 'column': 3}
    Extremite = SE__Extremite()
    NumeroPcc = {'sheet_name': 'SE', 'attribute_name': 'NumeroPcc', 'column': 79}


class SS__Extremite:
    Seg = {'sheet_name': 'SS', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44]}
    X = {'sheet_name': 'SS', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]}
    Sens = {'sheet_name': 'SS', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Sens', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}
    Voie = {'sheet_name': 'SS', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75]}
    Pk = {'sheet_name': 'SS', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76]}


class SS:
    Nom = {'sheet_name': 'SS', 'attribute_name': 'Nom', 'column': 1}
    Extremite = SS__Extremite()


class ZCI__Extremite:
    Seg = {'sheet_name': 'ZCI', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90]}
    X = {'sheet_name': 'ZCI', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91]}
    Sens = {'sheet_name': 'ZCI', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Sens', 'columns': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 89, 92]}
    Voie = {'sheet_name': 'ZCI', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151]}
    Pk = {'sheet_name': 'ZCI', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152]}


class ZCI:
    Nom = {'sheet_name': 'ZCI', 'attribute_name': 'Nom', 'column': 1}
    NomPas = {'sheet_name': 'ZCI', 'attribute_name': 'NomPas', 'column': 2}
    Extremite = ZCI__Extremite()


class Zaum__Extremite:
    Seg = {'sheet_name': 'Zaum', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55]}
    X = {'sheet_name': 'Zaum', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56]}
    Sens = {'sheet_name': 'Zaum', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Sens', 'columns': [15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57]}
    Voie = {'sheet_name': 'Zaum', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86]}
    Pk = {'sheet_name': 'Zaum', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87]}


class Zaum:
    Nom = {'sheet_name': 'Zaum', 'attribute_name': 'Nom', 'column': 1}
    QuaiAlarme1 = {'sheet_name': 'Zaum', 'attribute_name': 'QuaiAlarme1', 'column': 2}
    QuaiAlarme2 = {'sheet_name': 'Zaum', 'attribute_name': 'QuaiAlarme2', 'column': 3}
    TronconPreferentiel = {'sheet_name': 'Zaum', 'attribute_name': 'TronconPreferentiel', 'column': 4}
    AtsId = {'sheet_name': 'Zaum', 'attribute_name': 'AtsId', 'column': 5}
    DisplayableName = {'sheet_name': 'Zaum', 'attribute_name': 'DisplayableName', 'column': 6}
    DriverlessAuthorized = {'sheet_name': 'Zaum', 'attribute_name': 'DriverlessAuthorized', 'column': 7}
    AutomaticAuthorized = {'sheet_name': 'Zaum', 'attribute_name': 'AutomaticAuthorized', 'column': 8}
    EvacuationProtectionZoneName = {'sheet_name': 'Zaum', 'attribute_name': 'EvacuationProtectionZoneName', 'column': 9}
    IntegrityProtectionZoneName = {'sheet_name': 'Zaum', 'attribute_name': 'IntegrityProtectionZoneName', 'column': 10}
    DelocalizationProtectionZoneName = {'sheet_name': 'Zaum', 'attribute_name': 'DelocalizationProtectionZoneName', 'column': 11}
    DerailmentObstacleProtectionZoneName = {'sheet_name': 'Zaum', 'attribute_name': 'DerailmentObstacleProtectionZoneName', 'column': 12}
    Extremite = Zaum__Extremite()


class ZCRA__MouvZcra:
    PtArretOrig = {'sheet_name': 'ZCRA', 'attribute_name': 'MouvZcra', 'sub_attribute_name': 'PtArretOrig', 'columns': [4, 9, 14]}
    PtArretInter = {'sheet_name': 'ZCRA', 'attribute_name': 'MouvZcra', 'sub_attribute_name': 'PtArretInter', 'columns': [5, 10, 15]}
    PtArretDest = {'sheet_name': 'ZCRA', 'attribute_name': 'MouvZcra', 'sub_attribute_name': 'PtArretDest', 'columns': [6, 11, 16]}
    QuaiOrigine = {'sheet_name': 'ZCRA', 'attribute_name': 'MouvZcra', 'sub_attribute_name': 'QuaiOrigine', 'columns': [7, 12, 17]}
    SensExtOrigine = {'sheet_name': 'ZCRA', 'attribute_name': 'MouvZcra', 'sub_attribute_name': 'SensExtOrigine', 'columns': [8, 13, 18]}


class ZCRA__Extremite:
    Seg = {'sheet_name': 'ZCRA', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61]}
    X = {'sheet_name': 'ZCRA', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62]}
    Sens = {'sheet_name': 'ZCRA', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Sens', 'columns': [21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63]}
    Voie = {'sheet_name': 'ZCRA', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92]}
    Pk = {'sheet_name': 'ZCRA', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93]}


class ZCRA:
    Nom = {'sheet_name': 'ZCRA', 'attribute_name': 'Nom', 'column': 1}
    TronconPreferentiel = {'sheet_name': 'ZCRA', 'attribute_name': 'TronconPreferentiel', 'column': 2}
    PresenceAdc = {'sheet_name': 'ZCRA', 'attribute_name': 'PresenceAdc', 'column': 3}
    MouvZcra = ZCRA__MouvZcra()
    Extremite = ZCRA__Extremite()


class Zacp__Extremite:
    Seg = {'sheet_name': 'Zacp', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]}
    X = {'sheet_name': 'Zacp', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]}
    Sens = {'sheet_name': 'Zacp', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Sens', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]}
    Voie = {'sheet_name': 'Zacp', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [32, 34, 36, 38, 40, 42, 44, 46, 48, 50]}
    Pk = {'sheet_name': 'Zacp', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [33, 35, 37, 39, 41, 43, 45, 47, 49, 51]}


class Zacp:
    Nom = {'sheet_name': 'Zacp', 'attribute_name': 'Nom', 'column': 1}
    Extremite = Zacp__Extremite()


class ZLPV__De:
    Seg = {'sheet_name': 'ZLPV', 'attribute_name': 'De', 'sub_attribute_name': 'Seg', 'columns': [2]}
    X = {'sheet_name': 'ZLPV', 'attribute_name': 'De', 'sub_attribute_name': 'X', 'columns': [3]}
    DistanceAnticipation = {'sheet_name': 'ZLPV', 'attribute_name': 'De', 'sub_attribute_name': 'DistanceAnticipation', 'columns': [4]}
    Voie = {'sheet_name': 'ZLPV', 'attribute_name': 'De', 'sub_attribute_name': 'Voie', 'columns': [8]}
    Pk = {'sheet_name': 'ZLPV', 'attribute_name': 'De', 'sub_attribute_name': 'Pk', 'columns': [9]}


class ZLPV__A:
    Seg = {'sheet_name': 'ZLPV', 'attribute_name': 'A', 'sub_attribute_name': 'Seg', 'columns': [5]}
    X = {'sheet_name': 'ZLPV', 'attribute_name': 'A', 'sub_attribute_name': 'X', 'columns': [6]}
    DistanceAnticipation = {'sheet_name': 'ZLPV', 'attribute_name': 'A', 'sub_attribute_name': 'DistanceAnticipation', 'columns': [7]}
    Voie = {'sheet_name': 'ZLPV', 'attribute_name': 'A', 'sub_attribute_name': 'Voie', 'columns': [10]}
    Pk = {'sheet_name': 'ZLPV', 'attribute_name': 'A', 'sub_attribute_name': 'Pk', 'columns': [11]}


class ZLPV:
    VitesseZlpv = {'sheet_name': 'ZLPV', 'attribute_name': 'VitesseZlpv', 'column': 1}
    De = ZLPV__De()
    A = ZLPV__A()


class NV_PSR__From:
    Seg = {'sheet_name': 'NV_PSR', 'attribute_name': 'From', 'sub_attribute_name': 'Seg', 'columns': [3]}
    X = {'sheet_name': 'NV_PSR', 'attribute_name': 'From', 'sub_attribute_name': 'X', 'columns': [4]}
    Track = {'sheet_name': 'NV_PSR', 'attribute_name': 'From', 'sub_attribute_name': 'Track', 'columns': [7]}
    Kp = {'sheet_name': 'NV_PSR', 'attribute_name': 'From', 'sub_attribute_name': 'Kp', 'columns': [8]}


class NV_PSR__To:
    Seg = {'sheet_name': 'NV_PSR', 'attribute_name': 'To', 'sub_attribute_name': 'Seg', 'columns': [5]}
    X = {'sheet_name': 'NV_PSR', 'attribute_name': 'To', 'sub_attribute_name': 'X', 'columns': [6]}
    Track = {'sheet_name': 'NV_PSR', 'attribute_name': 'To', 'sub_attribute_name': 'Track', 'columns': [9]}
    Kp = {'sheet_name': 'NV_PSR', 'attribute_name': 'To', 'sub_attribute_name': 'Kp', 'columns': [10]}


class NV_PSR:
    Name = {'sheet_name': 'NV_PSR', 'attribute_name': 'Name', 'column': 1}
    SpeedValue = {'sheet_name': 'NV_PSR', 'attribute_name': 'SpeedValue', 'column': 2}
    From = NV_PSR__From()
    To = NV_PSR__To()
    AtsId = {'sheet_name': 'NV_PSR', 'attribute_name': 'AtsId', 'column': 11}
    WithRelaxation = {'sheet_name': 'NV_PSR', 'attribute_name': 'WithRelaxation', 'column': 12}
    RelaxationCause = {'sheet_name': 'NV_PSR', 'attribute_name': 'RelaxationCause', 'column': 13}
    CeilingSpeedValue = {'sheet_name': 'NV_PSR', 'attribute_name': 'CeilingSpeedValue', 'column': 14}


class ZLPV_Or__De:
    Seg = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'De', 'sub_attribute_name': 'Seg', 'columns': [4]}
    X = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'De', 'sub_attribute_name': 'X', 'columns': [5]}
    Voie = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'De', 'sub_attribute_name': 'Voie', 'columns': [8]}
    Pk = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'De', 'sub_attribute_name': 'Pk', 'columns': [9]}


class ZLPV_Or__A:
    Seg = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'A', 'sub_attribute_name': 'Seg', 'columns': [6]}
    X = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'A', 'sub_attribute_name': 'X', 'columns': [7]}
    Voie = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'A', 'sub_attribute_name': 'Voie', 'columns': [10]}
    Pk = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'A', 'sub_attribute_name': 'Pk', 'columns': [11]}


class ZLPV_Or:
    VitesseZlpv = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'VitesseZlpv', 'column': 1}
    Sens = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'Sens', 'column': 2}
    DistanceAnticipation = {'sheet_name': 'ZLPV_Or', 'attribute_name': 'DistanceAnticipation', 'column': 3}
    De = ZLPV_Or__De()
    A = ZLPV_Or__A()


class Calib:
    BaliseDeb = {'sheet_name': 'Calib', 'attribute_name': 'BaliseDeb', 'column': 1}
    BaliseFin = {'sheet_name': 'Calib', 'attribute_name': 'BaliseFin', 'column': 2}
    DistanceCalib = {'sheet_name': 'Calib', 'attribute_name': 'DistanceCalib', 'column': 3}
    SensCalib = {'sheet_name': 'Calib', 'attribute_name': 'SensCalib', 'column': 4}


class Zman:
    Nom = {'sheet_name': 'Zman', 'attribute_name': 'Nom', 'column': 1}
    SigZman1 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman1', 'column': 2}
    SigZman2 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman2', 'column': 3}
    SigZman3 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman3', 'column': 4}
    SigZman4 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman4', 'column': 5}
    SigZman5 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman5', 'column': 6}
    SigZman6 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman6', 'column': 7}
    SigZman7 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman7', 'column': 8}
    SigZman8 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman8', 'column': 9}
    SigZman9 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman9', 'column': 10}
    SigZman10 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman10', 'column': 11}
    SigZman11 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman11', 'column': 12}
    SigZman12 = {'sheet_name': 'Zman', 'attribute_name': 'SigZman12', 'column': 13}
    Ivb1 = {'sheet_name': 'Zman', 'attribute_name': 'Ivb1', 'column': 14}
    Ivb2 = {'sheet_name': 'Zman', 'attribute_name': 'Ivb2', 'column': 15}
    Ivb3 = {'sheet_name': 'Zman', 'attribute_name': 'Ivb3', 'column': 16}
    Ivb4 = {'sheet_name': 'Zman', 'attribute_name': 'Ivb4', 'column': 17}
    Ivb5 = {'sheet_name': 'Zman', 'attribute_name': 'Ivb5', 'column': 18}
    Ivb6 = {'sheet_name': 'Zman', 'attribute_name': 'Ivb6', 'column': 19}
    Ivb7 = {'sheet_name': 'Zman', 'attribute_name': 'Ivb7', 'column': 20}
    Ivb8 = {'sheet_name': 'Zman', 'attribute_name': 'Ivb8', 'column': 21}
    Ivb9 = {'sheet_name': 'Zman', 'attribute_name': 'Ivb9', 'column': 22}
    Ivb10 = {'sheet_name': 'Zman', 'attribute_name': 'Ivb10', 'column': 23}


class ZVR__Extremite:
    Seg = {'sheet_name': 'ZVR', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Seg', 'columns': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]}
    X = {'sheet_name': 'ZVR', 'attribute_name': 'Extremite', 'sub_attribute_name': 'X', 'columns': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]}
    Sens = {'sheet_name': 'ZVR', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Sens', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]}
    Voie = {'sheet_name': 'ZVR', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Voie', 'columns': [32, 34, 36, 38, 40, 42, 44, 46, 48, 50]}
    Pk = {'sheet_name': 'ZVR', 'attribute_name': 'Extremite', 'sub_attribute_name': 'Pk', 'columns': [33, 35, 37, 39, 41, 43, 45, 47, 49, 51]}


class ZVR:
    Nom = {'sheet_name': 'ZVR', 'attribute_name': 'Nom', 'column': 1}
    Extremite = ZVR__Extremite()


class CBTC_Eqpt__Equipements:
    Eqpt = {'sheet_name': 'CBTC_Eqpt', 'attribute_name': 'Equipements', 'sub_attribute_name': 'Eqpt', 'columns': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}


class CBTC_Eqpt:
    Signal = {'sheet_name': 'CBTC_Eqpt', 'attribute_name': 'Signal', 'column': 1}
    Equipements = CBTC_Eqpt__Equipements()


class Flux_Variant_HF:
    Nom = {'sheet_name': 'Flux_Variant_HF', 'attribute_name': 'Nom', 'column': 1}
    ClasseObjet = {'sheet_name': 'Flux_Variant_HF', 'attribute_name': 'ClasseObjet', 'column': 2}
    NomObjet = {'sheet_name': 'Flux_Variant_HF', 'attribute_name': 'NomObjet', 'column': 3}
    NomLogiqueInfo = {'sheet_name': 'Flux_Variant_HF', 'attribute_name': 'NomLogiqueInfo', 'column': 4}
    TypeFoncSecu = {'sheet_name': 'Flux_Variant_HF', 'attribute_name': 'TypeFoncSecu', 'column': 5}
    Troncon = {'sheet_name': 'Flux_Variant_HF', 'attribute_name': 'Troncon', 'column': 6}
    Message = {'sheet_name': 'Flux_Variant_HF', 'attribute_name': 'Message', 'column': 7}
    RgInfo = {'sheet_name': 'Flux_Variant_HF', 'attribute_name': 'RgInfo', 'column': 8}
    CommentaireDeGeneration = {'sheet_name': 'Flux_Variant_HF', 'attribute_name': 'CommentaireDeGeneration', 'column': 9}


class Flux_Variant_BF:
    Nom = {'sheet_name': 'Flux_Variant_BF', 'attribute_name': 'Nom', 'column': 1}
    ClasseObjet = {'sheet_name': 'Flux_Variant_BF', 'attribute_name': 'ClasseObjet', 'column': 2}
    NomObjet = {'sheet_name': 'Flux_Variant_BF', 'attribute_name': 'NomObjet', 'column': 3}
    NomLogiqueInfo = {'sheet_name': 'Flux_Variant_BF', 'attribute_name': 'NomLogiqueInfo', 'column': 4}
    TypeFoncSecu = {'sheet_name': 'Flux_Variant_BF', 'attribute_name': 'TypeFoncSecu', 'column': 5}
    Troncon = {'sheet_name': 'Flux_Variant_BF', 'attribute_name': 'Troncon', 'column': 6}
    Message = {'sheet_name': 'Flux_Variant_BF', 'attribute_name': 'Message', 'column': 7}
    RgInfo = {'sheet_name': 'Flux_Variant_BF', 'attribute_name': 'RgInfo', 'column': 8}
    CommentaireDeGeneration = {'sheet_name': 'Flux_Variant_BF', 'attribute_name': 'CommentaireDeGeneration', 'column': 9}


class Wayside_Eqpt__Function:
    Zc = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'Zc', 'columns': [3]}
    Oc = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'Oc', 'columns': [4]}
    RdIxl = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'RdIxl', 'columns': [5]}
    Zcr = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'Zcr', 'columns': [6]}
    Psd = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'Psd', 'columns': [7]}
    Ups = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'Ups', 'columns': [8]}
    Ftm = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'Ftm', 'columns': [9]}
    Dcs = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'Dcs', 'columns': [10]}


class Wayside_Eqpt:
    Name = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'Name', 'column': 1}
    EqptId = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'EqptId', 'column': 2}
    Function = Wayside_Eqpt__Function()
    OcType = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'OcType', 'column': 11}
    Location = {'sheet_name': 'Wayside_Eqpt', 'attribute_name': 'Location', 'column': 12}


class Flux_MES_PAS:
    Nom = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'Nom', 'column': 1}
    NomMes = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'NomMes', 'column': 2}
    ClasseObjet = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'ClasseObjet', 'column': 3}
    NomObjet = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'NomObjet', 'column': 4}
    NomLogiqueInfo = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'NomLogiqueInfo', 'column': 5}
    TypeInfo = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'TypeInfo', 'column': 6}
    Message = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'Message', 'column': 7}
    Extension = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'Extension', 'column': 8}
    RgInfo = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'RgInfo', 'column': 9}
    PasUtilisateur1 = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'PasUtilisateur1', 'column': 10}
    PasUtilisateur2 = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'PasUtilisateur2', 'column': 11}
    PasUtilisateur3 = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'PasUtilisateur3', 'column': 12}
    PasUtilisateur4 = {'sheet_name': 'Flux_MES_PAS', 'attribute_name': 'PasUtilisateur4', 'column': 13}


class Flux_PAS_MES:
    Nom = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'Nom', 'column': 1}
    NomMes = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'NomMes', 'column': 2}
    ClasseObjet = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'ClasseObjet', 'column': 3}
    NomObjet = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'NomObjet', 'column': 4}
    NomLogiqueInfo = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'NomLogiqueInfo', 'column': 5}
    TypeInfo = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'TypeInfo', 'column': 6}
    Message = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'Message', 'column': 7}
    Extension = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'Extension', 'column': 8}
    RgInfo = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'RgInfo', 'column': 9}
    PasUtilisateur1 = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'PasUtilisateur1', 'column': 10}
    PasUtilisateur2 = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'PasUtilisateur2', 'column': 11}
    PasUtilisateur3 = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'PasUtilisateur3', 'column': 12}
    PasUtilisateur4 = {'sheet_name': 'Flux_PAS_MES', 'attribute_name': 'PasUtilisateur4', 'column': 13}


class ATS_ATC:
    Nom = {'sheet_name': 'ATS_ATC', 'attribute_name': 'Nom', 'column': 1}
    ClasseObjet = {'sheet_name': 'ATS_ATC', 'attribute_name': 'ClasseObjet', 'column': 2}
    NomObjet = {'sheet_name': 'ATS_ATC', 'attribute_name': 'NomObjet', 'column': 3}
    NomLogiqueInfoAts = {'sheet_name': 'ATS_ATC', 'attribute_name': 'NomLogiqueInfoAts', 'column': 4}
    NomMessage = {'sheet_name': 'ATS_ATC', 'attribute_name': 'NomMessage', 'column': 5}
    RgInfo = {'sheet_name': 'ATS_ATC', 'attribute_name': 'RgInfo', 'column': 6}


class TM_MES_ATS:
    Nom = {'sheet_name': 'TM_MES_ATS', 'attribute_name': 'Nom', 'column': 1}
    Equipement = {'sheet_name': 'TM_MES_ATS', 'attribute_name': 'Equipement', 'column': 2}
    ClasseObjet = {'sheet_name': 'TM_MES_ATS', 'attribute_name': 'ClasseObjet', 'column': 3}
    NomObjet = {'sheet_name': 'TM_MES_ATS', 'attribute_name': 'NomObjet', 'column': 4}
    NomLogiqueInfoAts = {'sheet_name': 'TM_MES_ATS', 'attribute_name': 'NomLogiqueInfoAts', 'column': 5}
    NomMessage = {'sheet_name': 'TM_MES_ATS', 'attribute_name': 'NomMessage', 'column': 6}
    RgInfo = {'sheet_name': 'TM_MES_ATS', 'attribute_name': 'RgInfo', 'column': 7}


class TM_PAS_ATS:
    Nom = {'sheet_name': 'TM_PAS_ATS', 'attribute_name': 'Nom', 'column': 1}
    Equipement = {'sheet_name': 'TM_PAS_ATS', 'attribute_name': 'Equipement', 'column': 2}
    ClasseObjet = {'sheet_name': 'TM_PAS_ATS', 'attribute_name': 'ClasseObjet', 'column': 3}
    NomObjet = {'sheet_name': 'TM_PAS_ATS', 'attribute_name': 'NomObjet', 'column': 4}
    NomLogiqueInfoAts = {'sheet_name': 'TM_PAS_ATS', 'attribute_name': 'NomLogiqueInfoAts', 'column': 5}
    NomMessage = {'sheet_name': 'TM_PAS_ATS', 'attribute_name': 'NomMessage', 'column': 6}
    RgInfo = {'sheet_name': 'TM_PAS_ATS', 'attribute_name': 'RgInfo', 'column': 7}


class Network:
    Name = {'sheet_name': 'Network', 'attribute_name': 'Name', 'column': 1}
    Type = {'sheet_name': 'Network', 'attribute_name': 'Type', 'column': 2}
    Line = {'sheet_name': 'Network', 'attribute_name': 'Line', 'column': 3}
    BaseAddress = {'sheet_name': 'Network', 'attribute_name': 'BaseAddress', 'column': 4}
    Medium = {'sheet_name': 'Network', 'attribute_name': 'Medium', 'column': 5}
    Mask = {'sheet_name': 'Network', 'attribute_name': 'Mask', 'column': 6}
    Gateway = {'sheet_name': 'Network', 'attribute_name': 'Gateway', 'column': 7}
    Port = {'sheet_name': 'Network', 'attribute_name': 'Port', 'column': 8}
    OverallMask = {'sheet_name': 'Network', 'attribute_name': 'OverallMask', 'column': 9}
    CcMulticastAddress = {'sheet_name': 'Network', 'attribute_name': 'CcMulticastAddress', 'column': 10}
    PisMulticastAddress = {'sheet_name': 'Network', 'attribute_name': 'PisMulticastAddress', 'column': 11}
    CcTmsMulticastAddress = {'sheet_name': 'Network', 'attribute_name': 'CcTmsMulticastAddress', 'column': 12}
    TmsCcMulticastAddress = {'sheet_name': 'Network', 'attribute_name': 'TmsCcMulticastAddress', 'column': 13}


class LineSection_Eqpt:
    Name = {'sheet_name': 'LineSection_Eqpt', 'attribute_name': 'Name', 'column': 1}
    EqptId = {'sheet_name': 'LineSection_Eqpt', 'attribute_name': 'EqptId', 'column': 2}
    Type = {'sheet_name': 'LineSection_Eqpt', 'attribute_name': 'Type', 'column': 3}
    Zone = {'sheet_name': 'LineSection_Eqpt', 'attribute_name': 'Zone', 'column': 4}


class OnBoard_Eqpt__Function:
    IsRealCc = {'sheet_name': 'OnBoard_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'IsRealCc', 'columns': [3]}
    IsVirtualCc = {'sheet_name': 'OnBoard_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'IsVirtualCc', 'columns': [4]}
    IsTod = {'sheet_name': 'OnBoard_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'IsTod', 'columns': [5]}
    IsPis = {'sheet_name': 'OnBoard_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'IsPis', 'columns': [6]}
    IsTar = {'sheet_name': 'OnBoard_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'IsTar', 'columns': [7]}
    IsTmsBox = {'sheet_name': 'OnBoard_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'IsTmsBox', 'columns': [8]}
    IsPwmBox = {'sheet_name': 'OnBoard_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'IsPwmBox', 'columns': [9]}
    IsStreamBox = {'sheet_name': 'OnBoard_Eqpt', 'attribute_name': 'Function', 'sub_attribute_name': 'IsStreamBox', 'columns': [10]}


class OnBoard_Eqpt:
    Name = {'sheet_name': 'OnBoard_Eqpt', 'attribute_name': 'Name', 'column': 1}
    EqptId = {'sheet_name': 'OnBoard_Eqpt', 'attribute_name': 'EqptId', 'column': 2}
    Function = OnBoard_Eqpt__Function()


class Interstation:
    Nom = {'sheet_name': 'Interstation', 'attribute_name': 'Nom', 'column': 1}
    QuaiOrigine = {'sheet_name': 'Interstation', 'attribute_name': 'QuaiOrigine', 'column': 2}
    QuaiDestination = {'sheet_name': 'Interstation', 'attribute_name': 'QuaiDestination', 'column': 3}
    SensLigne = {'sheet_name': 'Interstation', 'attribute_name': 'SensLigne', 'column': 4}


class IATPM_tags__Routes:
    Route = {'sheet_name': 'IATPM_tags', 'attribute_name': 'Routes', 'sub_attribute_name': 'Route', 'columns': [11, 12, 13, 14, 15, 16]}


class IATPM_tags__VitalStoppingPoint:
    Seg = {'sheet_name': 'IATPM_tags', 'attribute_name': 'VitalStoppingPoint', 'sub_attribute_name': 'Seg', 'columns': [18]}
    X = {'sheet_name': 'IATPM_tags', 'attribute_name': 'VitalStoppingPoint', 'sub_attribute_name': 'X', 'columns': [19]}
    Track = {'sheet_name': 'IATPM_tags', 'attribute_name': 'VitalStoppingPoint', 'sub_attribute_name': 'Track', 'columns': [20]}
    Kp = {'sheet_name': 'IATPM_tags', 'attribute_name': 'VitalStoppingPoint', 'sub_attribute_name': 'Kp', 'columns': [21]}


class IATPM_tags__ImcTimeout:
    Distance = {'sheet_name': 'IATPM_tags', 'attribute_name': 'ImcTimeout', 'sub_attribute_name': 'Distance', 'columns': [25]}
    Value = {'sheet_name': 'IATPM_tags', 'attribute_name': 'ImcTimeout', 'sub_attribute_name': 'Value', 'columns': [26]}


class IATPM_tags__DmcTimeout:
    Distance = {'sheet_name': 'IATPM_tags', 'attribute_name': 'DmcTimeout', 'sub_attribute_name': 'Distance', 'columns': [27]}
    Value = {'sheet_name': 'IATPM_tags', 'attribute_name': 'DmcTimeout', 'sub_attribute_name': 'Value', 'columns': [28]}


class IATPM_tags:
    Name = {'sheet_name': 'IATPM_tags', 'attribute_name': 'Name', 'column': 1}
    BaliseName = {'sheet_name': 'IATPM_tags', 'attribute_name': 'BaliseName', 'column': 2}
    Type = {'sheet_name': 'IATPM_tags', 'attribute_name': 'Type', 'column': 3}
    NumTagSeg = {'sheet_name': 'IATPM_tags', 'attribute_name': 'NumTagSeg', 'column': 4}
    Seg = {'sheet_name': 'IATPM_tags', 'attribute_name': 'Seg', 'column': 5}
    X = {'sheet_name': 'IATPM_tags', 'attribute_name': 'X', 'column': 6}
    Voie = {'sheet_name': 'IATPM_tags', 'attribute_name': 'Voie', 'column': 7}
    Pk = {'sheet_name': 'IATPM_tags', 'attribute_name': 'Pk', 'column': 8}
    LayingType = {'sheet_name': 'IATPM_tags', 'attribute_name': 'LayingType', 'column': 9}
    Signal = {'sheet_name': 'IATPM_tags', 'attribute_name': 'Signal', 'column': 10}
    Routes = IATPM_tags__Routes()
    StopSignal = {'sheet_name': 'IATPM_tags', 'attribute_name': 'StopSignal', 'column': 17}
    VitalStoppingPoint = IATPM_tags__VitalStoppingPoint()
    WithOverlap = {'sheet_name': 'IATPM_tags', 'attribute_name': 'WithOverlap', 'column': 22}
    OverlapName = {'sheet_name': 'IATPM_tags', 'attribute_name': 'OverlapName', 'column': 23}
    OverlapReleaseDistance = {'sheet_name': 'IATPM_tags', 'attribute_name': 'OverlapReleaseDistance', 'column': 24}
    ImcTimeout = IATPM_tags__ImcTimeout()
    DmcTimeout = IATPM_tags__DmcTimeout()


class IATPM_Version_Tags:
    Name = {'sheet_name': 'IATPM_Version_Tags', 'attribute_name': 'Name', 'column': 1}
    BaliseName = {'sheet_name': 'IATPM_Version_Tags', 'attribute_name': 'BaliseName', 'column': 2}
    Seg = {'sheet_name': 'IATPM_Version_Tags', 'attribute_name': 'Seg', 'column': 3}
    X = {'sheet_name': 'IATPM_Version_Tags', 'attribute_name': 'X', 'column': 4}


class DynTag_Group__TagList:
    Tag = {'sheet_name': 'DynTag_Group', 'attribute_name': 'TagList', 'sub_attribute_name': 'Tag', 'columns': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]}


class DynTag_Group:
    Name = {'sheet_name': 'DynTag_Group', 'attribute_name': 'Name', 'column': 1}
    Id = {'sheet_name': 'DynTag_Group', 'attribute_name': 'Id', 'column': 2}
    TagList = DynTag_Group__TagList()


class Border_Area__Aiguille:
    Nom = {'sheet_name': 'Border_Area', 'attribute_name': 'Aiguille', 'sub_attribute_name': 'Nom', 'columns': [22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]}
    Position = {'sheet_name': 'Border_Area', 'attribute_name': 'Aiguille', 'sub_attribute_name': 'Position', 'columns': [23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51]}


class Border_Area:
    Name = {'sheet_name': 'Border_Area', 'attribute_name': 'Name', 'column': 1}
    Block1 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block1', 'column': 2}
    Block2 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block2', 'column': 3}
    Block3 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block3', 'column': 4}
    Block4 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block4', 'column': 5}
    Block5 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block5', 'column': 6}
    Block6 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block6', 'column': 7}
    Block7 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block7', 'column': 8}
    Block8 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block8', 'column': 9}
    Block9 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block9', 'column': 10}
    Block10 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block10', 'column': 11}
    Block11 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block11', 'column': 12}
    Block12 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block12', 'column': 13}
    Block13 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block13', 'column': 14}
    Block14 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block14', 'column': 15}
    Block15 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block15', 'column': 16}
    Block16 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block16', 'column': 17}
    Block17 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block17', 'column': 18}
    Block18 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block18', 'column': 19}
    Block19 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block19', 'column': 20}
    Block20 = {'sheet_name': 'Border_Area', 'attribute_name': 'Block20', 'column': 21}
    Aiguille = Border_Area__Aiguille()


class OVL_Border_Area:
    Nom = {'sheet_name': 'OVL_Border_Area', 'attribute_name': 'Nom', 'column': 1}
    SenderZc = {'sheet_name': 'OVL_Border_Area', 'attribute_name': 'SenderZc', 'column': 2}
    BorderArea = {'sheet_name': 'OVL_Border_Area', 'attribute_name': 'BorderArea', 'column': 3}
    Rank = {'sheet_name': 'OVL_Border_Area', 'attribute_name': 'Rank', 'column': 4}
    ZcReceiver1 = {'sheet_name': 'OVL_Border_Area', 'attribute_name': 'ZcReceiver1', 'column': 5}
    ZcReceiver2 = {'sheet_name': 'OVL_Border_Area', 'attribute_name': 'ZcReceiver2', 'column': 6}
    ZcReceiver3 = {'sheet_name': 'OVL_Border_Area', 'attribute_name': 'ZcReceiver3', 'column': 7}
    ZcReceiver4 = {'sheet_name': 'OVL_Border_Area', 'attribute_name': 'ZcReceiver4', 'column': 8}


class IXL_Overlap__VitalStoppingPoint:
    Seg = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'VitalStoppingPoint', 'sub_attribute_name': 'Seg', 'columns': [5]}
    X = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'VitalStoppingPoint', 'sub_attribute_name': 'X', 'columns': [6]}
    Sens = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'VitalStoppingPoint', 'sub_attribute_name': 'Sens', 'columns': [7]}
    Voie = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'VitalStoppingPoint', 'sub_attribute_name': 'Voie', 'columns': [8]}
    Pk = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'VitalStoppingPoint', 'sub_attribute_name': 'Pk', 'columns': [9]}


class IXL_Overlap__ReleasePoint:
    Seg = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'ReleasePoint', 'sub_attribute_name': 'Seg', 'columns': [10]}
    X = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'ReleasePoint', 'sub_attribute_name': 'X', 'columns': [11]}
    Track = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'ReleasePoint', 'sub_attribute_name': 'Track', 'columns': [12]}
    Kp = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'ReleasePoint', 'sub_attribute_name': 'Kp', 'columns': [13]}


class IXL_Overlap__Aiguille:
    Nom = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'Aiguille', 'sub_attribute_name': 'Nom', 'columns': [15, 17, 19, 21]}
    Position = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'Aiguille', 'sub_attribute_name': 'Position', 'columns': [16, 18, 20, 22]}


class IXL_Overlap:
    Name = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'Name', 'column': 1}
    DestinationSignal = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'DestinationSignal', 'column': 2}
    PlatformRelated = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'PlatformRelated', 'column': 3}
    WithTpp = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'WithTpp', 'column': 4}
    VitalStoppingPoint = IXL_Overlap__VitalStoppingPoint()
    ReleasePoint = IXL_Overlap__ReleasePoint()
    ReleaseTimerValue = {'sheet_name': 'IXL_Overlap', 'attribute_name': 'ReleaseTimerValue', 'column': 14}
    Aiguille = IXL_Overlap__Aiguille()


class Driving_Modes:
    Name = {'sheet_name': 'Driving_Modes', 'attribute_name': 'Name', 'column': 1}
    Group = {'sheet_name': 'Driving_Modes', 'attribute_name': 'Group', 'column': 2}
    Code = {'sheet_name': 'Driving_Modes', 'attribute_name': 'Code', 'column': 3}
    Abbreviation = {'sheet_name': 'Driving_Modes', 'attribute_name': 'Abbreviation', 'column': 4}


class Unprotected_Moves__Blocks:
    Block = {'sheet_name': 'Unprotected_Moves', 'attribute_name': 'Blocks', 'sub_attribute_name': 'Block', 'columns': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}


class Unprotected_Moves:
    Name = {'sheet_name': 'Unprotected_Moves', 'attribute_name': 'Name', 'column': 1}
    Blocks = Unprotected_Moves__Blocks()


class CBTC_Overlap__Switch:
    Name = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Switch', 'sub_attribute_name': 'Name', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]}
    Position = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Switch', 'sub_attribute_name': 'Position', 'columns': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}


class CBTC_Overlap:
    Name = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Name', 'column': 1}
    Signal = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Signal', 'column': 2}
    Block1 = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Block1', 'column': 3}
    Switch = CBTC_Overlap__Switch()
    Block2 = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Block2', 'column': 6}
    Block3 = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Block3', 'column': 9}
    Block4 = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Block4', 'column': 12}
    Block5 = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Block5', 'column': 15}
    Block6 = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Block6', 'column': 18}
    Block7 = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Block7', 'column': 21}
    Block8 = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Block8', 'column': 24}
    Block9 = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Block9', 'column': 27}
    Block10 = {'sheet_name': 'CBTC_Overlap', 'attribute_name': 'Block10', 'column': 30}


class Performance_Level:
    Name = {'sheet_name': 'Performance_Level', 'attribute_name': 'Name', 'column': 1}
    MaxAtoSpeed = {'sheet_name': 'Performance_Level', 'attribute_name': 'MaxAtoSpeed', 'column': 2}
    PercOfAtoSpeed = {'sheet_name': 'Performance_Level', 'attribute_name': 'PercOfAtoSpeed', 'column': 3}
    MaxAccel = {'sheet_name': 'Performance_Level', 'attribute_name': 'MaxAccel', 'column': 4}
    MaxDecel = {'sheet_name': 'Performance_Level', 'attribute_name': 'MaxDecel', 'column': 5}
    AtsId = {'sheet_name': 'Performance_Level', 'attribute_name': 'AtsId', 'column': 6}
    CoastingProfileLevel = {'sheet_name': 'Performance_Level', 'attribute_name': 'CoastingProfileLevel', 'column': 7}


class Restriction_Level:
    Name = {'sheet_name': 'Restriction_Level', 'attribute_name': 'Name', 'column': 1}
    MaxAccel = {'sheet_name': 'Restriction_Level', 'attribute_name': 'MaxAccel', 'column': 2}
    MaxDecel = {'sheet_name': 'Restriction_Level', 'attribute_name': 'MaxDecel', 'column': 3}
    Id = {'sheet_name': 'Restriction_Level', 'attribute_name': 'Id', 'column': 4}


class Carborne_Controllers__Tacho:
    OnTractionAxle = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'Tacho', 'sub_attribute_name': 'OnTractionAxle', 'columns': [9, 12]}
    OnBrakingAxle = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'Tacho', 'sub_attribute_name': 'OnBrakingAxle', 'columns': [10, 13]}
    Polarity = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'Tacho', 'sub_attribute_name': 'Polarity', 'columns': [11, 14]}


class Carborne_Controllers__Acceleros:
    AccelerosCar = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'Acceleros', 'sub_attribute_name': 'AccelerosCar', 'columns': [15]}
    Polarity = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'Acceleros', 'sub_attribute_name': 'Polarity', 'columns': [16]}


class Carborne_Controllers:
    Name = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'Name', 'column': 1}
    Cab = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'Cab', 'column': 2}
    IsInFixedTrainUnit = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'IsInFixedTrainUnit', 'column': 3}
    TiaConfiguration = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'TiaConfiguration', 'column': 4}
    FirstTiaToCab1 = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'FirstTiaToCab1', 'column': 5}
    SecondTiaToCab1 = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'SecondTiaToCab1', 'column': 6}
    TagReaderConfiguration = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'TagReaderConfiguration', 'column': 7}
    PulseNumber = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'PulseNumber', 'column': 8}
    Tacho = Carborne_Controllers__Tacho()
    Acceleros = Carborne_Controllers__Acceleros()
    MtorNumber = {'sheet_name': 'Carborne_Controllers', 'attribute_name': 'MtorNumber', 'column': 17}


class Car_Types__Bogey:
    AxleLocation = {'sheet_name': 'Car_Types', 'attribute_name': 'Bogey', 'sub_attribute_name': 'AxleLocation', 'columns': [16, 17, 18, 19]}


class Car_Types:
    Name = {'sheet_name': 'Car_Types', 'attribute_name': 'Name', 'column': 1}
    CarTypeId = {'sheet_name': 'Car_Types', 'attribute_name': 'CarTypeId', 'column': 2}
    IsCab = {'sheet_name': 'Car_Types', 'attribute_name': 'IsCab', 'column': 3}
    Length = {'sheet_name': 'Car_Types', 'attribute_name': 'Length', 'column': 4}
    Height = {'sheet_name': 'Car_Types', 'attribute_name': 'Height', 'column': 5}
    FloorHeight = {'sheet_name': 'Car_Types', 'attribute_name': 'FloorHeight', 'column': 6}
    EmptyMass = {'sheet_name': 'Car_Types', 'attribute_name': 'EmptyMass', 'column': 7}
    FullLoadMass = {'sheet_name': 'Car_Types', 'attribute_name': 'FullLoadMass', 'column': 8}
    DoorWidth = {'sheet_name': 'Car_Types', 'attribute_name': 'DoorWidth', 'column': 9}
    DoorsNumber = {'sheet_name': 'Car_Types', 'attribute_name': 'DoorsNumber', 'column': 10}
    Door1Location = {'sheet_name': 'Car_Types', 'attribute_name': 'Door1Location', 'column': 11}
    Door2Location = {'sheet_name': 'Car_Types', 'attribute_name': 'Door2Location', 'column': 12}
    Door3Location = {'sheet_name': 'Car_Types', 'attribute_name': 'Door3Location', 'column': 13}
    Door4Location = {'sheet_name': 'Car_Types', 'attribute_name': 'Door4Location', 'column': 14}
    Door5Location = {'sheet_name': 'Car_Types', 'attribute_name': 'Door5Location', 'column': 15}
    Bogey = Car_Types__Bogey()


class Train_Types__ManageGenericCommands:
    ManageCmdA = {'sheet_name': 'Train_Types', 'attribute_name': 'ManageGenericCommands', 'sub_attribute_name': 'ManageCmdA', 'columns': [34]}
    CmdALocation = {'sheet_name': 'Train_Types', 'attribute_name': 'ManageGenericCommands', 'sub_attribute_name': 'CmdALocation', 'columns': [35]}
    ManageCmdB = {'sheet_name': 'Train_Types', 'attribute_name': 'ManageGenericCommands', 'sub_attribute_name': 'ManageCmdB', 'columns': [36]}
    CmdBLocation = {'sheet_name': 'Train_Types', 'attribute_name': 'ManageGenericCommands', 'sub_attribute_name': 'CmdBLocation', 'columns': [37]}
    ManageCmdC = {'sheet_name': 'Train_Types', 'attribute_name': 'ManageGenericCommands', 'sub_attribute_name': 'ManageCmdC', 'columns': [38]}
    CmdCLocation = {'sheet_name': 'Train_Types', 'attribute_name': 'ManageGenericCommands', 'sub_attribute_name': 'CmdCLocation', 'columns': [39]}


class Train_Types__PowerCollectorDevices:
    Location = {'sheet_name': 'Train_Types', 'attribute_name': 'PowerCollectorDevices', 'sub_attribute_name': 'Location', 'columns': [40, 41, 42, 43, 44]}


class Train_Types__SpeedLevel:
    Id = {'sheet_name': 'Train_Types', 'attribute_name': 'SpeedLevel', 'sub_attribute_name': 'Id', 'columns': [46, 48, 50, 52, 54, 56, 58, 60]}
    Speed = {'sheet_name': 'Train_Types', 'attribute_name': 'SpeedLevel', 'sub_attribute_name': 'Speed', 'columns': [47, 49, 51, 53, 55, 57, 59, 61]}


class Train_Types:
    Name = {'sheet_name': 'Train_Types', 'attribute_name': 'Name', 'column': 1}
    TrainTypeId = {'sheet_name': 'Train_Types', 'attribute_name': 'TrainTypeId', 'column': 2}
    AvConsistType = {'sheet_name': 'Train_Types', 'attribute_name': 'AvConsistType', 'column': 3}
    Length = {'sheet_name': 'Train_Types', 'attribute_name': 'Length', 'column': 4}
    ShortestIndivisiblePartLength = {'sheet_name': 'Train_Types', 'attribute_name': 'ShortestIndivisiblePartLength', 'column': 5}
    EmptyMass = {'sheet_name': 'Train_Types', 'attribute_name': 'EmptyMass', 'column': 6}
    FullLoadMass = {'sheet_name': 'Train_Types', 'attribute_name': 'FullLoadMass', 'column': 7}
    RotatingMass = {'sheet_name': 'Train_Types', 'attribute_name': 'RotatingMass', 'column': 8}
    WheelMinDiam = {'sheet_name': 'Train_Types', 'attribute_name': 'WheelMinDiam', 'column': 9}
    WheelMaxDiam = {'sheet_name': 'Train_Types', 'attribute_name': 'WheelMaxDiam', 'column': 10}
    WheelMeanDiam = {'sheet_name': 'Train_Types', 'attribute_name': 'WheelMeanDiam', 'column': 11}
    RubberWheels = {'sheet_name': 'Train_Types', 'attribute_name': 'RubberWheels', 'column': 12}
    RubberWheelMinDiam = {'sheet_name': 'Train_Types', 'attribute_name': 'RubberWheelMinDiam', 'column': 13}
    CarNumber = {'sheet_name': 'Train_Types', 'attribute_name': 'CarNumber', 'column': 14}
    Car1 = {'sheet_name': 'Train_Types', 'attribute_name': 'Car1', 'column': 15}
    Car2 = {'sheet_name': 'Train_Types', 'attribute_name': 'Car2', 'column': 16}
    Car3 = {'sheet_name': 'Train_Types', 'attribute_name': 'Car3', 'column': 17}
    Car4 = {'sheet_name': 'Train_Types', 'attribute_name': 'Car4', 'column': 18}
    Car5 = {'sheet_name': 'Train_Types', 'attribute_name': 'Car5', 'column': 19}
    Car6 = {'sheet_name': 'Train_Types', 'attribute_name': 'Car6', 'column': 20}
    Car7 = {'sheet_name': 'Train_Types', 'attribute_name': 'Car7', 'column': 21}
    Car8 = {'sheet_name': 'Train_Types', 'attribute_name': 'Car8', 'column': 22}
    Car9 = {'sheet_name': 'Train_Types', 'attribute_name': 'Car9', 'column': 23}
    Car10 = {'sheet_name': 'Train_Types', 'attribute_name': 'Car10', 'column': 24}
    DegradedMode = {'sheet_name': 'Train_Types', 'attribute_name': 'DegradedMode', 'column': 25}
    IsolationInputType = {'sheet_name': 'Train_Types', 'attribute_name': 'IsolationInputType', 'column': 26}
    CcCutsTractionWhenEb = {'sheet_name': 'Train_Types', 'attribute_name': 'CcCutsTractionWhenEb', 'column': 27}
    CcCcComType = {'sheet_name': 'Train_Types', 'attribute_name': 'CcCcComType', 'column': 28}
    DisconnectRsFromTpForPassengerProtection = {'sheet_name': 'Train_Types', 'attribute_name': 'DisconnectRsFromTpForPassengerProtection', 'column': 29}
    DisconnectThroughEb = {'sheet_name': 'Train_Types', 'attribute_name': 'DisconnectThroughEb', 'column': 30}
    SendNvOutputInBypass = {'sheet_name': 'Train_Types', 'attribute_name': 'SendNvOutputInBypass', 'column': 31}
    TdBypassDedicatedInputAvailable = {'sheet_name': 'Train_Types', 'attribute_name': 'TdBypassDedicatedInputAvailable', 'column': 32}
    DriverlessModeAvailable = {'sheet_name': 'Train_Types', 'attribute_name': 'DriverlessModeAvailable', 'column': 33}
    ManageGenericCommands = Train_Types__ManageGenericCommands()
    PowerCollectorDevices = Train_Types__PowerCollectorDevices()
    MasterControllerType = {'sheet_name': 'Train_Types', 'attribute_name': 'MasterControllerType', 'column': 45}
    SpeedLevel = Train_Types__SpeedLevel()


class AV_Types__Bogey:
    AxleLocation = {'sheet_name': 'AV_Types', 'attribute_name': 'Bogey', 'sub_attribute_name': 'AxleLocation', 'columns': [13, 14, 15, 16]}


class AV_Types:
    Name = {'sheet_name': 'AV_Types', 'attribute_name': 'Name', 'column': 1}
    AvConsistType = {'sheet_name': 'AV_Types', 'attribute_name': 'AvConsistType', 'column': 2}
    Length = {'sheet_name': 'AV_Types', 'attribute_name': 'Length', 'column': 3}
    ShortestIndivisiblePartLength = {'sheet_name': 'AV_Types', 'attribute_name': 'ShortestIndivisiblePartLength', 'column': 4}
    Height = {'sheet_name': 'AV_Types', 'attribute_name': 'Height', 'column': 5}
    FloorHeight = {'sheet_name': 'AV_Types', 'attribute_name': 'FloorHeight', 'column': 6}
    EmptyMass = {'sheet_name': 'AV_Types', 'attribute_name': 'EmptyMass', 'column': 7}
    FullLoadMass = {'sheet_name': 'AV_Types', 'attribute_name': 'FullLoadMass', 'column': 8}
    RotatingMass = {'sheet_name': 'AV_Types', 'attribute_name': 'RotatingMass', 'column': 9}
    WheelMinDiam = {'sheet_name': 'AV_Types', 'attribute_name': 'WheelMinDiam', 'column': 10}
    WheelMaxDiam = {'sheet_name': 'AV_Types', 'attribute_name': 'WheelMaxDiam', 'column': 11}
    WheelMeanDiam = {'sheet_name': 'AV_Types', 'attribute_name': 'WheelMeanDiam', 'column': 12}
    Bogey = AV_Types__Bogey()
    IsolationInputType = {'sheet_name': 'AV_Types', 'attribute_name': 'IsolationInputType', 'column': 17}
    CcCutsTractionWhenEb = {'sheet_name': 'AV_Types', 'attribute_name': 'CcCutsTractionWhenEb', 'column': 18}
    CcCcComType = {'sheet_name': 'AV_Types', 'attribute_name': 'CcCcComType', 'column': 19}
    DisconnectRsFromTpForPassengerProtection = {'sheet_name': 'AV_Types', 'attribute_name': 'DisconnectRsFromTpForPassengerProtection', 'column': 20}
    DisconnectThroughEb = {'sheet_name': 'AV_Types', 'attribute_name': 'DisconnectThroughEb', 'column': 21}


class Flatbed_Types__Bogey:
    AxleLocation = {'sheet_name': 'Flatbed_Types', 'attribute_name': 'Bogey', 'sub_attribute_name': 'AxleLocation', 'columns': [9, 10, 11, 12]}


class Flatbed_Types:
    Name = {'sheet_name': 'Flatbed_Types', 'attribute_name': 'Name', 'column': 1}
    AvConsistType = {'sheet_name': 'Flatbed_Types', 'attribute_name': 'AvConsistType', 'column': 2}
    Length = {'sheet_name': 'Flatbed_Types', 'attribute_name': 'Length', 'column': 3}
    ShortestIndivisiblePartLength = {'sheet_name': 'Flatbed_Types', 'attribute_name': 'ShortestIndivisiblePartLength', 'column': 4}
    FloorHeight = {'sheet_name': 'Flatbed_Types', 'attribute_name': 'FloorHeight', 'column': 5}
    EmptyMass = {'sheet_name': 'Flatbed_Types', 'attribute_name': 'EmptyMass', 'column': 6}
    FullLoadMass = {'sheet_name': 'Flatbed_Types', 'attribute_name': 'FullLoadMass', 'column': 7}
    RotatingMass = {'sheet_name': 'Flatbed_Types', 'attribute_name': 'RotatingMass', 'column': 8}
    Bogey = Flatbed_Types__Bogey()


class AV_Consist:
    Name = {'sheet_name': 'AV_Consist', 'attribute_name': 'Name', 'column': 1}
    AvConsistTypeId = {'sheet_name': 'AV_Consist', 'attribute_name': 'AvConsistTypeId', 'column': 2}
    VehicleType1 = {'sheet_name': 'AV_Consist', 'attribute_name': 'VehicleType1', 'column': 3}
    VehicleType2 = {'sheet_name': 'AV_Consist', 'attribute_name': 'VehicleType2', 'column': 4}
    VehicleType3 = {'sheet_name': 'AV_Consist', 'attribute_name': 'VehicleType3', 'column': 5}
    VehicleType4 = {'sheet_name': 'AV_Consist', 'attribute_name': 'VehicleType4', 'column': 6}
    VehicleType5 = {'sheet_name': 'AV_Consist', 'attribute_name': 'VehicleType5', 'column': 7}
    MaxSpeed = {'sheet_name': 'AV_Consist', 'attribute_name': 'MaxSpeed', 'column': 8}
    PropulsionEnableDeactivationTractionCutTime = {'sheet_name': 'AV_Consist', 'attribute_name': 'PropulsionEnableDeactivationTractionCutTime', 'column': 9}
    EmergencyBrakeRequestTractionCutTime = {'sheet_name': 'AV_Consist', 'attribute_name': 'EmergencyBrakeRequestTractionCutTime', 'column': 10}
    CoastTime = {'sheet_name': 'AV_Consist', 'attribute_name': 'CoastTime', 'column': 11}
    HyperAcceleration = {'sheet_name': 'AV_Consist', 'attribute_name': 'HyperAcceleration', 'column': 12}
    EbRate = {'sheet_name': 'AV_Consist', 'attribute_name': 'EbRate', 'column': 13}
    SbRate = {'sheet_name': 'AV_Consist', 'attribute_name': 'SbRate', 'column': 14}
    TractionDirectionType = {'sheet_name': 'AV_Consist', 'attribute_name': 'TractionDirectionType', 'column': 15}
    Margin_A_Psr = {'sheet_name': 'AV_Consist', 'attribute_name': 'Margin_A_Psr', 'column': 16}
    Margin_B_Psr = {'sheet_name': 'AV_Consist', 'attribute_name': 'Margin_B_Psr', 'column': 17}
    RsCharacteristicsFileName = {'sheet_name': 'AV_Consist', 'attribute_name': 'RsCharacteristicsFileName', 'column': 18}


class Train_Consist:
    Name = {'sheet_name': 'Train_Consist', 'attribute_name': 'Name', 'column': 1}
    TrainConsistTypeId = {'sheet_name': 'Train_Consist', 'attribute_name': 'TrainConsistTypeId', 'column': 2}
    RescueOnly = {'sheet_name': 'Train_Consist', 'attribute_name': 'RescueOnly', 'column': 3}
    TrainType1 = {'sheet_name': 'Train_Consist', 'attribute_name': 'TrainType1', 'column': 4}
    TrainType2 = {'sheet_name': 'Train_Consist', 'attribute_name': 'TrainType2', 'column': 5}
    TrainType3 = {'sheet_name': 'Train_Consist', 'attribute_name': 'TrainType3', 'column': 6}
    TrainType4 = {'sheet_name': 'Train_Consist', 'attribute_name': 'TrainType4', 'column': 7}
    RsCharacteristicsFileName = {'sheet_name': 'Train_Consist', 'attribute_name': 'RsCharacteristicsFileName', 'column': 8}
    RecoveryRsCharacteristicsFileName = {'sheet_name': 'Train_Consist', 'attribute_name': 'RecoveryRsCharacteristicsFileName', 'column': 9}
    MaxSpeed = {'sheet_name': 'Train_Consist', 'attribute_name': 'MaxSpeed', 'column': 10}
    PropulsionEnableDeactivationTractionCutTime = {'sheet_name': 'Train_Consist', 'attribute_name': 'PropulsionEnableDeactivationTractionCutTime', 'column': 11}
    EmergencyBrakeRequestTractionCutTime = {'sheet_name': 'Train_Consist', 'attribute_name': 'EmergencyBrakeRequestTractionCutTime', 'column': 12}
    CoastTime = {'sheet_name': 'Train_Consist', 'attribute_name': 'CoastTime', 'column': 13}
    EbRate = {'sheet_name': 'Train_Consist', 'attribute_name': 'EbRate', 'column': 14}
    SbRate = {'sheet_name': 'Train_Consist', 'attribute_name': 'SbRate', 'column': 15}
    TractionDirectionType = {'sheet_name': 'Train_Consist', 'attribute_name': 'TractionDirectionType', 'column': 16}
    Margin_A_Psr = {'sheet_name': 'Train_Consist', 'attribute_name': 'Margin_A_Psr', 'column': 17}
    Margin_B_Psr = {'sheet_name': 'Train_Consist', 'attribute_name': 'Margin_B_Psr', 'column': 18}
    SleepingModeNotAvailable = {'sheet_name': 'Train_Consist', 'attribute_name': 'SleepingModeNotAvailable', 'column': 19}


class Train:
    Name = {'sheet_name': 'Train', 'attribute_name': 'Name', 'column': 1}
    Type = {'sheet_name': 'Train', 'attribute_name': 'Type', 'column': 2}
    CbtcTrainUnitId = {'sheet_name': 'Train', 'attribute_name': 'CbtcTrainUnitId', 'column': 3}
    TrainCustomerName = {'sheet_name': 'Train', 'attribute_name': 'TrainCustomerName', 'column': 4}
    DisplayableName = {'sheet_name': 'Train', 'attribute_name': 'DisplayableName', 'column': 5}
    CcConfiguration = {'sheet_name': 'Train', 'attribute_name': 'CcConfiguration', 'column': 6}
    VirtualCcName = {'sheet_name': 'Train', 'attribute_name': 'VirtualCcName', 'column': 7}
    Cab1CcName = {'sheet_name': 'Train', 'attribute_name': 'Cab1CcName', 'column': 8}
    Cab2CcName = {'sheet_name': 'Train', 'attribute_name': 'Cab2CcName', 'column': 9}
    Cab1TodName = {'sheet_name': 'Train', 'attribute_name': 'Cab1TodName', 'column': 10}
    Cab2TodName = {'sheet_name': 'Train', 'attribute_name': 'Cab2TodName', 'column': 11}
    PisName = {'sheet_name': 'Train', 'attribute_name': 'PisName', 'column': 12}
    TarName = {'sheet_name': 'Train', 'attribute_name': 'TarName', 'column': 13}
    TmsMvbBoxName = {'sheet_name': 'Train', 'attribute_name': 'TmsMvbBoxName', 'column': 14}
    PwmBoxName = {'sheet_name': 'Train', 'attribute_name': 'PwmBoxName', 'column': 15}


class Auxiliary_Vehicle:
    Name = {'sheet_name': 'Auxiliary_Vehicle', 'attribute_name': 'Name', 'column': 1}
    Type = {'sheet_name': 'Auxiliary_Vehicle', 'attribute_name': 'Type', 'column': 2}
    CbtcTrainUnitId = {'sheet_name': 'Auxiliary_Vehicle', 'attribute_name': 'CbtcTrainUnitId', 'column': 3}
    CustomerName = {'sheet_name': 'Auxiliary_Vehicle', 'attribute_name': 'CustomerName', 'column': 4}
    DisplayableName = {'sheet_name': 'Auxiliary_Vehicle', 'attribute_name': 'DisplayableName', 'column': 5}
    CcName = {'sheet_name': 'Auxiliary_Vehicle', 'attribute_name': 'CcName', 'column': 6}
    TodName = {'sheet_name': 'Auxiliary_Vehicle', 'attribute_name': 'TodName', 'column': 7}
    TarName = {'sheet_name': 'Auxiliary_Vehicle', 'attribute_name': 'TarName', 'column': 8}


class Traction_Profiles__NonVital:
    Empty = {'sheet_name': 'Traction_Profiles', 'attribute_name': 'NonVital', 'sub_attribute_name': 'Empty', 'columns': [3]}
    FullLoad = {'sheet_name': 'Traction_Profiles', 'attribute_name': 'NonVital', 'sub_attribute_name': 'FullLoad', 'columns': [4]}


class Traction_Profiles:
    TrainConsist = {'sheet_name': 'Traction_Profiles', 'attribute_name': 'TrainConsist', 'column': 1}
    Speed = {'sheet_name': 'Traction_Profiles', 'attribute_name': 'Speed', 'column': 2}
    NonVital = Traction_Profiles__NonVital()
    Vital = {'sheet_name': 'Traction_Profiles', 'attribute_name': 'Vital', 'column': 5}


class Flood_Gate__Limit:
    Seg = {'sheet_name': 'Flood_Gate', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [2, 7, 12, 17, 22, 27, 32, 37]}
    X = {'sheet_name': 'Flood_Gate', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [3, 8, 13, 18, 23, 28, 33, 38]}
    Direction = {'sheet_name': 'Flood_Gate', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [4, 9, 14, 19, 24, 29, 34, 39]}
    Track = {'sheet_name': 'Flood_Gate', 'attribute_name': 'Limit', 'sub_attribute_name': 'Track', 'columns': [5, 10, 15, 20, 25, 30, 35, 40]}
    Kp = {'sheet_name': 'Flood_Gate', 'attribute_name': 'Limit', 'sub_attribute_name': 'Kp', 'columns': [6, 11, 16, 21, 26, 31, 36, 41]}


class Flood_Gate__Blocks:
    Block = {'sheet_name': 'Flood_Gate', 'attribute_name': 'Blocks', 'sub_attribute_name': 'Block', 'columns': [42, 43, 44, 45, 46, 47, 48, 49]}


class Flood_Gate:
    Name = {'sheet_name': 'Flood_Gate', 'attribute_name': 'Name', 'column': 1}
    Limit = Flood_Gate__Limit()
    Blocks = Flood_Gate__Blocks()


class Coupling_Area:
    Name = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Name', 'column': 1}
    Block1 = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Block1', 'column': 2}
    Block2 = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Block2', 'column': 3}
    Block3 = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Block3', 'column': 4}
    Block4 = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Block4', 'column': 5}
    Block5 = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Block5', 'column': 6}
    Block6 = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Block6', 'column': 7}
    Block7 = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Block7', 'column': 8}
    Block8 = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Block8', 'column': 9}
    Block9 = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Block9', 'column': 10}
    Block10 = {'sheet_name': 'Coupling_Area', 'attribute_name': 'Block10', 'column': 11}


class Floor_Levels__Limit:
    Seg = {'sheet_name': 'Floor_Levels', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]}
    X = {'sheet_name': 'Floor_Levels', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}
    Direction = {'sheet_name': 'Floor_Levels', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]}


class Floor_Levels:
    Name = {'sheet_name': 'Floor_Levels', 'attribute_name': 'Name', 'column': 1}
    Type = {'sheet_name': 'Floor_Levels', 'attribute_name': 'Type', 'column': 2}
    Limit = Floor_Levels__Limit()


class EB_Rate_Area__Limit:
    Seg = {'sheet_name': 'EB_Rate_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44]}
    X = {'sheet_name': 'EB_Rate_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]}
    Direction = {'sheet_name': 'EB_Rate_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}


class EB_Rate_Area__EbRate:
    TrainConsistType = {'sheet_name': 'EB_Rate_Area', 'attribute_name': 'EbRate', 'sub_attribute_name': 'TrainConsistType', 'columns': [47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77]}
    Value = {'sheet_name': 'EB_Rate_Area', 'attribute_name': 'EbRate', 'sub_attribute_name': 'Value', 'columns': [48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78]}


class EB_Rate_Area:
    Name = {'sheet_name': 'EB_Rate_Area', 'attribute_name': 'Name', 'column': 1}
    Limit = EB_Rate_Area__Limit()
    EbRate = EB_Rate_Area__EbRate()


class Unwanted_Stop_Area__Limit:
    Seg = {'sheet_name': 'Unwanted_Stop_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}
    X = {'sheet_name': 'Unwanted_Stop_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]}
    Direction = {'sheet_name': 'Unwanted_Stop_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [8, 11, 14, 17, 20, 23, 26, 29, 32, 35]}


class Unwanted_Stop_Area:
    Name = {'sheet_name': 'Unwanted_Stop_Area', 'attribute_name': 'Name', 'column': 1}
    Type = {'sheet_name': 'Unwanted_Stop_Area', 'attribute_name': 'Type', 'column': 2}
    Cause = {'sheet_name': 'Unwanted_Stop_Area', 'attribute_name': 'Cause', 'column': 3}
    Direction = {'sheet_name': 'Unwanted_Stop_Area', 'attribute_name': 'Direction', 'column': 4}
    Applicability = {'sheet_name': 'Unwanted_Stop_Area', 'attribute_name': 'Applicability', 'column': 5}
    Limit = Unwanted_Stop_Area__Limit()


class Consist_OSP__AuthorisedConsist:
    ConsistName = {'sheet_name': 'Consist_OSP', 'attribute_name': 'AuthorisedConsist', 'sub_attribute_name': 'ConsistName', 'columns': [2, 10, 18, 26, 34, 42, 50, 58]}
    IsDefault = {'sheet_name': 'Consist_OSP', 'attribute_name': 'AuthorisedConsist', 'sub_attribute_name': 'IsDefault', 'columns': [3, 11, 19, 27, 35, 43, 51, 59]}
    PsdSubset = {'sheet_name': 'Consist_OSP', 'attribute_name': 'AuthorisedConsist', 'sub_attribute_name': 'PsdSubset', 'columns': [4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31, 36, 37, 38, 39, 44, 45, 46, 47, 52, 53, 54, 55, 60, 61, 62, 63]}
    TdSubset = {'sheet_name': 'Consist_OSP', 'attribute_name': 'AuthorisedConsist', 'sub_attribute_name': 'TdSubset', 'columns': [8, 9, 16, 17, 24, 25, 32, 33, 40, 41, 48, 49, 56, 57, 64, 65]}


class Consist_OSP:
    OspName = {'sheet_name': 'Consist_OSP', 'attribute_name': 'OspName', 'column': 1}
    AuthorisedConsist = Consist_OSP__AuthorisedConsist()


class Walkways_Area__ForbidEvac:
    LeftCentral = {'sheet_name': 'Walkways_Area', 'attribute_name': 'ForbidEvac', 'sub_attribute_name': 'LeftCentral', 'columns': [2]}
    LeftLateral = {'sheet_name': 'Walkways_Area', 'attribute_name': 'ForbidEvac', 'sub_attribute_name': 'LeftLateral', 'columns': [3]}
    RightCentral = {'sheet_name': 'Walkways_Area', 'attribute_name': 'ForbidEvac', 'sub_attribute_name': 'RightCentral', 'columns': [4]}
    RightLateral = {'sheet_name': 'Walkways_Area', 'attribute_name': 'ForbidEvac', 'sub_attribute_name': 'RightLateral', 'columns': [5]}


class Walkways_Area__Limit:
    Seg = {'sheet_name': 'Walkways_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}
    X = {'sheet_name': 'Walkways_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]}
    Direction = {'sheet_name': 'Walkways_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [8, 11, 14, 17, 20, 23, 26, 29, 32, 35]}


class Walkways_Area:
    Name = {'sheet_name': 'Walkways_Area', 'attribute_name': 'Name', 'column': 1}
    ForbidEvac = Walkways_Area__ForbidEvac()
    Limit = Walkways_Area__Limit()


class Customs_Area__Customs:
    Block = {'sheet_name': 'Customs_Area', 'attribute_name': 'Customs', 'sub_attribute_name': 'Block', 'columns': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}


class Customs_Area__Control:
    Block = {'sheet_name': 'Customs_Area', 'attribute_name': 'Control', 'sub_attribute_name': 'Block', 'columns': [12, 14, 16]}
    DistRun = {'sheet_name': 'Customs_Area', 'attribute_name': 'Control', 'sub_attribute_name': 'DistRun', 'columns': [13, 15, 17]}


class Customs_Area:
    Name = {'sheet_name': 'Customs_Area', 'attribute_name': 'Name', 'column': 1}
    Customs = Customs_Area__Customs()
    Control = Customs_Area__Control()


class CBTC_Prohibition_Area__IvbList:
    Ivb = {'sheet_name': 'CBTC_Prohibition_Area', 'attribute_name': 'IvbList', 'sub_attribute_name': 'Ivb', 'columns': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]}


class CBTC_Prohibition_Area:
    Name = {'sheet_name': 'CBTC_Prohibition_Area', 'attribute_name': 'Name', 'column': 1}
    IvbList = CBTC_Prohibition_Area__IvbList()
    ManageTrainNumber = {'sheet_name': 'CBTC_Prohibition_Area', 'attribute_name': 'ManageTrainNumber', 'column': 22}
    MaxTrainNumber = {'sheet_name': 'CBTC_Prohibition_Area', 'attribute_name': 'MaxTrainNumber', 'column': 23}
    ManageUnitNumber = {'sheet_name': 'CBTC_Prohibition_Area', 'attribute_name': 'ManageUnitNumber', 'column': 24}
    MaxUnitNumber = {'sheet_name': 'CBTC_Prohibition_Area', 'attribute_name': 'MaxUnitNumber', 'column': 25}


class TSR_Area__Limit:
    Seg = {'sheet_name': 'TSR_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}
    X = {'sheet_name': 'TSR_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]}
    Direction = {'sheet_name': 'TSR_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48]}


class TSR_Area:
    Name = {'sheet_name': 'TSR_Area', 'attribute_name': 'Name', 'column': 1}
    Number = {'sheet_name': 'TSR_Area', 'attribute_name': 'Number', 'column': 2}
    Label = {'sheet_name': 'TSR_Area', 'attribute_name': 'Label', 'column': 3}
    Limit = TSR_Area__Limit()


class Anchor:
    TrackName = {'sheet_name': 'Anchor', 'attribute_name': 'TrackName', 'column': 1}
    SurveyedKp = {'sheet_name': 'Anchor', 'attribute_name': 'SurveyedKp', 'column': 2}
    CivilKp = {'sheet_name': 'Anchor', 'attribute_name': 'CivilKp', 'column': 3}


class Chainage:
    ChainageType = {'sheet_name': 'Chainage', 'attribute_name': 'ChainageType', 'column': 1}
    TrackName = {'sheet_name': 'Chainage', 'attribute_name': 'TrackName', 'column': 2}
    CivilKpStart = {'sheet_name': 'Chainage', 'attribute_name': 'CivilKpStart', 'column': 3}
    CivilKpEnd = {'sheet_name': 'Chainage', 'attribute_name': 'CivilKpEnd', 'column': 4}


class Superseed_Tan:
    CommandType = {'sheet_name': 'Superseed_Tan', 'attribute_name': 'CommandType', 'column': 1}


class Dynamic_Brake_Test_Point__TestPoint:
    Seg = {'sheet_name': 'Dynamic_Brake_Test_Point', 'attribute_name': 'TestPoint', 'sub_attribute_name': 'Seg', 'columns': [2]}
    X = {'sheet_name': 'Dynamic_Brake_Test_Point', 'attribute_name': 'TestPoint', 'sub_attribute_name': 'X', 'columns': [3]}


class Dynamic_Brake_Test_Point__SpeedPoint:
    Seg = {'sheet_name': 'Dynamic_Brake_Test_Point', 'attribute_name': 'SpeedPoint', 'sub_attribute_name': 'Seg', 'columns': [5]}
    X = {'sheet_name': 'Dynamic_Brake_Test_Point', 'attribute_name': 'SpeedPoint', 'sub_attribute_name': 'X', 'columns': [6]}


class Dynamic_Brake_Test_Point:
    Name = {'sheet_name': 'Dynamic_Brake_Test_Point', 'attribute_name': 'Name', 'column': 1}
    TestPoint = Dynamic_Brake_Test_Point__TestPoint()
    ApproachDirection = {'sheet_name': 'Dynamic_Brake_Test_Point', 'attribute_name': 'ApproachDirection', 'column': 4}
    SpeedPoint = Dynamic_Brake_Test_Point__SpeedPoint()
    BrakeType = {'sheet_name': 'Dynamic_Brake_Test_Point', 'attribute_name': 'BrakeType', 'column': 7}
    Speed = {'sheet_name': 'Dynamic_Brake_Test_Point', 'attribute_name': 'Speed', 'column': 8}
    StoppingTime = {'sheet_name': 'Dynamic_Brake_Test_Point', 'attribute_name': 'StoppingTime', 'column': 9}


class Traffic_Stop__PlatformList:
    Name = {'sheet_name': 'Traffic_Stop', 'attribute_name': 'PlatformList', 'sub_attribute_name': 'Name', 'columns': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]}


class Traffic_Stop:
    Name = {'sheet_name': 'Traffic_Stop', 'attribute_name': 'Name', 'column': 1}
    TrafficStopSubsetName = {'sheet_name': 'Traffic_Stop', 'attribute_name': 'TrafficStopSubsetName', 'column': 2}
    PlatformList = Traffic_Stop__PlatformList()


class Protection_Zone__SweepingZoneList:
    Name = {'sheet_name': 'Protection_Zone', 'attribute_name': 'SweepingZoneList', 'sub_attribute_name': 'Name', 'columns': [5, 6, 7, 8, 9]}


class Protection_Zone__Limit:
    Seg = {'sheet_name': 'Protection_Zone', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52]}
    X = {'sheet_name': 'Protection_Zone', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53]}
    Direction = {'sheet_name': 'Protection_Zone', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54]}


class Protection_Zone:
    Name = {'sheet_name': 'Protection_Zone', 'attribute_name': 'Name', 'column': 1}
    Type = {'sheet_name': 'Protection_Zone', 'attribute_name': 'Type', 'column': 2}
    CbtcControlledFlag = {'sheet_name': 'Protection_Zone', 'attribute_name': 'CbtcControlledFlag', 'column': 3}
    SweepingFlag = {'sheet_name': 'Protection_Zone', 'attribute_name': 'SweepingFlag', 'column': 4}
    SweepingZoneList = Protection_Zone__SweepingZoneList()
    Limit = Protection_Zone__Limit()


class Crossing_Calling_Area__From:
    Seg = {'sheet_name': 'Crossing_Calling_Area', 'attribute_name': 'From', 'sub_attribute_name': 'Seg', 'columns': [3]}
    X = {'sheet_name': 'Crossing_Calling_Area', 'attribute_name': 'From', 'sub_attribute_name': 'X', 'columns': [4]}


class Crossing_Calling_Area__To:
    Seg = {'sheet_name': 'Crossing_Calling_Area', 'attribute_name': 'To', 'sub_attribute_name': 'Seg', 'columns': [5]}
    X = {'sheet_name': 'Crossing_Calling_Area', 'attribute_name': 'To', 'sub_attribute_name': 'X', 'columns': [6]}


class Crossing_Calling_Area:
    Name = {'sheet_name': 'Crossing_Calling_Area', 'attribute_name': 'Name', 'column': 1}
    Id = {'sheet_name': 'Crossing_Calling_Area', 'attribute_name': 'Id', 'column': 2}
    From = Crossing_Calling_Area__From()
    To = Crossing_Calling_Area__To()
    RequestDistance = {'sheet_name': 'Crossing_Calling_Area', 'attribute_name': 'RequestDistance', 'column': 7}
    RequestDelay = {'sheet_name': 'Crossing_Calling_Area', 'attribute_name': 'RequestDelay', 'column': 8}
    CheckIl_Set = {'sheet_name': 'Crossing_Calling_Area', 'attribute_name': 'CheckIl_Set', 'column': 9}


class ASR__Limit:
    Seg = {'sheet_name': 'ASR', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [6, 9, 12, 15, 18]}
    X = {'sheet_name': 'ASR', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [7, 10, 13, 16, 19]}
    Direction = {'sheet_name': 'ASR', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [8, 11, 14, 17, 20]}


class ASR:
    Name = {'sheet_name': 'ASR', 'attribute_name': 'Name', 'column': 1}
    Speed = {'sheet_name': 'ASR', 'attribute_name': 'Speed', 'column': 2}
    RelatedDirection = {'sheet_name': 'ASR', 'attribute_name': 'RelatedDirection', 'column': 3}
    SweepingAsrFlag = {'sheet_name': 'ASR', 'attribute_name': 'SweepingAsrFlag', 'column': 4}
    SentByIxl = {'sheet_name': 'ASR', 'attribute_name': 'SentByIxl', 'column': 5}
    Limit = ASR__Limit()


class PSD_Subsets__PsdNumber:
    Cell = {'sheet_name': 'PSD_Subsets', 'attribute_name': 'PsdNumber', 'sub_attribute_name': 'Cell', 'columns': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]}


class PSD_Subsets:
    Name = {'sheet_name': 'PSD_Subsets', 'attribute_name': 'Name', 'column': 1}
    Id = {'sheet_name': 'PSD_Subsets', 'attribute_name': 'Id', 'column': 2}
    PlatformName = {'sheet_name': 'PSD_Subsets', 'attribute_name': 'PlatformName', 'column': 3}
    PsdNumber = PSD_Subsets__PsdNumber()


class DCM_Transition_Zones__Limit:
    Seg = {'sheet_name': 'DCM_Transition_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44]}
    X = {'sheet_name': 'DCM_Transition_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]}
    Direction = {'sheet_name': 'DCM_Transition_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}


class DCM_Transition_Zones:
    Name = {'sheet_name': 'DCM_Transition_Zones', 'attribute_name': 'Name', 'column': 1}
    Limit = DCM_Transition_Zones__Limit()


class Adhesion_Zones__Limit:
    Seg = {'sheet_name': 'Adhesion_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]}
    X = {'sheet_name': 'Adhesion_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]}
    Direction = {'sheet_name': 'Adhesion_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}
    Voie = {'sheet_name': 'Adhesion_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Voie', 'columns': [33, 35, 37, 39, 41, 43, 45, 47, 49, 51]}
    Pk = {'sheet_name': 'Adhesion_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Pk', 'columns': [34, 36, 38, 40, 42, 44, 46, 48, 50, 52]}


class Adhesion_Zones:
    Name = {'sheet_name': 'Adhesion_Zones', 'attribute_name': 'Name', 'column': 1}
    Id = {'sheet_name': 'Adhesion_Zones', 'attribute_name': 'Id', 'column': 2}
    Limit = Adhesion_Zones__Limit()


class Adhesion_Level:
    Name = {'sheet_name': 'Adhesion_Level', 'attribute_name': 'Name', 'column': 1}
    MaxAccel = {'sheet_name': 'Adhesion_Level', 'attribute_name': 'MaxAccel', 'column': 2}
    MaxDecel = {'sheet_name': 'Adhesion_Level', 'attribute_name': 'MaxDecel', 'column': 3}
    Id = {'sheet_name': 'Adhesion_Level', 'attribute_name': 'Id', 'column': 4}


class Frontam_General_Data:
    Name = {'sheet_name': 'Frontam_General_Data', 'attribute_name': 'Name', 'column': 1}
    ObjectType = {'sheet_name': 'Frontam_General_Data', 'attribute_name': 'ObjectType', 'column': 2}
    ObjectName = {'sheet_name': 'Frontam_General_Data', 'attribute_name': 'ObjectName', 'column': 3}
    GeneralDataName = {'sheet_name': 'Frontam_General_Data', 'attribute_name': 'GeneralDataName', 'column': 4}
    TypeBitByte = {'sheet_name': 'Frontam_General_Data', 'attribute_name': 'TypeBitByte', 'column': 5}
    LineSectionName = {'sheet_name': 'Frontam_General_Data', 'attribute_name': 'LineSectionName', 'column': 6}
    Index = {'sheet_name': 'Frontam_General_Data', 'attribute_name': 'Index', 'column': 7}


class Generic_Command_Zones__CmdA:
    AppliedInZone = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'CmdA', 'sub_attribute_name': 'AppliedInZone', 'columns': [2]}
    SpeedThreshold = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'CmdA', 'sub_attribute_name': 'SpeedThreshold', 'columns': [3]}
    AnticipationTime = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'CmdA', 'sub_attribute_name': 'AnticipationTime', 'columns': [4]}


class Generic_Command_Zones__CmdB:
    AppliedInZone = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'CmdB', 'sub_attribute_name': 'AppliedInZone', 'columns': [5]}
    SpeedThreshold = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'CmdB', 'sub_attribute_name': 'SpeedThreshold', 'columns': [6]}
    AnticipationTime = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'CmdB', 'sub_attribute_name': 'AnticipationTime', 'columns': [7]}


class Generic_Command_Zones__CmdC:
    AppliedInZone = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'CmdC', 'sub_attribute_name': 'AppliedInZone', 'columns': [8]}
    SpeedThreshold = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'CmdC', 'sub_attribute_name': 'SpeedThreshold', 'columns': [9]}
    AnticipationTime = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'CmdC', 'sub_attribute_name': 'AnticipationTime', 'columns': [10]}


class Generic_Command_Zones__Limit:
    Seg = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [11, 14, 17, 20, 23, 26, 29, 32, 35, 38]}
    X = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39]}
    Direction = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [13, 16, 19, 22, 25, 28, 31, 34, 37, 40]}
    Voie = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Voie', 'columns': [41, 43, 45, 47, 49, 51, 53, 55, 57, 59]}
    Pk = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Pk', 'columns': [42, 44, 46, 48, 50, 52, 54, 56, 58, 60]}


class Generic_Command_Zones:
    Name = {'sheet_name': 'Generic_Command_Zones', 'attribute_name': 'Name', 'column': 1}
    CmdA = Generic_Command_Zones__CmdA()
    CmdB = Generic_Command_Zones__CmdB()
    CmdC = Generic_Command_Zones__CmdC()
    Limit = Generic_Command_Zones__Limit()


class DCS_Elementary_Zones__Limit:
    Seg = {'sheet_name': 'DCS_Elementary_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}
    X = {'sheet_name': 'DCS_Elementary_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}
    Direction = {'sheet_name': 'DCS_Elementary_Zones', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]}


class DCS_Elementary_Zones:
    Name = {'sheet_name': 'DCS_Elementary_Zones', 'attribute_name': 'Name', 'column': 1}
    SubsetName = {'sheet_name': 'DCS_Elementary_Zones', 'attribute_name': 'SubsetName', 'column': 2}
    AtsId = {'sheet_name': 'DCS_Elementary_Zones', 'attribute_name': 'AtsId', 'column': 3}
    ObjectId = {'sheet_name': 'DCS_Elementary_Zones', 'attribute_name': 'ObjectId', 'column': 4}
    Limit = DCS_Elementary_Zones__Limit()


class TSR_Possible_Speeds:
    Name = {'sheet_name': 'TSR_Possible_Speeds', 'attribute_name': 'Name', 'column': 1}
    Speed = {'sheet_name': 'TSR_Possible_Speeds', 'attribute_name': 'Speed', 'column': 2}


class TD_Subsets__TdNumber:
    Cell = {'sheet_name': 'TD_Subsets', 'attribute_name': 'TdNumber', 'sub_attribute_name': 'Cell', 'columns': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]}


class TD_Subsets:
    Name = {'sheet_name': 'TD_Subsets', 'attribute_name': 'Name', 'column': 1}
    Id = {'sheet_name': 'TD_Subsets', 'attribute_name': 'Id', 'column': 2}
    PassengerTrainTypeName = {'sheet_name': 'TD_Subsets', 'attribute_name': 'PassengerTrainTypeName', 'column': 3}
    TdNumber = TD_Subsets__TdNumber()


class Unwanted_Coupling_Area__Limit:
    Seg = {'sheet_name': 'Unwanted_Coupling_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [3, 6, 9, 12, 15]}
    X = {'sheet_name': 'Unwanted_Coupling_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [4, 7, 10, 13, 16]}
    Direction = {'sheet_name': 'Unwanted_Coupling_Area', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [5, 8, 11, 14, 17]}


class Unwanted_Coupling_Area:
    Name = {'sheet_name': 'Unwanted_Coupling_Area', 'attribute_name': 'Name', 'column': 1}
    Direction = {'sheet_name': 'Unwanted_Coupling_Area', 'attribute_name': 'Direction', 'column': 2}
    Limit = Unwanted_Coupling_Area__Limit()


class Cruising_Zones__CruisingZone:
    Seg = {'sheet_name': 'Cruising_Zones', 'attribute_name': 'CruisingZone', 'sub_attribute_name': 'Seg', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]}
    X = {'sheet_name': 'Cruising_Zones', 'attribute_name': 'CruisingZone', 'sub_attribute_name': 'X', 'columns': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}
    Direction = {'sheet_name': 'Cruising_Zones', 'attribute_name': 'CruisingZone', 'sub_attribute_name': 'Direction', 'columns': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}


class Cruising_Zones:
    CruisingZoneName = {'sheet_name': 'Cruising_Zones', 'attribute_name': 'CruisingZoneName', 'column': 1}
    OriginPlatform = {'sheet_name': 'Cruising_Zones', 'attribute_name': 'OriginPlatform', 'column': 2}
    DestinationPlatform = {'sheet_name': 'Cruising_Zones', 'attribute_name': 'DestinationPlatform', 'column': 3}
    CruisingZone = Cruising_Zones__CruisingZone()


class Passage_Detector:
    Name = {'sheet_name': 'Passage_Detector', 'attribute_name': 'Name', 'column': 1}
    Seg = {'sheet_name': 'Passage_Detector', 'attribute_name': 'Seg', 'column': 2}
    X = {'sheet_name': 'Passage_Detector', 'attribute_name': 'X', 'column': 3}


class Parking_Place:
    Name = {'sheet_name': 'Parking_Place', 'attribute_name': 'Name', 'column': 1}
    AtsId = {'sheet_name': 'Parking_Place', 'attribute_name': 'AtsId', 'column': 2}
    ParkingPlaceLimit1 = {'sheet_name': 'Parking_Place', 'attribute_name': 'ParkingPlaceLimit1', 'column': 3}
    ExternalLocMemorizationOffsetLimit1 = {'sheet_name': 'Parking_Place', 'attribute_name': 'ExternalLocMemorizationOffsetLimit1', 'column': 4}
    ParkingPlaceLimit2 = {'sheet_name': 'Parking_Place', 'attribute_name': 'ParkingPlaceLimit2', 'column': 5}
    ExternalLocMemorizationOffsetLimit2 = {'sheet_name': 'Parking_Place', 'attribute_name': 'ExternalLocMemorizationOffsetLimit2', 'column': 6}
    SignalName1 = {'sheet_name': 'Parking_Place', 'attribute_name': 'SignalName1', 'column': 7}
    SignalName2 = {'sheet_name': 'Parking_Place', 'attribute_name': 'SignalName2', 'column': 8}
    SignalName3 = {'sheet_name': 'Parking_Place', 'attribute_name': 'SignalName3', 'column': 9}
    SignalName4 = {'sheet_name': 'Parking_Place', 'attribute_name': 'SignalName4', 'column': 10}
    SignalName5 = {'sheet_name': 'Parking_Place', 'attribute_name': 'SignalName5', 'column': 11}


class StaticTag_Group__TagList:
    Tag = {'sheet_name': 'StaticTag_Group', 'attribute_name': 'TagList', 'sub_attribute_name': 'Tag', 'columns': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}


class StaticTag_Group:
    Name = {'sheet_name': 'StaticTag_Group', 'attribute_name': 'Name', 'column': 1}
    Id = {'sheet_name': 'StaticTag_Group', 'attribute_name': 'Id', 'column': 2}
    TagList = StaticTag_Group__TagList()


class Odometric_Zone__OdometricZone:
    Seg = {'sheet_name': 'Odometric_Zone', 'attribute_name': 'OdometricZone', 'sub_attribute_name': 'Seg', 'columns': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}
    X = {'sheet_name': 'Odometric_Zone', 'attribute_name': 'OdometricZone', 'sub_attribute_name': 'X', 'columns': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}
    Direction = {'sheet_name': 'Odometric_Zone', 'attribute_name': 'OdometricZone', 'sub_attribute_name': 'Direction', 'columns': [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]}


class Odometric_Zone:
    Name = {'sheet_name': 'Odometric_Zone', 'attribute_name': 'Name', 'column': 1}
    Level = {'sheet_name': 'Odometric_Zone', 'attribute_name': 'Level', 'column': 2}
    CurvatureRadius = {'sheet_name': 'Odometric_Zone', 'attribute_name': 'CurvatureRadius', 'column': 3}
    Banking = {'sheet_name': 'Odometric_Zone', 'attribute_name': 'Banking', 'column': 4}
    OdometricZone = Odometric_Zone__OdometricZone()


class Presence_Detector:
    Name = {'sheet_name': 'Presence_Detector', 'attribute_name': 'Name', 'column': 1}
    Seg = {'sheet_name': 'Presence_Detector', 'attribute_name': 'Seg', 'column': 2}
    X = {'sheet_name': 'Presence_Detector', 'attribute_name': 'X', 'column': 3}
    Direction = {'sheet_name': 'Presence_Detector', 'attribute_name': 'Direction', 'column': 4}


class Dispatchable_Point:
    Name = {'sheet_name': 'Dispatchable_Point', 'attribute_name': 'Name', 'column': 1}
    TrackName = {'sheet_name': 'Dispatchable_Point', 'attribute_name': 'TrackName', 'column': 2}
    SurveyedKp = {'sheet_name': 'Dispatchable_Point', 'attribute_name': 'SurveyedKp', 'column': 3}
    NumeroPcc = {'sheet_name': 'Dispatchable_Point', 'attribute_name': 'NumeroPcc', 'column': 4}
    NamePcc = {'sheet_name': 'Dispatchable_Point', 'attribute_name': 'NamePcc', 'column': 5}


class Equipped_Cars:
    Name = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'Name', 'column': 1}
    Type = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'Type', 'column': 2}
    CbtcCarId = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'CbtcCarId', 'column': 3}
    CarCustomerName = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'CarCustomerName', 'column': 4}
    DisplayableName = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'DisplayableName', 'column': 5}
    CcName = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'CcName', 'column': 6}
    TodName = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'TodName', 'column': 7}
    PisName = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'PisName', 'column': 8}
    TarName = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'TarName', 'column': 9}
    TmsMvbBoxName = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'TmsMvbBoxName', 'column': 10}
    StreamBoxName = {'sheet_name': 'Equipped_Cars', 'attribute_name': 'StreamBoxName', 'column': 11}


class FBCO__FrictionBrakeCutout:
    EbRateRatio0 = {'sheet_name': 'FBCO', 'attribute_name': 'FrictionBrakeCutout', 'sub_attribute_name': 'EbRateRatio0', 'columns': [3]}
    PbRateRatio0 = {'sheet_name': 'FBCO', 'attribute_name': 'FrictionBrakeCutout', 'sub_attribute_name': 'PbRateRatio0', 'columns': [4]}
    MaxSpeed0 = {'sheet_name': 'FBCO', 'attribute_name': 'FrictionBrakeCutout', 'sub_attribute_name': 'MaxSpeed0', 'columns': [5]}
    EbRateRatio = {'sheet_name': 'FBCO', 'attribute_name': 'FrictionBrakeCutout', 'sub_attribute_name': 'EbRateRatio', 'columns': [6, 9, 12, 15]}
    PbRateRatio = {'sheet_name': 'FBCO', 'attribute_name': 'FrictionBrakeCutout', 'sub_attribute_name': 'PbRateRatio', 'columns': [7, 10, 13, 16]}
    MaxSpeed = {'sheet_name': 'FBCO', 'attribute_name': 'FrictionBrakeCutout', 'sub_attribute_name': 'MaxSpeed', 'columns': [8, 11, 14, 17]}


class FBCO:
    PassengerTrainConsistName = {'sheet_name': 'FBCO', 'attribute_name': 'PassengerTrainConsistName', 'column': 1}
    FbcoMaxNumber = {'sheet_name': 'FBCO', 'attribute_name': 'FbcoMaxNumber', 'column': 2}
    FrictionBrakeCutout = FBCO__FrictionBrakeCutout()


class CSR__Limit:
    Seg = {'sheet_name': 'CSR', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [3, 6, 9, 12, 15]}
    X = {'sheet_name': 'CSR', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [4, 7, 10, 13, 16]}
    Direction = {'sheet_name': 'CSR', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [5, 8, 11, 14, 17]}


class CSR:
    Name = {'sheet_name': 'CSR', 'attribute_name': 'Name', 'column': 1}
    Speed = {'sheet_name': 'CSR', 'attribute_name': 'Speed', 'column': 2}
    Limit = CSR__Limit()


class Sweeping_Zone__Limit:
    Seg = {'sheet_name': 'Sweeping_Zone', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44]}
    X = {'sheet_name': 'Sweeping_Zone', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]}
    Direction = {'sheet_name': 'Sweeping_Zone', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}


class Sweeping_Zone__SubSweepingZoneList:
    Name = {'sheet_name': 'Sweeping_Zone', 'attribute_name': 'SubSweepingZoneList', 'sub_attribute_name': 'Name', 'columns': [47, 48, 51, 51, 51, 49, 51, 51, 50, 51]}


class Sweeping_Zone:
    Name = {'sheet_name': 'Sweeping_Zone', 'attribute_name': 'Name', 'column': 1}
    Limit = Sweeping_Zone__Limit()
    SubSweepingZoneList = Sweeping_Zone__SubSweepingZoneList()


class Sub_Sweeping_Zone__Limit:
    Seg = {'sheet_name': 'Sub_Sweeping_Zone', 'attribute_name': 'Limit', 'sub_attribute_name': 'Seg', 'columns': [4, 8]}
    X = {'sheet_name': 'Sub_Sweeping_Zone', 'attribute_name': 'Limit', 'sub_attribute_name': 'X', 'columns': [5, 9]}
    Direction = {'sheet_name': 'Sub_Sweeping_Zone', 'attribute_name': 'Limit', 'sub_attribute_name': 'Direction', 'columns': [6, 10]}
    MaxDist = {'sheet_name': 'Sub_Sweeping_Zone', 'attribute_name': 'Limit', 'sub_attribute_name': 'MaxDist', 'columns': [7, 11]}


class Sub_Sweeping_Zone:
    Name = {'sheet_name': 'Sub_Sweeping_Zone', 'attribute_name': 'Name', 'column': 1}
    AsrName = {'sheet_name': 'Sub_Sweeping_Zone', 'attribute_name': 'AsrName', 'column': 2}
    AtsSubSweepingZoneId = {'sheet_name': 'Sub_Sweeping_Zone', 'attribute_name': 'AtsSubSweepingZoneId', 'column': 3}
    Limit = Sub_Sweeping_Zone__Limit()


class DCSYS:
    Ligne = Ligne()
    Voie = Voie()
    Troncon = Troncon()
    Seg = Seg()
    Aig = Aig()
    Quai = Quai()
    PtA = PtA()
    OSP_ATS_Id = OSP_ATS_Id()
    CDV = CDV()
    IVB = IVB()
    CV = CV()
    Sig = Sig()
    Sig_Zone = Sig_Zone()
    Profil = Profil()
    Bal = Bal()
    Coasting_Profiles = Coasting_Profiles()
    CELL = CELL()
    ZA_EFF_T = ZA_EFF_T()
    SP = SP()
    Iti = Iti()
    CBTC_TER = CBTC_TER()
    PAS = PAS()
    Sas_ZSM_CBTC = Sas_ZSM_CBTC()
    DP = DP()
    Sieving_Limit = Sieving_Limit()
    ZSM_CBTC = ZSM_CBTC()
    SE = SE()
    SS = SS()
    ZCI = ZCI()
    Zaum = Zaum()
    ZCRA = ZCRA()
    Zacp = Zacp()
    ZLPV = ZLPV()
    NV_PSR = NV_PSR()
    ZLPV_Or = ZLPV_Or()
    Calib = Calib()
    Zman = Zman()
    ZVR = ZVR()
    CBTC_Eqpt = CBTC_Eqpt()
    Flux_Variant_HF = Flux_Variant_HF()
    Flux_Variant_BF = Flux_Variant_BF()
    Wayside_Eqpt = Wayside_Eqpt()
    Flux_MES_PAS = Flux_MES_PAS()
    Flux_PAS_MES = Flux_PAS_MES()
    ATS_ATC = ATS_ATC()
    TM_MES_ATS = TM_MES_ATS()
    TM_PAS_ATS = TM_PAS_ATS()
    Network = Network()
    LineSection_Eqpt = LineSection_Eqpt()
    OnBoard_Eqpt = OnBoard_Eqpt()
    Interstation = Interstation()
    IATPM_tags = IATPM_tags()
    IATPM_Version_Tags = IATPM_Version_Tags()
    DynTag_Group = DynTag_Group()
    Border_Area = Border_Area()
    OVL_Border_Area = OVL_Border_Area()
    IXL_Overlap = IXL_Overlap()
    Driving_Modes = Driving_Modes()
    Unprotected_Moves = Unprotected_Moves()
    CBTC_Overlap = CBTC_Overlap()
    Performance_Level = Performance_Level()
    Restriction_Level = Restriction_Level()
    Carborne_Controllers = Carborne_Controllers()
    Car_Types = Car_Types()
    Train_Types = Train_Types()
    AV_Types = AV_Types()
    Flatbed_Types = Flatbed_Types()
    AV_Consist = AV_Consist()
    Train_Consist = Train_Consist()
    Train = Train()
    Auxiliary_Vehicle = Auxiliary_Vehicle()
    Traction_Profiles = Traction_Profiles()
    Flood_Gate = Flood_Gate()
    Coupling_Area = Coupling_Area()
    Floor_Levels = Floor_Levels()
    EB_Rate_Area = EB_Rate_Area()
    Unwanted_Stop_Area = Unwanted_Stop_Area()
    Consist_OSP = Consist_OSP()
    Walkways_Area = Walkways_Area()
    Customs_Area = Customs_Area()
    CBTC_Prohibition_Area = CBTC_Prohibition_Area()
    TSR_Area = TSR_Area()
    Anchor = Anchor()
    Chainage = Chainage()
    Superseed_Tan = Superseed_Tan()
    Dynamic_Brake_Test_Point = Dynamic_Brake_Test_Point()
    Traffic_Stop = Traffic_Stop()
    Protection_Zone = Protection_Zone()
    Crossing_Calling_Area = Crossing_Calling_Area()
    ASR = ASR()
    PSD_Subsets = PSD_Subsets()
    DCM_Transition_Zones = DCM_Transition_Zones()
    Adhesion_Zones = Adhesion_Zones()
    Adhesion_Level = Adhesion_Level()
    Frontam_General_Data = Frontam_General_Data()
    Generic_Command_Zones = Generic_Command_Zones()
    DCS_Elementary_Zones = DCS_Elementary_Zones()
    TSR_Possible_Speeds = TSR_Possible_Speeds()
    TD_Subsets = TD_Subsets()
    Unwanted_Coupling_Area = Unwanted_Coupling_Area()
    Cruising_Zones = Cruising_Zones()
    Passage_Detector = Passage_Detector()
    Parking_Place = Parking_Place()
    StaticTag_Group = StaticTag_Group()
    Odometric_Zone = Odometric_Zone()
    Presence_Detector = Presence_Detector()
    Dispatchable_Point = Dispatchable_Point()
    Equipped_Cars = Equipped_Cars()
    FBCO = FBCO()
    CSR = CSR()
    Sweeping_Zone = Sweeping_Zone()
    Sub_Sweeping_Zone = Sub_Sweeping_Zone()
