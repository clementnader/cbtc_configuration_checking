#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------------------------ #
# Automatically generated Python file defining a DCSYS class containing the column information of  #
# sheets and attributes from the CCTool-OO Schema sheet of the CCTool-OO Schema file.              #
# ------------------------------------------------------------------------------------------------ #
# Compliant with Ref Sys 07-03-03-00                                                               #
# ------------------------------------------------------------------------------------------------ #


class Ligne__SegmentsDepolarises:
	Cell = {'sh_name': 'Ligne', 'attr_name': 'SegmentsDepolarises', 'sub_attr_name': 'Cell', 'cols': [7, 8, 9, 10, 11, 12, 13, 14]}


class Ligne__LoopbackSegments:
	Cell = {'sh_name': 'Ligne', 'attr_name': 'LoopbackSegments', 'sub_attr_name': 'Cell', 'cols': [18, 19, 20, 21, 22, 23, 24, 25]}


class Ligne:
	Nom = {'sh_name': 'Ligne', 'attr_name': 'Nom', 'col': 1}
	Numero = {'sh_name': 'Ligne', 'attr_name': 'Numero', 'col': 2}
	Referentiel = {'sh_name': 'Ligne', 'attr_name': 'Referentiel', 'col': 3}
	SegmentReference = {'sh_name': 'Ligne', 'attr_name': 'SegmentReference', 'col': 4}
	OrientationGauche = {'sh_name': 'Ligne', 'attr_name': 'OrientationGauche', 'col': 5}
	OrientationDroite = {'sh_name': 'Ligne', 'attr_name': 'OrientationDroite', 'col': 6}
	SegmentsDepolarises = Ligne__SegmentsDepolarises()
	Version = {'sh_name': 'Ligne', 'attr_name': 'Version', 'col': 15}
	CbtcVersionKey = {'sh_name': 'Ligne', 'attr_name': 'CbtcVersionKey', 'col': 16}
	CbtcVersionRelease = {'sh_name': 'Ligne', 'attr_name': 'CbtcVersionRelease', 'col': 17}
	LoopbackSegments = Ligne__LoopbackSegments()


class Voie:
	Nom = {'sh_name': 'Voie', 'attr_name': 'Nom', 'col': 1}
	Ligne = {'sh_name': 'Voie', 'attr_name': 'Ligne', 'col': 2}
	NumeroSurLigne = {'sh_name': 'Voie', 'attr_name': 'NumeroSurLigne', 'col': 3}
	NomPcc = {'sh_name': 'Voie', 'attr_name': 'NomPcc', 'col': 4}
	Type = {'sh_name': 'Voie', 'attr_name': 'Type', 'col': 5}
	SensNominal = {'sh_name': 'Voie', 'attr_name': 'SensNominal', 'col': 6}
	PkDebut = {'sh_name': 'Voie', 'attr_name': 'PkDebut', 'col': 7}
	PkFin = {'sh_name': 'Voie', 'attr_name': 'PkFin', 'col': 8}


class Troncon__ExtremiteSurVoie:
	Voie = {'sh_name': 'Troncon', 'attr_name': 'ExtremiteSurVoie', 'sub_attr_name': 'Voie', 'cols': [9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66]}
	PkDebut = {'sh_name': 'Troncon', 'attr_name': 'ExtremiteSurVoie', 'sub_attr_name': 'PkDebut', 'cols': [10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67]}
	PkFin = {'sh_name': 'Troncon', 'attr_name': 'ExtremiteSurVoie', 'sub_attr_name': 'PkFin', 'cols': [11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68]}


class Troncon:
	Nom = {'sh_name': 'Troncon', 'attr_name': 'Nom', 'col': 1}
	Ligne = {'sh_name': 'Troncon', 'attr_name': 'Ligne', 'col': 2}
	NumeroTronconLigne = {'sh_name': 'Troncon', 'attr_name': 'NumeroTronconLigne', 'col': 3}
	NumVersion = {'sh_name': 'Troncon', 'attr_name': 'NumVersion', 'col': 4}
	TronconUtile1 = {'sh_name': 'Troncon', 'attr_name': 'TronconUtile1', 'col': 5}
	TronconUtile2 = {'sh_name': 'Troncon', 'attr_name': 'TronconUtile2', 'col': 6}
	TronconUtile3 = {'sh_name': 'Troncon', 'attr_name': 'TronconUtile3', 'col': 7}
	TronconUtile4 = {'sh_name': 'Troncon', 'attr_name': 'TronconUtile4', 'col': 8}
	ExtremiteSurVoie = Troncon__ExtremiteSurVoie()


class Seg__SegmentsVoisins:
	Amont = {'sh_name': 'Seg', 'attr_name': 'SegmentsVoisins', 'sub_attr_name': 'Amont', 'cols': [8, 9]}
	Aval = {'sh_name': 'Seg', 'attr_name': 'SegmentsVoisins', 'sub_attr_name': 'Aval', 'cols': [10, 11]}


class Seg:
	Nom = {'sh_name': 'Seg', 'attr_name': 'Nom', 'col': 1}
	Troncon = {'sh_name': 'Seg', 'attr_name': 'Troncon', 'col': 2}
	NumSegmentTroncon = {'sh_name': 'Seg', 'attr_name': 'NumSegmentTroncon', 'col': 3}
	Voie = {'sh_name': 'Seg', 'attr_name': 'Voie', 'col': 4}
	Origine = {'sh_name': 'Seg', 'attr_name': 'Origine', 'col': 5}
	Fin = {'sh_name': 'Seg', 'attr_name': 'Fin', 'col': 6}
	Longueur = {'sh_name': 'Seg', 'attr_name': 'Longueur', 'col': 7}
	SegmentsVoisins = Seg__SegmentsVoisins()
	SensLigne = {'sh_name': 'Seg', 'attr_name': 'SensLigne', 'col': 12}
	RingSegment = {'sh_name': 'Seg', 'attr_name': 'RingSegment', 'col': 13}
	RejectionDistance = {'sh_name': 'Seg', 'attr_name': 'RejectionDistance', 'col': 14}


class Aig__SwitchBlockLockingArea:
	Ivb = {'sh_name': 'Aig', 'attr_name': 'SwitchBlockLockingArea', 'sub_attr_name': 'Ivb', 'cols': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}


class Aig__CbtcProtectingSwitchArea:
	Ivb = {'sh_name': 'Aig', 'attr_name': 'CbtcProtectingSwitchArea', 'sub_attr_name': 'Ivb', 'cols': [18, 19, 20, 21, 22, 23, 24, 25, 26, 27]}


class Aig__AreaRightPositionFlank:
	BeginSeg = {'sh_name': 'Aig', 'attr_name': 'AreaRightPositionFlank', 'sub_attr_name': 'BeginSeg', 'cols': [28, 33, 38, 43]}
	BeginX = {'sh_name': 'Aig', 'attr_name': 'AreaRightPositionFlank', 'sub_attr_name': 'BeginX', 'cols': [29, 34, 39, 44]}
	EndSeg = {'sh_name': 'Aig', 'attr_name': 'AreaRightPositionFlank', 'sub_attr_name': 'EndSeg', 'cols': [30, 35, 40, 45]}
	EndX = {'sh_name': 'Aig', 'attr_name': 'AreaRightPositionFlank', 'sub_attr_name': 'EndX', 'cols': [31, 36, 41, 46]}
	Direction = {'sh_name': 'Aig', 'attr_name': 'AreaRightPositionFlank', 'sub_attr_name': 'Direction', 'cols': [32, 37, 42, 47]}


class Aig__AreaLeftPositionFlank:
	BeginSeg = {'sh_name': 'Aig', 'attr_name': 'AreaLeftPositionFlank', 'sub_attr_name': 'BeginSeg', 'cols': [48, 53, 58, 63]}
	BeginX = {'sh_name': 'Aig', 'attr_name': 'AreaLeftPositionFlank', 'sub_attr_name': 'BeginX', 'cols': [49, 54, 59, 64]}
	EndSeg = {'sh_name': 'Aig', 'attr_name': 'AreaLeftPositionFlank', 'sub_attr_name': 'EndSeg', 'cols': [50, 55, 60, 65]}
	EndX = {'sh_name': 'Aig', 'attr_name': 'AreaLeftPositionFlank', 'sub_attr_name': 'EndX', 'cols': [51, 56, 61, 66]}
	Direction = {'sh_name': 'Aig', 'attr_name': 'AreaLeftPositionFlank', 'sub_attr_name': 'Direction', 'cols': [52, 57, 62, 67]}


class Aig:
	Nom = {'sh_name': 'Aig', 'attr_name': 'Nom', 'col': 1}
	SegmentPointe = {'sh_name': 'Aig', 'attr_name': 'SegmentPointe', 'col': 2}
	SegmentTd = {'sh_name': 'Aig', 'attr_name': 'SegmentTd', 'col': 3}
	SegmentTg = {'sh_name': 'Aig', 'attr_name': 'SegmentTg', 'col': 4}
	NumeroPcc = {'sh_name': 'Aig', 'attr_name': 'NumeroPcc', 'col': 5}
	SwitchBlockLockingArea = Aig__SwitchBlockLockingArea()
	FreeToMove = {'sh_name': 'Aig', 'attr_name': 'FreeToMove', 'col': 16}
	Trailable = {'sh_name': 'Aig', 'attr_name': 'Trailable', 'col': 17}
	CbtcProtectingSwitchArea = Aig__CbtcProtectingSwitchArea()
	AreaRightPositionFlank = Aig__AreaRightPositionFlank()
	AreaLeftPositionFlank = Aig__AreaLeftPositionFlank()


class Quai__Station:
	Nom = {'sh_name': 'Quai', 'attr_name': 'Station', 'sub_attr_name': 'Nom', 'cols': [3]}
	Abreviation = {'sh_name': 'Quai', 'attr_name': 'Station', 'sub_attr_name': 'Abreviation', 'cols': [4]}
	NumStationLigne = {'sh_name': 'Quai', 'attr_name': 'Station', 'sub_attr_name': 'NumStationLigne', 'cols': [5]}


class Quai__ExtremiteDuQuai:
	Seg = {'sh_name': 'Quai', 'attr_name': 'ExtremiteDuQuai', 'sub_attr_name': 'Seg', 'cols': [9, 17]}
	X = {'sh_name': 'Quai', 'attr_name': 'ExtremiteDuQuai', 'sub_attr_name': 'X', 'cols': [10, 18]}
	CoteOuvPortes = {'sh_name': 'Quai', 'attr_name': 'ExtremiteDuQuai', 'sub_attr_name': 'CoteOuvPortes', 'cols': [11, 19]}
	SensExt = {'sh_name': 'Quai', 'attr_name': 'ExtremiteDuQuai', 'sub_attr_name': 'SensExt', 'cols': [12, 20]}
	Voie = {'sh_name': 'Quai', 'attr_name': 'ExtremiteDuQuai', 'sub_attr_name': 'Voie', 'cols': [13, 21]}
	Pk = {'sh_name': 'Quai', 'attr_name': 'ExtremiteDuQuai', 'sub_attr_name': 'Pk', 'cols': [14, 22]}
	CvspDistance = {'sh_name': 'Quai', 'attr_name': 'ExtremiteDuQuai', 'sub_attr_name': 'CvspDistance', 'cols': [15, 23]}
	TerminalStation = {'sh_name': 'Quai', 'attr_name': 'ExtremiteDuQuai', 'sub_attr_name': 'TerminalStation', 'cols': [16, 24]}


class Quai__PointDArret:
	Name = {'sh_name': 'Quai', 'attr_name': 'PointDArret', 'sub_attr_name': 'Name', 'cols': [25, 35, 45]}
	Number = {'sh_name': 'Quai', 'attr_name': 'PointDArret', 'sub_attr_name': 'Number', 'cols': [26, 36, 46]}
	Seg = {'sh_name': 'Quai', 'attr_name': 'PointDArret', 'sub_attr_name': 'Seg', 'cols': [27, 37, 47]}
	X = {'sh_name': 'Quai', 'attr_name': 'PointDArret', 'sub_attr_name': 'X', 'cols': [28, 38, 48]}
	SensAssocie = {'sh_name': 'Quai', 'attr_name': 'PointDArret', 'sub_attr_name': 'SensAssocie', 'cols': [29, 39, 49]}
	SensApproche = {'sh_name': 'Quai', 'attr_name': 'PointDArret', 'sub_attr_name': 'SensApproche', 'cols': [30, 40, 50]}
	TypePtArretQuai = {'sh_name': 'Quai', 'attr_name': 'PointDArret', 'sub_attr_name': 'TypePtArretQuai', 'cols': [31, 41, 51]}
	StaticTest = {'sh_name': 'Quai', 'attr_name': 'PointDArret', 'sub_attr_name': 'StaticTest', 'cols': [32, 42, 52]}
	Voie = {'sh_name': 'Quai', 'attr_name': 'PointDArret', 'sub_attr_name': 'Voie', 'cols': [33, 43, 53]}
	Pk = {'sh_name': 'Quai', 'attr_name': 'PointDArret', 'sub_attr_name': 'Pk', 'cols': [34, 44, 54]}


class Quai__PointDEntree:
	Seg = {'sh_name': 'Quai', 'attr_name': 'PointDEntree', 'sub_attr_name': 'Seg', 'cols': [55, 59, 63, 67, 71, 75]}
	X = {'sh_name': 'Quai', 'attr_name': 'PointDEntree', 'sub_attr_name': 'X', 'cols': [56, 60, 64, 68, 72, 76]}
	Voie = {'sh_name': 'Quai', 'attr_name': 'PointDEntree', 'sub_attr_name': 'Voie', 'cols': [57, 61, 65, 69, 73, 77]}
	Pk = {'sh_name': 'Quai', 'attr_name': 'PointDEntree', 'sub_attr_name': 'Pk', 'cols': [58, 62, 66, 70, 74, 78]}


class Quai__FacadesDeQuai:
	EqptCfq = {'sh_name': 'Quai', 'attr_name': 'FacadesDeQuai', 'sub_attr_name': 'EqptCfq', 'cols': [89]}
	CoteFq = {'sh_name': 'Quai', 'attr_name': 'FacadesDeQuai', 'sub_attr_name': 'CoteFq', 'cols': [90]}


class Quai:
	Nom = {'sh_name': 'Quai', 'attr_name': 'Nom', 'col': 1}
	NumQuaiStation = {'sh_name': 'Quai', 'attr_name': 'NumQuaiStation', 'col': 2}
	Station = Quai__Station()
	InhibAccessibilite = {'sh_name': 'Quai', 'attr_name': 'InhibAccessibilite', 'col': 6}
	CheckBrakes = {'sh_name': 'Quai', 'attr_name': 'CheckBrakes', 'col': 7}
	AllowAccelerometersCalibration = {'sh_name': 'Quai', 'attr_name': 'AllowAccelerometersCalibration', 'col': 8}
	ExtremiteDuQuai = Quai__ExtremiteDuQuai()
	PointDArret = Quai__PointDArret()
	PointDEntree = Quai__PointDEntree()
	AvecPassagers = {'sh_name': 'Quai', 'attr_name': 'AvecPassagers', 'col': 79}
	AvecFq = {'sh_name': 'Quai', 'attr_name': 'AvecFq', 'col': 80}
	PsdNumber = {'sh_name': 'Quai', 'attr_name': 'PsdNumber', 'col': 81}
	PsdNumbering = {'sh_name': 'Quai', 'attr_name': 'PsdNumbering', 'col': 82}
	AvecPrecPtArret = {'sh_name': 'Quai', 'attr_name': 'AvecPrecPtArret', 'col': 83}
	RightSideOpeningTime = {'sh_name': 'Quai', 'attr_name': 'RightSideOpeningTime', 'col': 84}
	LeftSideOpeningTime = {'sh_name': 'Quai', 'attr_name': 'LeftSideOpeningTime', 'col': 85}
	DoublePlatformOpeningDelay = {'sh_name': 'Quai', 'attr_name': 'DoublePlatformOpeningDelay', 'col': 86}
	DisableAutomaticDoorClosing = {'sh_name': 'Quai', 'attr_name': 'DisableAutomaticDoorClosing', 'col': 87}
	RelatedWaysideEquip = {'sh_name': 'Quai', 'attr_name': 'RelatedWaysideEquip', 'col': 88}
	FacadesDeQuai = Quai__FacadesDeQuai()
	NumeroPccQuai = {'sh_name': 'Quai', 'attr_name': 'NumeroPccQuai', 'col': 91}
	NumeroPccStation = {'sh_name': 'Quai', 'attr_name': 'NumeroPccStation', 'col': 92}
	WithEss = {'sh_name': 'Quai', 'attr_name': 'WithEss', 'col': 93}
	WithTh = {'sh_name': 'Quai', 'attr_name': 'WithTh', 'col': 94}
	WithTad = {'sh_name': 'Quai', 'attr_name': 'WithTad', 'col': 95}
	PsdMessagesRouted = {'sh_name': 'Quai', 'attr_name': 'PsdMessagesRouted', 'col': 96}
	Router = {'sh_name': 'Quai', 'attr_name': 'Router', 'col': 97}


