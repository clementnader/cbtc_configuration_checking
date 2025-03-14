# CBTC SA Verification Tool

This tool helps with some verifications.

---
## 1. How to use the tool

### 1.1. Inputs to launch the tool

- <ins>**DC_SYS**</ins>: It is an Excel file (.xls) provided in the project database C_D470 containing the configuration of the line (System Configuration Data / Données de Configuration Système).


- <ins>**CCTool-OO Schema**</ins>: It is an Excel file (.xls) provided in §3.1 of Core Data Preparation Format Specification (C_D413-2). It defines the schema of the DC_SYS_CORE file.


- <ins>**DC_PAR**</ins>: It is an Excel file (.xls) provided in the project database C_D470 containing the definition of parameters (Parameters Configuration Data / Données de Configuration Paramétrage).


- <ins>**DC_BOP**</ins>: It is used for the verification of routes and overlaps. It is an Excel file (.xls) provided in the project database C_D470 (directly in the folder or inside subfolder C64_D413) containing the correspondence between the switches position at CBTC level (left/right) and at IXL level (normal/reverse).


- <ins>**Block_Definition**</ins>: It is an optional file useful for the survey verification. It is used to establish the mapping between the block names from DC_SYS and the joint names given in the Survey. It is an Excel file containing the denomination of the block limits (joints and buffers). It has to be formatted as follows:
  - 2 lines of header.
  - 1 column named CDV_ID (usually first column). It contains all blocks names from DC_SYS (sheet CDV).
  - 2 columns LISTE EXTREMITES::LISTE SEGMENT_ID and LISTE EXTREMITES::LISTE EXT_ABS_SEG (usually the second and third columns). They contain respectively the list of limits segments and the list of the limits offsets. The elements of the lists are separated with semicolon ';'.
  - and multiple columns named OBJET EXTREMITE N, with N from 1 to the maximum number of block limits. Each column contains the name of the correspond limit that will appear in the survey.

  The position of the columns is not relevant for the tool but the name of the columns is.

If this file is not provided, the tool will automatically try to find the block limit names (joint names) by mixing the two blocks of the limit (e.g. JOI_AAA_MMM_BBB_NNN for joint between TC_AAA_MMM and TC_BBB_NNN). It will create various name patterns to try to adapt to the different projects.


- <ins>**C11_D470**</ins>: It is the path to the project CC kit C11_D470.


- <ins>**Survey**</ins>: They are Excel files (.xls, .xlsx or .xlsm) containing the surveyed information. As the template can differ, the user needs to specify to the tool:
   - survey_address: the path to the file.
   - survey_sheet: the survey sheet name containing the survey data.
   - all_sheets: boolean (True/False) to specify to use all the sheets of the file to get the survey data.
   - start_row: the first row containing the surveyed information (after the header line).
   - and the different columns for the data the tool will use:
     - reference_column: column containing the name of the surveyed element.
     - type_column: column containing the type of the surveyed element:
       - for switches, type shall be:<br />
       **SWP**, **SWITCH**, **SWITCH_POINT** or **SWITCH POINT**.
       - for platform ends, type shall be:<br />
       **PLATFORM**, **PLATFORM_END**, **PLATFORM END**,<br />
       **PLATFORM_EXTREMITY** or **PLATFORM EXTREMITY**.
       - for OSPs, type shall be:<br />
       **OSP**, **PAE**, **PLATFORM_OSP** or **PLATFORM OSP**.
       - for blocks, type shall be:<br />
       **TC**, **TRACK_CIRCUIT**, **TRACK CIRCUIT**, **TRACK CIRCUITS JOINT**,<br />
       **AXLE COUNTER** or **INSULATED JOINT**.
       - for signals, type shall be:<br />
       **SIG** or **SIGNAL**.
       - for buffers, type shall be:<br />
       **SIGNAL_BUFFER**, **SIGNAL BUFFER**, **BUFFER** or **BS**.
       - for tags, type shall be:<br />
       **BAL**, **BALISE**, **TAG**, **TAGS**,<br />
       **FIXED_BAL**, **FIXED BAL**, **FIXED_BALISE**, **FIXED BALISE**,<br />
       **FIXED_TAG**, **FIXED TAG**, **FIXED_TAGS** or **FIXED TAGS**.
       - for dynamic tags, type shall be:<br />
       **IATPM_BAL**, **IATPM BAL**, **IATPM_BALISE**, **IATPM BALISE**,<br />
       **IATPM_TAG**, **IATPM TAG**, **IATPM_TAGS**, **IATPM TAGS**,<br />
       **IATP_BAL**, **IATP BAL**, **IATP_BALISE**, **IATP BALISE**,<br />
       **IATP_TAG**, **IATP TAG**, **IATP_TAGS** or **IATP TAGS**.
       - for floodgates, type shall be:<br />
       **FLOOD_GATE**, **FLOOD GATE**, **FLOODGATE** or **FLOODGATES**.
     - track_column: column containing the track of the element,
     - surveyed_kp_column: column containing the kilometer point surveyed by a geometer.

Projects can have various survey files. In that case, user have to specify all information for each file separating the various information with a comma ",".


- <ins>**Route Control Tables**</ins>:


- <ins>**Overlap Control Tables**</ins>:


---
### 1.2. Steps to use the tool:

0. A preliminary step to take once in order to install the required Python libraries:
   - Modify the file "**install_python_modules.bat**" to add to the PATH your Python 3.9 executable and modify the PYTHON_EXE variable to match your Python 3.9 executable name. <br />
 (for python.exe -> "set PYTHON_EXE=python", for python39.exe -> "set PYTHON_EXE=python39", etc.)
   - Launch "**install_python_modules.bat**". This executable will **install the required Python libraries**. <br />
 If a proxy error occurs, try to modify the line "%PYTHON_EXE% -m pip install %%x --proxy http://z-proxy1.loc.global.sys" to remove the proxy argument at the end and try to use a local network (disconnect from the VPN or from office network). (The proxy address is working in Hitachi network.) <br />
 If an error occurs saying that pip is not installed, try to launch the command "python39 -m ensurepip --default-pip" (to update with the name or your Python 3.9 executable). It will install the default version of pip.


1. Modify the file "**launch.bat**" to add to the PATH your Python 3.9 executable and modify the PYTHON_EXE variable to match your Python 3.9 executable name.


2. Modify the file "**main.py**" to select the function(s) you want to launch. An explanation of the function is given in the file, as well as the required inputs to launch the function.


3. Modify the file "**config.ini**" to give the inputs required to launch the functions.


4. Launch "**launch.bat**". It will launch the functions specified in main.py using the inputs from config.ini.


5. Information is given throughout the launch inside the cmd window. A log file is creating capturing the logs written inside the cmd window.
