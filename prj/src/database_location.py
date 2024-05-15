#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["Projects", "PROJECT_NAME", "DATABASE_LOC"]


class Projects:
    Ankara_L1 = "Ankara_L1"
    Ankara_L2 = "Ankara_L2"
    Brussels = "Brussels"
    Copenhagen = "Copenhagen"
    Glasgow = "Glasgow"
    Lima = "Lima"
    Milan = "Milan"
    Riyadh = "Riyadh"
    Thessaloniki = "Thessaloniki"

    Baltimore = "Baltimore"
    BART = "BART"
    Hurontario = "Hurontario"
    MSH = "MSH"
    KMRC = "KMRC"
    NMML1 = "NMML1"
    Noida = "Noida"
    Shenyang = "Shenyang"
    Wenzhou = "Wenzhou"
    Mock_up = "Mock-up"
    Mock_up_2 = "Mock-up 2"
    Mock_up_3 = "Mock-up 3"
    Mock_up_4 = "Mock-up 4"
    Mock_up_5 = "Mock-up 5"


# --- Main projects --- #
# PROJECT_NAME = Projects.Ankara_L1
# PROJECT_NAME = Projects.Ankara_L2
# PROJECT_NAME = Projects.Brussels
# PROJECT_NAME = Projects.Copenhagen
# PROJECT_NAME = Projects.Glasgow
# PROJECT_NAME = Projects.Lima
# PROJECT_NAME = Projects.Milan
# PROJECT_NAME = Projects.Riyadh
PROJECT_NAME = Projects.Thessaloniki

# --- USA --- #
# PROJECT_NAME = Projects.Baltimore
# PROJECT_NAME = Projects.BART
# PROJECT_NAME = Projects.Hurontario
# PROJECT_NAME = Projects.MSH
# --- India --- #
# PROJECT_NAME = Projects.KMRC
# PROJECT_NAME = Projects.NMML1
# PROJECT_NAME = Projects.Noida
# --- China --- #
# PROJECT_NAME = Projects.Shenyang
# PROJECT_NAME = Projects.Wenzhou
# --- Mock-up --- #
# PROJECT_NAME = Projects.Mock_up
# PROJECT_NAME = Projects.Mock_up_2
# PROJECT_NAME = Projects.Mock_up_3
# PROJECT_NAME = Projects.Mock_up_4
# PROJECT_NAME = Projects.Mock_up_5