class PtA:
	Nom = {'sh_name': 'PtA', 'attr_name': 'Nom', 'col': 1}
	NumPtAtoSegment = {'sh_name': 'PtA', 'attr_name': 'NumPtAtoSegment', 'col': 2}
	Seg = {'sh_name': 'PtA', 'attr_name': 'Seg', 'col': 3}
	X = {'sh_name': 'PtA', 'attr_name': 'X', 'col': 4}
	SensAssocie = {'sh_name': 'PtA', 'attr_name': 'SensAssocie', 'col': 5}
	SensApproche = {'sh_name': 'PtA', 'attr_name': 'SensApproche', 'col': 6}
	Voie = {'sh_name': 'PtA', 'attr_name': 'Voie', 'col': 7}
	Pk = {'sh_name': 'PtA', 'attr_name': 'Pk', 'col': 8}
	TypePtAto = {'sh_name': 'PtA', 'attr_name': 'TypePtAto', 'col': 9}
	ArretPermanentCpa = {'sh_name': 'PtA', 'attr_name': 'ArretPermanentCpa', 'col': 10}
	ParkingPosition = {'sh_name': 'PtA', 'attr_name': 'ParkingPosition', 'col': 11}
	StaticTestAllowed = {'sh_name': 'PtA', 'attr_name': 'StaticTestAllowed', 'col': 12}
	TrainDoorsOpeningSide = {'sh_name': 'PtA', 'attr_name': 'TrainDoorsOpeningSide', 'col': 13}
	WashingOsp = {'sh_name': 'PtA', 'attr_name': 'WashingOsp', 'col': 14}
	OspProxDist = {'sh_name': 'PtA', 'attr_name': 'OspProxDist', 'col': 15}
	AllowAccelerometersCalibration = {'sh_name': 'PtA', 'attr_name': 'AllowAccelerometersCalibration', 'col': 16}


class OSP_ATS_Id:
	Name = {'sh_name': 'OSP_ATS_Id', 'attr_name': 'Name', 'col': 1}
	Type = {'sh_name': 'OSP_ATS_Id', 'attr_name': 'Type', 'col': 2}
	AtsId = {'sh_name': 'OSP_ATS_Id', 'attr_name': 'AtsId', 'col': 3}


class CDV__Extremite:
	Seg = {'sh_name': 'CDV', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [14, 16, 18, 20, 22, 24, 26, 28, 30, 32]}
	X = {'sh_name': 'CDV', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [15, 17, 19, 21, 23, 25, 27, 29, 31, 33]}
	Voie = {'sh_name': 'CDV', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [34, 36, 38, 40, 42, 44, 46, 48, 50, 52]}
	Pk = {'sh_name': 'CDV', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [35, 37, 39, 41, 43, 45, 47, 49, 51, 53]}


class CDV__AnticipationSecuritaire:
	Ext = {'sh_name': 'CDV', 'attr_name': 'AnticipationSecuritaire', 'sub_attr_name': 'Ext', 'cols': [54, 55, 56, 57, 58, 59, 60, 61, 62, 63]}


class CDV__AnticipationErgonomique:
	Ext = {'sh_name': 'CDV', 'attr_name': 'AnticipationErgonomique', 'sub_attr_name': 'Ext', 'cols': [64, 65, 66, 67, 68, 69, 70, 71, 72, 73]}


class CDV:
	Nom = {'sh_name': 'CDV', 'attr_name': 'Nom', 'col': 1}
	DetectArb = {'sh_name': 'CDV', 'attr_name': 'DetectArb', 'col': 2}
	DetectNcArb = {'sh_name': 'CDV', 'attr_name': 'DetectNcArb', 'col': 3}
	DetectNrb = {'sh_name': 'CDV', 'attr_name': 'DetectNrb', 'col': 4}
	DetectNcNrb = {'sh_name': 'CDV', 'attr_name': 'DetectNcNrb', 'col': 5}
	AFiabiliser = {'sh_name': 'CDV', 'attr_name': 'AFiabiliser', 'col': 6}
	ExtendedSievingAllowed = {'sh_name': 'CDV', 'attr_name': 'ExtendedSievingAllowed', 'col': 7}
	RailRoadEntrance = {'sh_name': 'CDV', 'attr_name': 'RailRoadEntrance', 'col': 8}
	BrokenRailDetection = {'sh_name': 'CDV', 'attr_name': 'BrokenRailDetection', 'col': 9}
	DedicatedLineSection = {'sh_name': 'CDV', 'attr_name': 'DedicatedLineSection', 'col': 10}
	ReachBlockAllowed = {'sh_name': 'CDV', 'attr_name': 'ReachBlockAllowed', 'col': 11}
	IxlGivesBlockInitStatus = {'sh_name': 'CDV', 'attr_name': 'IxlGivesBlockInitStatus', 'col': 12}
	IxlGivesNotHeldStatus = {'sh_name': 'CDV', 'attr_name': 'IxlGivesNotHeldStatus', 'col': 13}
	Extremite = CDV__Extremite()
	AnticipationSecuritaire = CDV__AnticipationSecuritaire()
	AnticipationErgonomique = CDV__AnticipationErgonomique()
	AtsBlockId = {'sh_name': 'CDV', 'attr_name': 'AtsBlockId', 'col': 74}


class IVB__Limit:
	Seg = {'sh_name': 'IVB', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [10, 12, 14, 16, 18, 20, 22, 24, 26, 28]}
	X = {'sh_name': 'IVB', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [11, 13, 15, 17, 19, 21, 23, 25, 27, 29]}
	Track = {'sh_name': 'IVB', 'attr_name': 'Limit', 'sub_attr_name': 'Track', 'cols': [30, 32, 34, 36, 38, 40, 42, 44, 46, 48]}
	Kp = {'sh_name': 'IVB', 'attr_name': 'Limit', 'sub_attr_name': 'Kp', 'cols': [31, 33, 35, 37, 39, 41, 43, 45, 47, 49]}


class IVB__DiamondCrossingSwitches:
	SwitchName = {'sh_name': 'IVB', 'attr_name': 'DiamondCrossingSwitches', 'sub_attr_name': 'SwitchName', 'cols': [51, 52, 53, 54]}


class IVB:
	Name = {'sh_name': 'IVB', 'attr_name': 'Name', 'col': 1}
	Id = {'sh_name': 'IVB', 'attr_name': 'Id', 'col': 2}
	SentToIxl = {'sh_name': 'IVB', 'attr_name': 'SentToIxl', 'col': 3}
	UsedByIxl = {'sh_name': 'IVB', 'attr_name': 'UsedByIxl', 'col': 4}
	BlockFreed = {'sh_name': 'IVB', 'attr_name': 'BlockFreed', 'col': 5}
	ZcName = {'sh_name': 'IVB', 'attr_name': 'ZcName', 'col': 6}
	DirectionLockingBlock = {'sh_name': 'IVB', 'attr_name': 'DirectionLockingBlock', 'col': 7}
	UnlockNormal = {'sh_name': 'IVB', 'attr_name': 'UnlockNormal', 'col': 8}
	UnlockReverse = {'sh_name': 'IVB', 'attr_name': 'UnlockReverse', 'col': 9}
	Limit = IVB__Limit()
	DiamondCrossing = {'sh_name': 'IVB', 'attr_name': 'DiamondCrossing', 'col': 50}
	DiamondCrossingSwitches = IVB__DiamondCrossingSwitches()
	RelatedBlock = {'sh_name': 'IVB', 'attr_name': 'RelatedBlock', 'col': 55}


class CV__Extremite:
	Seg = {'sh_name': 'CV', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [2, 4, 6]}
	X = {'sh_name': 'CV', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [3, 5, 7]}
	Voie = {'sh_name': 'CV', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [8, 10, 12]}
	Pk = {'sh_name': 'CV', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [9, 11, 13]}


class CV:
	Nom = {'sh_name': 'CV', 'attr_name': 'Nom', 'col': 1}
	Extremite = CV__Extremite()
	IsEndOfTrack = {'sh_name': 'CV', 'attr_name': 'IsEndOfTrack', 'col': 14}


class Sig__IvbJoint:
	UpstreamIvb = {'sh_name': 'Sig', 'attr_name': 'IvbJoint', 'sub_attr_name': 'UpstreamIvb', 'cols': [12]}
	DownstreamIvb = {'sh_name': 'Sig', 'attr_name': 'IvbJoint', 'sub_attr_name': 'DownstreamIvb', 'cols': [13]}


class Sig:
	Nom = {'sh_name': 'Sig', 'attr_name': 'Nom', 'col': 1}
	Type = {'sh_name': 'Sig', 'attr_name': 'Type', 'col': 2}
	Seg = {'sh_name': 'Sig', 'attr_name': 'Seg', 'col': 3}
	X = {'sh_name': 'Sig', 'attr_name': 'X', 'col': 4}
	Sens = {'sh_name': 'Sig', 'attr_name': 'Sens', 'col': 5}
	Voie = {'sh_name': 'Sig', 'attr_name': 'Voie', 'col': 6}
	Pk = {'sh_name': 'Sig', 'attr_name': 'Pk', 'col': 7}
	R_Cli = {'sh_name': 'Sig', 'attr_name': 'R_Cli', 'col': 8}
	DistPap = {'sh_name': 'Sig', 'attr_name': 'DistPap', 'col': 9}
	VspType = {'sh_name': 'Sig', 'attr_name': 'VspType', 'col': 10}
	DelayedLtDistance = {'sh_name': 'Sig', 'attr_name': 'DelayedLtDistance', 'col': 11}
	IvbJoint = Sig__IvbJoint()
	Da_Passage = {'sh_name': 'Sig', 'attr_name': 'Da_Passage', 'col': 14}
	TypeDa = {'sh_name': 'Sig', 'attr_name': 'TypeDa', 'col': 15}
	D_Echap = {'sh_name': 'Sig', 'attr_name': 'D_Echap', 'col': 16}
	Du_Assistee = {'sh_name': 'Sig', 'attr_name': 'Du_Assistee', 'col': 17}
	D_Libre = {'sh_name': 'Sig', 'attr_name': 'D_Libre', 'col': 18}
	Enc_Dep = {'sh_name': 'Sig', 'attr_name': 'Enc_Dep', 'col': 19}
	OverlapType = {'sh_name': 'Sig', 'attr_name': 'OverlapType', 'col': 20}
	Annulable = {'sh_name': 'Sig', 'attr_name': 'Annulable', 'col': 21}
	WithFunc_Stop = {'sh_name': 'Sig', 'attr_name': 'WithFunc_Stop', 'col': 22}
	CbtcTrainAppProvided = {'sh_name': 'Sig', 'attr_name': 'CbtcTrainAppProvided', 'col': 23}
	NumeroPcc = {'sh_name': 'Sig', 'attr_name': 'NumeroPcc', 'col': 24}
	PositionForcee = {'sh_name': 'Sig', 'attr_name': 'PositionForcee', 'col': 25}
	SortieTerritoireCbtc = {'sh_name': 'Sig', 'attr_name': 'SortieTerritoireCbtc', 'col': 26}
	PresenceDynamicTag = {'sh_name': 'Sig', 'attr_name': 'PresenceDynamicTag', 'col': 27}
	WithIatpDepCheck = {'sh_name': 'Sig', 'attr_name': 'WithIatpDepCheck', 'col': 28}
	RelatedTag1 = {'sh_name': 'Sig', 'attr_name': 'RelatedTag1', 'col': 29}
	RelatedTag2 = {'sh_name': 'Sig', 'attr_name': 'RelatedTag2', 'col': 30}
	RelatedTag3 = {'sh_name': 'Sig', 'attr_name': 'RelatedTag3', 'col': 31}
	RelatedTag4 = {'sh_name': 'Sig', 'attr_name': 'RelatedTag4', 'col': 32}
	RelatedTag5 = {'sh_name': 'Sig', 'attr_name': 'RelatedTag5', 'col': 33}
	RelatedTag6 = {'sh_name': 'Sig', 'attr_name': 'RelatedTag6', 'col': 34}
	RelatedTag7 = {'sh_name': 'Sig', 'attr_name': 'RelatedTag7', 'col': 35}
	RelatedTag8 = {'sh_name': 'Sig', 'attr_name': 'RelatedTag8', 'col': 36}
	RelatedTag9 = {'sh_name': 'Sig', 'attr_name': 'RelatedTag9', 'col': 37}
	RelatedTag10 = {'sh_name': 'Sig', 'attr_name': 'RelatedTag10', 'col': 38}


class Sig_Zone__ExtremitesZoneArmementDa:
	Seg = {'sh_name': 'Sig_Zone', 'attr_name': 'ExtremitesZoneArmementDa', 'sub_attr_name': 'Seg', 'cols': [2, 6, 10, 14, 18, 22]}
	X = {'sh_name': 'Sig_Zone', 'attr_name': 'ExtremitesZoneArmementDa', 'sub_attr_name': 'X', 'cols': [3, 7, 11, 15, 19, 23]}
	Voie = {'sh_name': 'Sig_Zone', 'attr_name': 'ExtremitesZoneArmementDa', 'sub_attr_name': 'Voie', 'cols': [4, 8, 12, 16, 20, 24]}
	Pk = {'sh_name': 'Sig_Zone', 'attr_name': 'ExtremitesZoneArmementDa', 'sub_attr_name': 'Pk', 'cols': [5, 9, 13, 17, 21, 25]}


class Sig_Zone__PointsDEntreeZoneDApproche:
	Seg = {'sh_name': 'Sig_Zone', 'attr_name': 'PointsDEntreeZoneDApproche', 'sub_attr_name': 'Seg', 'cols': [26, 30, 34, 38, 42, 46]}
	X = {'sh_name': 'Sig_Zone', 'attr_name': 'PointsDEntreeZoneDApproche', 'sub_attr_name': 'X', 'cols': [27, 31, 35, 39, 43, 47]}
	Voie = {'sh_name': 'Sig_Zone', 'attr_name': 'PointsDEntreeZoneDApproche', 'sub_attr_name': 'Voie', 'cols': [28, 32, 36, 40, 44, 48]}
	Pk = {'sh_name': 'Sig_Zone', 'attr_name': 'PointsDEntreeZoneDApproche', 'sub_attr_name': 'Pk', 'cols': [29, 33, 37, 41, 45, 49]}


class Sig_Zone__PointsDEntreeZoneEnclDepass:
	Seg = {'sh_name': 'Sig_Zone', 'attr_name': 'PointsDEntreeZoneEnclDepass', 'sub_attr_name': 'Seg', 'cols': [50, 54, 58, 62, 66, 70]}
	X = {'sh_name': 'Sig_Zone', 'attr_name': 'PointsDEntreeZoneEnclDepass', 'sub_attr_name': 'X', 'cols': [51, 55, 59, 63, 67, 71]}
	Voie = {'sh_name': 'Sig_Zone', 'attr_name': 'PointsDEntreeZoneEnclDepass', 'sub_attr_name': 'Voie', 'cols': [52, 56, 60, 64, 68, 72]}
	Pk = {'sh_name': 'Sig_Zone', 'attr_name': 'PointsDEntreeZoneEnclDepass', 'sub_attr_name': 'Pk', 'cols': [53, 57, 61, 65, 69, 73]}


class Sig_Zone__ItiInterdictionAnnulation:
	Iti = {'sh_name': 'Sig_Zone', 'attr_name': 'ItiInterdictionAnnulation', 'sub_attr_name': 'Iti', 'cols': [74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93]}


class Sig_Zone__ConcealBlocksList:
	Block = {'sh_name': 'Sig_Zone', 'attr_name': 'ConcealBlocksList', 'sub_attr_name': 'Block', 'cols': [94, 95, 96, 97, 98, 99, 100, 101, 102, 103]}


class Sig_Zone:
	NomDuSignal = {'sh_name': 'Sig_Zone', 'attr_name': 'NomDuSignal', 'col': 1}
	ExtremitesZoneArmementDa = Sig_Zone__ExtremitesZoneArmementDa()
	PointsDEntreeZoneDApproche = Sig_Zone__PointsDEntreeZoneDApproche()
	PointsDEntreeZoneEnclDepass = Sig_Zone__PointsDEntreeZoneEnclDepass()
	ItiInterdictionAnnulation = Sig_Zone__ItiInterdictionAnnulation()
	ConcealBlocksList = Sig_Zone__ConcealBlocksList()


class Profil:
	Pente = {'sh_name': 'Profil', 'attr_name': 'Pente', 'col': 1}
	Seg = {'sh_name': 'Profil', 'attr_name': 'Seg', 'col': 2}
	X = {'sh_name': 'Profil', 'attr_name': 'X', 'col': 3}
	Voie = {'sh_name': 'Profil', 'attr_name': 'Voie', 'col': 4}
	Pk = {'sh_name': 'Profil', 'attr_name': 'Pk', 'col': 5}


class Bal:
	Nom = {'sh_name': 'Bal', 'attr_name': 'Nom', 'col': 1}
	BaliseName = {'sh_name': 'Bal', 'attr_name': 'BaliseName', 'col': 2}
	NumBaliseSeg = {'sh_name': 'Bal', 'attr_name': 'NumBaliseSeg', 'col': 3}
	Seg = {'sh_name': 'Bal', 'attr_name': 'Seg', 'col': 4}
	X = {'sh_name': 'Bal', 'attr_name': 'X', 'col': 5}
	Voie = {'sh_name': 'Bal', 'attr_name': 'Voie', 'col': 6}
	Pk = {'sh_name': 'Bal', 'attr_name': 'Pk', 'col': 7}
	TypePose = {'sh_name': 'Bal', 'attr_name': 'TypePose', 'col': 8}
	NumeroPcc = {'sh_name': 'Bal', 'attr_name': 'NumeroPcc', 'col': 9}
	ReadingOccurrence = {'sh_name': 'Bal', 'attr_name': 'ReadingOccurrence', 'col': 10}


