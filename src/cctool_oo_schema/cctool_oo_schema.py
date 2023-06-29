#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Ligne__SegmentsDepolarises:
	Cell = [7, 8, 9, 10, 11, 12, 13, 14]


class Ligne__LoopbackSegments:
	Cell = [18, 19, 20, 21, 22, 23, 24, 25]


class Ligne:
	Nom = 1
	Numero = 2
	Referentiel = 3
	SegmentReference = 4
	OrientationGauche = 5
	OrientationDroite = 6
	SegmentsDepolarises = Ligne__SegmentsDepolarises()
	Version = 15
	CbtcVersionKey = 16
	CbtcVersionRelease = 17
	LoopbackSegments = Ligne__LoopbackSegments()


class Voie:
	Nom = 1
	Ligne = 2
	NumeroSurLigne = 3
	NomPcc = 4
	Type = 5
	SensNominal = 6
	PkDebut = 7
	PkFin = 8


class Troncon__ExtremiteSurVoie:
	Voie = [9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66]
	PkDebut = [10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67]
	PkFin = [11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68]


class Troncon:
	Nom = 1
	Ligne = 2
	NumeroTronconLigne = 3
	NumVersion = 4
	TronconUtile1 = 5
	TronconUtile2 = 6
	TronconUtile3 = 7
	TronconUtile4 = 8
	ExtremiteSurVoie = Troncon__ExtremiteSurVoie()


class Seg__SegmentsVoisins:
	Amont = [8, 9]
	Aval = [10, 11]


class Seg:
	Nom = 1
	Troncon = 2
	NumSegmentTroncon = 3
	Voie = 4
	Origine = 5
	Fin = 6
	Longueur = 7
	SegmentsVoisins = Seg__SegmentsVoisins()
	SensLigne = 12
	RingSegment = 13
	RejectionDistance = 14


class Aig__SwitchBlockLockingArea:
	Ivb = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


class Aig__CbtcProtectingSwitchArea:
	Ivb = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27]


class Aig__AreaRightPositionFlank:
	BeginSeg = [28, 33, 38, 43]
	BeginX = [29, 34, 39, 44]
	EndSeg = [30, 35, 40, 45]
	EndX = [31, 36, 41, 46]
	Direction = [32, 37, 42, 47]


class Aig__AreaLeftPositionFlank:
	BeginSeg = [48, 53, 58, 63]
	BeginX = [49, 54, 59, 64]
	EndSeg = [50, 55, 60, 65]
	EndX = [51, 56, 61, 66]
	Direction = [52, 57, 62, 67]


class Aig:
	Nom = 1
	SegmentPointe = 2
	SegmentTd = 3
	SegmentTg = 4
	NumeroPcc = 5
	SwitchBlockLockingArea = Aig__SwitchBlockLockingArea()
	FreeToMove = 16
	Trailable = 17
	CbtcProtectingSwitchArea = Aig__CbtcProtectingSwitchArea()
	AreaRightPositionFlank = Aig__AreaRightPositionFlank()
	AreaLeftPositionFlank = Aig__AreaLeftPositionFlank()


class Quai__Station:
	Nom = [3]
	Abreviation = [4]
	NumStationLigne = [5]


class Quai__ExtremiteDuQuai:
	Seg = [9, 17]
	X = [10, 18]
	CoteOuvPortes = [11, 19]
	SensExt = [12, 20]
	Voie = [13, 21]
	Pk = [14, 22]
	CvspDistance = [15, 23]
	TerminalStation = [16, 24]


class Quai__PointDArret:
	Name = [25, 35, 45]
	Number = [26, 36, 46]
	Seg = [27, 37, 47]
	X = [28, 38, 48]
	SensAssocie = [29, 39, 49]
	SensApproche = [30, 40, 50]
	TypePtArretQuai = [31, 41, 51]
	StaticTest = [32, 42, 52]
	Voie = [33, 43, 53]
	Pk = [34, 44, 54]


class Quai__PointDEntree:
	Seg = [55, 59, 63, 67, 71, 75]
	X = [56, 60, 64, 68, 72, 76]
	Voie = [57, 61, 65, 69, 73, 77]
	Pk = [58, 62, 66, 70, 74, 78]


class Quai__FacadesDeQuai:
	EqptCfq = [89]
	CoteFq = [90]


class Quai:
	Nom = 1
	NumQuaiStation = 2
	Station = Quai__Station()
	InhibAccessibilite = 6
	CheckBrakes = 7
	AllowAccelerometersCalibration = 8
	ExtremiteDuQuai = Quai__ExtremiteDuQuai()
	PointDArret = Quai__PointDArret()
	PointDEntree = Quai__PointDEntree()
	AvecPassagers = 79
	AvecFq = 80
	PsdNumber = 81
	PsdNumbering = 82
	AvecPrecPtArret = 83
	RightSideOpeningTime = 84
	LeftSideOpeningTime = 85
	DoublePlatformOpeningDelay = 86
	DisableAutomaticDoorClosing = 87
	RelatedWaysideEquip = 88
	FacadesDeQuai = Quai__FacadesDeQuai()
	NumeroPccQuai = 91
	NumeroPccStation = 92
	WithEss = 93
	WithTh = 94
	WithTad = 95
	PsdMessagesRouted = 96
	Router = 97


class PtA:
	Nom = 1
	NumPtAtoSegment = 2
	Seg = 3
	X = 4
	SensAssocie = 5
	SensApproche = 6
	Voie = 7
	Pk = 8
	TypePtAto = 9
	ArretPermanentCpa = 10
	ParkingPosition = 11
	StaticTestAllowed = 12
	TrainDoorsOpeningSide = 13
	WashingOsp = 14
	OspProxDist = 15
	AllowAccelerometersCalibration = 16


class OSP_ATS_Id:
	Name = 1
	Type = 2
	AtsId = 3


