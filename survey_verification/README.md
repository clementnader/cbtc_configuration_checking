# SURVEY VERIFICATION TOOL

This tool helps with the **Correspondence with Site Survey** verification at SA level asked by the *System DPSA* (C_D413-2) in §2.1.2 and §3.2.

---
## 1. Description of the Correspondence with Site Survey activity
The Correspondence with Site Survey activity is described in §2.1.2 of System DPSA. <br />
The objective to verify the **consistency of the data in the C_D470** (more specifically in the DC_SYS file) **according to the topographic measures or site survey**.

The exhaustive list of objects to verify is given in the attached file in §3.2 of the System DPSA.

---
## 2. Tool behavior
The tool automates the verification for the following elements:
- Switches positioning,
- Platform ends and OSPs positioning,
- Blocks positioning,
- Signals and Buffers positioning,
- Localization and Dynamic tags positioning,
- Flood Gates positioning.

The tool lists every element from the DC_SYS of these types, and its position and tries to associate it using its name to the corresponding object from the survey. Objects are not associated if they are not on the same track in DC_SYS and survey, or if multiple elements in the survey can be associated to a same element in DC_SYS. The tool lists also every element from the survey that have not been associated. The objects are ordered by (track, KP).

---
## 3. How to use the tool

### 3.1. Inputs to launch the tool
- <ins>**CCTool-OO Schema**</ins>: It is an Excel file (.xls) provided in §3.1 of Core Data Preparation Format Specification (C_D413-2). It defines the schema of the DC_SYS_CORE file.


- <ins>**DC_SYS**</ins>: It is an Excel file (.xls) provided in the project database C_D470.


- *Optionally* <ins>**Block Def.**</ins>: It is an optional file used to establish the mapping between the block names from DC_SYS and the joint names given in the Survey. It is an Excel file containing the denomination of the block limits (joints and buffers). It has to be formatted as follows:
  - 2 lines of header.
  - 1 column named CDV_ID (usually first column). It contains all blocks names from DC_SYS (sheet CDV).
  - 2 columns LISTE EXTREMITES::LISTE SEGMENT_ID and LISTE EXTREMITES::LISTE EXT_ABS_SEG (usually the second and third columns). They contain respectively the list of limits segments and the list of the limits offsets. The elements of the lists are separated with semicolon ';'.
  - and multiple columns named OBJET EXTREMITE N, with N from 1 to the maximum number of block limits. Each column contains the name of the correspond limit that will appear in the survey.

  The position of the columns is not relevant for the tool but the name of the columns is.

If this file is not provided, the tool will automatically try to find the block limit names by mixing the two blocks of the limit (e.g. JOI_AAA_MMM_BBB_NNN for joint between TC_AAA_MMM and TC_BBB_NNN). It will create various name patterns to try to adapt to the different projects.


- <ins>**Survey file(s)**</ins>: They are Excel files (.xls, .xlsx or .xlsm) containing the surveyed information. As the template can differ, the user needs to specify to the tool:
   - the survey sheet name, or you can specify to use all the sheets of the file to get the survey data,
   - the first row containing the surveyed information (after the header line),
   - and the different columns for the data the tool will use:
     - reference name: name of the surveyed element,
     - type: type of the surveyed element:
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
     - track: track of the element,
     - surveyed KP: kilometer point surveyed by a geometer.

   Projects can have various survey files. In that case, user have to specify path and information for all these files. They have to be **added in chronological order**, with the oldest first and the most recent last. (The tool will consider that the newer values supersede the older ones. A comment is nevertheless written to inform the user of different values for a same object.)

**<ins>Note</ins>**: Tool will display in the logs the list of all other survey types that are not parsed by the tool. In case of another name for an object, one can modify the file _prj/src/survey/survey_types.py and add the extra name to the list "survey_type_names" inside the corresponding sub dictionary inside dictionary SURVEY_TYPES_DICT.

---
### 3.2. Steps to use the tool to compare the DC_SYS information with the survey file(s):