class Coasting_Profiles__CoastingZone:
	TriggerSpeed = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CoastingZone', 'sub_attr_name': 'TriggerSpeed', 'cols': [8, 43, 78]}
	StartTrack = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CoastingZone', 'sub_attr_name': 'StartTrack', 'cols': [9, 44, 79]}
	StartKp = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CoastingZone', 'sub_attr_name': 'StartKp', 'cols': [10, 45, 80]}
	EndTrack = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CoastingZone', 'sub_attr_name': 'EndTrack', 'cols': [11, 46, 81]}
	EndKp = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CoastingZone', 'sub_attr_name': 'EndKp', 'cols': [12, 47, 82]}
	Seg = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CoastingZone', 'sub_attr_name': 'Seg', 'cols': [13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 83, 86, 89, 92, 95, 98, 101, 104, 107, 110]}
	X = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CoastingZone', 'sub_attr_name': 'X', 'cols': [14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 84, 87, 90, 93, 96, 99, 102, 105, 108, 111]}
	Direction = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CoastingZone', 'sub_attr_name': 'Direction', 'cols': [15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 85, 88, 91, 94, 97, 100, 103, 106, 109, 112]}


class Coasting_Profiles:
	CoastingProfileName = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CoastingProfileName', 'col': 1}
	Origin = {'sh_name': 'Coasting_Profiles', 'attr_name': 'Origin', 'col': 2}
	Destination = {'sh_name': 'Coasting_Profiles', 'attr_name': 'Destination', 'col': 3}
	CoastingProfileLevel = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CoastingProfileLevel', 'col': 4}
	TheoreticalRuntime = {'sh_name': 'Coasting_Profiles', 'attr_name': 'TheoreticalRuntime', 'col': 5}
	CruisingSpeed = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CruisingSpeed', 'col': 6}
	CruisingZoneName = {'sh_name': 'Coasting_Profiles', 'attr_name': 'CruisingZoneName', 'col': 7}
	CoastingZone = Coasting_Profiles__CoastingZone()


class CELL__Wcc:
	Nom = {'sh_name': 'CELL', 'attr_name': 'Wcc', 'sub_attr_name': 'Nom', 'cols': [3]}


class CELL__PasCellule:
	Cell = {'sh_name': 'CELL', 'attr_name': 'PasCellule', 'sub_attr_name': 'Cell', 'cols': [4, 5, 6, 7, 8]}


class CELL__TronconsPropres:
	Cell = {'sh_name': 'CELL', 'attr_name': 'TronconsPropres', 'sub_attr_name': 'Cell', 'cols': [9, 10, 11, 12]}


class CELL__TronconsAnticipes:
	Cell = {'sh_name': 'CELL', 'attr_name': 'TronconsAnticipes', 'sub_attr_name': 'Cell', 'cols': [13, 14, 15, 16]}


class CELL__Extremite:
	Seg = {'sh_name': 'CELL', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60]}
	X = {'sh_name': 'CELL', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61]}
	Sens = {'sh_name': 'CELL', 'attr_name': 'Extremite', 'sub_attr_name': 'Sens', 'cols': [20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62]}
	Voie = {'sh_name': 'CELL', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91]}
	Pk = {'sh_name': 'CELL', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92]}


class CELL:
	Nom = {'sh_name': 'CELL', 'attr_name': 'Nom', 'col': 1}
	NumCellule = {'sh_name': 'CELL', 'attr_name': 'NumCellule', 'col': 2}
	Wcc = CELL__Wcc()
	PasCellule = CELL__PasCellule()
	TronconsPropres = CELL__TronconsPropres()
	TronconsAnticipes = CELL__TronconsAnticipes()
	ServeurDInvariants = {'sh_name': 'CELL', 'attr_name': 'ServeurDInvariants', 'col': 17}
	Extremite = CELL__Extremite()


class ZA_EFF_T__Extremite:
	Seg = {'sh_name': 'ZA_EFF_T', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}
	X = {'sh_name': 'ZA_EFF_T', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}
	Sens = {'sh_name': 'ZA_EFF_T', 'attr_name': 'Extremite', 'sub_attr_name': 'Sens', 'cols': [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]}
	Voie = {'sh_name': 'ZA_EFF_T', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [35, 37, 39, 41, 43, 45, 47, 49, 51, 53]}
	Pk = {'sh_name': 'ZA_EFF_T', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [36, 38, 40, 42, 44, 46, 48, 50, 52, 54]}


class ZA_EFF_T:
	Nom = {'sh_name': 'ZA_EFF_T', 'attr_name': 'Nom', 'col': 1}
	Type = {'sh_name': 'ZA_EFF_T', 'attr_name': 'Type', 'col': 2}
	TriggerCondition = {'sh_name': 'ZA_EFF_T', 'attr_name': 'TriggerCondition', 'col': 3}
	MaximumTractionEffort = {'sh_name': 'ZA_EFF_T', 'attr_name': 'MaximumTractionEffort', 'col': 4}
	Extremite = ZA_EFF_T__Extremite()


class SP:
	Nom = {'sh_name': 'SP', 'attr_name': 'Nom', 'col': 1}
	TerminusOuSp = {'sh_name': 'SP', 'attr_name': 'TerminusOuSp', 'col': 2}
	QuaiArrivee = {'sh_name': 'SP', 'attr_name': 'QuaiArrivee', 'col': 3}
	SensExtArrivee = {'sh_name': 'SP', 'attr_name': 'SensExtArrivee', 'col': 4}
	QuaiDepart = {'sh_name': 'SP', 'attr_name': 'QuaiDepart', 'col': 5}
	SensExtDepart = {'sh_name': 'SP', 'attr_name': 'SensExtDepart', 'col': 6}
	RetournementSp = {'sh_name': 'SP', 'attr_name': 'RetournementSp', 'col': 7}
	TypeSigSp = {'sh_name': 'SP', 'attr_name': 'TypeSigSp', 'col': 8}
	SignalSortieQuai = {'sh_name': 'SP', 'attr_name': 'SignalSortieQuai', 'col': 9}
	PointArretAto = {'sh_name': 'SP', 'attr_name': 'PointArretAto', 'col': 10}


class Iti__RouteIvb:
	Ivb = {'sh_name': 'Iti', 'attr_name': 'RouteIvb', 'sub_attr_name': 'Ivb', 'cols': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]}


class Iti__Aiguille:
	Nom = {'sh_name': 'Iti', 'attr_name': 'Aiguille', 'sub_attr_name': 'Nom', 'cols': [26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54]}
	Position = {'sh_name': 'Iti', 'attr_name': 'Aiguille', 'sub_attr_name': 'Position', 'cols': [27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55]}


class Iti:
	Nom = {'sh_name': 'Iti', 'attr_name': 'Nom', 'col': 1}
	SignalOrig = {'sh_name': 'Iti', 'attr_name': 'SignalOrig', 'col': 2}
	OriginIvb = {'sh_name': 'Iti', 'attr_name': 'OriginIvb', 'col': 3}
	RouteIvb = Iti__RouteIvb()
	DestinationIvb = {'sh_name': 'Iti', 'attr_name': 'DestinationIvb', 'col': 24}
	CdvDestEchap = {'sh_name': 'Iti', 'attr_name': 'CdvDestEchap', 'col': 25}
	Aiguille = Iti__Aiguille()


class CBTC_TER__Extremite:
	Seg = {'sh_name': 'CBTC_TER', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51]}
	X = {'sh_name': 'CBTC_TER', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52]}
	Sens = {'sh_name': 'CBTC_TER', 'attr_name': 'Extremite', 'sub_attr_name': 'Sens', 'cols': [11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53]}


class CBTC_TER__ItinerairesDeSortie:
	Iti = {'sh_name': 'CBTC_TER', 'attr_name': 'ItinerairesDeSortie', 'sub_attr_name': 'Iti', 'cols': [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]}


class CBTC_TER__PointEntreeTerritoireCbtc:
	Seg = {'sh_name': 'CBTC_TER', 'attr_name': 'PointEntreeTerritoireCbtc', 'sub_attr_name': 'Seg', 'cols': [74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122]}
	X = {'sh_name': 'CBTC_TER', 'attr_name': 'PointEntreeTerritoireCbtc', 'sub_attr_name': 'X', 'cols': [75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123]}


class CBTC_TER:
	Nom = {'sh_name': 'CBTC_TER', 'attr_name': 'Nom', 'col': 1}
	TypeTerritoireCbtc = {'sh_name': 'CBTC_TER', 'attr_name': 'TypeTerritoireCbtc', 'col': 2}
	AtcOffAllowed = {'sh_name': 'CBTC_TER', 'attr_name': 'AtcOffAllowed', 'col': 3}
	EvacuationInhibition = {'sh_name': 'CBTC_TER', 'attr_name': 'EvacuationInhibition', 'col': 4}
	WaysideDelocAlarmInhibition = {'sh_name': 'CBTC_TER', 'attr_name': 'WaysideDelocAlarmInhibition', 'col': 5}
	SleepingOrLocMemorizationAllowed = {'sh_name': 'CBTC_TER', 'attr_name': 'SleepingOrLocMemorizationAllowed', 'col': 6}
	RadioCoverageType = {'sh_name': 'CBTC_TER', 'attr_name': 'RadioCoverageType', 'col': 7}
	RearSievingRequired = {'sh_name': 'CBTC_TER', 'attr_name': 'RearSievingRequired', 'col': 8}
	Extremite = CBTC_TER__Extremite()
	ItinerairesDeSortie = CBTC_TER__ItinerairesDeSortie()
	PointEntreeTerritoireCbtc = CBTC_TER__PointEntreeTerritoireCbtc()


class PAS__ExtremiteSuivi:
	Seg = {'sh_name': 'PAS', 'attr_name': 'ExtremiteSuivi', 'sub_attr_name': 'Seg', 'cols': [4, 10, 16, 22, 28, 34, 40, 46, 52, 58, 64, 70, 76, 82, 88, 94, 100, 106, 112, 118, 124, 130, 136, 142, 148, 154, 160, 166, 172, 178]}
	X = {'sh_name': 'PAS', 'attr_name': 'ExtremiteSuivi', 'sub_attr_name': 'X', 'cols': [5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95, 101, 107, 113, 119, 125, 131, 137, 143, 149, 155, 161, 167, 173, 179]}
	Sens = {'sh_name': 'PAS', 'attr_name': 'ExtremiteSuivi', 'sub_attr_name': 'Sens', 'cols': [6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96, 102, 108, 114, 120, 126, 132, 138, 144, 150, 156, 162, 168, 174, 180]}
	Voie = {'sh_name': 'PAS', 'attr_name': 'ExtremiteSuivi', 'sub_attr_name': 'Voie', 'cols': [7, 13, 19, 25, 31, 37, 43, 49, 55, 61, 67, 73, 79, 85, 91, 97, 103, 109, 115, 121, 127, 133, 139, 145, 151, 157, 163, 169, 175, 181]}
	Pk = {'sh_name': 'PAS', 'attr_name': 'ExtremiteSuivi', 'sub_attr_name': 'Pk', 'cols': [8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86, 92, 98, 104, 110, 116, 122, 128, 134, 140, 146, 152, 158, 164, 170, 176, 182]}
	MaxDist = {'sh_name': 'PAS', 'attr_name': 'ExtremiteSuivi', 'sub_attr_name': 'MaxDist', 'cols': [9, 15, 21, 27, 33, 39, 45, 51, 57, 63, 69, 75, 81, 87, 93, 99, 105, 111, 117, 123, 129, 135, 141, 147, 153, 159, 165, 171, 177, 183]}


class PAS__TronconsGeresParLePas:
	Troncon = {'sh_name': 'PAS', 'attr_name': 'TronconsGeresParLePas', 'sub_attr_name': 'Troncon', 'cols': [184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203]}


class PAS:
	Nom = {'sh_name': 'PAS', 'attr_name': 'Nom', 'col': 1}
	TrackingAreaSubsetName = {'sh_name': 'PAS', 'attr_name': 'TrackingAreaSubsetName', 'col': 2}
	AtsZcId = {'sh_name': 'PAS', 'attr_name': 'AtsZcId', 'col': 3}
	ExtremiteSuivi = PAS__ExtremiteSuivi()
	TronconsGeresParLePas = PAS__TronconsGeresParLePas()
	ConcealmentType = {'sh_name': 'PAS', 'attr_name': 'ConcealmentType', 'col': 204}
	TracksMultiConsists = {'sh_name': 'PAS', 'attr_name': 'TracksMultiConsists', 'col': 205}
	DynamicSievingEnabled = {'sh_name': 'PAS', 'attr_name': 'DynamicSievingEnabled', 'col': 206}


class Sas_ZSM_CBTC:
	Nom = {'sh_name': 'Sas_ZSM_CBTC', 'attr_name': 'Nom', 'col': 1}
	PasEmetteur = {'sh_name': 'Sas_ZSM_CBTC', 'attr_name': 'PasEmetteur', 'col': 2}
	ZsmCbtc = {'sh_name': 'Sas_ZSM_CBTC', 'attr_name': 'ZsmCbtc', 'col': 3}
	Rang = {'sh_name': 'Sas_ZSM_CBTC', 'attr_name': 'Rang', 'col': 4}
	PasRecepteur1 = {'sh_name': 'Sas_ZSM_CBTC', 'attr_name': 'PasRecepteur1', 'col': 5}
	PasRecepteur2 = {'sh_name': 'Sas_ZSM_CBTC', 'attr_name': 'PasRecepteur2', 'col': 6}
	PasRecepteur3 = {'sh_name': 'Sas_ZSM_CBTC', 'attr_name': 'PasRecepteur3', 'col': 7}
	PasRecepteur4 = {'sh_name': 'Sas_ZSM_CBTC', 'attr_name': 'PasRecepteur4', 'col': 8}


class DP:
	Nom = {'sh_name': 'DP', 'attr_name': 'Nom', 'col': 1}
	Type = {'sh_name': 'DP', 'attr_name': 'Type', 'col': 2}
	Seg = {'sh_name': 'DP', 'attr_name': 'Seg', 'col': 3}
	X = {'sh_name': 'DP', 'attr_name': 'X', 'col': 4}
	Voie = {'sh_name': 'DP', 'attr_name': 'Voie', 'col': 5}
	Pk = {'sh_name': 'DP', 'attr_name': 'Pk', 'col': 6}
	NumeroPcc = {'sh_name': 'DP', 'attr_name': 'NumeroPcc', 'col': 7}


class Sieving_Limit:
	Name = {'sh_name': 'Sieving_Limit', 'attr_name': 'Name', 'col': 1}
	Type = {'sh_name': 'Sieving_Limit', 'attr_name': 'Type', 'col': 2}
	RelatedBlock = {'sh_name': 'Sieving_Limit', 'attr_name': 'RelatedBlock', 'col': 3}
	Seg = {'sh_name': 'Sieving_Limit', 'attr_name': 'Seg', 'col': 4}
	X = {'sh_name': 'Sieving_Limit', 'attr_name': 'X', 'col': 5}
	Voie = {'sh_name': 'Sieving_Limit', 'attr_name': 'Voie', 'col': 6}
	Pk = {'sh_name': 'Sieving_Limit', 'attr_name': 'Pk', 'col': 7}
	Direction = {'sh_name': 'Sieving_Limit', 'attr_name': 'Direction', 'col': 8}


class ZSM_CBTC__SignauxZsm:
	Sigman = {'sh_name': 'ZSM_CBTC', 'attr_name': 'SignauxZsm', 'sub_attr_name': 'Sigman', 'cols': [2, 3]}


class ZSM_CBTC__ExtZsm:
	Seg = {'sh_name': 'ZSM_CBTC', 'attr_name': 'ExtZsm', 'sub_attr_name': 'Seg', 'cols': [4, 8]}
	X = {'sh_name': 'ZSM_CBTC', 'attr_name': 'ExtZsm', 'sub_attr_name': 'X', 'cols': [5, 9]}
	Voie = {'sh_name': 'ZSM_CBTC', 'attr_name': 'ExtZsm', 'sub_attr_name': 'Voie', 'cols': [6, 10]}
	Pk = {'sh_name': 'ZSM_CBTC', 'attr_name': 'ExtZsm', 'sub_attr_name': 'Pk', 'cols': [7, 11]}


class ZSM_CBTC:
	Nom = {'sh_name': 'ZSM_CBTC', 'attr_name': 'Nom', 'col': 1}
	SignauxZsm = ZSM_CBTC__SignauxZsm()
	ExtZsm = ZSM_CBTC__ExtZsm()
	SegReference = {'sh_name': 'ZSM_CBTC', 'attr_name': 'SegReference', 'col': 12}
	SensAutorise = {'sh_name': 'ZSM_CBTC', 'attr_name': 'SensAutorise', 'col': 13}
	SensDefaut = {'sh_name': 'ZSM_CBTC', 'attr_name': 'SensDefaut', 'col': 14}
	InterlockingVirtualBlock = {'sh_name': 'ZSM_CBTC', 'attr_name': 'InterlockingVirtualBlock', 'col': 15}
	DefaultIxlDirection = {'sh_name': 'ZSM_CBTC', 'attr_name': 'DefaultIxlDirection', 'col': 16}


class SE__Extremite:
	Seg = {'sh_name': 'SE', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}
	X = {'sh_name': 'SE', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]}
	Sens = {'sh_name': 'SE', 'attr_name': 'Extremite', 'sub_attr_name': 'Sens', 'cols': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48]}
	Voie = {'sh_name': 'SE', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77]}
	Pk = {'sh_name': 'SE', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78]}


class SE:
	Nom = {'sh_name': 'SE', 'attr_name': 'Nom', 'col': 1}
	Type = {'sh_name': 'SE', 'attr_name': 'Type', 'col': 2}
	Ss = {'sh_name': 'SE', 'attr_name': 'Ss', 'col': 3}
	Extremite = SE__Extremite()
	NumeroPcc = {'sh_name': 'SE', 'attr_name': 'NumeroPcc', 'col': 79}


class SS__Extremite:
	Seg = {'sh_name': 'SS', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44]}
	X = {'sh_name': 'SS', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]}
	Sens = {'sh_name': 'SS', 'attr_name': 'Extremite', 'sub_attr_name': 'Sens', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}
	Voie = {'sh_name': 'SS', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75]}
	Pk = {'sh_name': 'SS', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76]}