class CDV__Extremite:
	Seg = [14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
	X = [15, 17, 19, 21, 23, 25, 27, 29, 31, 33]
	Voie = [34, 36, 38, 40, 42, 44, 46, 48, 50, 52]
	Pk = [35, 37, 39, 41, 43, 45, 47, 49, 51, 53]


class CDV__AnticipationSecuritaire:
	Ext = [54, 55, 56, 57, 58, 59, 60, 61, 62, 63]


class CDV__AnticipationErgonomique:
	Ext = [64, 65, 66, 67, 68, 69, 70, 71, 72, 73]


class CDV:
	Nom = 1
	DetectArb = 2
	DetectNcArb = 3
	DetectNrb = 4
	DetectNcNrb = 5
	AFiabiliser = 6
	ExtendedSievingAllowed = 7
	RailRoadEntrance = 8
	BrokenRailDetection = 9
	DedicatedLineSection = 10
	ReachBlockAllowed = 11
	IxlGivesBlockInitStatus = 12
	IxlGivesNotHeldStatus = 13
	Extremite = CDV__Extremite()
	AnticipationSecuritaire = CDV__AnticipationSecuritaire()
	AnticipationErgonomique = CDV__AnticipationErgonomique()
	AtsBlockId = 74


class IVB__Limit:
	Seg = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
	X = [11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
	Track = [30, 32, 34, 36, 38, 40, 42, 44, 46, 48]
	Kp = [31, 33, 35, 37, 39, 41, 43, 45, 47, 49]


class IVB__DiamondCrossingSwitches:
	SwitchName = [51, 52, 53, 54]


class IVB:
	Name = 1
	Id = 2
	SentToIxl = 3
	UsedByIxl = 4
	BlockFreed = 5
	ZcName = 6
	DirectionLockingBlock = 7
	UnlockNormal = 8
	UnlockReverse = 9
	Limit = IVB__Limit()
	DiamondCrossing = 50
	DiamondCrossingSwitches = IVB__DiamondCrossingSwitches()
	RelatedBlock = 55


class CV__Extremite:
	Seg = [2, 4, 6]
	X = [3, 5, 7]
	Voie = [8, 10, 12]
	Pk = [9, 11, 13]


class CV:
	Nom = 1
	Extremite = CV__Extremite()
	IsEndOfTrack = 14


class Sig__IvbJoint:
	UpstreamIvb = [12]
	DownstreamIvb = [13]


class Sig:
	Nom = 1
	Type = 2
	Seg = 3
	X = 4
	Sens = 5
	Voie = 6
	Pk = 7
	R_Cli = 8
	DistPap = 9
	VspType = 10
	DelayedLtDistance = 11
	IvbJoint = Sig__IvbJoint()
	Da_Passage = 14
	TypeDa = 15
	D_Echap = 16
	Du_Assistee = 17
	D_Libre = 18
	Enc_Dep = 19
	OverlapType = 20
	Annulable = 21
	WithFunc_Stop = 22
	CbtcTrainAppProvided = 23
	NumeroPcc = 24
	PositionForcee = 25
	SortieTerritoireCbtc = 26
	PresenceDynamicTag = 27
	WithIatpDepCheck = 28
	RelatedTag1 = 29
	RelatedTag2 = 30
	RelatedTag3 = 31
	RelatedTag4 = 32
	RelatedTag5 = 33
	RelatedTag6 = 34
	RelatedTag7 = 35
	RelatedTag8 = 36
	RelatedTag9 = 37
	RelatedTag10 = 38


class Sig_Zone__ExtremitesZoneArmementDa:
	Seg = [2, 6, 10, 14, 18, 22]
	X = [3, 7, 11, 15, 19, 23]
	Voie = [4, 8, 12, 16, 20, 24]
	Pk = [5, 9, 13, 17, 21, 25]


class Sig_Zone__PointsDEntreeZoneDApproche:
	Seg = [26, 30, 34, 38, 42, 46]
	X = [27, 31, 35, 39, 43, 47]
	Voie = [28, 32, 36, 40, 44, 48]
	Pk = [29, 33, 37, 41, 45, 49]


class Sig_Zone__PointsDEntreeZoneEnclDepass:
	Seg = [50, 54, 58, 62, 66, 70]
	X = [51, 55, 59, 63, 67, 71]
	Voie = [52, 56, 60, 64, 68, 72]
	Pk = [53, 57, 61, 65, 69, 73]


class Sig_Zone__ItiInterdictionAnnulation:
	Iti = [74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93]


class Sig_Zone__ConcealBlocksList:
	Block = [94, 95, 96, 97, 98, 99, 100, 101, 102, 103]


class Sig_Zone:
	NomDuSignal = 1
	ExtremitesZoneArmementDa = Sig_Zone__ExtremitesZoneArmementDa()
	PointsDEntreeZoneDApproche = Sig_Zone__PointsDEntreeZoneDApproche()
	PointsDEntreeZoneEnclDepass = Sig_Zone__PointsDEntreeZoneEnclDepass()
	ItiInterdictionAnnulation = Sig_Zone__ItiInterdictionAnnulation()
	ConcealBlocksList = Sig_Zone__ConcealBlocksList()


class Profil:
	Pente = 1
	Seg = 2
	X = 3
	Voie = 4
	Pk = 5


class Bal:
	Nom = 1
	BaliseName = 2
	NumBaliseSeg = 3
	Seg = 4
	X = 5
	Voie = 6
	Pk = 7
	TypePose = 8
	NumeroPcc = 9
	ReadingOccurrence = 10


class Coasting_Profiles__CoastingZone:
	TriggerSpeed = [8, 43, 78]
	StartTrack = [9, 44, 79]
	StartKp = [10, 45, 80]
	EndTrack = [11, 46, 81]
	EndKp = [12, 47, 82]
	Seg = [13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 83, 86, 89, 92, 95, 98, 101, 104, 107, 110]
	X = [14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 84, 87, 90, 93, 96, 99, 102, 105, 108, 111]
	Direction = [15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 85, 88, 91, 94, 97, 100, 103, 106, 109, 112]


class Coasting_Profiles:
	CoastingProfileName = 1
	Origin = 2
	Destination = 3
	CoastingProfileLevel = 4
	TheoreticalRuntime = 5
	CruisingSpeed = 6
	CruisingZoneName = 7
	CoastingZone = Coasting_Profiles__CoastingZone()


class CELL__Wcc:
	Nom = [3]


class CELL__PasCellule:
	Cell = [4, 5, 6, 7, 8]


class CELL__TronconsPropres:
	Cell = [9, 10, 11, 12]


class CELL__TronconsAnticipes:
	Cell = [13, 14, 15, 16]


class CELL__Extremite:
	Seg = [18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60]
	X = [19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61]
	Sens = [20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62]
	Voie = [63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91]
	Pk = [64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92]


class CELL:
	Nom = 1
	NumCellule = 2
	Wcc = CELL__Wcc()
	PasCellule = CELL__PasCellule()
	TronconsPropres = CELL__TronconsPropres()
	TronconsAnticipes = CELL__TronconsAnticipes()
	ServeurDInvariants = 17
	Extremite = CELL__Extremite()


class ZA_EFF_T__Extremite:
	Seg = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]
	X = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]
	Sens = [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
	Voie = [35, 37, 39, 41, 43, 45, 47, 49, 51, 53]
	Pk = [36, 38, 40, 42, 44, 46, 48, 50, 52, 54]


class ZA_EFF_T:
	Nom = 1
	Type = 2
	TriggerCondition = 3
	MaximumTractionEffort = 4
	Extremite = ZA_EFF_T__Extremite()


class SP:
	Nom = 1
	TerminusOuSp = 2
	QuaiArrivee = 3
	SensExtArrivee = 4
	QuaiDepart = 5
	SensExtDepart = 6
	RetournementSp = 7
	TypeSigSp = 8
	SignalSortieQuai = 9
	PointArretAto = 10


class Iti__RouteIvb:
	Ivb = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]