0. A preliminary step to perform only once in order to install the required Python libraries:
   - Modify the file "**install_python_modules.bat**" to add to the PATH your Python 3.9 (or more recent version) executable if needed (remove the "REM " in front of a line to uncomment it) and modify the PYTHON_EXE variable to match your Python executable name. <br />
     (for python.exe -> "set PYTHON_EXE=python", for python39.exe -> "set PYTHON_EXE=python39", etc.) <br />
     You can modify your environment variable PATH at user level to add the folder containing the python executable to avoid having to set this PATH variable each time you want to use Python. <br />
     It is good practice to copy your Python executable (python.exe) and rename the copy to match your Python version (python39.exe or python312.exe for example).
   - Launch "**install_python_modules.bat**". This executable will **install the required Python libraries**. <br />
 If a proxy error occurs, comment (add a REM in front) the line<br />
   "%PYTHON_EXE% -m pip install %%x --proxy http://z-proxy1.loc.global.sys"<br />
   and uncomment (remove the REM in front) the line without the proxy argument at the end and use a local network (disconnect from the VPN or from office network).<br />
   The proxy address is working in Hitachi network. <br />
 If an error occurs saying that pip is not installed, try to launch the command "python39 -m ensurepip --default-pip" (to update with the name or your Python executable). It will install the default version of pip.


1. Modify the file "**survey_verification.bat**" in the same fashion as "install_python_modules.bat" to add to the PATH your Python 3.9 (or more recent version) executable if needed and modify the PYTHON_EXE variable to match your Python executable name.


2. Launch "**survey_verification.bat**". It will launch the Python script to check the correspondence with the site survey.


3. A window will appear and ask for the **CCTool-OO Schema file** applicable to your version. <br />
It is used for the tool to read the DC_SYS in order to know in each sheet the columns corresponding to each attribute.


4. Then, another window will appear and ask for the **DC_SYS**, **Block Definition file**, and the **survey file(s)**. <br />
Instead of using the Block Definition file, you can check **automatic joint names** and let the tool generate the joint names. Note that it will only work if the joint names in the survey correspond to the two block names forming the joint. <br />
Once the survey file has been selected, you need to specify:
   - the **Survey Sheet** name, or you can tick the checkbox **use all sheets** so that the tool uses all visible sheets of the survey file to get the survey data. You can hide sheets that are not relevant so that the tool ignores them,
   - the **First Data Row** containing the surveyed information (after the header rows),
   - and the different columns for the data the tool will use (note that you can use either the letter of the column or the corresponding number):
     - **Reference Column**: the column containing the objects name,
     - **Type Column**: the column containing the objects type (e.g. SWP, TC, TAG...),
     - **Track Column**: the column containing the objects track,
     - **Surveyed KP Column**: the column containing the objects surveyed KP.

You also have the possibility to add other survey files (some projects have various files for the survey). If it is the case, you have to **add the survey files in chronological order**, with the oldest first and the most recent last. (The tool will consider that the newer values supersede the older ones. A comment is nevertheless written to inform the user of different values for a same object.)


5. Once all the information has been specified, you can press the button **"Launch Survey Verification"**. <br />
Information logs are provided in the command window during the execution and are also stored into a log file created in the tool directory.


6. At the end of the execution, an Excel file of the verification is created in the tool directory and is opened automatically in a new session of Excel.

---
## 4 Results
The tool generates an Excel verification file called "Correspondence with Site Survey - *DC_SYS_FOLDER_NAME*.xlsx".

### 4.1 Result file structure
Sheet **"Header"** is pre-filled with the Author name corresponding to the Windows session user, the C_D470 corresponding to the name of the folder containing the specified DC_SYS, the block definition file if any, the survey file(s), the date and the tool version.

Sheet **"FD - Site Survey"** contains the list of objects to verify given in the attached file in §3.2 of the System DPSA. The aim is to use this file directly as the verification result file to add to the DPSR. However, the user shall verify that this list given by the tool correctly correspond to what is effectively given by the System DPSA.

For each type of objects that is automated, there is **a dedicated sheet** containing the results of the verification:
- a sheet **"Switch"** containing the center (*SWP*_C), the left (*SWP*_L) and right (*SWP*_R) points of the switches.
- a sheet **"Platform"** containing the platform ends (*PLT_NAME*__Limit_N), the platform OSPs and the not platform related OSPs. The different objects types have different colors.
- a sheet **"Block"** containing the block joints (JOI_*BLOCK1*\_*BLOCK2* or JOI_*BLOCK1*__end_of_track), if a Block Def. file has been specified, an extra column will appear to display the associated joint name or buffer name.
- a sheet **"Signal"** containing the home signals (type MANOEUVRE), the permanently red signals (type PERMANENT_ARRET) and the buffers (type HEURTOIR). The different objects types have different colors.
- a sheet **"Tag"** containing the localization tags and the dynamic tags. The different objects types have different colors.
- a sheet **"FloodGate"** containing the floodgate ends (*FG_NAME*__Limit_N).