class SS:
	Nom = {'sh_name': 'SS', 'attr_name': 'Nom', 'col': 1}
	Extremite = SS__Extremite()


class ZCI__Extremite:
	Seg = {'sh_name': 'ZCI', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90]}
	X = {'sh_name': 'ZCI', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91]}
	Sens = {'sh_name': 'ZCI', 'attr_name': 'Extremite', 'sub_attr_name': 'Sens', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 89, 92]}
	Voie = {'sh_name': 'ZCI', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151]}
	Pk = {'sh_name': 'ZCI', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152]}


class ZCI:
	Nom = {'sh_name': 'ZCI', 'attr_name': 'Nom', 'col': 1}
	NomPas = {'sh_name': 'ZCI', 'attr_name': 'NomPas', 'col': 2}
	Extremite = ZCI__Extremite()


class Zaum__Extremite:
	Seg = {'sh_name': 'Zaum', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54]}
	X = {'sh_name': 'Zaum', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55]}
	Sens = {'sh_name': 'Zaum', 'attr_name': 'Extremite', 'sub_attr_name': 'Sens', 'cols': [14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56]}
	Voie = {'sh_name': 'Zaum', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85]}
	Pk = {'sh_name': 'Zaum', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86]}


class Zaum:
	Nom = {'sh_name': 'Zaum', 'attr_name': 'Nom', 'col': 1}
	QuaiAlarme1 = {'sh_name': 'Zaum', 'attr_name': 'QuaiAlarme1', 'col': 2}
	QuaiAlarme2 = {'sh_name': 'Zaum', 'attr_name': 'QuaiAlarme2', 'col': 3}
	TronconPreferentiel = {'sh_name': 'Zaum', 'attr_name': 'TronconPreferentiel', 'col': 4}
	AtsId = {'sh_name': 'Zaum', 'attr_name': 'AtsId', 'col': 5}
	DriverlessAuthorized = {'sh_name': 'Zaum', 'attr_name': 'DriverlessAuthorized', 'col': 6}
	AutomaticAuthorized = {'sh_name': 'Zaum', 'attr_name': 'AutomaticAuthorized', 'col': 7}
	EvacuationProtectionZoneName = {'sh_name': 'Zaum', 'attr_name': 'EvacuationProtectionZoneName', 'col': 8}
	IntegrityProtectionZoneName = {'sh_name': 'Zaum', 'attr_name': 'IntegrityProtectionZoneName', 'col': 9}
	DelocalizationProtectionZoneName = {'sh_name': 'Zaum', 'attr_name': 'DelocalizationProtectionZoneName', 'col': 10}
	DerailmentObstacleProtectionZoneName = {'sh_name': 'Zaum', 'attr_name': 'DerailmentObstacleProtectionZoneName', 'col': 11}
	Extremite = Zaum__Extremite()


class ZCRA__MouvZcra:
	PtArretOrig = {'sh_name': 'ZCRA', 'attr_name': 'MouvZcra', 'sub_attr_name': 'PtArretOrig', 'cols': [4, 9, 14]}
	PtArretInter = {'sh_name': 'ZCRA', 'attr_name': 'MouvZcra', 'sub_attr_name': 'PtArretInter', 'cols': [5, 10, 15]}
	PtArretDest = {'sh_name': 'ZCRA', 'attr_name': 'MouvZcra', 'sub_attr_name': 'PtArretDest', 'cols': [6, 11, 16]}
	QuaiOrigine = {'sh_name': 'ZCRA', 'attr_name': 'MouvZcra', 'sub_attr_name': 'QuaiOrigine', 'cols': [7, 12, 17]}
	SensExtOrigine = {'sh_name': 'ZCRA', 'attr_name': 'MouvZcra', 'sub_attr_name': 'SensExtOrigine', 'cols': [8, 13, 18]}


class ZCRA__Extremite:
	Seg = {'sh_name': 'ZCRA', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61]}
	X = {'sh_name': 'ZCRA', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62]}
	Sens = {'sh_name': 'ZCRA', 'attr_name': 'Extremite', 'sub_attr_name': 'Sens', 'cols': [21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63]}
	Voie = {'sh_name': 'ZCRA', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92]}
	Pk = {'sh_name': 'ZCRA', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93]}


class ZCRA:
	Nom = {'sh_name': 'ZCRA', 'attr_name': 'Nom', 'col': 1}
	TronconPreferentiel = {'sh_name': 'ZCRA', 'attr_name': 'TronconPreferentiel', 'col': 2}
	PresenceAdc = {'sh_name': 'ZCRA', 'attr_name': 'PresenceAdc', 'col': 3}
	MouvZcra = ZCRA__MouvZcra()
	Extremite = ZCRA__Extremite()


class Zacp__Extremite:
	Seg = {'sh_name': 'Zacp', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]}
	X = {'sh_name': 'Zacp', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]}
	Sens = {'sh_name': 'Zacp', 'attr_name': 'Extremite', 'sub_attr_name': 'Sens', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]}
	Voie = {'sh_name': 'Zacp', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [32, 34, 36, 38, 40, 42, 44, 46, 48, 50]}
	Pk = {'sh_name': 'Zacp', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [33, 35, 37, 39, 41, 43, 45, 47, 49, 51]}


class Zacp:
	Nom = {'sh_name': 'Zacp', 'attr_name': 'Nom', 'col': 1}
	Extremite = Zacp__Extremite()


class ZLPV__De:
	Seg = {'sh_name': 'ZLPV', 'attr_name': 'De', 'sub_attr_name': 'Seg', 'cols': [2]}
	X = {'sh_name': 'ZLPV', 'attr_name': 'De', 'sub_attr_name': 'X', 'cols': [3]}
	DistanceAnticipation = {'sh_name': 'ZLPV', 'attr_name': 'De', 'sub_attr_name': 'DistanceAnticipation', 'cols': [4]}
	Voie = {'sh_name': 'ZLPV', 'attr_name': 'De', 'sub_attr_name': 'Voie', 'cols': [8]}
	Pk = {'sh_name': 'ZLPV', 'attr_name': 'De', 'sub_attr_name': 'Pk', 'cols': [9]}


class ZLPV__A:
	Seg = {'sh_name': 'ZLPV', 'attr_name': 'A', 'sub_attr_name': 'Seg', 'cols': [5]}
	X = {'sh_name': 'ZLPV', 'attr_name': 'A', 'sub_attr_name': 'X', 'cols': [6]}
	DistanceAnticipation = {'sh_name': 'ZLPV', 'attr_name': 'A', 'sub_attr_name': 'DistanceAnticipation', 'cols': [7]}
	Voie = {'sh_name': 'ZLPV', 'attr_name': 'A', 'sub_attr_name': 'Voie', 'cols': [10]}
	Pk = {'sh_name': 'ZLPV', 'attr_name': 'A', 'sub_attr_name': 'Pk', 'cols': [11]}


class ZLPV:
	VitesseZlpv = {'sh_name': 'ZLPV', 'attr_name': 'VitesseZlpv', 'col': 1}
	De = ZLPV__De()
	A = ZLPV__A()


class NV_PSR__From:
	Seg = {'sh_name': 'NV_PSR', 'attr_name': 'From', 'sub_attr_name': 'Seg', 'cols': [3]}
	X = {'sh_name': 'NV_PSR', 'attr_name': 'From', 'sub_attr_name': 'X', 'cols': [4]}
	Track = {'sh_name': 'NV_PSR', 'attr_name': 'From', 'sub_attr_name': 'Track', 'cols': [7]}
	Kp = {'sh_name': 'NV_PSR', 'attr_name': 'From', 'sub_attr_name': 'Kp', 'cols': [8]}


class NV_PSR__To:
	Seg = {'sh_name': 'NV_PSR', 'attr_name': 'To', 'sub_attr_name': 'Seg', 'cols': [5]}
	X = {'sh_name': 'NV_PSR', 'attr_name': 'To', 'sub_attr_name': 'X', 'cols': [6]}
	Track = {'sh_name': 'NV_PSR', 'attr_name': 'To', 'sub_attr_name': 'Track', 'cols': [9]}
	Kp = {'sh_name': 'NV_PSR', 'attr_name': 'To', 'sub_attr_name': 'Kp', 'cols': [10]}


class NV_PSR:
	Name = {'sh_name': 'NV_PSR', 'attr_name': 'Name', 'col': 1}
	SpeedValue = {'sh_name': 'NV_PSR', 'attr_name': 'SpeedValue', 'col': 2}
	From = NV_PSR__From()
	To = NV_PSR__To()
	AtsId = {'sh_name': 'NV_PSR', 'attr_name': 'AtsId', 'col': 11}
	WithRelaxation = {'sh_name': 'NV_PSR', 'attr_name': 'WithRelaxation', 'col': 12}
	RelaxationCause = {'sh_name': 'NV_PSR', 'attr_name': 'RelaxationCause', 'col': 13}
	CeilingSpeedValue = {'sh_name': 'NV_PSR', 'attr_name': 'CeilingSpeedValue', 'col': 14}


class ZLPV_Or__De:
	Seg = {'sh_name': 'ZLPV_Or', 'attr_name': 'De', 'sub_attr_name': 'Seg', 'cols': [4]}
	X = {'sh_name': 'ZLPV_Or', 'attr_name': 'De', 'sub_attr_name': 'X', 'cols': [5]}
	Voie = {'sh_name': 'ZLPV_Or', 'attr_name': 'De', 'sub_attr_name': 'Voie', 'cols': [8]}
	Pk = {'sh_name': 'ZLPV_Or', 'attr_name': 'De', 'sub_attr_name': 'Pk', 'cols': [9]}


class ZLPV_Or__A:
	Seg = {'sh_name': 'ZLPV_Or', 'attr_name': 'A', 'sub_attr_name': 'Seg', 'cols': [6]}
	X = {'sh_name': 'ZLPV_Or', 'attr_name': 'A', 'sub_attr_name': 'X', 'cols': [7]}
	Voie = {'sh_name': 'ZLPV_Or', 'attr_name': 'A', 'sub_attr_name': 'Voie', 'cols': [10]}
	Pk = {'sh_name': 'ZLPV_Or', 'attr_name': 'A', 'sub_attr_name': 'Pk', 'cols': [11]}


class ZLPV_Or:
	VitesseZlpv = {'sh_name': 'ZLPV_Or', 'attr_name': 'VitesseZlpv', 'col': 1}
	Sens = {'sh_name': 'ZLPV_Or', 'attr_name': 'Sens', 'col': 2}
	DistanceAnticipation = {'sh_name': 'ZLPV_Or', 'attr_name': 'DistanceAnticipation', 'col': 3}
	De = ZLPV_Or__De()
	A = ZLPV_Or__A()


class Calib:
	BaliseDeb = {'sh_name': 'Calib', 'attr_name': 'BaliseDeb', 'col': 1}
	BaliseFin = {'sh_name': 'Calib', 'attr_name': 'BaliseFin', 'col': 2}
	DistanceCalib = {'sh_name': 'Calib', 'attr_name': 'DistanceCalib', 'col': 3}
	SensCalib = {'sh_name': 'Calib', 'attr_name': 'SensCalib', 'col': 4}


class Zman:
	Nom = {'sh_name': 'Zman', 'attr_name': 'Nom', 'col': 1}
	SigZman1 = {'sh_name': 'Zman', 'attr_name': 'SigZman1', 'col': 2}
	SigZman2 = {'sh_name': 'Zman', 'attr_name': 'SigZman2', 'col': 3}
	SigZman3 = {'sh_name': 'Zman', 'attr_name': 'SigZman3', 'col': 4}
	SigZman4 = {'sh_name': 'Zman', 'attr_name': 'SigZman4', 'col': 5}
	SigZman5 = {'sh_name': 'Zman', 'attr_name': 'SigZman5', 'col': 6}
	SigZman6 = {'sh_name': 'Zman', 'attr_name': 'SigZman6', 'col': 7}
	SigZman7 = {'sh_name': 'Zman', 'attr_name': 'SigZman7', 'col': 8}
	SigZman8 = {'sh_name': 'Zman', 'attr_name': 'SigZman8', 'col': 9}
	SigZman9 = {'sh_name': 'Zman', 'attr_name': 'SigZman9', 'col': 10}
	SigZman10 = {'sh_name': 'Zman', 'attr_name': 'SigZman10', 'col': 11}
	SigZman11 = {'sh_name': 'Zman', 'attr_name': 'SigZman11', 'col': 12}
	SigZman12 = {'sh_name': 'Zman', 'attr_name': 'SigZman12', 'col': 13}
	Ivb1 = {'sh_name': 'Zman', 'attr_name': 'Ivb1', 'col': 14}
	Ivb2 = {'sh_name': 'Zman', 'attr_name': 'Ivb2', 'col': 15}
	Ivb3 = {'sh_name': 'Zman', 'attr_name': 'Ivb3', 'col': 16}
	Ivb4 = {'sh_name': 'Zman', 'attr_name': 'Ivb4', 'col': 17}
	Ivb5 = {'sh_name': 'Zman', 'attr_name': 'Ivb5', 'col': 18}
	Ivb6 = {'sh_name': 'Zman', 'attr_name': 'Ivb6', 'col': 19}
	Ivb7 = {'sh_name': 'Zman', 'attr_name': 'Ivb7', 'col': 20}
	Ivb8 = {'sh_name': 'Zman', 'attr_name': 'Ivb8', 'col': 21}
	Ivb9 = {'sh_name': 'Zman', 'attr_name': 'Ivb9', 'col': 22}
	Ivb10 = {'sh_name': 'Zman', 'attr_name': 'Ivb10', 'col': 23}


class ZVR__Extremite:
	Seg = {'sh_name': 'ZVR', 'attr_name': 'Extremite', 'sub_attr_name': 'Seg', 'cols': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]}
	X = {'sh_name': 'ZVR', 'attr_name': 'Extremite', 'sub_attr_name': 'X', 'cols': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]}
	Sens = {'sh_name': 'ZVR', 'attr_name': 'Extremite', 'sub_attr_name': 'Sens', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]}
	Voie = {'sh_name': 'ZVR', 'attr_name': 'Extremite', 'sub_attr_name': 'Voie', 'cols': [32, 34, 36, 38, 40, 42, 44, 46, 48, 50]}
	Pk = {'sh_name': 'ZVR', 'attr_name': 'Extremite', 'sub_attr_name': 'Pk', 'cols': [33, 35, 37, 39, 41, 43, 45, 47, 49, 51]}


class ZVR:
	Nom = {'sh_name': 'ZVR', 'attr_name': 'Nom', 'col': 1}
	Extremite = ZVR__Extremite()


class CBTC_Eqpt__Equipements:
	Eqpt = {'sh_name': 'CBTC_Eqpt', 'attr_name': 'Equipements', 'sub_attr_name': 'Eqpt', 'cols': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}


class CBTC_Eqpt:
	Signal = {'sh_name': 'CBTC_Eqpt', 'attr_name': 'Signal', 'col': 1}
	Equipements = CBTC_Eqpt__Equipements()


class Flux_Variant_HF:
	Nom = {'sh_name': 'Flux_Variant_HF', 'attr_name': 'Nom', 'col': 1}
	ClasseObjet = {'sh_name': 'Flux_Variant_HF', 'attr_name': 'ClasseObjet', 'col': 2}
	NomObjet = {'sh_name': 'Flux_Variant_HF', 'attr_name': 'NomObjet', 'col': 3}
	NomLogiqueInfo = {'sh_name': 'Flux_Variant_HF', 'attr_name': 'NomLogiqueInfo', 'col': 4}
	TypeFoncSecu = {'sh_name': 'Flux_Variant_HF', 'attr_name': 'TypeFoncSecu', 'col': 5}
	Troncon = {'sh_name': 'Flux_Variant_HF', 'attr_name': 'Troncon', 'col': 6}
	Message = {'sh_name': 'Flux_Variant_HF', 'attr_name': 'Message', 'col': 7}
	RgInfo = {'sh_name': 'Flux_Variant_HF', 'attr_name': 'RgInfo', 'col': 8}
	CommentaireDeGeneration = {'sh_name': 'Flux_Variant_HF', 'attr_name': 'CommentaireDeGeneration', 'col': 9}


class Flux_Variant_BF:
	Nom = {'sh_name': 'Flux_Variant_BF', 'attr_name': 'Nom', 'col': 1}
	ClasseObjet = {'sh_name': 'Flux_Variant_BF', 'attr_name': 'ClasseObjet', 'col': 2}
	NomObjet = {'sh_name': 'Flux_Variant_BF', 'attr_name': 'NomObjet', 'col': 3}
	NomLogiqueInfo = {'sh_name': 'Flux_Variant_BF', 'attr_name': 'NomLogiqueInfo', 'col': 4}
	TypeFoncSecu = {'sh_name': 'Flux_Variant_BF', 'attr_name': 'TypeFoncSecu', 'col': 5}
	Troncon = {'sh_name': 'Flux_Variant_BF', 'attr_name': 'Troncon', 'col': 6}
	Message = {'sh_name': 'Flux_Variant_BF', 'attr_name': 'Message', 'col': 7}
	RgInfo = {'sh_name': 'Flux_Variant_BF', 'attr_name': 'RgInfo', 'col': 8}
	CommentaireDeGeneration = {'sh_name': 'Flux_Variant_BF', 'attr_name': 'CommentaireDeGeneration', 'col': 9}


class Wayside_Eqpt__Function:
	Zc = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'Zc', 'cols': [3]}
	Oc = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'Oc', 'cols': [4]}
	Zcr = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'Zcr', 'cols': [5]}
	Psd = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'Psd', 'cols': [6]}
	Ups = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'Ups', 'cols': [7]}
	Ftm = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'Ftm', 'cols': [8]}
	Dcs = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'Dcs', 'cols': [9]}