class Iti__Aiguille:
	Nom = [26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54]
	Position = [27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55]


class Iti:
	Nom = 1
	SignalOrig = 2
	OriginIvb = 3
	RouteIvb = Iti__RouteIvb()
	DestinationIvb = 24
	CdvDestEchap = 25
	Aiguille = Iti__Aiguille()


class CBTC_TER__Extremite:
	Seg = [9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51]
	X = [10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52]
	Sens = [11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53]


class CBTC_TER__ItinerairesDeSortie:
	Iti = [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]


class CBTC_TER__PointEntreeTerritoireCbtc:
	Seg = [74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122]
	X = [75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123]


class CBTC_TER:
	Nom = 1
	TypeTerritoireCbtc = 2
	AtcOffAllowed = 3
	EvacuationInhibition = 4
	WaysideDelocAlarmInhibition = 5
	SleepingOrLocMemorizationAllowed = 6
	RadioCoverageType = 7
	RearSievingRequired = 8
	Extremite = CBTC_TER__Extremite()
	ItinerairesDeSortie = CBTC_TER__ItinerairesDeSortie()
	PointEntreeTerritoireCbtc = CBTC_TER__PointEntreeTerritoireCbtc()


class PAS__ExtremiteSuivi:
	Seg = [4, 10, 16, 22, 28, 34, 40, 46, 52, 58, 64, 70, 76, 82, 88, 94, 100, 106, 112, 118, 124, 130, 136, 142, 148, 154, 160, 166, 172, 178]
	X = [5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95, 101, 107, 113, 119, 125, 131, 137, 143, 149, 155, 161, 167, 173, 179]
	Sens = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96, 102, 108, 114, 120, 126, 132, 138, 144, 150, 156, 162, 168, 174, 180]
	Voie = [7, 13, 19, 25, 31, 37, 43, 49, 55, 61, 67, 73, 79, 85, 91, 97, 103, 109, 115, 121, 127, 133, 139, 145, 151, 157, 163, 169, 175, 181]
	Pk = [8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86, 92, 98, 104, 110, 116, 122, 128, 134, 140, 146, 152, 158, 164, 170, 176, 182]
	MaxDist = [9, 15, 21, 27, 33, 39, 45, 51, 57, 63, 69, 75, 81, 87, 93, 99, 105, 111, 117, 123, 129, 135, 141, 147, 153, 159, 165, 171, 177, 183]


class PAS__TronconsGeresParLePas:
	Troncon = [184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203]


class PAS:
	Nom = 1
	TrackingAreaSubsetName = 2
	AtsZcId = 3
	ExtremiteSuivi = PAS__ExtremiteSuivi()
	TronconsGeresParLePas = PAS__TronconsGeresParLePas()
	ConcealmentType = 204
	TracksMultiConsists = 205
	DynamicSievingEnabled = 206


class Sas_ZSM_CBTC:
	Nom = 1
	PasEmetteur = 2
	ZsmCbtc = 3
	Rang = 4
	PasRecepteur1 = 5
	PasRecepteur2 = 6
	PasRecepteur3 = 7
	PasRecepteur4 = 8


class DP:
	Nom = 1
	Type = 2
	Seg = 3
	X = 4
	Voie = 5
	Pk = 6
	NumeroPcc = 7


class Sieving_Limit:
	Name = 1
	Type = 2
	RelatedBlock = 3
	Seg = 4
	X = 5
	Voie = 6
	Pk = 7
	Direction = 8


class ZSM_CBTC__SignauxZsm:
	Sigman = [2, 3]