### 4.2 Verification sheet structure
Each sheet follows the same structure:

- **<ins>Column A</ins>** contains the **data name**.

    For signals, buffers, tags and OSPs, it corresponds directly to the name in DC_SYS.

    For switches, it is the switch name plus a suffix:

  - "_C" for the center point (corresponding to position on the point segment of the switch).

  - "_L" and "_R" for the left and right heel points (corresponding to position on the heels of the switch).

  For platform ends and floodgates ends, it is the name of the object plus a prefix "__Limit_X" to specify the number of the object end. <br />

  For block joints, the name is generated by mixing the two blocks that have this common limit.


- **<ins>Column B</ins>** contains the **DC_SYS object type** from which the data is extracted (useful for platform to differentiate platform ends, platform OSPs and not platform related OSPs, for signals to differentiate home signals, permanently reds and buffers, and for tags to differentiate static and dynamic tags).


- **<ins>Columns C and D</ins>** contain the **positioning (track, KP)** collected from the **DC_SYS**.


- If a Block Def. is used, an extra column will appear in sheet "Block" containing the corresponding limit name from the block definition file.


- **<ins>Column E</ins>** contains the object **reference name** from the **survey**.


- **<ins>Column F</ins>** contains the information set in the **type** column in the **survey** (useful for platform to differentiate platform ends and OSPs, for signals to differentiate signals and buffers, for tags to differentiate static and dynamic tags, and for blocks to differentiate joints and buffers if buffers are specified inside the Block Def. file).


- **<ins>Columns G and H</ins>** contain the **positioning (track, surveyed KP)** collected from the **survey file(s)**.

    A comment is put on surveyed KP cells in column H to specify from which survey file and sheet the information was collected (can be useful in multiple survey files are used or if all_sheets option is selected).

The different objects are ordered by track and then KP from the DC_SYS if they exist, else from the survey.

- **<ins>Column I</ins>** contains the computation of the **difference** between the two KP values.

    If the object is not found in the survey, "**Not Surveyed**" is written.

    If the object is found in the survey but not in the DC_SYS, "**Not in DC_SYS**" is written.


- **<ins>Column J</ins>** contains the **status of the verification**: if the difference is lower (in absolute value) than the tolerance (set in cell B1), the status is OK, else it is KO.

    If one data is missing, the same message ("Not Surveyed" or "Not in DC_SYS") is written as in the Difference column.


- **<ins>Column K</ins>** contains **automatic comments**. Comments can be written by the tool in some specific cases (for example, if the same object has been found in different survey files, if the same object has been found multiple times in the same survey file, if the KP value in the survey appears to be with a different sign from the DC_SYS KP value...). The column is hidden if no automatic comments are written.


- **<ins>Column L</ins>** is left free for the **manual verification** status.


- **<ins>Column M</ins>** is left free for **comments** from the user.

### 4.3 Tool functions
#### 4.3.1 Switch points: center and heel positions
It can happen that instead of giving the 3 positions for the switches: _C (center point), _L (left heel) and _R (right heel), the survey ignores the center point or one of the heel because they are on the same track (and so at the same position) as another position of the switch: the survey only gives the position of the switch on the Normal track and on the Reverse (deviated) track. <br />
In that case, the tool tries to do the association with the other position of the switch that is on the same track and writes a comment.

#### 4.3.2 Platform ends positioning when Middle Platforms are given in the survey
It can happen that instead of begin and end limits of the platforms, the middles of the platform are given in the survey. <br />
In that case, the tool creates a Defined Name on the middle platform positions, and uses it in addition to the platforms length to compute the position of the platforms limits. <br />
An extra row is created in the first rows for the user to specify the platforms length.

#### 4.3.3 Opposite sign in survey
It can happen that the sign of surveyed KP in survey does not match the one in DC_SYS. <br />
In that case, the tool writes in the automatic comments a formula to do the computation of the difference with absolute values on the KPs and check if this difference is lower than the tolerance.
