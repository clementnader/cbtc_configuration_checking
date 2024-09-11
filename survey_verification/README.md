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
- Signals and buffers positioning,
- Localization and Dynamic tags positioning,
- Flood Gates positioning.

The tool lists every element from the DC_SYS of these types, and its position and tries to associate it using its name to the corresponding object from the survey. Objects are not associated if they are not on the same track in DC_SYS and survey, or if multiple elements in the survey can be associated to a same element in DC_SYS. The tool lists also every element from the survey that have not been associated. The objects are ordered by (track, KP).

---
## 3. How to use the tool

### 3.1. Inputs to launch the tool
- <ins>**CCTool-OO Schema**</ins>: It is an Excel file (.xls) provided in §3.1 of Core Data Preparation Format Specification (C_D413-2). It defines the schema of the DC_SYS_CORE file.


- <ins>**DC_SYS**</ins>: It is an Excel file (.xls) provided in the project database C_D470.


- *Optionally* <ins>**Block Def.**</ins>: It is an Excel file containing the denomination of the block limits (joints and buffers). It has to be formatted as follows:
  - 2 lines of header.
  - 1 column named CDV_ID (usually first column). It contains all blocks names from DC_SYS (sheet CDV).
  - 2 columns LISTE EXTREMITES::LISTE SEGMENT_ID and LISTE EXTREMITES::LISTE EXT_ABS_SEG (usually the second and third columns). They contain respectively the list of limits segments and the list of the limits offsets. The elements of the lists are separated with commas ';'.
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
       - for flood gates, type shall be:<br />
       **FLOOD_GATE**, **FLOOD GATE**, **FLOODGATE** or **FLOODGATES**.
     - track: track of the element,
     - surveyed KP: kilometer point surveyed by a geometer.
   
   Projects can have various survey files. In that case, user have to specify path and information for all these files. They have to be **added in chronological order**, with the oldest first and the most recent last. (The tool will consider that the newer values supersede the older ones. A comment is nevertheless written to inform the user of different values for a same object.)

Tool will display in the logs the list of all other survey types that are not parsed by the tool. In case of another name for an object, one can modify the file prj/src/survey/survey_types.py and add the extra name to the list "survey_type_names" inside the corresponding sub dictionary inside dictionary SURVEY_TYPES_DICT.

---
### 3.2. Steps to use the tool to compare the DC_SYS information with the survey file(s):

0. A preliminary step to take once in order to install the required Python libraries, it has to be done once by the user on their computer:
   - Modify the file "**install_python_modules.bat**" to add to the PATH your Python 3.9 executable (remove the “REM ” in front of a line to uncomment it) and modify the PYTHON_EXE variable to match your Python 3.9 executable name. <br />
     (for python.exe -> "set PYTHON_EXE=python", for python39.exe -> "set PYTHON_EXE=python39", etc.) <br />
     Or modify you environment variable PATH at user level to add the folder containing the python executable. And copy and rename the Python executable to be python39.exe.
   - Launch "**install_python_modules.bat**". This executable will **install the required Python libraries**. <br />
 If a proxy error occurs, comment (add a REM in front) the line<br />
   "%PYTHON_EXE% -m pip install %%x --proxy http://z-proxy1.loc.global.sys"<br />
   and uncomment (remove the REM in front) the line without the proxy argument at the end and use a local network (disconnect from the VPN or from office network).<br />
   (The proxy address is working in Hitachi network.) <br />
 If an error occurs saying that pip is not installed, try to launch the command "python39 -m ensurepip --default-pip" (to update with the name or your Python 3.9 executable). It will install the default version of pip.


1. Modify the file "**survey_verification.bat**" to add to the PATH your Python 3.9 executable and modify the PYTHON_EXE variable to match your Python 3.9 executable name. <br />
(Set it up in the same way as "install_python_modules.bat".)


2. Launch "**survey_verification.bat**". It will launch the Python script to check the correspondence with the site survey.


3. A window will appear and ask for the **CCTool-OO Schema file** applicable to your version. <br />
(It is used for the tool to read the DC_SYS in order to know the columns corresponding to each attribute.)


4. Then, another window will appear and ask for the **DC_SYS**, optionally the **Block Def.**, and the **survey file(s)**. <br />
To select a Block Def. file, you need to uncheck **automatic joint names** and select the correspond file.<br />
Once the survey file has been selected, you need to specify:
   - the **Survey Sheet** name, or you can select the checkbox so that the tool uses **All Sheets** of the survey file to get the survey data,
   - the **First Data Row** containing the surveyed information (after the header),
   - and the different columns for the data the tool will use (note that you can use either the letter of the column or the corresponding number):
     - **Reference Column** (the column containing the objects name),
     - **Type Column** (the column containing the objects type (e.g. SWP, TC, TAG...)),
     - **Track Column** (the column containing the objects track),
     - **Surveyed KP Column** (the column containing the objects surveyed KP).