class Wayside_Eqpt:
	Name = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'Name', 'col': 1}
	EqptId = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'EqptId', 'col': 2}
	Function = Wayside_Eqpt__Function()
	OcType = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'OcType', 'col': 10}
	Location = {'sh_name': 'Wayside_Eqpt', 'attr_name': 'Location', 'col': 11}


class Flux_MES_PAS:
	Nom = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'Nom', 'col': 1}
	NomMes = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'NomMes', 'col': 2}
	ClasseObjet = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'ClasseObjet', 'col': 3}
	NomObjet = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'NomObjet', 'col': 4}
	NomLogiqueInfo = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'NomLogiqueInfo', 'col': 5}
	TypeInfo = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'TypeInfo', 'col': 6}
	Message = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'Message', 'col': 7}
	Extension = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'Extension', 'col': 8}
	RgInfo = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'RgInfo', 'col': 9}
	PasUtilisateur1 = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'PasUtilisateur1', 'col': 10}
	PasUtilisateur2 = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'PasUtilisateur2', 'col': 11}
	PasUtilisateur3 = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'PasUtilisateur3', 'col': 12}
	PasUtilisateur4 = {'sh_name': 'Flux_MES_PAS', 'attr_name': 'PasUtilisateur4', 'col': 13}


class Flux_PAS_MES:
	Nom = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'Nom', 'col': 1}
	NomMes = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'NomMes', 'col': 2}
	ClasseObjet = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'ClasseObjet', 'col': 3}
	NomObjet = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'NomObjet', 'col': 4}
	NomLogiqueInfo = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'NomLogiqueInfo', 'col': 5}
	TypeInfo = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'TypeInfo', 'col': 6}
	Message = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'Message', 'col': 7}
	Extension = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'Extension', 'col': 8}
	RgInfo = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'RgInfo', 'col': 9}
	PasUtilisateur1 = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'PasUtilisateur1', 'col': 10}
	PasUtilisateur2 = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'PasUtilisateur2', 'col': 11}
	PasUtilisateur3 = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'PasUtilisateur3', 'col': 12}
	PasUtilisateur4 = {'sh_name': 'Flux_PAS_MES', 'attr_name': 'PasUtilisateur4', 'col': 13}


class ATS_ATC:
	Nom = {'sh_name': 'ATS_ATC', 'attr_name': 'Nom', 'col': 1}
	ClasseObjet = {'sh_name': 'ATS_ATC', 'attr_name': 'ClasseObjet', 'col': 2}
	NomObjet = {'sh_name': 'ATS_ATC', 'attr_name': 'NomObjet', 'col': 3}
	NomLogiqueInfoAts = {'sh_name': 'ATS_ATC', 'attr_name': 'NomLogiqueInfoAts', 'col': 4}
	NomMessage = {'sh_name': 'ATS_ATC', 'attr_name': 'NomMessage', 'col': 5}
	RgInfo = {'sh_name': 'ATS_ATC', 'attr_name': 'RgInfo', 'col': 6}


class TM_MES_ATS:
	Nom = {'sh_name': 'TM_MES_ATS', 'attr_name': 'Nom', 'col': 1}
	Equipement = {'sh_name': 'TM_MES_ATS', 'attr_name': 'Equipement', 'col': 2}
	ClasseObjet = {'sh_name': 'TM_MES_ATS', 'attr_name': 'ClasseObjet', 'col': 3}
	NomObjet = {'sh_name': 'TM_MES_ATS', 'attr_name': 'NomObjet', 'col': 4}
	NomLogiqueInfoAts = {'sh_name': 'TM_MES_ATS', 'attr_name': 'NomLogiqueInfoAts', 'col': 5}
	NomMessage = {'sh_name': 'TM_MES_ATS', 'attr_name': 'NomMessage', 'col': 6}
	RgInfo = {'sh_name': 'TM_MES_ATS', 'attr_name': 'RgInfo', 'col': 7}


class TM_PAS_ATS:
	Nom = {'sh_name': 'TM_PAS_ATS', 'attr_name': 'Nom', 'col': 1}
	Equipement = {'sh_name': 'TM_PAS_ATS', 'attr_name': 'Equipement', 'col': 2}
	ClasseObjet = {'sh_name': 'TM_PAS_ATS', 'attr_name': 'ClasseObjet', 'col': 3}
	NomObjet = {'sh_name': 'TM_PAS_ATS', 'attr_name': 'NomObjet', 'col': 4}
	NomLogiqueInfoAts = {'sh_name': 'TM_PAS_ATS', 'attr_name': 'NomLogiqueInfoAts', 'col': 5}
	NomMessage = {'sh_name': 'TM_PAS_ATS', 'attr_name': 'NomMessage', 'col': 6}
	RgInfo = {'sh_name': 'TM_PAS_ATS', 'attr_name': 'RgInfo', 'col': 7}


class Network:
	Name = {'sh_name': 'Network', 'attr_name': 'Name', 'col': 1}
	Type = {'sh_name': 'Network', 'attr_name': 'Type', 'col': 2}
	Line = {'sh_name': 'Network', 'attr_name': 'Line', 'col': 3}
	BaseAddress = {'sh_name': 'Network', 'attr_name': 'BaseAddress', 'col': 4}
	Medium = {'sh_name': 'Network', 'attr_name': 'Medium', 'col': 5}
	Mask = {'sh_name': 'Network', 'attr_name': 'Mask', 'col': 6}
	Gateway = {'sh_name': 'Network', 'attr_name': 'Gateway', 'col': 7}
	Port = {'sh_name': 'Network', 'attr_name': 'Port', 'col': 8}
	OverallMask = {'sh_name': 'Network', 'attr_name': 'OverallMask', 'col': 9}
	CcMulticastAddress = {'sh_name': 'Network', 'attr_name': 'CcMulticastAddress', 'col': 10}
	PisMulticastAddress = {'sh_name': 'Network', 'attr_name': 'PisMulticastAddress', 'col': 11}
	CcTmsMulticastAddress = {'sh_name': 'Network', 'attr_name': 'CcTmsMulticastAddress', 'col': 12}
	TmsCcMulticastAddress = {'sh_name': 'Network', 'attr_name': 'TmsCcMulticastAddress', 'col': 13}


class LineSection_Eqpt:
	Name = {'sh_name': 'LineSection_Eqpt', 'attr_name': 'Name', 'col': 1}
	EqptId = {'sh_name': 'LineSection_Eqpt', 'attr_name': 'EqptId', 'col': 2}
	Type = {'sh_name': 'LineSection_Eqpt', 'attr_name': 'Type', 'col': 3}
	Zone = {'sh_name': 'LineSection_Eqpt', 'attr_name': 'Zone', 'col': 4}


