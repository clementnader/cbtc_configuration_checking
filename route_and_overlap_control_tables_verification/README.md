# ROUTE AND OVERLAP CONTROL TABLES VERIFICATION TOOL

This tool helps with the **Verification of the Route and Overlap** verification at SA level asked by the *System DPSA* (C_D413-2) in §??.

---
## 1. Description of the Route and Overlap Verification activity
The Route and Overlap Verification activity is described in the Foundation Data Analysis of System DPSA. <br />
The objective to verify the **correspondence between routes in DC_SYS (sheet Iti) and overlaps in DC_SYS (sheet IXL_Overlap) versus the IXL information**.

---
## 2. Tool behavior
The tool automates the verification for the following elements:
- for Routes:
  - route name, start signal, list of IVBs of the route (including the Destination IVB), list of switches and their position.
- for Overlaps:
  - overlap name, corresponding signal, VSP position according to the IVB path from IXL, list of switches and their position.

---
## 3. How to use the tool

### 3.1. Inputs to launch the tool
- <ins>**CCTool-OO Schema**</ins>: It is an Excel file (.xls) provided in §3.1 of Core Data Preparation Format Specification (C_D413-2). It defines the schema of the DC_SYS_CORE file.


- <ins>**DC_SYS**</ins>: It is an Excel file (.xls) provided in the project database C_D470.


- <ins>**DC_BOP**</ins>: It is used for the verification of routes and overlaps. It is an Excel file (.xls) provided in the project database C_D470 (directly in the folder or inside subfolder C64_D413) containing the correspondence between the switches position at CBTC level (left/right) and at IXL level (normal/reverse).


---
### 3.2. Steps to use the tool to compare the DC_SYS information with the survey file(s):

0. A preliminary step to take once in order to install the required Python libraries:
   - Modify the file "**install_python_modules.bat**" to add to the PATH your Python 3.9 executable (remove the "REM " in front of a line to uncomment it) and modify the PYTHON_EXE variable to match your Python 3.9 executable name. <br />
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


6. The result Excel file is placed in the tool directory and is opened automatically in a new session of Excel.

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