class ZSM_CBTC__ExtZsm:
	Seg = [4, 8]
	X = [5, 9]
	Voie = [6, 10]
	Pk = [7, 11]


class ZSM_CBTC:
	Nom = 1
	SignauxZsm = ZSM_CBTC__SignauxZsm()
	ExtZsm = ZSM_CBTC__ExtZsm()
	SegReference = 12
	SensAutorise = 13
	SensDefaut = 14
	InterlockingVirtualBlock = 15
	DefaultIxlDirection = 16


class SE__Extremite:
	Seg = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]
	X = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]
	Sens = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48]
	Voie = [49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77]
	Pk = [50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78]


class SE:
	Nom = 1
	Type = 2
	Ss = 3
	Extremite = SE__Extremite()
	NumeroPcc = 79


class SS__Extremite:
	Seg = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44]
	X = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]
	Sens = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]
	Voie = [47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75]
	Pk = [48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76]


class SS:
	Nom = 1
	Extremite = SS__Extremite()


class ZCI__Extremite:
	Seg = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90]
	X = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91]
	Sens = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 89, 92]
	Voie = [93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151]
	Pk = [94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152]


class ZCI:
	Nom = 1
	NomPas = 2
	Extremite = ZCI__Extremite()


class Zaum__Extremite:
	Seg = [12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54]
	X = [13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55]
	Sens = [14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56]
	Voie = [57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85]
	Pk = [58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86]


class Zaum:
	Nom = 1
	QuaiAlarme1 = 2
	QuaiAlarme2 = 3
	TronconPreferentiel = 4
	AtsId = 5
	DriverlessAuthorized = 6
	AutomaticAuthorized = 7
	EvacuationProtectionZoneName = 8
	IntegrityProtectionZoneName = 9
	DelocalizationProtectionZoneName = 10
	DerailmentObstacleProtectionZoneName = 11
	Extremite = Zaum__Extremite()


class ZCRA__MouvZcra:
	PtArretOrig = [4, 9, 14]
	PtArretInter = [5, 10, 15]
	PtArretDest = [6, 11, 16]
	QuaiOrigine = [7, 12, 17]
	SensExtOrigine = [8, 13, 18]


class ZCRA__Extremite:
	Seg = [19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61]
	X = [20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62]
	Sens = [21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63]
	Voie = [64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92]
	Pk = [65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93]


class ZCRA:
	Nom = 1
	TronconPreferentiel = 2
	PresenceAdc = 3
	MouvZcra = ZCRA__MouvZcra()
	Extremite = ZCRA__Extremite()


class Zacp__Extremite:
	Seg = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
	X = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
	Sens = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
	Voie = [32, 34, 36, 38, 40, 42, 44, 46, 48, 50]
	Pk = [33, 35, 37, 39, 41, 43, 45, 47, 49, 51]


class Zacp:
	Nom = 1
	Extremite = Zacp__Extremite()


class ZLPV__De:
	Seg = [2]
	X = [3]
	DistanceAnticipation = [4]
	Voie = [8]
	Pk = [9]


class ZLPV__A:
	Seg = [5]
	X = [6]
	DistanceAnticipation = [7]
	Voie = [10]
	Pk = [11]


class ZLPV:
	VitesseZlpv = 1
	De = ZLPV__De()
	A = ZLPV__A()


class NV_PSR__From:
	Seg = [3]
	X = [4]
	Track = [7]
	Kp = [8]


class NV_PSR__To:
	Seg = [5]
	X = [6]
	Track = [9]
	Kp = [10]


class NV_PSR:
	Name = 1
	SpeedValue = 2
	From = NV_PSR__From()
	To = NV_PSR__To()
	AtsId = 11
	WithRelaxation = 12
	RelaxationCause = 13
	CeilingSpeedValue = 14


class ZLPV_Or__De:
	Seg = [4]
	X = [5]
	Voie = [8]
	Pk = [9]


class ZLPV_Or__A:
	Seg = [6]
	X = [7]
	Voie = [10]
	Pk = [11]


class ZLPV_Or:
	VitesseZlpv = 1
	Sens = 2
	DistanceAnticipation = 3
	De = ZLPV_Or__De()
	A = ZLPV_Or__A()


class Calib:
	BaliseDeb = 1
	BaliseFin = 2
	DistanceCalib = 3
	SensCalib = 4


class Zman:
	Nom = 1
	SigZman1 = 2
	SigZman2 = 3
	SigZman3 = 4
	SigZman4 = 5
	SigZman5 = 6
	SigZman6 = 7
	SigZman7 = 8
	SigZman8 = 9
	SigZman9 = 10
	SigZman10 = 11
	SigZman11 = 12
	SigZman12 = 13
	Ivb1 = 14
	Ivb2 = 15
	Ivb3 = 16
	Ivb4 = 17
	Ivb5 = 18
	Ivb6 = 19
	Ivb7 = 20
	Ivb8 = 21
	Ivb9 = 22
	Ivb10 = 23


class ZVR__Extremite:
	Seg = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
	X = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
	Sens = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
	Voie = [32, 34, 36, 38, 40, 42, 44, 46, 48, 50]
	Pk = [33, 35, 37, 39, 41, 43, 45, 47, 49, 51]


class ZVR:
	Nom = 1
	Extremite = ZVR__Extremite()


class CBTC_Eqpt__Equipements:
	Eqpt = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


class CBTC_Eqpt:
	Signal = 1
	Equipements = CBTC_Eqpt__Equipements()


class Flux_Variant_HF:
	Nom = 1
	ClasseObjet = 2
	NomObjet = 3
	NomLogiqueInfo = 4
	TypeFoncsecu = 5
	Troncon = 6
	Message = 7
	RgInfo = 8
	CommentaireDeGeneration = 9