class OnBoard_Eqpt__Function:
	IsRealCc = {'sh_name': 'OnBoard_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'IsRealCc', 'cols': [3]}
	IsVirtualCc = {'sh_name': 'OnBoard_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'IsVirtualCc', 'cols': [4]}
	IsTod = {'sh_name': 'OnBoard_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'IsTod', 'cols': [5]}
	IsPis = {'sh_name': 'OnBoard_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'IsPis', 'cols': [6]}
	IsTar = {'sh_name': 'OnBoard_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'IsTar', 'cols': [7]}
	IsTmsMvbBox = {'sh_name': 'OnBoard_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'IsTmsMvbBox', 'cols': [8]}
	IsPwmBox = {'sh_name': 'OnBoard_Eqpt', 'attr_name': 'Function', 'sub_attr_name': 'IsPwmBox', 'cols': [9]}


class OnBoard_Eqpt:
	Name = {'sh_name': 'OnBoard_Eqpt', 'attr_name': 'Name', 'col': 1}
	EqptId = {'sh_name': 'OnBoard_Eqpt', 'attr_name': 'EqptId', 'col': 2}
	Function = OnBoard_Eqpt__Function()


class Interstation:
	Nom = {'sh_name': 'Interstation', 'attr_name': 'Nom', 'col': 1}
	QuaiOrigine = {'sh_name': 'Interstation', 'attr_name': 'QuaiOrigine', 'col': 2}
	QuaiDestination = {'sh_name': 'Interstation', 'attr_name': 'QuaiDestination', 'col': 3}
	SensLigne = {'sh_name': 'Interstation', 'attr_name': 'SensLigne', 'col': 4}


class IATPM_tags__Routes:
	Route = {'sh_name': 'IATPM_tags', 'attr_name': 'Routes', 'sub_attr_name': 'Route', 'cols': [11, 12, 13, 14, 15, 16]}


class IATPM_tags__VitalStoppingPoint:
	Seg = {'sh_name': 'IATPM_tags', 'attr_name': 'VitalStoppingPoint', 'sub_attr_name': 'Seg', 'cols': [18]}
	X = {'sh_name': 'IATPM_tags', 'attr_name': 'VitalStoppingPoint', 'sub_attr_name': 'X', 'cols': [19]}
	Track = {'sh_name': 'IATPM_tags', 'attr_name': 'VitalStoppingPoint', 'sub_attr_name': 'Track', 'cols': [20]}
	Kp = {'sh_name': 'IATPM_tags', 'attr_name': 'VitalStoppingPoint', 'sub_attr_name': 'Kp', 'cols': [21]}


class IATPM_tags__ImcTimeout:
	Distance = {'sh_name': 'IATPM_tags', 'attr_name': 'ImcTimeout', 'sub_attr_name': 'Distance', 'cols': [25]}
	Value = {'sh_name': 'IATPM_tags', 'attr_name': 'ImcTimeout', 'sub_attr_name': 'Value', 'cols': [26]}


class IATPM_tags__DmcTimeout:
	Distance = {'sh_name': 'IATPM_tags', 'attr_name': 'DmcTimeout', 'sub_attr_name': 'Distance', 'cols': [27]}
	Value = {'sh_name': 'IATPM_tags', 'attr_name': 'DmcTimeout', 'sub_attr_name': 'Value', 'cols': [28]}


class IATPM_tags:
	Name = {'sh_name': 'IATPM_tags', 'attr_name': 'Name', 'col': 1}
	BaliseName = {'sh_name': 'IATPM_tags', 'attr_name': 'BaliseName', 'col': 2}
	Type = {'sh_name': 'IATPM_tags', 'attr_name': 'Type', 'col': 3}
	NumTagSeg = {'sh_name': 'IATPM_tags', 'attr_name': 'NumTagSeg', 'col': 4}
	Seg = {'sh_name': 'IATPM_tags', 'attr_name': 'Seg', 'col': 5}
	X = {'sh_name': 'IATPM_tags', 'attr_name': 'X', 'col': 6}
	Voie = {'sh_name': 'IATPM_tags', 'attr_name': 'Voie', 'col': 7}
	Pk = {'sh_name': 'IATPM_tags', 'attr_name': 'Pk', 'col': 8}
	LayingType = {'sh_name': 'IATPM_tags', 'attr_name': 'LayingType', 'col': 9}
	Signal = {'sh_name': 'IATPM_tags', 'attr_name': 'Signal', 'col': 10}
	Routes = IATPM_tags__Routes()
	StopSignal = {'sh_name': 'IATPM_tags', 'attr_name': 'StopSignal', 'col': 17}
	VitalStoppingPoint = IATPM_tags__VitalStoppingPoint()
	WithOverlap = {'sh_name': 'IATPM_tags', 'attr_name': 'WithOverlap', 'col': 22}
	OverlapName = {'sh_name': 'IATPM_tags', 'attr_name': 'OverlapName', 'col': 23}
	OverlapReleaseDistance = {'sh_name': 'IATPM_tags', 'attr_name': 'OverlapReleaseDistance', 'col': 24}
	ImcTimeout = IATPM_tags__ImcTimeout()
	DmcTimeout = IATPM_tags__DmcTimeout()


class IATPM_Version_Tags:
	Name = {'sh_name': 'IATPM_Version_Tags', 'attr_name': 'Name', 'col': 1}
	BaliseName = {'sh_name': 'IATPM_Version_Tags', 'attr_name': 'BaliseName', 'col': 2}
	Seg = {'sh_name': 'IATPM_Version_Tags', 'attr_name': 'Seg', 'col': 3}
	X = {'sh_name': 'IATPM_Version_Tags', 'attr_name': 'X', 'col': 4}


class DynTag_Group__TagList:
	Tag = {'sh_name': 'DynTag_Group', 'attr_name': 'TagList', 'sub_attr_name': 'Tag', 'cols': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}


class DynTag_Group:
	Name = {'sh_name': 'DynTag_Group', 'attr_name': 'Name', 'col': 1}
	Id = {'sh_name': 'DynTag_Group', 'attr_name': 'Id', 'col': 2}
	TagList = DynTag_Group__TagList()


class Border_Area:
	Name = {'sh_name': 'Border_Area', 'attr_name': 'Name', 'col': 1}
	Block1 = {'sh_name': 'Border_Area', 'attr_name': 'Block1', 'col': 2}
	Block2 = {'sh_name': 'Border_Area', 'attr_name': 'Block2', 'col': 3}
	Block3 = {'sh_name': 'Border_Area', 'attr_name': 'Block3', 'col': 4}
	Block4 = {'sh_name': 'Border_Area', 'attr_name': 'Block4', 'col': 5}
	Block5 = {'sh_name': 'Border_Area', 'attr_name': 'Block5', 'col': 6}
	Block6 = {'sh_name': 'Border_Area', 'attr_name': 'Block6', 'col': 7}
	Block7 = {'sh_name': 'Border_Area', 'attr_name': 'Block7', 'col': 8}
	Block8 = {'sh_name': 'Border_Area', 'attr_name': 'Block8', 'col': 9}
	Block9 = {'sh_name': 'Border_Area', 'attr_name': 'Block9', 'col': 10}
	Block10 = {'sh_name': 'Border_Area', 'attr_name': 'Block10', 'col': 11}
	Block11 = {'sh_name': 'Border_Area', 'attr_name': 'Block11', 'col': 12}
	Block12 = {'sh_name': 'Border_Area', 'attr_name': 'Block12', 'col': 13}
	Block13 = {'sh_name': 'Border_Area', 'attr_name': 'Block13', 'col': 14}
	Block14 = {'sh_name': 'Border_Area', 'attr_name': 'Block14', 'col': 15}
	Block15 = {'sh_name': 'Border_Area', 'attr_name': 'Block15', 'col': 16}
	Block16 = {'sh_name': 'Border_Area', 'attr_name': 'Block16', 'col': 17}
	Block17 = {'sh_name': 'Border_Area', 'attr_name': 'Block17', 'col': 18}
	Block18 = {'sh_name': 'Border_Area', 'attr_name': 'Block18', 'col': 19}
	Block19 = {'sh_name': 'Border_Area', 'attr_name': 'Block19', 'col': 20}
	Block20 = {'sh_name': 'Border_Area', 'attr_name': 'Block20', 'col': 21}


class OVL_Border_Area:
	Nom = {'sh_name': 'OVL_Border_Area', 'attr_name': 'Nom', 'col': 1}
	SenderZc = {'sh_name': 'OVL_Border_Area', 'attr_name': 'SenderZc', 'col': 2}
	BorderArea = {'sh_name': 'OVL_Border_Area', 'attr_name': 'BorderArea', 'col': 3}
	Rank = {'sh_name': 'OVL_Border_Area', 'attr_name': 'Rank', 'col': 4}
	ZcReceiver1 = {'sh_name': 'OVL_Border_Area', 'attr_name': 'ZcReceiver1', 'col': 5}
	ZcReceiver2 = {'sh_name': 'OVL_Border_Area', 'attr_name': 'ZcReceiver2', 'col': 6}
	ZcReceiver3 = {'sh_name': 'OVL_Border_Area', 'attr_name': 'ZcReceiver3', 'col': 7}
	ZcReceiver4 = {'sh_name': 'OVL_Border_Area', 'attr_name': 'ZcReceiver4', 'col': 8}


class IXL_Overlap__VitalStoppingPoint:
	Seg = {'sh_name': 'IXL_Overlap', 'attr_name': 'VitalStoppingPoint', 'sub_attr_name': 'Seg', 'cols': [5]}
	X = {'sh_name': 'IXL_Overlap', 'attr_name': 'VitalStoppingPoint', 'sub_attr_name': 'X', 'cols': [6]}
	Sens = {'sh_name': 'IXL_Overlap', 'attr_name': 'VitalStoppingPoint', 'sub_attr_name': 'Sens', 'cols': [7]}
	Voie = {'sh_name': 'IXL_Overlap', 'attr_name': 'VitalStoppingPoint', 'sub_attr_name': 'Voie', 'cols': [8]}
	Pk = {'sh_name': 'IXL_Overlap', 'attr_name': 'VitalStoppingPoint', 'sub_attr_name': 'Pk', 'cols': [9]}


class IXL_Overlap__ReleasePoint:
	Seg = {'sh_name': 'IXL_Overlap', 'attr_name': 'ReleasePoint', 'sub_attr_name': 'Seg', 'cols': [10]}
	X = {'sh_name': 'IXL_Overlap', 'attr_name': 'ReleasePoint', 'sub_attr_name': 'X', 'cols': [11]}
	Track = {'sh_name': 'IXL_Overlap', 'attr_name': 'ReleasePoint', 'sub_attr_name': 'Track', 'cols': [12]}
	Kp = {'sh_name': 'IXL_Overlap', 'attr_name': 'ReleasePoint', 'sub_attr_name': 'Kp', 'cols': [13]}


class IXL_Overlap__Aiguille:
	Nom = {'sh_name': 'IXL_Overlap', 'attr_name': 'Aiguille', 'sub_attr_name': 'Nom', 'cols': [15, 17, 19, 21]}
	Position = {'sh_name': 'IXL_Overlap', 'attr_name': 'Aiguille', 'sub_attr_name': 'Position', 'cols': [16, 18, 20, 22]}


class IXL_Overlap:
	Name = {'sh_name': 'IXL_Overlap', 'attr_name': 'Name', 'col': 1}
	DestinationSignal = {'sh_name': 'IXL_Overlap', 'attr_name': 'DestinationSignal', 'col': 2}
	PlatformRelated = {'sh_name': 'IXL_Overlap', 'attr_name': 'PlatformRelated', 'col': 3}
	WithTpp = {'sh_name': 'IXL_Overlap', 'attr_name': 'WithTpp', 'col': 4}
	VitalStoppingPoint = IXL_Overlap__VitalStoppingPoint()
	ReleasePoint = IXL_Overlap__ReleasePoint()
	ReleaseTimerValue = {'sh_name': 'IXL_Overlap', 'attr_name': 'ReleaseTimerValue', 'col': 14}
	Aiguille = IXL_Overlap__Aiguille()


class Driving_Modes:
	Name = {'sh_name': 'Driving_Modes', 'attr_name': 'Name', 'col': 1}
	Group = {'sh_name': 'Driving_Modes', 'attr_name': 'Group', 'col': 2}
	Code = {'sh_name': 'Driving_Modes', 'attr_name': 'Code', 'col': 3}
	Abbreviation = {'sh_name': 'Driving_Modes', 'attr_name': 'Abbreviation', 'col': 4}


class Unprotected_Moves__Blocks:
	Block = {'sh_name': 'Unprotected_Moves', 'attr_name': 'Blocks', 'sub_attr_name': 'Block', 'cols': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}


class Unprotected_Moves:
	Name = {'sh_name': 'Unprotected_Moves', 'attr_name': 'Name', 'col': 1}
	Blocks = Unprotected_Moves__Blocks()


class CBTC_Overlap__Switch:
	Name = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Switch', 'sub_attr_name': 'Name', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]}
	Position = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Switch', 'sub_attr_name': 'Position', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}


class CBTC_Overlap:
	Name = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Name', 'col': 1}
	Signal = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Signal', 'col': 2}
	Block1 = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Block1', 'col': 3}
	Switch = CBTC_Overlap__Switch()
	Block2 = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Block2', 'col': 6}
	Block3 = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Block3', 'col': 9}
	Block4 = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Block4', 'col': 12}
	Block5 = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Block5', 'col': 15}
	Block6 = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Block6', 'col': 18}
	Block7 = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Block7', 'col': 21}
	Block8 = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Block8', 'col': 24}
	Block9 = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Block9', 'col': 27}
	Block10 = {'sh_name': 'CBTC_Overlap', 'attr_name': 'Block10', 'col': 30}


class Performance_Level:
	Name = {'sh_name': 'Performance_Level', 'attr_name': 'Name', 'col': 1}
	MaxAtoSpeed = {'sh_name': 'Performance_Level', 'attr_name': 'MaxAtoSpeed', 'col': 2}
	PercOfAtoSpeed = {'sh_name': 'Performance_Level', 'attr_name': 'PercOfAtoSpeed', 'col': 3}
	MaxAccel = {'sh_name': 'Performance_Level', 'attr_name': 'MaxAccel', 'col': 4}
	MaxDecel = {'sh_name': 'Performance_Level', 'attr_name': 'MaxDecel', 'col': 5}
	AtsId = {'sh_name': 'Performance_Level', 'attr_name': 'AtsId', 'col': 6}
	CoastingProfileLevel = {'sh_name': 'Performance_Level', 'attr_name': 'CoastingProfileLevel', 'col': 7}


class Restriction_Level:
	Name = {'sh_name': 'Restriction_Level', 'attr_name': 'Name', 'col': 1}
	MaxAccel = {'sh_name': 'Restriction_Level', 'attr_name': 'MaxAccel', 'col': 2}
	MaxDecel = {'sh_name': 'Restriction_Level', 'attr_name': 'MaxDecel', 'col': 3}
	Id = {'sh_name': 'Restriction_Level', 'attr_name': 'Id', 'col': 4}


class Carborne_Controllers__Tacho:
	OnTractionAxle = {'sh_name': 'Carborne_Controllers', 'attr_name': 'Tacho', 'sub_attr_name': 'OnTractionAxle', 'cols': [8, 11]}
	OnBrakingAxle = {'sh_name': 'Carborne_Controllers', 'attr_name': 'Tacho', 'sub_attr_name': 'OnBrakingAxle', 'cols': [9, 12]}
	Polarity = {'sh_name': 'Carborne_Controllers', 'attr_name': 'Tacho', 'sub_attr_name': 'Polarity', 'cols': [10, 13]}


class Carborne_Controllers__Acceleros:
	AccelerosCar = {'sh_name': 'Carborne_Controllers', 'attr_name': 'Acceleros', 'sub_attr_name': 'AccelerosCar', 'cols': [14]}
	Polarity = {'sh_name': 'Carborne_Controllers', 'attr_name': 'Acceleros', 'sub_attr_name': 'Polarity', 'cols': [15]}


class Carborne_Controllers:
	Name = {'sh_name': 'Carborne_Controllers', 'attr_name': 'Name', 'col': 1}
	Cab = {'sh_name': 'Carborne_Controllers', 'attr_name': 'Cab', 'col': 2}
	TiaConfiguration = {'sh_name': 'Carborne_Controllers', 'attr_name': 'TiaConfiguration', 'col': 3}
	FirstTiaToCab1 = {'sh_name': 'Carborne_Controllers', 'attr_name': 'FirstTiaToCab1', 'col': 4}
	SecondTiaToCab1 = {'sh_name': 'Carborne_Controllers', 'attr_name': 'SecondTiaToCab1', 'col': 5}
	TagReaderConfiguration = {'sh_name': 'Carborne_Controllers', 'attr_name': 'TagReaderConfiguration', 'col': 6}
	PulseNumber = {'sh_name': 'Carborne_Controllers', 'attr_name': 'PulseNumber', 'col': 7}
	Tacho = Carborne_Controllers__Tacho()
	Acceleros = Carborne_Controllers__Acceleros()
	MtorNumber = {'sh_name': 'Carborne_Controllers', 'attr_name': 'MtorNumber', 'col': 16}


class Car__Bogey:
	AxleLocation = {'sh_name': 'Car', 'attr_name': 'Bogey', 'sub_attr_name': 'AxleLocation', 'cols': [15, 16, 17, 18]}


class Car:
	Name = {'sh_name': 'Car', 'attr_name': 'Name', 'col': 1}
	IsCab = {'sh_name': 'Car', 'attr_name': 'IsCab', 'col': 2}
	Length = {'sh_name': 'Car', 'attr_name': 'Length', 'col': 3}
	Height = {'sh_name': 'Car', 'attr_name': 'Height', 'col': 4}
	FloorHeight = {'sh_name': 'Car', 'attr_name': 'FloorHeight', 'col': 5}
	EmptyMass = {'sh_name': 'Car', 'attr_name': 'EmptyMass', 'col': 6}
	FullLoadMass = {'sh_name': 'Car', 'attr_name': 'FullLoadMass', 'col': 7}
	DoorWidth = {'sh_name': 'Car', 'attr_name': 'DoorWidth', 'col': 8}
	DoorsNumber = {'sh_name': 'Car', 'attr_name': 'DoorsNumber', 'col': 9}
	Door1Location = {'sh_name': 'Car', 'attr_name': 'Door1Location', 'col': 10}
	Door2Location = {'sh_name': 'Car', 'attr_name': 'Door2Location', 'col': 11}
	Door3Location = {'sh_name': 'Car', 'attr_name': 'Door3Location', 'col': 12}
	Door4Location = {'sh_name': 'Car', 'attr_name': 'Door4Location', 'col': 13}
	Door5Location = {'sh_name': 'Car', 'attr_name': 'Door5Location', 'col': 14}
	Bogey = Car__Bogey()


class Train_Types__ManageGenericCommands:
	ManageCmdA = {'sh_name': 'Train_Types', 'attr_name': 'ManageGenericCommands', 'sub_attr_name': 'ManageCmdA', 'cols': [32]}
	CmdALocation = {'sh_name': 'Train_Types', 'attr_name': 'ManageGenericCommands', 'sub_attr_name': 'CmdALocation', 'cols': [33]}
	ManageCmdB = {'sh_name': 'Train_Types', 'attr_name': 'ManageGenericCommands', 'sub_attr_name': 'ManageCmdB', 'cols': [34]}
	CmdBLocation = {'sh_name': 'Train_Types', 'attr_name': 'ManageGenericCommands', 'sub_attr_name': 'CmdBLocation', 'cols': [35]}
	ManageCmdC = {'sh_name': 'Train_Types', 'attr_name': 'ManageGenericCommands', 'sub_attr_name': 'ManageCmdC', 'cols': [36]}
	CmdCLocation = {'sh_name': 'Train_Types', 'attr_name': 'ManageGenericCommands', 'sub_attr_name': 'CmdCLocation', 'cols': [37]}


class Train_Types__PowerCollectorDevices:
	Location = {'sh_name': 'Train_Types', 'attr_name': 'PowerCollectorDevices', 'sub_attr_name': 'Location', 'cols': [38, 39, 40, 41, 42]}


class Train_Types__SpeedLevel:
	Id = {'sh_name': 'Train_Types', 'attr_name': 'SpeedLevel', 'sub_attr_name': 'Id', 'cols': [44, 46, 48, 50, 52, 54, 56, 58]}
	Speed = {'sh_name': 'Train_Types', 'attr_name': 'SpeedLevel', 'sub_attr_name': 'Speed', 'cols': [45, 47, 49, 51, 53, 55, 57, 59]}


class Train_Types:
	Name = {'sh_name': 'Train_Types', 'attr_name': 'Name', 'col': 1}
	TrainTypeId = {'sh_name': 'Train_Types', 'attr_name': 'TrainTypeId', 'col': 2}
	AvConsistType = {'sh_name': 'Train_Types', 'attr_name': 'AvConsistType', 'col': 3}
	Length = {'sh_name': 'Train_Types', 'attr_name': 'Length', 'col': 4}
	ShortestIndivisiblePartLength = {'sh_name': 'Train_Types', 'attr_name': 'ShortestIndivisiblePartLength', 'col': 5}
	EmptyMass = {'sh_name': 'Train_Types', 'attr_name': 'EmptyMass', 'col': 6}
	FullLoadMass = {'sh_name': 'Train_Types', 'attr_name': 'FullLoadMass', 'col': 7}
	RotatingMass = {'sh_name': 'Train_Types', 'attr_name': 'RotatingMass', 'col': 8}
	WheelMinDiam = {'sh_name': 'Train_Types', 'attr_name': 'WheelMinDiam', 'col': 9}
	WheelMaxDiam = {'sh_name': 'Train_Types', 'attr_name': 'WheelMaxDiam', 'col': 10}
	WheelMeanDiam = {'sh_name': 'Train_Types', 'attr_name': 'WheelMeanDiam', 'col': 11}
	CarNumber = {'sh_name': 'Train_Types', 'attr_name': 'CarNumber', 'col': 12}
	Car1 = {'sh_name': 'Train_Types', 'attr_name': 'Car1', 'col': 13}
	Car2 = {'sh_name': 'Train_Types', 'attr_name': 'Car2', 'col': 14}
	Car3 = {'sh_name': 'Train_Types', 'attr_name': 'Car3', 'col': 15}
	Car4 = {'sh_name': 'Train_Types', 'attr_name': 'Car4', 'col': 16}
	Car5 = {'sh_name': 'Train_Types', 'attr_name': 'Car5', 'col': 17}
	Car6 = {'sh_name': 'Train_Types', 'attr_name': 'Car6', 'col': 18}
	Car7 = {'sh_name': 'Train_Types', 'attr_name': 'Car7', 'col': 19}
	Car8 = {'sh_name': 'Train_Types', 'attr_name': 'Car8', 'col': 20}
	Car9 = {'sh_name': 'Train_Types', 'attr_name': 'Car9', 'col': 21}
	Car10 = {'sh_name': 'Train_Types', 'attr_name': 'Car10', 'col': 22}
	DegradedMode = {'sh_name': 'Train_Types', 'attr_name': 'DegradedMode', 'col': 23}
	IsolationInputType = {'sh_name': 'Train_Types', 'attr_name': 'IsolationInputType', 'col': 24}
	CcCutsTractionWhenEb = {'sh_name': 'Train_Types', 'attr_name': 'CcCutsTractionWhenEb', 'col': 25}
	CcCcComType = {'sh_name': 'Train_Types', 'attr_name': 'CcCcComType', 'col': 26}
	DisconnectRsFromTpForPassengerProtection = {'sh_name': 'Train_Types', 'attr_name': 'DisconnectRsFromTpForPassengerProtection', 'col': 27}
	DisconnectThroughEb = {'sh_name': 'Train_Types', 'attr_name': 'DisconnectThroughEb', 'col': 28}
	SendNvOutputInBypass = {'sh_name': 'Train_Types', 'attr_name': 'SendNvOutputInBypass', 'col': 29}
	TdBypassDedicatedInputAvailable = {'sh_name': 'Train_Types', 'attr_name': 'TdBypassDedicatedInputAvailable', 'col': 30}
	DriverlessModeAvailable = {'sh_name': 'Train_Types', 'attr_name': 'DriverlessModeAvailable', 'col': 31}
	ManageGenericCommands = Train_Types__ManageGenericCommands()
	PowerCollectorDevices = Train_Types__PowerCollectorDevices()
	MasterControllerType = {'sh_name': 'Train_Types', 'attr_name': 'MasterControllerType', 'col': 43}
	SpeedLevel = Train_Types__SpeedLevel()


class AV_Types__Bogey:
	AxleLocation = {'sh_name': 'AV_Types', 'attr_name': 'Bogey', 'sub_attr_name': 'AxleLocation', 'cols': [13, 14, 15, 16]}


class AV_Types:
	Name = {'sh_name': 'AV_Types', 'attr_name': 'Name', 'col': 1}
	AvConsistType = {'sh_name': 'AV_Types', 'attr_name': 'AvConsistType', 'col': 2}
	Length = {'sh_name': 'AV_Types', 'attr_name': 'Length', 'col': 3}
	ShortestIndivisiblePartLength = {'sh_name': 'AV_Types', 'attr_name': 'ShortestIndivisiblePartLength', 'col': 4}
	Height = {'sh_name': 'AV_Types', 'attr_name': 'Height', 'col': 5}
	FloorHeight = {'sh_name': 'AV_Types', 'attr_name': 'FloorHeight', 'col': 6}
	EmptyMass = {'sh_name': 'AV_Types', 'attr_name': 'EmptyMass', 'col': 7}
	FullLoadMass = {'sh_name': 'AV_Types', 'attr_name': 'FullLoadMass', 'col': 8}
	RotatingMass = {'sh_name': 'AV_Types', 'attr_name': 'RotatingMass', 'col': 9}
	WheelMinDiam = {'sh_name': 'AV_Types', 'attr_name': 'WheelMinDiam', 'col': 10}
	WheelMaxDiam = {'sh_name': 'AV_Types', 'attr_name': 'WheelMaxDiam', 'col': 11}
	WheelMeanDiam = {'sh_name': 'AV_Types', 'attr_name': 'WheelMeanDiam', 'col': 12}
	Bogey = AV_Types__Bogey()
	IsolationInputType = {'sh_name': 'AV_Types', 'attr_name': 'IsolationInputType', 'col': 17}
	CcCutsTractionWhenEb = {'sh_name': 'AV_Types', 'attr_name': 'CcCutsTractionWhenEb', 'col': 18}
	CcCcComType = {'sh_name': 'AV_Types', 'attr_name': 'CcCcComType', 'col': 19}
	DisconnectRsFromTpForPassengerProtection = {'sh_name': 'AV_Types', 'attr_name': 'DisconnectRsFromTpForPassengerProtection', 'col': 20}
	DisconnectThroughEb = {'sh_name': 'AV_Types', 'attr_name': 'DisconnectThroughEb', 'col': 21}


class Flatbed_Types__Bogey:
	AxleLocation = {'sh_name': 'Flatbed_Types', 'attr_name': 'Bogey', 'sub_attr_name': 'AxleLocation', 'cols': [9, 10, 11, 12]}


class Flatbed_Types:
	Name = {'sh_name': 'Flatbed_Types', 'attr_name': 'Name', 'col': 1}
	AvConsistType = {'sh_name': 'Flatbed_Types', 'attr_name': 'AvConsistType', 'col': 2}
	Length = {'sh_name': 'Flatbed_Types', 'attr_name': 'Length', 'col': 3}
	ShortestIndivisiblePartLength = {'sh_name': 'Flatbed_Types', 'attr_name': 'ShortestIndivisiblePartLength', 'col': 4}
	FloorHeight = {'sh_name': 'Flatbed_Types', 'attr_name': 'FloorHeight', 'col': 5}
	EmptyMass = {'sh_name': 'Flatbed_Types', 'attr_name': 'EmptyMass', 'col': 6}
	FullLoadMass = {'sh_name': 'Flatbed_Types', 'attr_name': 'FullLoadMass', 'col': 7}
	RotatingMass = {'sh_name': 'Flatbed_Types', 'attr_name': 'RotatingMass', 'col': 8}
	Bogey = Flatbed_Types__Bogey()


class AV_Consist:
	Name = {'sh_name': 'AV_Consist', 'attr_name': 'Name', 'col': 1}
	AvConsistTypeId = {'sh_name': 'AV_Consist', 'attr_name': 'AvConsistTypeId', 'col': 2}
	VehicleType1 = {'sh_name': 'AV_Consist', 'attr_name': 'VehicleType1', 'col': 3}
	VehicleType2 = {'sh_name': 'AV_Consist', 'attr_name': 'VehicleType2', 'col': 4}
	VehicleType3 = {'sh_name': 'AV_Consist', 'attr_name': 'VehicleType3', 'col': 5}
	VehicleType4 = {'sh_name': 'AV_Consist', 'attr_name': 'VehicleType4', 'col': 6}
	VehicleType5 = {'sh_name': 'AV_Consist', 'attr_name': 'VehicleType5', 'col': 7}
	MaxSpeed = {'sh_name': 'AV_Consist', 'attr_name': 'MaxSpeed', 'col': 8}
	PropulsionEnableDeactivationTractionCutTime = {'sh_name': 'AV_Consist', 'attr_name': 'PropulsionEnableDeactivationTractionCutTime', 'col': 9}
	EmergencyBrakeRequestTractionCutTime = {'sh_name': 'AV_Consist', 'attr_name': 'EmergencyBrakeRequestTractionCutTime', 'col': 10}
	CoastTime = {'sh_name': 'AV_Consist', 'attr_name': 'CoastTime', 'col': 11}
	HyperAcceleration = {'sh_name': 'AV_Consist', 'attr_name': 'HyperAcceleration', 'col': 12}
	EbRate = {'sh_name': 'AV_Consist', 'attr_name': 'EbRate', 'col': 13}
	SbRate = {'sh_name': 'AV_Consist', 'attr_name': 'SbRate', 'col': 14}
	TractionDirectionType = {'sh_name': 'AV_Consist', 'attr_name': 'TractionDirectionType', 'col': 15}
	Margin_A_Psr = {'sh_name': 'AV_Consist', 'attr_name': 'Margin_A_Psr', 'col': 16}
	Margin_B_Psr = {'sh_name': 'AV_Consist', 'attr_name': 'Margin_B_Psr', 'col': 17}
	RsCharacteristicsFileName = {'sh_name': 'AV_Consist', 'attr_name': 'RsCharacteristicsFileName', 'col': 18}


class Train_Consist:
	Name = {'sh_name': 'Train_Consist', 'attr_name': 'Name', 'col': 1}
	TrainConsistTypeId = {'sh_name': 'Train_Consist', 'attr_name': 'TrainConsistTypeId', 'col': 2}
	RescueOnly = {'sh_name': 'Train_Consist', 'attr_name': 'RescueOnly', 'col': 3}
	TrainType1 = {'sh_name': 'Train_Consist', 'attr_name': 'TrainType1', 'col': 4}
	TrainType2 = {'sh_name': 'Train_Consist', 'attr_name': 'TrainType2', 'col': 5}
	TrainType3 = {'sh_name': 'Train_Consist', 'attr_name': 'TrainType3', 'col': 6}
	TrainType4 = {'sh_name': 'Train_Consist', 'attr_name': 'TrainType4', 'col': 7}
	RsCharacteristicsFileName = {'sh_name': 'Train_Consist', 'attr_name': 'RsCharacteristicsFileName', 'col': 8}
	RecoveryRsCharacteristicsFileName = {'sh_name': 'Train_Consist', 'attr_name': 'RecoveryRsCharacteristicsFileName', 'col': 9}
	MaxSpeed = {'sh_name': 'Train_Consist', 'attr_name': 'MaxSpeed', 'col': 10}
	PropulsionEnableDeactivationTractionCutTime = {'sh_name': 'Train_Consist', 'attr_name': 'PropulsionEnableDeactivationTractionCutTime', 'col': 11}
	EmergencyBrakeRequestTractionCutTime = {'sh_name': 'Train_Consist', 'attr_name': 'EmergencyBrakeRequestTractionCutTime', 'col': 12}
	CoastTime = {'sh_name': 'Train_Consist', 'attr_name': 'CoastTime', 'col': 13}
	EbRate = {'sh_name': 'Train_Consist', 'attr_name': 'EbRate', 'col': 14}
	SbRate = {'sh_name': 'Train_Consist', 'attr_name': 'SbRate', 'col': 15}
	TractionDirectionType = {'sh_name': 'Train_Consist', 'attr_name': 'TractionDirectionType', 'col': 16}
	Margin_A_Psr = {'sh_name': 'Train_Consist', 'attr_name': 'Margin_A_Psr', 'col': 17}
	Margin_B_Psr = {'sh_name': 'Train_Consist', 'attr_name': 'Margin_B_Psr', 'col': 18}
	SleepingModeNotAvailable = {'sh_name': 'Train_Consist', 'attr_name': 'SleepingModeNotAvailable', 'col': 19}


class Train:
	Name = {'sh_name': 'Train', 'attr_name': 'Name', 'col': 1}
	Type = {'sh_name': 'Train', 'attr_name': 'Type', 'col': 2}
	CbtcTrainUnitId = {'sh_name': 'Train', 'attr_name': 'CbtcTrainUnitId', 'col': 3}
	TrainCustomerName = {'sh_name': 'Train', 'attr_name': 'TrainCustomerName', 'col': 4}
	CcConfiguration = {'sh_name': 'Train', 'attr_name': 'CcConfiguration', 'col': 5}
	VirtualCcName = {'sh_name': 'Train', 'attr_name': 'VirtualCcName', 'col': 6}
	Cab1CcName = {'sh_name': 'Train', 'attr_name': 'Cab1CcName', 'col': 7}
	Cab2CcName = {'sh_name': 'Train', 'attr_name': 'Cab2CcName', 'col': 8}
	Cab1TodName = {'sh_name': 'Train', 'attr_name': 'Cab1TodName', 'col': 9}
	Cab2TodName = {'sh_name': 'Train', 'attr_name': 'Cab2TodName', 'col': 10}
	PisName = {'sh_name': 'Train', 'attr_name': 'PisName', 'col': 11}
	TarName = {'sh_name': 'Train', 'attr_name': 'TarName', 'col': 12}
	TmsMvbBoxName = {'sh_name': 'Train', 'attr_name': 'TmsMvbBoxName', 'col': 13}
	PwmBoxName = {'sh_name': 'Train', 'attr_name': 'PwmBoxName', 'col': 14}


class Auxiliary_Vehicle:
	Name = {'sh_name': 'Auxiliary_Vehicle', 'attr_name': 'Name', 'col': 1}
	Type = {'sh_name': 'Auxiliary_Vehicle', 'attr_name': 'Type', 'col': 2}
	CbtcTrainUnitId = {'sh_name': 'Auxiliary_Vehicle', 'attr_name': 'CbtcTrainUnitId', 'col': 3}
	CustomerName = {'sh_name': 'Auxiliary_Vehicle', 'attr_name': 'CustomerName', 'col': 4}
	CcName = {'sh_name': 'Auxiliary_Vehicle', 'attr_name': 'CcName', 'col': 5}
	TodName = {'sh_name': 'Auxiliary_Vehicle', 'attr_name': 'TodName', 'col': 6}
	TarName = {'sh_name': 'Auxiliary_Vehicle', 'attr_name': 'TarName', 'col': 7}


class Traction_Profiles__NonVital:
	Empty = {'sh_name': 'Traction_Profiles', 'attr_name': 'NonVital', 'sub_attr_name': 'Empty', 'cols': [3]}
	FullLoad = {'sh_name': 'Traction_Profiles', 'attr_name': 'NonVital', 'sub_attr_name': 'FullLoad', 'cols': [4]}


class Traction_Profiles:
	TrainConsist = {'sh_name': 'Traction_Profiles', 'attr_name': 'TrainConsist', 'col': 1}
	Speed = {'sh_name': 'Traction_Profiles', 'attr_name': 'Speed', 'col': 2}
	NonVital = Traction_Profiles__NonVital()
	Vital = {'sh_name': 'Traction_Profiles', 'attr_name': 'Vital', 'col': 5}


class Flood_Gate__Limit:
	Seg = {'sh_name': 'Flood_Gate', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [2, 7, 12, 17, 22, 27, 32, 37]}
	X = {'sh_name': 'Flood_Gate', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [3, 8, 13, 18, 23, 28, 33, 38]}
	Direction = {'sh_name': 'Flood_Gate', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [4, 9, 14, 19, 24, 29, 34, 39]}
	Track = {'sh_name': 'Flood_Gate', 'attr_name': 'Limit', 'sub_attr_name': 'Track', 'cols': [5, 10, 15, 20, 25, 30, 35, 40]}
	Kp = {'sh_name': 'Flood_Gate', 'attr_name': 'Limit', 'sub_attr_name': 'Kp', 'cols': [6, 11, 16, 21, 26, 31, 36, 41]}


class Flood_Gate__Blocks:
	Block = {'sh_name': 'Flood_Gate', 'attr_name': 'Blocks', 'sub_attr_name': 'Block', 'cols': [42, 43, 44, 45, 46, 47, 48, 49]}


class Flood_Gate:
	Name = {'sh_name': 'Flood_Gate', 'attr_name': 'Name', 'col': 1}
	Limit = Flood_Gate__Limit()
	Blocks = Flood_Gate__Blocks()


class Coupling_Area:
	Name = {'sh_name': 'Coupling_Area', 'attr_name': 'Name', 'col': 1}
	Block1 = {'sh_name': 'Coupling_Area', 'attr_name': 'Block1', 'col': 2}
	Block2 = {'sh_name': 'Coupling_Area', 'attr_name': 'Block2', 'col': 3}
	Block3 = {'sh_name': 'Coupling_Area', 'attr_name': 'Block3', 'col': 4}
	Block4 = {'sh_name': 'Coupling_Area', 'attr_name': 'Block4', 'col': 5}
	Block5 = {'sh_name': 'Coupling_Area', 'attr_name': 'Block5', 'col': 6}
	Block6 = {'sh_name': 'Coupling_Area', 'attr_name': 'Block6', 'col': 7}
	Block7 = {'sh_name': 'Coupling_Area', 'attr_name': 'Block7', 'col': 8}
	Block8 = {'sh_name': 'Coupling_Area', 'attr_name': 'Block8', 'col': 9}
	Block9 = {'sh_name': 'Coupling_Area', 'attr_name': 'Block9', 'col': 10}
	Block10 = {'sh_name': 'Coupling_Area', 'attr_name': 'Block10', 'col': 11}


class Floor_Levels__Limit:
	Seg = {'sh_name': 'Floor_Levels', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]}
	X = {'sh_name': 'Floor_Levels', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}
	Direction = {'sh_name': 'Floor_Levels', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]}


class Floor_Levels:
	Name = {'sh_name': 'Floor_Levels', 'attr_name': 'Name', 'col': 1}
	Type = {'sh_name': 'Floor_Levels', 'attr_name': 'Type', 'col': 2}
	Limit = Floor_Levels__Limit()


class EB_Rate_Area__Limit:
	Seg = {'sh_name': 'EB_Rate_Area', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44]}
	X = {'sh_name': 'EB_Rate_Area', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]}
	Direction = {'sh_name': 'EB_Rate_Area', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}


class EB_Rate_Area__EbRate:
	TrainConsistType = {'sh_name': 'EB_Rate_Area', 'attr_name': 'EbRate', 'sub_attr_name': 'TrainConsistType', 'cols': [47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77]}
	Value = {'sh_name': 'EB_Rate_Area', 'attr_name': 'EbRate', 'sub_attr_name': 'Value', 'cols': [48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78]}


class EB_Rate_Area:
	Name = {'sh_name': 'EB_Rate_Area', 'attr_name': 'Name', 'col': 1}
	Limit = EB_Rate_Area__Limit()
	EbRate = EB_Rate_Area__EbRate()


class Unwanted_Stop_Area__Limit:
	Seg = {'sh_name': 'Unwanted_Stop_Area', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}
	X = {'sh_name': 'Unwanted_Stop_Area', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]}
	Direction = {'sh_name': 'Unwanted_Stop_Area', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [8, 11, 14, 17, 20, 23, 26, 29, 32, 35]}


class Unwanted_Stop_Area:
	Name = {'sh_name': 'Unwanted_Stop_Area', 'attr_name': 'Name', 'col': 1}
	Type = {'sh_name': 'Unwanted_Stop_Area', 'attr_name': 'Type', 'col': 2}
	Cause = {'sh_name': 'Unwanted_Stop_Area', 'attr_name': 'Cause', 'col': 3}
	Direction = {'sh_name': 'Unwanted_Stop_Area', 'attr_name': 'Direction', 'col': 4}
	Applicability = {'sh_name': 'Unwanted_Stop_Area', 'attr_name': 'Applicability', 'col': 5}
	Limit = Unwanted_Stop_Area__Limit()


class Consist_OSP__AuthorisedConsist:
	ConsistName = {'sh_name': 'Consist_OSP', 'attr_name': 'AuthorisedConsist', 'sub_attr_name': 'ConsistName', 'cols': [2, 10, 18, 26, 34, 42, 50, 58]}
	IsDefault = {'sh_name': 'Consist_OSP', 'attr_name': 'AuthorisedConsist', 'sub_attr_name': 'IsDefault', 'cols': [3, 11, 19, 27, 35, 43, 51, 59]}
	PsdSubset = {'sh_name': 'Consist_OSP', 'attr_name': 'AuthorisedConsist', 'sub_attr_name': 'PsdSubset', 'cols': [4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31, 36, 37, 38, 39, 44, 45, 46, 47, 52, 53, 54, 55, 60, 61, 62, 63]}
	TdSubset = {'sh_name': 'Consist_OSP', 'attr_name': 'AuthorisedConsist', 'sub_attr_name': 'TdSubset', 'cols': [8, 9, 16, 17, 24, 25, 32, 33, 40, 41, 48, 49, 56, 57, 64, 65]}


class Consist_OSP:
	OspName = {'sh_name': 'Consist_OSP', 'attr_name': 'OspName', 'col': 1}
	AuthorisedConsist = Consist_OSP__AuthorisedConsist()


class Walkways_Area__ForbidEvac:
	LeftCentral = {'sh_name': 'Walkways_Area', 'attr_name': 'ForbidEvac', 'sub_attr_name': 'LeftCentral', 'cols': [2]}
	LeftLateral = {'sh_name': 'Walkways_Area', 'attr_name': 'ForbidEvac', 'sub_attr_name': 'LeftLateral', 'cols': [3]}
	RightCentral = {'sh_name': 'Walkways_Area', 'attr_name': 'ForbidEvac', 'sub_attr_name': 'RightCentral', 'cols': [4]}
	RightLateral = {'sh_name': 'Walkways_Area', 'attr_name': 'ForbidEvac', 'sub_attr_name': 'RightLateral', 'cols': [5]}


class Walkways_Area__Limit:
	Seg = {'sh_name': 'Walkways_Area', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}
	X = {'sh_name': 'Walkways_Area', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]}
	Direction = {'sh_name': 'Walkways_Area', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [8, 11, 14, 17, 20, 23, 26, 29, 32, 35]}


