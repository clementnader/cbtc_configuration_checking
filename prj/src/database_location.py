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


# --- Main projects --- #
# PROJECT_NAME = Projects.Ankara_L1
# PROJECT_NAME = Projects.Ankara_L2
# PROJECT_NAME = Projects.Brussels
# PROJECT_NAME = Projects.Copenhagen  # TODO: Survey: update floodgate verification as for platform
# PROJECT_NAME = Projects.Glasgow
# PROJECT_NAME = Projects.Lima
# PROJECT_NAME = Projects.Milan
# PROJECT_NAME = Projects.Riyadh
PROJECT_NAME = Projects.Thessaloniki

# --- USA --- #
# PROJECT_NAME = Projects.Baltimore
# PROJECT_NAME = Projects.BART
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


class ProjectDatabaseLoc:
    class ControlTablesLoc:
        line = r""  # Main Line
        cmc = r""   # CMC: Control and Maintenance Center
        cmc2 = r""  # if CMC is split in two parts

    class SurveyLoc:
        survey_addr = None
        survey_sheet = None
        all_sheets = None
        start_row = None
        ref_col = None
        type_col = None
        track_col = None
        survey_kp_col = None

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

    def __init__(self, project_name: str):

        # ------------------------------- Ankara_L1 -------------------------------#
        if project_name == Projects.Ankara_L1:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L1\ANK_L1_C_D470_V12_05_RC2\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Ank\ANK_L1\ANK_L1_C_D470_V12_05_RC2\DC_PAR.xls"
            # self.block_def = r"C:\Users\naderc\Desktop\Ank\ANK_L1\circuitdevoie.xlsx"
            # -- Survey -- #
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
            # self.block_def = r"C:\Users\naderc\Desktop\Ank\ANK_L2\CIRCUIT_DE_VOIE.xls"
            # -- Survey -- #
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
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B_R3\DC_SYS_old.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B_R5\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B_R5\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\BXL\BXL_C_D470_72_01_03_V07_P1B_R5\C64_D413\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\BXL\BXL_C11_D470_72_01_03_V07_P1B_R4"
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
            self.control_tables_route.line = (r"C:\Users\naderc\Desktop\BXL\control tables new"
                                              r"\90000536.L02.FR-BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES "
                                              r"ITINÉRAIRES_FR_rev01.00_ERASME-ANTENNA LINE.pdf")
            self.control_tables_route.cmc = (r"C:\Users\naderc\Desktop\BXL\Control Tables"
                                             r"\BXL_IXL_LISTE DES ITINÉRAIRES + PARAMÈTRES DES ITINÉRAIRES_FR_"
                                             r"rev01.00_ERASME DEPOT.pdf")
            # self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\BXL\Control Tables"
            #                                     r"\BXL_IXL_LISTE DES OVERLAP + PARAMETRES OVERLAP_FR_"
            #                                     r"rev00.02_ERASME-ANTENNA LINE.pdf")
            self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\BXL\control tables new"
                                                r"\90000537.L02.FR-BXL_IXL_ LISTE DES OVERLAP + PARAMÈTRES "
                                                r"OVERLAP_FR_rev01.00_ERASME-ANTENNA LINE.pdf")
            self.control_tables_overlap.cmc = (r"C:\Users\naderc\Desktop\BXL\Control Tables"
                                               r"\BXL_IXL_LISTE DES OVERLAP + PARAMETRES OVERLAP_FR_"
                                               r"rev01.00_ERASME DEPOT.pdf")

        # ------------------------------- Copenhagen -------------------------------#
        elif project_name == Projects.Copenhagen:
            # self.dc_sys_addr_old = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_15_00_RC5\DC_SYS.xls"
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_06_06_01_V04_R3\DC_SYS_R3.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_06_06_01_V04_R3\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\KCR\KCR_C_D470_06_06_01_V04_R3\C64_D413\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\KCR\KCR_C11_D470_06_06_01_V04_R3"
            # self.block_def = r"C:\Users\naderc\Desktop\KCR\CIRCUIT_DE_VOIE_patch_12_01_RC2.xls"
            # -- Survey -- #
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
            self.control_tables_route.cmc = (r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES"
                                             r"\CR-ASTS-045017-11.00-ATT001- CMC CT Routes.pdf")
            self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES"
                                                r"\CR-ASTS-045009-07.00-ATT001- Line CT Overlap.pdf")
            self.control_tables_overlap.cmc = (r"C:\Users\naderc\Desktop\KCR\CONTROL TABLES"
                                               r"\CR-ASTS-045019-09.00 ATC CMC Control Tables Overlap.pdf")

        # ------------------------------- Glasgow -------------------------------#
        elif project_name == Projects.Glasgow:
            iatp = True
            if iatp:
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V05\DC_SYS_IATPM.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V05\DC_PAR.xls"
                self.dc_bop_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_06_06_01_V05\C64_D413\DC_BOP.xls"
                self.kit_c11_dir = r"C:\Users\naderc\Desktop\Glasgow\GW_C11_D470_06_06_01_V05"
            else:
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_07_03_01_V01\DC_SYS.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\Glasgow\GW_C_D470_07_03_01_V01\DC_PAR.xls"
            # -- Survey -- #
            # self.survey_loc.survey_addr = [r"C:\Users\naderc\Desktop\Glasgow\SURVEY"
            #                                r"\2022_03_11_Inner_Circle_Features.xlsx",
            #                                r"C:\Users\naderc\Desktop\Glasgow\SURVEY"
            #                                r"\2022_03_11_Outer_Circle_Features.xlsx"]
            # self.survey_loc.survey_sheet = [r"Inner Circle", r"Outer Circle"]
            # self.survey_loc.all_sheets = [False, False]
            # self.survey_loc.start_row = [2, 2]
            # self.survey_loc.ref_col = [1, 1]
            # self.survey_loc.type_col = [2, 2]
            # self.survey_loc.track_col = [3, 3]
            # self.survey_loc.survey_kp_col = [4, 4]
            self.survey_loc.survey_addr = (r"C:\Users\naderc\Desktop\Glasgow"
                                           r"\2023_02_20 Survey Data and Input Sheet.xlsx")
            self.survey_loc.survey_sheet = r"GW_ML_survey_inputs"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 2
            self.survey_loc.track_col = 3
            self.survey_loc.survey_kp_col = 4
            # -- Control Tables -- #
            self.control_tables_route.line = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables"
                                              r"\GWISIGIXL0180-01.00 - ATT002_Circles Control tables_"
                                              r"Rev00-3-86-Routes.pdf")
            self.control_tables_route.cmc = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables"
                                             r"\GWISIGIXL0180-01.00 - ATT001_Depot Control tables_"
                                             r"Rev00-3-81-Routes.pdf")
            self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables"
                                                r"\GWISIGIXL0180-01.00 - ATT002_Circles Control tables_"
                                                r"Rev00-173-236-Overlap.pdf")
            self.control_tables_overlap.cmc = (r"C:\Users\naderc\Desktop\Glasgow\Control Tables"
                                               r"\GWISIGIXL0180-01.00 - ATT001_Depot Control tables_"
                                               r"Rev00-162-173-Overlap.pdf")

        # ------------------------------- Lima -------------------------------#
        elif project_name == Projects.Lima:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\LIMA\ML2_C_D470_DB0402RC1\DC_SYS_0402RC1.xls"
            # -- Survey -- #
            self.survey_loc.survey_addr = r"C:\Users\naderc\Desktop\LIMA\Objects_List - v3 Rev 01.xlsx"
            self.survey_loc.survey_sheet = r"Object List"
            self.survey_loc.all_sheets = False
            self.survey_loc.start_row = 2
            self.survey_loc.ref_col = 1
            self.survey_loc.type_col = 3
            self.survey_loc.track_col = 4
            self.survey_loc.survey_kp_col = 7

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
                                                  r"\M4-ST00PGRE-55047_00.04_Allegato_1-5-168 - LINE - Routes.pdf")
                self.control_tables_route.cmc = (r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\CONTROL TABLES"
                                                 r"\M4-ST00PGRE-55047_00.04_Allegato_1-461-646 - DEPOT - Routes.pdf")
                self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\CONTROL TABLES"
                                                    r"\M4-ST00PGRE-55047_00.04_Allegato_1-341-397 - LINE - Overlap.pdf")
                self.control_tables_overlap.cmc = (r"C:\Users\naderc\Desktop\ML4\3. DEP_LN01\CONTROL TABLES"
                                                   r"\M4-ST00PGRE-55047_00.04_Allegato_1-833-847 - DEPOT - Overlap.pdf")
            # WHOLE
            elif ver == "WHOLE":
                self.dc_sys_addr = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C_D470_V03_01_RC3\ML4_DC_SYS.xls"
                self.dc_par_addr = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C_D470_V03_01_RC3\ML4_DC_PAR.xls"
                self.dc_bop_addr = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C_D470_V03_01_RC3\DC_BOP.xls"
                self.kit_c11_dir = r"C:\Users\naderc\Desktop\ML4\4. WHOLE\ML4_WH_C11_D470_06_06_02_V04"
                # -- Survey -- #
                self.survey_loc.survey_addr = [r"C:\Users\naderc\Desktop\ML4\SURVEY"
                                               r"\(ML4) LN04_Object_List_01.xlsx",
                                               r"C:\Users\naderc\Desktop\ML4\SURVEY"
                                               r"\ML4_TF2 REPORT OBJECT_AFS_REV_5.1.xlsx",
                                               r"C:\Users\naderc\Desktop\ML4\SURVEY"
                                               r"\ML4_TF3 AFS DB integration template.xlsx",
                                               r"C:\Users\naderc\Desktop\ML4\SURVEY"
                                               r"\ml4 tki_depot_ln01_object.xlsx",
                                               r"C:\Users\naderc\Desktop\ML4\SURVEY"
                                               r"\ML4_LN02 - Coni Zugna to Sforza AFS Object List.xlsx"]
                self.survey_loc.all_sheets = [False, False, False, False, False]
                self.survey_loc.survey_sheet = ["Foglio1", "Foglio1", "Import", "ML4 TKI_Depot_LN01_Object_List_",
                                                "AFS Coni Zugna to Sforza"]
                self.survey_loc.start_row = [4, 3, 3, 2, 2]
                self.survey_loc.ref_col = [2, 2, 1, 1, 1]
                self.survey_loc.type_col = [1, 1, 2, 2, 2]
                self.survey_loc.track_col = [4, 4, 3, 3, 3]
                self.survey_loc.survey_kp_col = [7, 7, 4, 5, 5]
                # -- Control Tables -- #
                self.control_tables_route.line = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE"
                                                  r"\M4-ST00PGRE-55047_02.00_Allegato_1 WHOLE-6-167-Routes.pdf")
                self.control_tables_route.cmc = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE"
                                                 r"\M4-ST00PGRE-55047_02.00_Allegato_1 WHOLE-378-535-Routes.pdf")
                self.control_tables_route.cmc2 = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE"
                                                  r"\M4-ST00PGRE-55047_02.00_Allegato_1 WHOLE-814-955-Routes.pdf")
                self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE"
                                                    r"\M4-ST00PGRE-55047_02.00_Allegato_1 WHOLE-330-338-Overlap.pdf")
                self.control_tables_overlap.cmc = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE"
                                                   r"\M4-ST00PGRE-55047_02.00_Allegato_1 WHOLE-690-747-Overlap.pdf")
                self.control_tables_overlap.cmc2 = (r"C:\Users\naderc\Desktop\ML4\Control Tables\WHOLE"
                                                    r"\M4-ST00PGRE-55047_02.00_Allegato_1 WHOLE-1098-1144-Overlap.pdf")

        # ------------------------------- Riyadh -------------------------------#
        elif project_name == Projects.Riyadh:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_SYS.xls"
            self.dc_par_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\Riyadh\RL3_C_D470_09_01_RC1\DC_BOP_old.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\Riyadh\RL3_C11_D470_06_06_00_V07"
            self.kit_c121_d470_dir = r"C:\Users\naderc\Desktop\Riyadh\RL3_C121_D470_06_06_00_V04_20230327_165125"
            # self.block_def = r"C:\Users\naderc\Desktop\Riyadh\CIRCUIT_DE_VOIE RL3.xls"
            # -- Survey -- #
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
            self.control_tables_route.cmc = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                             r"\WEST DEPOT - CONTROL TABLES (AUTOMATIC AREA)"
                                             r"\Appendix B_Routes.pdf")
            self.control_tables_route.cmc2 = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                              r"\EAST DEPOT - CONTROL TABLES (AUTOMATIC AREA)"
                                              r"\Appendix B_Routes.pdf")
            self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                                r"\MAIN LINE - CONTROL TABLES"
                                                r"\Appendix E_Overlap.pdf")
            self.control_tables_overlap.cmc = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                               r"\WEST DEPOT - CONTROL TABLES (AUTOMATIC AREA)"
                                               r"\Appendix E_Overlap.pdf")
            self.control_tables_overlap.cmc2 = (r"C:\Users\naderc\Desktop\Riyadh\Control Tables"
                                                r"\EAST DEPOT - CONTROL TABLES (AUTOMATIC AREA)"
                                                r"\Appendix E_Overlap.pdf")

        # ------------------------------- Thessaloniki -------------------------------#
        elif project_name == Projects.Thessaloniki:
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V02_RC3\DC_SYS_old.xls"
            # self.dc_sys_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V03_RC3\DC_SYS.xls"
            self.dc_sys_addr = (r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V03_RC3"
                                r"\DC_SYS_patched_sw_block_locking_area.xls")
            self.dc_par_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V03_RC3\DC_PAR.xls"
            self.dc_bop_addr = r"C:\Users\naderc\Desktop\TSK\TSK_C_D470_07_03_03_V03_RC3\DC_BOP.xls"
            self.kit_c11_dir = r"C:\Users\naderc\Desktop\TSK\TSK_C11_D470_07_03_03_V06"
            self.kit_c121_d470_dir = r"C:\Users\naderc\Desktop\TSK\TSK_C121_D470_07_03_03_V04\20230619_122002\ZC\Export"
            # -- Survey -- #
            self.survey_loc.survey_addr = [r"C:\Users\naderc\Desktop\TSK\SURVEY\1G00LV615R808A_EN_Annex_A.xlsx",
                                           r"C:\Users\naderc\Desktop\TSK\SURVEY\1G00LV615R808A_EN_Annex_B.xls",
                                           r"C:\Users\naderc\Desktop\TSK\SURVEY\1G00LV615R808A_EN_Annex_C.xlsx"]
            self.survey_loc.survey_sheet = [r"TSK_Object_list_310720_ro", r"TSK_Object_list_REV.3", r"Φύλλο1"]
            self.survey_loc.all_sheets = [False, False, False]
            self.survey_loc.start_row = [2, 2, 3]
            self.survey_loc.ref_col = [1, 1, 13]
            self.survey_loc.type_col = [2, 2, 14]
            self.survey_loc.track_col = [3, 3, 15]
            self.survey_loc.survey_kp_col = [7, 7, 17]
            # -- Control Tables -- #
            self.control_tables_route.line = (r"C:\Users\naderc\Desktop\TSK\Control Tables rev 04.00"
                                              r"\1G00LV601R721B_EN_ANNEX_B - IXL MAIN LINE CONTROL TABLES - "
                                              r"Routes.pdf")
            self.control_tables_route.cmc = (r"C:\Users\naderc\Desktop\TSK\Control Tables rev 04.00"
                                             r"\1G00LV601R722B_EN_ANNEX_B - IXL PYLEA DEPOT CONTROL TABLES - "
                                             r"Routes.pdf")
            self.control_tables_overlap.line = (r"C:\Users\naderc\Desktop\TSK\Control Tables rev 04.00"
                                                r"\1G00LV601R721B_EN_ANNEX_D - IXL MAIN LINE CONTROL TABLES - "
                                                r"Overlaps.pdf")
            self.control_tables_overlap.cmc = (r"C:\Users\naderc\Desktop\TSK\Control Tables rev 04.00"
                                               r"\1G00LV601R722B_EN_ANNEX_D - IXL PYLEA DEPOT CONTROL TABLES - "
                                               r"Overlaps.pdf")

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------- Other projects -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

        # --- USA --- #

        # ------------------------------- Baltimore -------------------------------#
        elif project_name == Projects.Baltimore:
            self.dc_sys_addr = r"C:\Users\naderc\Desktop\USA\Baltimore\DC_SYS MTAB 721 ++.xls"

        # ------------------------------- BART -------------------------------#
        elif project_name == Projects.BART:
            self.dc_sys_addr = (r"C:\Users\naderc\Desktop\USA\BART"
                                r"\BART_V2.3.0_SYS_1-DC_SYS-DRAGON_2.1.1 (RefSys 7.2.1.1).xls")

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
            self.block_def = r"C:\Users\naderc\Desktop\INDIA\NOIDA\CIRCUIT_DE_VOIE.xls"
            # -- Survey -- #
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


DATABASE_LOC = ProjectDatabaseLoc(PROJECT_NAME)