class Flux_Variant_BF:
	Nom = 1
	ClasseObjet = 2
	NomObjet = 3
	NomLogiqueInfo = 4
	TypeFoncsecu = 5
	Troncon = 6
	Message = 7
	RgInfo = 8
	CommentaireDeGeneration = 9


class Wayside_Eqpt__Function:
	Zc = [3]
	Oc = [4]
	Zcr = [5]
	Psd = [6]
	Ups = [7]
	Ftm = [8]
	Dcs = [9]


class Wayside_Eqpt:
	Name = 1
	EqptId = 2
	Function = Wayside_Eqpt__Function()
	OcType = 10
	Location = 11


class Flux_MES_PAS:
	Nom = 1
	NomMes = 2
	ClasseObjet = 3
	NomObjet = 4
	NomLogiqueInfo = 5
	TypeInfo = 6
	Message = 7
	Extension = 8
	RgInfo = 9
	PasUtilisateur1 = 10
	PasUtilisateur2 = 11
	PasUtilisateur3 = 12
	PasUtilisateur4 = 13


class Flux_PAS_MES:
	Nom = 1
	NomMes = 2
	ClasseObjet = 3
	NomObjet = 4
	NomLogiqueInfo = 5
	TypeInfo = 6
	Message = 7
	Extension = 8
	RgInfo = 9
	PasUtilisateur1 = 10
	PasUtilisateur2 = 11
	PasUtilisateur3 = 12
	PasUtilisateur4 = 13


class ATS_ATC:
	Nom = 1
	ClasseObjet = 2
	NomObjet = 3
	NomLogiqueInfoAts = 4
	NomMessage = 5
	RgInfo = 6


class TM_MES_ATS:
	Nom = 1
	Equipement = 2
	ClasseObjet = 3
	NomObjet = 4
	NomLogiqueInfoAts = 5
	NomMessage = 6
	RgInfo = 7


class TM_PAS_ATS:
	Nom = 1
	Equipement = 2
	ClasseObjet = 3
	NomObjet = 4
	NomLogiqueInfoAts = 5
	NomMessage = 6
	RgInfo = 7


class Network:
	Name = 1
	Type = 2
	Line = 3
	BaseAddress = 4
	Medium = 5
	Mask = 6
	Gateway = 7
	Port = 8
	OverallMask = 9
	CcMulticastAddress = 10
	PisMulticastAddress = 11
	CcTmsMulticastAddress = 12
	TmsCcMulticastAddress = 13


class LineSection_Eqpt:
	Name = 1
	EqptId = 2
	Type = 3
	Zone = 4


class OnBoard_Eqpt__Function:
	IsRealCc = [3]
	IsVirtualCc = [4]
	IsTod = [5]
	IsPis = [6]
	IsTar = [7]
	IsTmsmvbBox = [8]
	IsPwmBox = [9]


class OnBoard_Eqpt:
	Name = 1
	EqptId = 2
	Function = OnBoard_Eqpt__Function()


class Interstation:
	Nom = 1
	QuaiOrigine = 2
	QuaiDestination = 3
	SensLigne = 4


class IATPM_tags__Routes:
	Route = [11, 12, 13, 14, 15, 16]


class IATPM_tags__VitalStoppingPoint:
	Seg = [18]
	X = [19]
	Track = [20]
	Kp = [21]


class IATPM_tags__ImcTimeout:
	Distance = [25]
	Value = [26]


class IATPM_tags__DmcTimeout:
	Distance = [27]
	Value = [28]


class IATPM_tags:
	Name = 1
	BaliseName = 2
	Type = 3
	NumTagSeg = 4
	Seg = 5
	X = 6
	Voie = 7
	Pk = 8
	LayingType = 9
	Signal = 10
	Routes = IATPM_tags__Routes()
	StopSignal = 17
	VitalStoppingPoint = IATPM_tags__VitalStoppingPoint()
	WithOverlap = 22
	OverlapName = 23
	OverlapReleaseDistance = 24
	ImcTimeout = IATPM_tags__ImcTimeout()
	DmcTimeout = IATPM_tags__DmcTimeout()


class IATPM_Version_Tags:
	Name = 1
	BaliseName = 2
	Seg = 3
	X = 4


class DynTag_Group__TagList:
	Tag = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


class DynTag_Group:
	Name = 1
	Id = 2
	TagList = DynTag_Group__TagList()


class Border_Area:
	Name = 1
	Block1 = 2
	Block2 = 3
	Block3 = 4
	Block4 = 5
	Block5 = 6
	Block6 = 7
	Block7 = 8
	Block8 = 9
	Block9 = 10
	Block10 = 11
	Block11 = 12
	Block12 = 13
	Block13 = 14
	Block14 = 15
	Block15 = 16
	Block16 = 17
	Block17 = 18
	Block18 = 19
	Block19 = 20
	Block20 = 21


class OVL_Border_Area:
	Nom = 1
	SenderZc = 2
	BorderArea = 3
	Rank = 4
	ZcReceiver1 = 5
	ZcReceiver2 = 6
	ZcReceiver3 = 7
	ZcReceiver4 = 8


class IXL_Overlap__VitalStoppingPoint:
	Seg = [5]
	X = [6]
	Sens = [7]
	Voie = [8]
	Pk = [9]


class IXL_Overlap__ReleasePoint:
	Seg = [10]
	X = [11]
	Track = [12]
	Kp = [13]


class IXL_Overlap__Aiguille:
	Nom = [15, 17, 19, 21]
	Position = [16, 18, 20, 22]


class IXL_Overlap:
	Name = 1
	DestinationSignal = 2
	PlatformRelated = 3
	WithTpp = 4
	VitalStoppingPoint = IXL_Overlap__VitalStoppingPoint()
	ReleasePoint = IXL_Overlap__ReleasePoint()
	ReleaseTimerValue = 14
	Aiguille = IXL_Overlap__Aiguille()