class Walkways_Area:
	Name = {'sh_name': 'Walkways_Area', 'attr_name': 'Name', 'col': 1}
	ForbidEvac = Walkways_Area__ForbidEvac()
	Limit = Walkways_Area__Limit()


class Customs_Area__Customs:
	Block = {'sh_name': 'Customs_Area', 'attr_name': 'Customs', 'sub_attr_name': 'Block', 'cols': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}


class Customs_Area__Control:
	Block = {'sh_name': 'Customs_Area', 'attr_name': 'Control', 'sub_attr_name': 'Block', 'cols': [12, 14, 16]}
	DistRun = {'sh_name': 'Customs_Area', 'attr_name': 'Control', 'sub_attr_name': 'DistRun', 'cols': [13, 15, 17]}


class Customs_Area:
	Name = {'sh_name': 'Customs_Area', 'attr_name': 'Name', 'col': 1}
	Customs = Customs_Area__Customs()
	Control = Customs_Area__Control()


class CBTC_Prohibition_Area__IvbList:
	Ivb = {'sh_name': 'CBTC_Prohibition_Area', 'attr_name': 'IvbList', 'sub_attr_name': 'Ivb', 'cols': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]}


class CBTC_Prohibition_Area:
	Name = {'sh_name': 'CBTC_Prohibition_Area', 'attr_name': 'Name', 'col': 1}
	IvbList = CBTC_Prohibition_Area__IvbList()
	ManageTrainNumber = {'sh_name': 'CBTC_Prohibition_Area', 'attr_name': 'ManageTrainNumber', 'col': 22}
	MaxTrainNumber = {'sh_name': 'CBTC_Prohibition_Area', 'attr_name': 'MaxTrainNumber', 'col': 23}
	ManageUnitNumber = {'sh_name': 'CBTC_Prohibition_Area', 'attr_name': 'ManageUnitNumber', 'col': 24}
	MaxUnitNumber = {'sh_name': 'CBTC_Prohibition_Area', 'attr_name': 'MaxUnitNumber', 'col': 25}


class TSR_Area__Limit:
	Seg = {'sh_name': 'TSR_Area', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}
	X = {'sh_name': 'TSR_Area', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]}
	Direction = {'sh_name': 'TSR_Area', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48]}


class TSR_Area:
	Name = {'sh_name': 'TSR_Area', 'attr_name': 'Name', 'col': 1}
	Number = {'sh_name': 'TSR_Area', 'attr_name': 'Number', 'col': 2}
	Label = {'sh_name': 'TSR_Area', 'attr_name': 'Label', 'col': 3}
	Limit = TSR_Area__Limit()


class Anchor:
	TrackName = {'sh_name': 'Anchor', 'attr_name': 'TrackName', 'col': 1}
	SurveyedKp = {'sh_name': 'Anchor', 'attr_name': 'SurveyedKp', 'col': 2}
	CivilKp = {'sh_name': 'Anchor', 'attr_name': 'CivilKp', 'col': 3}