class ProjectDatabaseLoc:
    class ControlTablesLoc:
        line = r""  # Main Line
        depot = r""   # Depot
        depot2 = r""  # if Depot is split in two parts

    class SurveyLoc:
        survey_addr = None
        survey_sheet = None
        all_sheets = None
        start_row = None
        ref_col = None
        type_col = None
        track_col = None
        survey_kp_col = None

    class IxlApz:
        ixl_apz_file = None
        ixl_apz_sheet_name = None
        start_line = None
        sig_column = None
        apz_start_column = None
        apz_nb_columns = None

    cctool_oo_schema = r""
    dc_sys_addr = r""
    dc_sys_addr_old = r""
    dc_par_addr = r""
    dc_bop_addr = r""
    block_def = None
    survey_loc = SurveyLoc()
    kit_c11_dir = r""
    kit_c121_d470_dir = r""
    control_tables_route = ControlTablesLoc()
    control_tables_overlap = ControlTablesLoc()
    ixl_apz = IxlApz()

    def __init__(self, project_name: str):

        # ------------------------------- Ankara_L1 -------------------------------#
        if project_name == Projects.Ankara_L1:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L1\ANK_L1_C_D470_V12_05_RC2\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L1\ANK_L1_C_D470_V12_05_RC2\DC_PAR.xls"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\Ank\ANK_L1\circuitdevoie.xlsx"
            self.survey_loc.survey_addr = (r"C:\Users\naderc\Desktop\Ank\SURVEY"
                                           r"\ANK_L1_C_D932_14_00_RC1.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # ------------------------------- Ankara_L2 -------------------------------#
        if project_name == Projects.Ankara_L2:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L2\ANK_L2_C_D470_V06_00_RC4\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L2\ANK_L2_C_D470_V06_00_RC4\DC_PAR.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\Ank\ANK_L2\ANK_L2_C11_D470_06_05_03_V07"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\Ank\ANK_L2\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = [r"C:\Users\naderc\Desktop\Ank\SURVEY\ANK_L2_C_D932_01_00_RC2.xlsx",
                                           r"C:\Users\naderc\Desktop\Ank\SURVEY"
                                           r"\Metro_gzrgh_KM_SON_BufferAdded_FoulingPadded_JointAdded_rev01.xlsx"]
            self.survey_loc.survey_sheet = [r"Result Final", r"Survey_Template"]
            self.survey_loc.all_sheets = [False, False]
            self.survey_loc.start_row = [2, 2]
            self.survey_loc.ref_col = [1, 1]
            self.survey_loc.type_col = [4, 2]
            self.survey_loc.track_col = [2, 3]
            self.survey_loc.survey_kp_col = [3, 5]

        # ------------------------------- Brussels -------------------------------#
        elif project_name == Projects.Brussels:
            phase_2 = False
            if not phase_2:
                # self.dc_sys_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B_R3\DC_SYS_old.xls"
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B_R4\DC_SYS.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B_R4\DC_PAR.xls"
                self.dc_bop_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B_R4\C64_D413\DC_BOP.xls"
                self.kit_c11_dir = r"C:\Users\naderc\Desktop\BXL\BXL_C11_D470_72_01_03_V07_P1B_R4"
            else:
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\BXL\PHASE 2\BXL_C_D470_72_02_01_V01_P1B2\DC_SYS.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\BXL\PHASE 2\BXL_C_D470_72_02_01_V01_P1B2\DC_PAR.xls"
            # -- Survey -- #
            self.survey_loc.survey_addr = [r"C:\Users\naderc\Desktop\BXL\BXL_Photobook_survey.xlsx",
                                           r"C:\Users\naderc\Desktop\BXL\Project_BXL_survey 05-10-2023.xlsx"]
            self.survey_loc.survey_sheet = [r"PhotoBook", r"AFS_DEP_ML_DEF_05.10.23REV_1"]
            self.survey_loc.all_sheets = [False, False]
            self.survey_loc.start_row = [2, 13]
            self.survey_loc.ref_col = [1, 1]
            self.survey_loc.type_col = [2, 2]
            self.survey_loc.track_col = [3, 3]
            self.survey_loc.survey_kp_col = [4, 11]
            # -- Control Tables -- #
            # self.control_tables_route.line = (r"C:\Users\naderc\Desktop\BXL\Control Tables"
            #                                   r"\BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_"
            #                                   r"rev00.02_ERASME-ANTENNA LINE.pdf")
            # self.control_tables_route.line = (r"C:\Users\naderc\Desktop\BXL\control tables new"
            #                                   r"\90000536.L02.FR-BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES "
            #                                   r"ITINÉRAIRES_FR_rev01.00_ERASME-ANTENNA LINE.pdf")
            # self.control_tables_route.depot = (r"C:\Users\naderc\Desktop\BXL\Control Tables"
            #                                  r"\BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_"
            #                                  r"rev01.00_ERASME DEPOT.pdf")
            self.control_tables_route.line = (r"C:\Users\naderc\Desktop\BXL\Control Tables rev 02.00\MAIN LINE"
                                              r"\90000536.L02.FR-BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES "
                                              r"ITINÉRAIRES_FR_rev02.00.pdf")
            self.control_tables_route.depot = (r"C:\Users\naderc\Desktop\BXL\Control Tables rev 02.00\DEPOT"
                                               r"\90000528_L02_FR-BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES "
                                               r"ITINÉRAIRES_FR_rev02_00.pdf")
            # self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\BXL\Control Tables"
            #                                     r"\BXL_IXL_LISTE DES OVERLAP + PARAMETRES OVERLAP_FR_"
            #                                     r"rev00.02_ERASME-ANTENNA LINE.pdf")
            # self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\BXL\control tables new"
            #                                     r"\90000537.L02.FR-BXL_IXL_ LISTE DES OVERLAP + PARAMÈTRES "
            #                                     r"OVERLAP_FR_rev01.00_ERASME-ANTENNA LINE.pdf")
            # self.control_tables_overlap.depot = (r"C:\Users\naderc\Desktop\BXL\Control Tables"
            #                                    r"\BXL_IXL_LISTE DES OVERLAP + PARAMETRES OVERLAP_FR_"
            #                                    r"rev01.00_ERASME DEPOT.pdf")
            self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\BXL\Control Tables rev 02.00\MAIN LINE"
                                                r"\90000537.L02.FR-BXL_IXL_ LISTE DES OVERLAP + PARAMÈTRES "
                                                r"OVERLAP_FR_rev02.00.pdf")
            self.control_tables_overlap.depot = (r"C:\Users\naderc\Desktop\BXL\Control Tables rev 02.00\DEPOT"
                                                 r"\90000530.L02.FR-BXL_IXL_ LISTE DES OVERLAP + PARAMETRES "
                                                 r"OVERLAP_FR_rev01.00.pdf")

        # ------------------------------- Copenhagen -------------------------------#
        elif project_name == Projects.Copenhagen:
            # self.dc_sys_addr_old = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_15_00_RC5\DC_SYS.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_06_06_01_V04_R3\DC_SYS_R3.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_06_06_01_V04_R3\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_06_06_01_V04_R3\C64_D413\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\KCR\KCR_C11_D470_06_06_01_V04_R3"
            # -- Survey -- #
            # self.block_def = r"C:\Users\naderc\Desktop\KCR\CIRCUIT_DE_VOIE_patch_12_01_RC2.xls"
            self.survey_loc.survey_addr = [r"C:\Users\naderc\Desktop\KCR"
                                           r"\CR-ASTS-042189 - 15.00_ATT002 - ATC- KCR C_D932 - "
                                           r"Field Survey report.xlsx",
                                           r"C:\Users\naderc\Desktop\KCR"
                                           r"\AFS_Project_KCR_Sydhavn_survey_eng table_30.08.23.xlsx"]
            self.survey_loc.survey_sheet = [r"Result Final", r"D932"]
            self.survey_loc.all_sheets = [False, False]
            self.survey_loc.start_row = [2, 3]
            self.survey_loc.ref_col = [1, 1]
            self.survey_loc.type_col = [4, 2]
            self.survey_loc.track_col = [2, 3]
            self.survey_loc.survey_kp_col = [3, 5]
            # -- Control Tables -- #
            self.control_tables_route.line = (r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES"
                                              r"\CR-ASTS-045007-11.00-ATT001- Line CT Routes.pdf")
            self.control_tables_route.depot = (r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES"
                                               r"\CR-ASTS-045017-11.00-ATT001- CMC CT Routes.pdf")
            self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES"
                                                r"\CR-ASTS-045009-07.00-ATT001- Line CT Overlap.pdf")
            self.control_tables_overlap.depot = (r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES"
                                                 r"\CR-ASTS-045019-09.00 ATC CMC Control Tables Overlap.pdf")
            # -- IXL Approach Zone -- #
            self.ixl_apz.ixl_apz_file = (r"C:\Users\naderc\Desktop\KCR\CR-ASTS-GEN=Gen-PS=ATC=GEN-IFM-ICD-042155_14.00"
                                         r"#ATT004XLSX - ATC - C12_D404  IXL APZ Rev01.xlsx")
            self.ixl_apz.ixl_apz_sheet_name = r"IXL APZ"
            self.ixl_apz.start_line = 2
            self.ixl_apz.sig_column = 'A'
            self.ixl_apz.apz_start_column = 2
            self.ixl_apz.apz_nb_columns = 5

        # ------------------------------- Glasgow -------------------------------#
        elif project_name == Projects.Glasgow:
            iatp = False
            if iatp:
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V05\DC_SYS_IATPM.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V05\DC_PAR.xls"
                self.dc_bop_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V05\C64_D413\DC_BOP.xls"
                self.kit_c11_dir = r"C:\Users\naderc\Desktop\Glasgow\GW_C11_D470_06_06_01_V05"
                # -- Control Tables -- #
                self.control_tables_route.line = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables\IATP"
                                                  r"\GWISIGIXL0180-01.00 - ATT002_Circles Control tables_"
                                                  r"Rev00-3-86-Routes.pdf")
                self.control_tables_route.depot = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables\IATP"
                                                   r"\GWISIGIXL0180-01.00 - ATT001_Depot Control tables_"
                                                   r"Rev00-3-81-Routes.pdf")
                self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables\IATP"
                                                    r"\GWISIGIXL0180-01.00 - ATT002_Circles Control tables_"
                                                    r"Rev00-173-236-Overlap.pdf")
                self.control_tables_overlap.depot = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables\IATP"
                                                     r"\GWISIGIXL0180-01.00 - ATT001_Depot Control tables_"
                                                     r"Rev00-162-173-Overlap.pdf")
            else:
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_07_03_03_V02\DC_SYS.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_07_03_03_V02\DC_PAR.xls"
                self.dc_bop_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_07_03_03_V02\C64_D413\DC_BOP.xls"
                # -- Control Tables -- #
                self.control_tables_route.line = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables\CBTC"
                                                  r"\GWISIGIXL0400-00.00-ATT002 - Appendix B_Routes_Rev00.pdf")
                self.control_tables_route.depot = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables\CBTC"
                                                   r"\GWISIGIXL0401-00.00-ATT002 - Appendix L_Routes_Rev00.pdf")
                self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables\CBTC"
                                                    r"\GWISIGIXL0400-00.00-ATT006 - Appendix F_Overlap_Rev00.pdf")
            # -- Survey -- #
            self.survey_loc.survey_addr = (r"C:\Users\naderc\Desktop\Glasgow\SURVEY"
                                           r"\2024_03_16 Survey Data and Input Sheet_FCB amendments.xlsx")
            self.survey_loc.survey_sheet = r"GW_ML_survey_inputs"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 2
            self.survey_loc.track_col = 3
            self.survey_loc.survey_kp_col = 5

        # ------------------------------- Lima -------------------------------#
        elif project_name == Projects.Lima:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\LIMA\ML2_C_D470_DB0402RC1\DC_SYS_0402RC1.xls"
            # -- Survey -- #
            self.survey_loc.survey_addr = r"C:\Users\naderc\Desktop\LIMA\Objects_List - v3 Rev 01.xlsx"
            self.survey_loc.survey_sheet = r"Dico"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 8
            self.survey_loc.track_col = 7
            self.survey_loc.survey_kp_col = 10

        # ------------------------------- Milan -------------------------------#
        elif project_name == Projects.Milan:
            # ver = "TF3"
            # ver = "DEPOT + LN01"
            ver = "WHOLE"
            # TF3
            if ver == "TF3":
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\ML4\2. TF3\ML4_TF3_C_D470_01_02_RC2\ML4_DC_SYS.xls"
                # self.dc_sys_addr_old = r"C:\Users\naderc\Desktop\ML4\2. TF3\ML4_DC_SYS_01_01_RC3.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\ML4\2. TF3\ML4_TF3_C_D470_01_02_RC2\ML4_DC_PAR.xls"
                self.dc_bop_addr = r"C:\Users\naderc\Desktop\ML4\2. TF3\ML4_TF3_C_D470_01_02_RC2\DC_BOP.xls"
                self.kit_c11_dir = r"C:\Users\naderc\Desktop\ML4\2. TF3\ML4_TF3_C11_D470_06_05_05_V04"
                # -- Control Tables -- #
                self.control_tables_route.line = (r"C:\Users\naderc\Desktop\ML4\2. TF3\Control Tables"
                                                  r"\M4-ST00PGRE-55634_01.00_Allegato_1-TF3-5-144 - Routes.pdf")
                self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\ML4\2. TF3\Control Tables"
                                                    r"\M4-ST00PGRE-55634_01.00_Allegato_1-TF3-285-328 - Overlap.pdf")
            # DEPOT + LN01
            elif ver == "DEPOT + LN01":
                self.dc_sys_addr = (r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\ML4_DEP_LN01_C_D470_02_00_RC5"
                                    r"\ML4_DC_SYS.xls")
                self.dc_par_addr = (r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\ML4_DEP_LN01_C_D470_02_00_RC5"
                                    r"\ML4_DC_PAR.xls")
                self.dc_bop_addr = (r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\ML4_DEP_LN01_C_D470_02_00_RC5"
                                    r"\DC_BOP.xls")
                self.kit_c11_dir = r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\ML4_DEP_LN01_C11_D470_06_06_02_V02"
                # -- Control Tables -- #
                self.control_tables_route.line = (r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\CONTROL TABLES"
                                                  r"\M4-ST00PGRE-55047_00.04_Allegato_1-5-168"
                                                  r" - LINE - Routes.pdf")
                self.control_tables_route.depot = (r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\CONTROL TABLES"
                                                   r"\M4-ST00PGRE-55047_00.04_Allegato_1-461-646"
                                                   r" - DEPOT - Routes.pdf")
                self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\CONTROL TABLES"
                                                    r"\M4-ST00PGRE-55047_00.04_Allegato_1-341-397"
                                                    r" - LINE - Overlap.pdf")
                self.control_tables_overlap.depot = (r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\CONTROL TABLES"
                                                     r"\M4-ST00PGRE-55047_00.04_Allegato_1-833-847"
                                                     r" - DEPOT - Overlap.pdf")
            # WHOLE
            elif ver == "WHOLE":
                # self.dc_sys_addr = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C_D470_V03_01_RC3\ML4_DC_SYS.xls"
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C_D470_V03_02_RC2\ML4_DC_SYS.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C_D470_V03_02_RC2\ML4_DC_PAR.xls"
                self.dc_bop_addr = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C_D470_V03_02_RC2\DC_BOP.xls"
                self.kit_c11_dir = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C11_D470_06_06_02_V04"
                # -- Survey -- #
                self.survey_loc.survey_addr = [r"C:\Users\naderc\Desktop\ML4\SURVEY"
                                               r"\(ML4) LN04_Object_List_01_return28.03.24.xlsx",
                                               r"C:\Users\naderc\Desktop\ML4\SURVEY"
                                               r"\ML4_TF2 REPORT OBJECT_AFS_REV_5.1.xlsx",
                                               r"C:\Users\naderc\Desktop\ML4\SURVEY"
                                               r"\ML4_TF3 AFS DB integration template.xlsx",
                                               r"C:\Users\naderc\Desktop\ML4\SURVEY"
                                               r"\ml4 tki_depot_ln01_object.xlsx",
                                               r"C:\Users\naderc\Desktop\ML4\SURVEY"
                                               r"\ML4_LN02 - Coni Zugna to Sforza AFS Object List.xlsx"]
                self.survey_loc.all_sheets = [False, False, False, False, False]
                self.survey_loc.survey_sheet = ["Object_List_LN04", "Foglio1", "Import",
                                                "ML4 TKI_Depot_LN01_Object_List_", "AFS Coni Zugna to Sforza"]
                self.survey_loc.start_row = [2, 3, 3, 2, 2]
                self.survey_loc.ref_col = [1, 2, 1, 1, 1]
                self.survey_loc.type_col = [2, 1, 2, 2, 2]
                self.survey_loc.track_col = [3, 4, 3, 3, 3]
                self.survey_loc.survey_kp_col = [5, 7, 4, 5, 5]
                # -- Control Tables -- #
                # self.control_tables_route.line = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev03.00"
                #                                   r"\M4-ST00PGRE-55047_03.00_Allegato_1-6-161.pdf")
                # self.control_tables_route.depot = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev03.00"
                #                                    r"\M4-ST00PGRE-55047_03.00_Allegato_1-370-523.pdf")
                # self.control_tables_route.depot2 = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev03.00"
                #                                     r"\M4-ST00PGRE-55047_03.00_Allegato_1-796-937.pdf")
                # self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev03.00"
                #                                     r"\M4-ST00PGRE-55047_03.00_Allegato_1-318-326.pdf")
                # self.control_tables_overlap.depot = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev03.00"
                #                                      r"\M4-ST00PGRE-55047_03.00_Allegato_1-678-733.pdf")
                # self.control_tables_overlap.depot2 = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev03.00"
                #                                       r"\M4-ST00PGRE-55047_03.00_Allegato_1-1080-1128.pdf")
                self.control_tables_route.line = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev04.00"
                                                  r"\M4-ST00PGRE-55047_04.00_Allegato_1-6-161.pdf")
                self.control_tables_route.depot = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev04.00"
                                                   r"\M4-ST00PGRE-55047_04.00_Allegato_1-370-523.pdf")
                self.control_tables_route.depot2 = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev04.00"
                                                    r"\M4-ST00PGRE-55047_04.00_Allegato_1-796-937.pdf")
                self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev04.00"
                                                    r"\M4-ST00PGRE-55047_04.00_Allegato_1-318-326.pdf")
                self.control_tables_overlap.depot = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev04.00"
                                                     r"\M4-ST00PGRE-55047_04.00_Allegato_1-678-733.pdf")
                self.control_tables_overlap.depot2 = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE rev04.00"
                                                      r"\M4-ST00PGRE-55047_04.00_Allegato_1-1080-1128.pdf")
                # -- IXL Approach Zone -- #
                self.ixl_apz.ixl_apz_file = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_IXL_APZ.xlsx"
                self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
                self.ixl_apz.start_line = 2
                self.ixl_apz.sig_column = 'B'
                self.ixl_apz.apz_start_column = 6
                self.ixl_apz.apz_nb_columns = 3

        # ------------------------------- Riyadh -------------------------------#
        elif project_name == Projects.Riyadh:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_BOP_old.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\Riyadh\RL3_C11_D470_06_06_00_V07"
            self.kit_c121_d470_dir = r"C:\Users\naderc\Desktop\Riyadh\RL3_C121_D470_06_06_00_V04_20230327_165125"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\Riyadh\CIRCUIT_DE_VOIE RL3.xls"
            self.survey_loc.survey_addr = r"C:\Users\naderc\Desktop\Riyadh\Appendix K - RL3_D932_ed14.xls"
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3
            # -- Control Tables -- #
            self.control_tables_route.line = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                              r"\MAIN LINE - CONTROL TABLES"
                                              r"\Appendix B_Routes.pdf")
            self.control_tables_route.depot = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                               r"\WEST DEPOT - CONTROL TABLES (AUTOMATIC AREA)"
                                               r"\Appendix B_Routes.pdf")
            self.control_tables_route.depot2 = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                                r"\EAST DEPOT - CONTROL TABLES (AUTOMATIC AREA)"
                                                r"\Appendix B_Routes.pdf")
            self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                                r"\MAIN LINE - CONTROL TABLES"
                                                r"\Appendix E_Overlap.pdf")
            self.control_tables_overlap.depot = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                                 r"\WEST DEPOT - CONTROL TABLES (AUTOMATIC AREA)"
                                                 r"\Appendix E_Overlap.pdf")
            self.control_tables_overlap.depot2 = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                                  r"\EAST DEPOT - CONTROL TABLES (AUTOMATIC AREA)"
                                                  r"\Appendix E_Overlap.pdf")

        # ------------------------------- Thessaloniki -------------------------------#
        elif project_name == Projects.Thessaloniki:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V03_RC3\DC_SYS.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V04_RC2\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V04_RC2\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V04_RC2\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\TSK\TSK_C11_D470_07_03_03_V06"
            self.kit_c121_d470_dir = r"C:\Users\naderc\Desktop\TSK\TSK_C121_D470_07_03_03_V04\20230619_122002\ZC\Export"
            # -- Survey -- #
            self.survey_loc.survey_addr = [
                r"C:\Users\naderc\Desktop\TSK\SURVEY\1G00LV615R808A_EN_Annex_A.xlsx",
                r"C:\Users\naderc\Desktop\TSK\SURVEY\1G00LV615R808A_EN_Annex_B.xls",
                r"C:\Users\naderc\Desktop\TSK\SURVEY\1G00LV615R808A_EN_Annex_C.xlsx",
                r"C:\Users\naderc\Desktop\TSK\SURVEY\survey_report_TSK_Aktor_additional.xlsx"]
            self.survey_loc.survey_sheet = [r"TSK_Object_list_310720_ro", r"TSK_Object_list_REV.3",
                                            r"Φύλλο1", r"Feuil1"]
            self.survey_loc.all_sheets = [False, False, False, False]
            self.survey_loc.start_row = [2, 2, 3, 2]
            self.survey_loc.ref_col = [1, 1, 13, 2]
            self.survey_loc.type_col = [2, 2, 14, 3]
            self.survey_loc.track_col = [3, 3, 15, 4]
            self.survey_loc.survey_kp_col = [7, 7, 17, 6]
            # -- Control Tables -- #
            self.control_tables_route.line = (r"C:\Users\naderc\Desktop\TSK\Control Tables rev 05.00"
                                              r"\1G00LV601R721B_EN_ANNEX_B.pdf")
            self.control_tables_route.depot = (r"C:\Users\naderc\Desktop\TSK\Control Tables rev 05.00"
                                               r"\1G00LV601R722B_EN_ANNEX_B.pdf")
            self.control_tables_route.depot2 = (r"C:\Users\naderc\Desktop\TSK\Control Tables KLM rev 02.00"
                                                r"\1GE0LV601R721A_EN_ANNEX_B_KLM_rev02.00.pdf")
            self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\TSK\Control Tables rev 05.00"
                                                r"\1G00LV601R721B_EN_ANNEX_D.pdf")
            self.control_tables_overlap.depot = (r"C:\Users\naderc\Desktop\TSK\Control Tables rev 05.00"
                                                 r"\1G00LV601R722B_EN_ANNEX_D.pdf")
            self.control_tables_overlap.depot2 = (r"C:\Users\naderc\Desktop\TSK\Control Tables KLM rev 02.00"
                                                  r"\1GE0LV601R721A_EN_ANNEX_D_KLM_rev02.00.pdf")
            # -- IXL Approach Zone -- #
            self.ixl_apz.ixl_apz_file = r"C:\Users\naderc\Desktop\TSK\TSK_IXL_APZ.xlsx"
            self.ixl_apz.ixl_apz_sheet_name = r"IXL_APZ"
            self.ixl_apz.start_line = 2
            self.ixl_apz.sig_column = 'E'
            self.ixl_apz.apz_start_column = 6
            self.ixl_apz.apz_nb_columns = 2

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------- Other projects -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

        # --- USA --- #

        # ------------------------------- Baltimore -------------------------------#
        elif project_name == Projects.Baltimore:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\Baltimore MTA\MTA_C_D470_02_00_RC10\DC_SYS.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\Baltimore MTA\MTA_C_D470_V_02_01_RC2\DC_SYS.xls"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\USA\Baltimore MTA\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = r"C:\Users\naderc\Desktop\USA\Baltimore MTA\MTA_D932.xlsx"
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # ------------------------------- BART -------------------------------#
        elif project_name == Projects.BART:
            self.dc_sys_addr = (r"C:\Users\naderc\Desktop\USA\BART"
                                r"\BART_V2.3.0_SYS_1-DC_SYS-DRAGON_2.1.1 (RefSys 7.2.1.1).xls")

        # ------------------------------- Hurontario -------------------------------#
        elif project_name == Projects.Hurontario:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\Hurontario\HLR_C_D470_V_7_3_3_0_RC1\DC_SYS.xls"

        # ------------------------------- MSH -------------------------------#
        elif project_name == Projects.MSH:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\MSH\MSH_C_D470_V09_02_RC1\DC_SYS.xls"
            # -- Survey -- #
            self.survey_loc.survey_addr = r"C:\Users\naderc\Desktop\USA\MSH\Topo_V_06_00.xlsx"
            self.survey_loc.survey_sheet = None
            self.survey_loc.all_sheets = True
            self.survey_loc.start_row = 4
            self.survey_loc.ref_col = 2
            self.survey_loc.type_col = 1
            self.survey_loc.track_col = 3
            self.survey_loc.survey_kp_col = 5

        # --- India --- #

        # ------------------------------- KMRC Kolkata -------------------------------#
        elif project_name == Projects.KMRC:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\INDIA\KMRC Kolkata\KMRC_PH2A_C_D470_00_00_RC03\DC_SYS.xls"
            # -- Survey -- #
            self.survey_loc.survey_addr = [r"C:\Users\naderc\Desktop\INDIA\KMRC Kolkata"
                                           r"\KMRC-76054_Rev01_C_D932 - Advanced field survey report.xlsm",
                                           r"C:\Users\naderc\Desktop\INDIA\KMRC Kolkata"
                                           r"\KMRC-26054_Rev09_C_D932 - Advanced field survey report.xlsm"]
            self.survey_loc.survey_sheet = [r"Result Final", r"KMRC-PH2A"]
            self.survey_loc.all_sheets = [False, False]
            self.survey_loc.start_row = [2, 2]
            self.survey_loc.ref_col = [1, 2]
            self.survey_loc.type_col = [4, 6]
            self.survey_loc.track_col = [2, 4]
            self.survey_loc.survey_kp_col = [3, 5]

        # ------------------------------- NMML1 -------------------------------#
        elif project_name == Projects.NMML1:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\INDIA\NMML1\NMML1_PH2_C_D470_00_00_RC5\DC_SYS.xls"
            # -- Survey -- #
            self.survey_loc.survey_addr = (r"C:\Users\naderc\Desktop\INDIA\NMML1"
                                           r"\NMML1_C_D932_Line1_Advanced_field_survey_report.xlsm")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 5

        # ------------------------------- NOIDA -------------------------------#
        elif project_name == Projects.Noida:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\INDIA\NOIDA\NS01_C_D470_10_00_RC1\DC_SYS.xls"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\INDIA\NOIDA\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (r"C:\Users\naderc\Desktop\INDIA\NOIDA"
                                           r"\NS01-L-SIG-9-0001 NS01_C_D932 - Advanced field survey report_06.00.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 3

        # --- China --- #

        # ------------------------------- Shenyang -------------------------------#
        elif project_name == Projects.Shenyang:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\CHINA\CHINA V4\Shenyang\SHYL1_10_00\DC_SYS_SHYL1_10_00.xls"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\CHINA\CHINA V4\Shenyang\SHYL1_10_00\CIRCUIT_DE_VOIE.xls"
            self.survey_loc.survey_addr = (r"C:\Users\naderc\Desktop\CHINA\CHINA V4\Shenyang"
                                           r"\SY_L1_SIG_DB_D932_1409_V3.3_2016_5_11.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # ------------------------------- Wenzhou -------------------------------#
        elif project_name == Projects.Wenzhou:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\CHINA\WENZHOU\WZS1_C_D470_08_01\DC_SYS_0801.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\CHINA\WENZHOU\WZS1_C_D470_08_04\DC_SYS_0804.xls"
            # -- Survey -- #
            self.block_def = r"C:\Users\naderc\Desktop\CHINA\WENZHOU\WZS1_C_D470_08_01\CIRCUIT_DE_VOIE_Corrected.xls"
            self.survey_loc.survey_addr = (r"C:\Users\naderc\Desktop\CHINA\WENZHOU"
                                           r"\WZ_S1P1_SIG_DB_D932_1409_D932_V1.8_modified.xlsx")
            self.survey_loc.survey_sheet = r"Result Final"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 4
            self.survey_loc.track_col = 2
            self.survey_loc.survey_kp_col = 6

        # --- Mock-up --- #

        # ------------------------------- Mock-up -------------------------------#
        elif project_name == Projects.Mock_up:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Mock-Up DC_SYS\DC_SYS_mock-up.xls"

        # ------------------------------- Mock-up 2 -------------------------------#
        elif project_name == Projects.Mock_up_2:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Mock-Up DC_SYS\DC_SYS_mock-up2.xls"

        # ------------------------------- Mock-up 3 -------------------------------#
        elif project_name == Projects.Mock_up_3:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Mock-Up DC_SYS\DC_SYS_mock-up3.xls"

        # ------------------------------- Mock-up 4 -------------------------------#
        elif project_name == Projects.Mock_up_4:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Mock-Up DC_SYS\DC_SYS_mock-up4.xls"

        # ------------------------------- Mock-up 5 -------------------------------#
        elif project_name == Projects.Mock_up_5:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Mock-Up DC_SYS\DC_SYS_mock-up5.xls"


DATABASE_LOC = ProjectDatabaseLoc(PROJECT_NAME)