class Driving_Modes:
	Name = 1
	Group = 2
	Code = 3
	Abbreviation = 4


class Unprotected_Moves__Blocks:
	Block = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


class Unprotected_Moves:
	Name = 1
	Blocks = Unprotected_Moves__Blocks()


class CBTC_Overlap__Switch:
	Name = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
	Position = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]


class CBTC_Overlap:
	Name = 1
	Signal = 2
	Block1 = 3
	Switch = CBTC_Overlap__Switch()
	Block2 = 6
	Block3 = 9
	Block4 = 12
	Block5 = 15
	Block6 = 18
	Block7 = 21
	Block8 = 24
	Block9 = 27
	Block10 = 30


class Performance_Level:
	Name = 1
	MaxAtoSpeed = 2
	PercOfAtoSpeed = 3
	MaxAccel = 4
	MaxDecel = 5
	AtsId = 6
	CoastingProfileLevel = 7


class Restriction_Level:
	Name = 1
	MaxAccel = 2
	MaxDecel = 3
	Id = 4


class Carborne_Controllers__Tacho:
	OnTractionAxle = [8, 11]
	OnBrakingAxle = [9, 12]
	Polarity = [10, 13]


class Carborne_Controllers__Acceleros:
	AccelerosCar = [14]
	Polarity = [15]


class Carborne_Controllers:
	Name = 1
	Cab = 2
	TiaConfiguration = 3
	FirstTiaToCab1 = 4
	SecondTiaToCab1 = 5
	TagReaderConfiguration = 6
	PulseNumber = 7
	Tacho = Carborne_Controllers__Tacho()
	Acceleros = Carborne_Controllers__Acceleros()
	MtorNumber = 16


class Car__Bogey:
	AxleLocation = [15, 16, 17, 18]


class Car:
	Name = 1
	IsCab = 2
	Length = 3
	Height = 4
	FloorHeight = 5
	EmptyMass = 6
	FullLoadMass = 7
	DoorWidth = 8
	DoorsNumber = 9
	Door1Location = 10
	Door2Location = 11
	Door3Location = 12
	Door4Location = 13
	Door5Location = 14
	Bogey = Car__Bogey()


class Train_Types__ManageGenericCommands:
	ManageCmdA = [32]
	CmdALocation = [33]
	ManageCmdB = [34]
	CmdBLocation = [35]
	ManageCmdC = [36]
	CmdCLocation = [37]


class Train_Types__PowerCollectorDevices:
	Location = [38, 39, 40, 41, 42]


class Train_Types__SpeedLevel:
	Id = [44, 46, 48, 50, 52, 54, 56, 58]
	Speed = [45, 47, 49, 51, 53, 55, 57, 59]


class Train_Types:
	Name = 1
	TrainTypeId = 2
	AvConsistType = 3
	Length = 4
	ShortestIndivisiblePartLength = 5
	EmptyMass = 6
	FullLoadMass = 7
	RotatingMass = 8
	WheelMinDiam = 9
	WheelMaxDiam = 10
	WheelMeanDiam = 11
	CarNumber = 12
	Car1 = 13
	Car2 = 14
	Car3 = 15
	Car4 = 16
	Car5 = 17
	Car6 = 18
	Car7 = 19
	Car8 = 20
	Car9 = 21
	Car10 = 22
	DegradedMode = 23
	IsolationInputType = 24
	CcCutsTractionWhenEb = 25
	CcCcComType = 26
	DisconnectRsFromTpForPassengerProtection = 27
	DisconnectThroughEb = 28
	SendNvOutputInBypass = 29
	TdBypassDedicatedInputAvailable = 30
	DriverlessModeAvailable = 31
	ManageGenericCommands = Train_Types__ManageGenericCommands()
	PowerCollectorDevices = Train_Types__PowerCollectorDevices()
	MasterControllerType = 43
	SpeedLevel = Train_Types__SpeedLevel()


class AV_Types__Bogey:
	AxleLocation = [13, 14, 15, 16]


class AV_Types:
	Name = 1
	AvConsistType = 2
	Length = 3
	ShortestIndivisiblePartLength = 4
	Height = 5
	FloorHeight = 6
	EmptyMass = 7
	FullLoadMass = 8
	RotatingMass = 9
	WheelMinDiam = 10
	WheelMaxDiam = 11
	WheelMeanDiam = 12
	Bogey = AV_Types__Bogey()
	IsolationInputType = 17
	CcCutsTractionWhenEb = 18
	CcCcComType = 19
	DisconnectRsFromTpForPassengerProtection = 20
	DisconnectThroughEb = 21


class Flatbed_Types__Bogey:
	AxleLocation = [9, 10, 11, 12]


class Flatbed_Types:
	Name = 1
	AvConsistType = 2
	Length = 3
	ShortestIndivisiblePartLength = 4
	FloorHeight = 5
	EmptyMass = 6
	FullLoadMass = 7
	RotatingMass = 8
	Bogey = Flatbed_Types__Bogey()


class AV_Consist:
	Name = 1
	AvConsistTypeId = 2
	VehicleType1 = 3
	VehicleType2 = 4
	VehicleType3 = 5
	VehicleType4 = 6
	VehicleType5 = 7
	MaxSpeed = 8
	PropulsionEnableDeactivationTractionCutTime = 9
	EmergencyBrakeRequestTractionCutTime = 10
	CoastTime = 11
	HyperAcceleration = 12
	EbRate = 13
	SbRate = 14
	TractionDirectionType = 15
	Margin_A_Psr = 16
	Margin_B_Psr = 17
	RsCharacteristicsFileName = 18