class Chainage:
	ChainageType = {'sh_name': 'Chainage', 'attr_name': 'ChainageType', 'col': 1}
	TrackName = {'sh_name': 'Chainage', 'attr_name': 'TrackName', 'col': 2}
	CivilKpStart = {'sh_name': 'Chainage', 'attr_name': 'CivilKpStart', 'col': 3}
	CivilKpEnd = {'sh_name': 'Chainage', 'attr_name': 'CivilKpEnd', 'col': 4}


class Superseed_Tan:
	CommandType = {'sh_name': 'Superseed_Tan', 'attr_name': 'CommandType', 'col': 1}


class Dynamic_Brake_Test_Point__TestPoint:
	Seg = {'sh_name': 'Dynamic_Brake_Test_Point', 'attr_name': 'TestPoint', 'sub_attr_name': 'Seg', 'cols': [2]}
	X = {'sh_name': 'Dynamic_Brake_Test_Point', 'attr_name': 'TestPoint', 'sub_attr_name': 'X', 'cols': [3]}


class Dynamic_Brake_Test_Point__SpeedPoint:
	Seg = {'sh_name': 'Dynamic_Brake_Test_Point', 'attr_name': 'SpeedPoint', 'sub_attr_name': 'Seg', 'cols': [5]}
	X = {'sh_name': 'Dynamic_Brake_Test_Point', 'attr_name': 'SpeedPoint', 'sub_attr_name': 'X', 'cols': [6]}


class Dynamic_Brake_Test_Point:
	Name = {'sh_name': 'Dynamic_Brake_Test_Point', 'attr_name': 'Name', 'col': 1}
	TestPoint = Dynamic_Brake_Test_Point__TestPoint()
	ApproachDirection = {'sh_name': 'Dynamic_Brake_Test_Point', 'attr_name': 'ApproachDirection', 'col': 4}
	SpeedPoint = Dynamic_Brake_Test_Point__SpeedPoint()
	BrakeType = {'sh_name': 'Dynamic_Brake_Test_Point', 'attr_name': 'BrakeType', 'col': 7}
	Speed = {'sh_name': 'Dynamic_Brake_Test_Point', 'attr_name': 'Speed', 'col': 8}
	StoppingTime = {'sh_name': 'Dynamic_Brake_Test_Point', 'attr_name': 'StoppingTime', 'col': 9}


class Traffic_Stop__PlatformList:
	Name = {'sh_name': 'Traffic_Stop', 'attr_name': 'PlatformList', 'sub_attr_name': 'Name', 'cols': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]}


class Traffic_Stop:
	Name = {'sh_name': 'Traffic_Stop', 'attr_name': 'Name', 'col': 1}
	TrafficStopSubsetName = {'sh_name': 'Traffic_Stop', 'attr_name': 'TrafficStopSubsetName', 'col': 2}
	PlatformList = Traffic_Stop__PlatformList()


class Protection_Zone__Limit:
	Seg = {'sh_name': 'Protection_Zone', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}
	X = {'sh_name': 'Protection_Zone', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]}
	Direction = {'sh_name': 'Protection_Zone', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48]}


class Protection_Zone:
	Name = {'sh_name': 'Protection_Zone', 'attr_name': 'Name', 'col': 1}
	Type = {'sh_name': 'Protection_Zone', 'attr_name': 'Type', 'col': 2}
	CbtcControlledFlag = {'sh_name': 'Protection_Zone', 'attr_name': 'CbtcControlledFlag', 'col': 3}
	Limit = Protection_Zone__Limit()


class Crossing_Calling_Area__From:
	Seg = {'sh_name': 'Crossing_Calling_Area', 'attr_name': 'From', 'sub_attr_name': 'Seg', 'cols': [3]}
	X = {'sh_name': 'Crossing_Calling_Area', 'attr_name': 'From', 'sub_attr_name': 'X', 'cols': [4]}


class Crossing_Calling_Area__To:
	Seg = {'sh_name': 'Crossing_Calling_Area', 'attr_name': 'To', 'sub_attr_name': 'Seg', 'cols': [5]}
	X = {'sh_name': 'Crossing_Calling_Area', 'attr_name': 'To', 'sub_attr_name': 'X', 'cols': [6]}


class Crossing_Calling_Area:
	Name = {'sh_name': 'Crossing_Calling_Area', 'attr_name': 'Name', 'col': 1}
	Id = {'sh_name': 'Crossing_Calling_Area', 'attr_name': 'Id', 'col': 2}
	From = Crossing_Calling_Area__From()
	To = Crossing_Calling_Area__To()
	RequestDistance = {'sh_name': 'Crossing_Calling_Area', 'attr_name': 'RequestDistance', 'col': 7}
	RequestDelay = {'sh_name': 'Crossing_Calling_Area', 'attr_name': 'RequestDelay', 'col': 8}
	CheckIl_Set = {'sh_name': 'Crossing_Calling_Area', 'attr_name': 'CheckIl_Set', 'col': 9}


class ASR__Limit:
	Seg = {'sh_name': 'ASR', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [4, 7, 10, 13, 16]}
	X = {'sh_name': 'ASR', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [5, 8, 11, 14, 17]}
	Direction = {'sh_name': 'ASR', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [6, 9, 12, 15, 18]}


class ASR:
	Name = {'sh_name': 'ASR', 'attr_name': 'Name', 'col': 1}
	Speed = {'sh_name': 'ASR', 'attr_name': 'Speed', 'col': 2}
	RelatedDirection = {'sh_name': 'ASR', 'attr_name': 'RelatedDirection', 'col': 3}
	Limit = ASR__Limit()


class PSD_Subsets__PsdNumber:
	Cell = {'sh_name': 'PSD_Subsets', 'attr_name': 'PsdNumber', 'sub_attr_name': 'Cell', 'cols': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]}


class PSD_Subsets:
	Name = {'sh_name': 'PSD_Subsets', 'attr_name': 'Name', 'col': 1}
	Id = {'sh_name': 'PSD_Subsets', 'attr_name': 'Id', 'col': 2}
	PlatformName = {'sh_name': 'PSD_Subsets', 'attr_name': 'PlatformName', 'col': 3}
	PsdNumber = PSD_Subsets__PsdNumber()


class DCM_Transition_Zones__Limit:
	Seg = {'sh_name': 'DCM_Transition_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44]}
	X = {'sh_name': 'DCM_Transition_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]}
	Direction = {'sh_name': 'DCM_Transition_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]}


class DCM_Transition_Zones:
	Name = {'sh_name': 'DCM_Transition_Zones', 'attr_name': 'Name', 'col': 1}
	Limit = DCM_Transition_Zones__Limit()


class Adhesion_Zones__Limit:
	Seg = {'sh_name': 'Adhesion_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]}
	X = {'sh_name': 'Adhesion_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]}
	Direction = {'sh_name': 'Adhesion_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}
	Voie = {'sh_name': 'Adhesion_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Voie', 'cols': [33, 35, 37, 39, 41, 43, 45, 47, 49, 51]}
	Pk = {'sh_name': 'Adhesion_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Pk', 'cols': [34, 36, 38, 40, 42, 44, 46, 48, 50, 52]}


class Adhesion_Zones:
	Name = {'sh_name': 'Adhesion_Zones', 'attr_name': 'Name', 'col': 1}
	Id = {'sh_name': 'Adhesion_Zones', 'attr_name': 'Id', 'col': 2}
	Limit = Adhesion_Zones__Limit()


class Adhesion_Level:
	Name = {'sh_name': 'Adhesion_Level', 'attr_name': 'Name', 'col': 1}
	MaxAccel = {'sh_name': 'Adhesion_Level', 'attr_name': 'MaxAccel', 'col': 2}
	MaxDecel = {'sh_name': 'Adhesion_Level', 'attr_name': 'MaxDecel', 'col': 3}
	Id = {'sh_name': 'Adhesion_Level', 'attr_name': 'Id', 'col': 4}


class Frontam_General_Data:
	Name = {'sh_name': 'Frontam_General_Data', 'attr_name': 'Name', 'col': 1}
	ObjectType = {'sh_name': 'Frontam_General_Data', 'attr_name': 'ObjectType', 'col': 2}
	ObjectName = {'sh_name': 'Frontam_General_Data', 'attr_name': 'ObjectName', 'col': 3}
	GeneralDataName = {'sh_name': 'Frontam_General_Data', 'attr_name': 'GeneralDataName', 'col': 4}
	TypeBitByte = {'sh_name': 'Frontam_General_Data', 'attr_name': 'TypeBitByte', 'col': 5}
	LineSectionName = {'sh_name': 'Frontam_General_Data', 'attr_name': 'LineSectionName', 'col': 6}
	Index = {'sh_name': 'Frontam_General_Data', 'attr_name': 'Index', 'col': 7}


class Generic_Command_Zones__CmdA:
	AppliedInZone = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'CmdA', 'sub_attr_name': 'AppliedInZone', 'cols': [2]}
	SpeedThreshold = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'CmdA', 'sub_attr_name': 'SpeedThreshold', 'cols': [3]}
	AnticipationTime = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'CmdA', 'sub_attr_name': 'AnticipationTime', 'cols': [4]}


class Generic_Command_Zones__CmdB:
	AppliedInZone = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'CmdB', 'sub_attr_name': 'AppliedInZone', 'cols': [5]}
	SpeedThreshold = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'CmdB', 'sub_attr_name': 'SpeedThreshold', 'cols': [6]}
	AnticipationTime = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'CmdB', 'sub_attr_name': 'AnticipationTime', 'cols': [7]}


class Generic_Command_Zones__CmdC:
	AppliedInZone = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'CmdC', 'sub_attr_name': 'AppliedInZone', 'cols': [8]}
	SpeedThreshold = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'CmdC', 'sub_attr_name': 'SpeedThreshold', 'cols': [9]}
	AnticipationTime = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'CmdC', 'sub_attr_name': 'AnticipationTime', 'cols': [10]}


class Generic_Command_Zones__Limit:
	Seg = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [11, 14, 17, 20, 23, 26, 29, 32, 35, 38]}
	X = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [12, 15, 18, 21, 24, 27, 30, 33, 36, 39]}
	Direction = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [13, 16, 19, 22, 25, 28, 31, 34, 37, 40]}
	Voie = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Voie', 'cols': [41, 43, 45, 47, 49, 51, 53, 55, 57, 59]}
	Pk = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Pk', 'cols': [42, 44, 46, 48, 50, 52, 54, 56, 58, 60]}


class Generic_Command_Zones:
	Name = {'sh_name': 'Generic_Command_Zones', 'attr_name': 'Name', 'col': 1}
	CmdA = Generic_Command_Zones__CmdA()
	CmdB = Generic_Command_Zones__CmdB()
	CmdC = Generic_Command_Zones__CmdC()
	Limit = Generic_Command_Zones__Limit()


class DCS_Elementary_Zones__Limit:
	Seg = {'sh_name': 'DCS_Elementary_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}
	X = {'sh_name': 'DCS_Elementary_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}
	Direction = {'sh_name': 'DCS_Elementary_Zones', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]}


class DCS_Elementary_Zones:
	Name = {'sh_name': 'DCS_Elementary_Zones', 'attr_name': 'Name', 'col': 1}
	SubsetName = {'sh_name': 'DCS_Elementary_Zones', 'attr_name': 'SubsetName', 'col': 2}
	AtsId = {'sh_name': 'DCS_Elementary_Zones', 'attr_name': 'AtsId', 'col': 3}
	ObjectId = {'sh_name': 'DCS_Elementary_Zones', 'attr_name': 'ObjectId', 'col': 4}
	Limit = DCS_Elementary_Zones__Limit()


class TSR_Possible_Speeds:
	Name = {'sh_name': 'TSR_Possible_Speeds', 'attr_name': 'Name', 'col': 1}
	Speed = {'sh_name': 'TSR_Possible_Speeds', 'attr_name': 'Speed', 'col': 2}


class TD_Subsets__TdNumber:
	Cell = {'sh_name': 'TD_Subsets', 'attr_name': 'TdNumber', 'sub_attr_name': 'Cell', 'cols': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]}


class TD_Subsets:
	Name = {'sh_name': 'TD_Subsets', 'attr_name': 'Name', 'col': 1}
	Id = {'sh_name': 'TD_Subsets', 'attr_name': 'Id', 'col': 2}
	PassengerTrainTypeName = {'sh_name': 'TD_Subsets', 'attr_name': 'PassengerTrainTypeName', 'col': 3}
	TdNumber = TD_Subsets__TdNumber()


class Unwanted_Coupling_Area__Limit:
	Seg = {'sh_name': 'Unwanted_Coupling_Area', 'attr_name': 'Limit', 'sub_attr_name': 'Seg', 'cols': [3, 6, 9, 12, 15]}
	X = {'sh_name': 'Unwanted_Coupling_Area', 'attr_name': 'Limit', 'sub_attr_name': 'X', 'cols': [4, 7, 10, 13, 16]}
	Direction = {'sh_name': 'Unwanted_Coupling_Area', 'attr_name': 'Limit', 'sub_attr_name': 'Direction', 'cols': [5, 8, 11, 14, 17]}


class Unwanted_Coupling_Area:
	Name = {'sh_name': 'Unwanted_Coupling_Area', 'attr_name': 'Name', 'col': 1}
	Direction = {'sh_name': 'Unwanted_Coupling_Area', 'attr_name': 'Direction', 'col': 2}
	Limit = Unwanted_Coupling_Area__Limit()


class Cruising_Zones__CruisingZone:
	Seg = {'sh_name': 'Cruising_Zones', 'attr_name': 'CruisingZone', 'sub_attr_name': 'Seg', 'cols': [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]}
	X = {'sh_name': 'Cruising_Zones', 'attr_name': 'CruisingZone', 'sub_attr_name': 'X', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}
	Direction = {'sh_name': 'Cruising_Zones', 'attr_name': 'CruisingZone', 'sub_attr_name': 'Direction', 'cols': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}


class Cruising_Zones:
	CruisingZoneName = {'sh_name': 'Cruising_Zones', 'attr_name': 'CruisingZoneName', 'col': 1}
	OriginPlatform = {'sh_name': 'Cruising_Zones', 'attr_name': 'OriginPlatform', 'col': 2}
	DestinationPlatform = {'sh_name': 'Cruising_Zones', 'attr_name': 'DestinationPlatform', 'col': 3}
	CruisingZone = Cruising_Zones__CruisingZone()


class Passage_Detector:
	Name = {'sh_name': 'Passage_Detector', 'attr_name': 'Name', 'col': 1}
	Seg = {'sh_name': 'Passage_Detector', 'attr_name': 'Seg', 'col': 2}
	X = {'sh_name': 'Passage_Detector', 'attr_name': 'X', 'col': 3}


class Parking_Place:
	Name = {'sh_name': 'Parking_Place', 'attr_name': 'Name', 'col': 1}
	AtsId = {'sh_name': 'Parking_Place', 'attr_name': 'AtsId', 'col': 2}
	ParkingPlaceLimit1 = {'sh_name': 'Parking_Place', 'attr_name': 'ParkingPlaceLimit1', 'col': 3}
	ExternalLocMemorizationOffsetLimit1 = {'sh_name': 'Parking_Place', 'attr_name': 'ExternalLocMemorizationOffsetLimit1', 'col': 4}
	ParkingPlaceLimit2 = {'sh_name': 'Parking_Place', 'attr_name': 'ParkingPlaceLimit2', 'col': 5}
	ExternalLocMemorizationOffsetLimit2 = {'sh_name': 'Parking_Place', 'attr_name': 'ExternalLocMemorizationOffsetLimit2', 'col': 6}
	SignalName1 = {'sh_name': 'Parking_Place', 'attr_name': 'SignalName1', 'col': 7}
	SignalName2 = {'sh_name': 'Parking_Place', 'attr_name': 'SignalName2', 'col': 8}
	SignalName3 = {'sh_name': 'Parking_Place', 'attr_name': 'SignalName3', 'col': 9}
	SignalName4 = {'sh_name': 'Parking_Place', 'attr_name': 'SignalName4', 'col': 10}
	SignalName5 = {'sh_name': 'Parking_Place', 'attr_name': 'SignalName5', 'col': 11}


class StaticTag_Group__TagList:
	Tag = {'sh_name': 'StaticTag_Group', 'attr_name': 'TagList', 'sub_attr_name': 'Tag', 'cols': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}


class StaticTag_Group:
	Name = {'sh_name': 'StaticTag_Group', 'attr_name': 'Name', 'col': 1}
	Id = {'sh_name': 'StaticTag_Group', 'attr_name': 'Id', 'col': 2}
	TagList = StaticTag_Group__TagList()


class Odometric_Zone__OdometricZone:
	Seg = {'sh_name': 'Odometric_Zone', 'attr_name': 'OdometricZone', 'sub_attr_name': 'Seg', 'cols': [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]}
	X = {'sh_name': 'Odometric_Zone', 'attr_name': 'OdometricZone', 'sub_attr_name': 'X', 'cols': [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]}
	Direction = {'sh_name': 'Odometric_Zone', 'attr_name': 'OdometricZone', 'sub_attr_name': 'Direction', 'cols': [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]}


class Odometric_Zone:
	Name = {'sh_name': 'Odometric_Zone', 'attr_name': 'Name', 'col': 1}
	Level = {'sh_name': 'Odometric_Zone', 'attr_name': 'Level', 'col': 2}
	CurvatureRadius = {'sh_name': 'Odometric_Zone', 'attr_name': 'CurvatureRadius', 'col': 3}
	Banking = {'sh_name': 'Odometric_Zone', 'attr_name': 'Banking', 'col': 4}
	OdometricZone = Odometric_Zone__OdometricZone()


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
	Car = Car()
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