You will also have the possibility to add other survey files (some projects have various files for the survey). If it is the case, you have to **add the survey files in chronological order**, with the oldest first and the most recent last. (The tool will consider that the newer values supersede the older ones. A comment is nevertheless written to inform the user of different values for a same object.)


5. Once all the information has been specified, you can press the button **"Launch Survey Verification"**. <br />
Information logs are provided in the command window during the execution.


6. The result Excel file is placed into the Desktop and is opened automatically in a new session of Excel.

---
## 4 Results
The tool generates an Excel verification file called "Correspondence with Site Survey - *DC_SYS_FOLDER_NAME*.xlsx".

### 4.1 Result file structure
Sheet **"Header"** is pre-filled with the Author name corresponding to the Windows session user, the C_D470 corresponding to the name of the folder containing the specified DC_SYS, the date and the tool version.

Sheet **"Survey"** contains the exhaustive list of objects to verify given in the attached file in §3.2 of the System DPSA. The aim is to use this file directly as the verification result file to add to the DPSR.

For each type of objects that is automated, there is **a dedicated sheet** containing the results of the verification:
- a sheet **"Switch"** containing the center (*SWP*_C), the left (*SWP*_L) and right (*SWP*_R) points of the switches.
- a sheet **"Platform"** containing the platform ends (*PLT_NAME*__Limit_N), the platform OSPs and the not platform related OSPs. The different objects types have different colors.
- a sheet **"Block"** containing the block joints (JOI_*BLOCK1*\_*BLOCK2* or JOI_*BLOCK1*__end_of_track), if a Block Def. file has been specified, an extra column will appear to display the associated joint name or buffer name.
- a sheet **"Signal"** containing the home signals (type MANOEUVRE), the permanently red signals (type PERMANENT_ARRET) and the buffers (type HEURTOIR). The different objects types have different colors.
- a sheet **"Tag"** containing the localization tags and the dynamic tags. The different objects types have different colors.
- a sheet **"FloodGate"** containing the flood gate ends (*FG_NAME*__Limit_N).

### 4.2 Verification sheet structure
Each sheet follows the same structure:

- **<ins>Column A</ins>** contains the **data name**.

    For signals, buffers, tags and OSPs, it corresponds directly to the name in DC_SYS.

    For switch, it is the switch name plus a suffix:

  - "_C" for the center point (corresponding to position on the point segment of the switch).

  - "_L" and "_R" for the left and right heel points (corresponding to position on the heels of the switch).

  For platform ends and flood gates ends, it is the name of the object plus a prefix to specify the number of the object end. <br />

  For block joints, the name is generated by mixing the two blocks that have this common limit.


- **<ins>Column B</ins>** contains the **DC_SYS object type** from which the data is extracted (useful for platform to differentiate platform ends, platform OSPs and not platform related OSPs, for signals to differentiate home signals, permanently reds and buffers, and for tags to differentiate static and dynamic tags).


- **<ins>Columns C and D</ins>** contain the **positioning (track, KP)** collected from the **DC_SYS**.


- If a Block Def. is used, an extra column will appear in sheet "Block" containing the corresponding limit name from the block definition file.


- **<ins>Column E</ins>** contains the object **reference name** from the **survey**.


- **<ins>Column F</ins>** contains the information set in the **type** column in the **survey** (useful for platform to differentiate platform ends and OSPs, for signals to differentiate signals and buffers, for tags to differentiate static and dynamic tags, and for blocks to differentiate joints and buffers if buffers are specified inside the Block Def. file).


- **<ins>Columns G and H</ins>** contain the **positioning (track, KP)** collected from the **survey file(s)**.

    A comment is put on cells in column H to specify from which survey the information was collected (can be useful in multiple survey files are used).

The results are ordered by track and then KP from the DC_SYS if they exist, else from the survey.

- **<ins>Column I</ins>** contains the computation of the **difference** between the two KP values. 

    If the object is not found in the survey, "**Not Surveyed**" is written.
    
    If the object is found in the survey but not in the DC_SYS, "**Not in DC_SYS**" is written.


- **<ins>Column J</ins>** contains the **status of the verification**: if the difference is lower (in absolute value) than the tolerance (set in cell B1), the status is OK, else it is KO.

    If one data is missing, the same message ("Not Surveyed" or "Not in DC_SYS") is written as in the Difference column.


- **<ins>Column K</ins>** contains **automatic comments**. Comments can be written by the tool in some specific cases (for example, if the same object has been found in different survey files, if the same object has been found multiple times in the same survey file, if the KP value in the survey appears to be with a different sign from the DC_SYS KP value...). The column is hidden if no automatic comments are written.


- **<ins>Column L</ins>** is left free for the **manual verification** status. 


- **<ins>Column M</ins>** is left free for **comments** from the user. 