class Train_Consist:
	Name = 1
	TrainConsistTypeId = 2
	RescueOnly = 3
	TrainType1 = 4
	TrainType2 = 5
	TrainType3 = 6
	TrainType4 = 7
	RsCharacteristicsFileName = 8
	RecoveryRsCharacteristicsFileName = 9
	MaxSpeed = 10
	PropulsionEnableDeactivationTractionCutTime = 11
	EmergencyBrakeRequestTractionCutTime = 12
	CoastTime = 13
	EbRate = 14
	SbRate = 15
	TractionDirectionType = 16
	Margin_A_Psr = 17
	Margin_B_Psr = 18
	SleepingModeNotAvailable = 19


class Train:
	Name = 1
	Type = 2
	CbtcTrainUnitId = 3
	TrainCustomerName = 4
	CcConfiguration = 5
	VirtualCcName = 6
	Cab1CcName = 7
	Cab2CcName = 8
	Cab1TodName = 9
	Cab2TodName = 10
	PisName = 11
	TarName = 12
	TmsmvbBoxName = 13
	PwmBoxName = 14


class Auxiliary_Vehicle:
	Name = 1
	Type = 2
	CbtcTrainUnitId = 3
	CustomerName = 4
	CcName = 5
	TodName = 6
	TarName = 7


class Traction_Profiles__NonVital:
	Empty = [3]
	FullLoad = [4]


class Traction_Profiles:
	TrainConsist = 1
	Speed = 2
	NonVital = Traction_Profiles__NonVital()
	Vital = 5


class Flood_Gate__Limit:
	Seg = [2, 7, 12, 17, 22, 27, 32, 37]
	X = [3, 8, 13, 18, 23, 28, 33, 38]
	Direction = [4, 9, 14, 19, 24, 29, 34, 39]
	Track = [5, 10, 15, 20, 25, 30, 35, 40]
	Kp = [6, 11, 16, 21, 26, 31, 36, 41]


class Flood_Gate__Blocks:
	Block = [42, 43, 44, 45, 46, 47, 48, 49]


class Flood_Gate:
	Name = 1
	Limit = Flood_Gate__Limit()
	Blocks = Flood_Gate__Blocks()


class Coupling_area:
	Name = 1
	Block1 = 2
	Block2 = 3
	Block3 = 4
	Block4 = 5
	Block5 = 6
	Block6 = 7
	Block7 = 8
	Block8 = 9
	Block9 = 10
	Block10 = 11


class Floor_Levels__Limit:
	Seg = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]
	X = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]
	Direction = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]


class Floor_Levels:
	Name = 1
	Type = 2
	Limit = Floor_Levels__Limit()


class EB_Rate_Area__Limit:
	Seg = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44]
	X = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]
	Direction = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]


class EB_Rate_Area__EbRate:
	TrainConsistType = [47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77]
	Value = [48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78]


class EB_Rate_Area:
	Name = 1
	Limit = EB_Rate_Area__Limit()
	EbRate = EB_Rate_Area__EbRate()


class Unwanted_Stop_Area__Limit:
	Seg = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]
	X = [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
	Direction = [8, 11, 14, 17, 20, 23, 26, 29, 32, 35]


class Unwanted_Stop_Area:
	Name = 1
	Type = 2
	Cause = 3
	Direction = 4
	Applicability = 5
	Limit = Unwanted_Stop_Area__Limit()


class Consist_OSP__AuthorisedConsist:
	ConsistName = [2, 10, 18, 26, 34, 42, 50, 58]
	IsDefault = [3, 11, 19, 27, 35, 43, 51, 59]
	PsdSubset = [4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31, 36, 37, 38, 39, 44, 45, 46, 47, 52, 53, 54, 55, 60, 61, 62, 63]
	TdSubset = [8, 9, 16, 17, 24, 25, 32, 33, 40, 41, 48, 49, 56, 57, 64, 65]


class Consist_OSP:
	OspName = 1
	AuthorisedConsist = Consist_OSP__AuthorisedConsist()


class Walkways_Area__ForbidEvac:
	LeftCentral = [2]
	LeftLateral = [3]
	RightCentral = [4]
	RightLateral = [5]


class Walkways_Area__Limit:
	Seg = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]
	X = [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
	Direction = [8, 11, 14, 17, 20, 23, 26, 29, 32, 35]


class Walkways_Area:
	Name = 1
	ForbidEvac = Walkways_Area__ForbidEvac()
	Limit = Walkways_Area__Limit()


class Customs_Area__Customs:
	Block = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


class Customs_Area__Control:
	Block = [12, 14, 16]
	DistRun = [13, 15, 17]


class Customs_Area:
	Name = 1
	Customs = Customs_Area__Customs()
	Control = Customs_Area__Control()


class CBTC_Prohibition_Area__IvbList:
	Ivb = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]


class CBTC_Prohibition_Area:
	Name = 1
	IvbList = CBTC_Prohibition_Area__IvbList()
	ManageTrainNumber = 22
	MaxTrainNumber = 23
	ManageUnitNumber = 24
	MaxUnitNumber = 25


class TSR_Area__Limit:
	Seg = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]
	X = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]
	Direction = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48]


class TSR_Area:
	Name = 1
	Number = 2
	Label = 3
	Limit = TSR_Area__Limit()


class Anchor:
	TrackName = 1
	SurveyedKp = 2
	CivilKp = 3


class Chainage:
	ChainageType = 1
	TrackName = 2
	CivilKpStart = 3
	CivilKpEnd = 4


class Superseed_Tan:
	CommandType = 1


class Dynamic_Brake_Test_Point__TestPoint:
	Seg = [2]
	X = [3]


class Dynamic_Brake_Test_Point__SpeedPoint:
	Seg = [5]
	X = [6]


class Dynamic_Brake_Test_Point:
	Name = 1
	TestPoint = Dynamic_Brake_Test_Point__TestPoint()
	ApproachDirection = 4
	SpeedPoint = Dynamic_Brake_Test_Point__SpeedPoint()
	BrakeType = 7
	Speed = 8
	StoppingTime = 9


class Traffic_Stop__PlatformList:
	Name = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]


class Traffic_Stop:
	Name = 1
	TrafficStopSubsetName = 2
	PlatformList = Traffic_Stop__PlatformList()


class Protection_Zone__Limit:
	Seg = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]
	X = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47]
	Direction = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48]


class Protection_Zone:
	Name = 1
	Type = 2
	CbtcControlledFlag = 3
	Limit = Protection_Zone__Limit()


class Crossing_Calling_Area__From:
	Seg = [3]
	X = [4]


class Crossing_Calling_Area__To:
	Seg = [5]
	X = [6]


class Crossing_Calling_Area:
	Name = 1
	Id = 2
	From = Crossing_Calling_Area__From()
	To = Crossing_Calling_Area__To()
	RequestDistance = 7
	RequestDelay = 8
	CheckIl_Set = 9


class ASR__Limit:
	Seg = [4, 7, 10, 13, 16]
	X = [5, 8, 11, 14, 17]
	Direction = [6, 9, 12, 15, 18]


class ASR:
	Name = 1
	Speed = 2
	RelatedDirection = 3
	Limit = ASR__Limit()


class PSD_Subsets__Psd:
	Cell = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]


class PSD_Subsets:
	Name = 1
	Id = 2
	PlatformName = 3
	Psd = PSD_Subsets__Psd()


class DCM_Transition_Zones__Limit:
	Seg = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44]
	X = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]
	Direction = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]


class DCM_Transition_Zones:
	Name = 1
	Limit = DCM_Transition_Zones__Limit()


class Adhesion_Zones__Limit:
	Seg = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
	X = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
	Direction = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]
	Voie = [33, 35, 37, 39, 41, 43, 45, 47, 49, 51]
	Pk = [34, 36, 38, 40, 42, 44, 46, 48, 50, 52]


class Adhesion_Zones:
	Name = 1
	Id = 2
	Limit = Adhesion_Zones__Limit()


class Adhesion_Level:
	Name = 1
	MaxAccel = 2
	MaxDecel = 3
	Id = 4


class Frontam_General_Data:
	Name = 1
	ObjectType = 2
	ObjectName = 3
	GeneralDataName = 4
	TypeBitbyte = 5
	LineSectionName = 6
	Index = 7


class Generic_Command_Zones__CmdA:
	AppliedInZone = [2]
	SpeedThreshold = [3]
	AnticipationTime = [4]


class Generic_Command_Zones__CmdB:
	AppliedInZone = [5]
	SpeedThreshold = [6]
	AnticipationTime = [7]


class Generic_Command_Zones__CmdC:
	AppliedInZone = [8]
	SpeedThreshold = [9]
	AnticipationTime = [10]


class Generic_Command_Zones__Limit:
	Seg = [11, 14, 17, 20, 23, 26, 29, 32, 35, 38]
	X = [12, 15, 18, 21, 24, 27, 30, 33, 36, 39]
	Direction = [13, 16, 19, 22, 25, 28, 31, 34, 37, 40]
	Voie = [41, 43, 45, 47, 49, 51, 53, 55, 57, 59]
	Pk = [42, 44, 46, 48, 50, 52, 54, 56, 58, 60]


class Generic_Command_Zones:
	Name = 1
	CmdA = Generic_Command_Zones__CmdA()
	CmdB = Generic_Command_Zones__CmdB()
	CmdC = Generic_Command_Zones__CmdC()
	Limit = Generic_Command_Zones__Limit()


class DCS_Elementary_Zones__Limit:
	Seg = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]
	X = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]
	Direction = [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]


class DCS_Elementary_Zones:
	Name = 1
	SubsetName = 2
	AtsId = 3
	ObjectId = 4
	Limit = DCS_Elementary_Zones__Limit()


class TSR_Possible_Speeds:
	Name = 1
	Speed = 2


class TD_Subsets__Td:
	Cell = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]


class TD_Subsets:
	Name = 1
	Id = 2
	PassengerTrainTypeName = 3
	Td = TD_Subsets__Td()


class Unwanted_Coupling_Area__Limit:
	Seg = [3, 6, 9, 12, 15]
	X = [4, 7, 10, 13, 16]
	Direction = [5, 8, 11, 14, 17]


class Unwanted_Coupling_Area:
	Name = 1
	Direction = 2
	Limit = Unwanted_Coupling_Area__Limit()


class Cruising_Zones__CruisingZone:
	Seg = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
	X = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]
	Direction = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]


class Cruising_Zones:
	CruisingZoneName = 1
	OriginPlatform = 2
	DestinationPlatform = 3
	CruisingZone = Cruising_Zones__CruisingZone()


class Passage_Detector:
	Name = 1
	Seg = 2
	X = 3


class Parking_Place:
	Name = 1
	AtsId = 2
	ParkingPlaceLimit1 = 3
	ExternalLocMemorizationOffsetLimit1 = 4
	ParkingPlaceLimit2 = 5
	ExternalLocMemorizationOffsetLimit2 = 6
	SignalName1 = 7
	SignalName2 = 8
	SignalName3 = 9
	SignalName4 = 10
	SignalName5 = 11


class StaticTag_Group__TagList:
	Tag = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


class StaticTag_Group:
	Name = 1
	Id = 2
	TagList = StaticTag_Group__TagList()


class Odometric_Zones__OdometricZone:
	Seg = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32]
	X = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33]
	Direction = [7, 10, 13, 16, 19, 22, 25, 28, 31, 34]


class Odometric_Zones:
	Name = 1
	Level = 2
	CurvatureRadius = 3
	Banking = 4
	OdometricZone = Odometric_Zones__OdometricZone()


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
	Coupling_area = Coupling_area()
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
	Odometric_Zones = Odometric_Zones()
