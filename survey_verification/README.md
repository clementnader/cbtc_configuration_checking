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
- Switch positioning,
- Platform end positioning,
- Block positioning,
- Signal and buffer positioning,
- Switch positioning,
- Tag positioning,
- Flood Gate positioning.

---
## 3. How to use the tool

### 3.1. Inputs to launch the tool
- <ins>**CCTool-OO Schema**</ins>: It is an Excel file (.xls) provided in §3.1 of Core Data Preparation Format Specification (C_D413-2). It defines the schema of the DC_SYS_CORE file.
- <ins>**DC_SYS**</ins>: It is an Excel file (.xls) provided in the project database C_D470.
- <ins>**Survey file(s)**</ins>: They are Excel files (.xls, .xlsx or .xlsm) containing the surveyed information. As the template can differ, the user needs to specify to the tool:
   - the survey sheet name, or you can specify to use all the sheets of the file to get the survey data,
   - the first row containing the surveyed information (after the header line),
   - and the different columns for the data the tool will use:
     - reference name: name of the surveyed element,
     - type: type of the surveyed element:
       - for switches, type shall be **SWP**, **SWITCH** or **SWITCH POINT**.
       - for platform ends, type shall be **PLATFORM** or **PLATFORM END**.
       - for blocks, type shall be **TC**, **AXLE COUNTER** or **INSULATED JOINT**.
       - for signals, type shall be **SIGNAL**.
       - for buffers, type shall be **SIGNAL_BUFFER** or **BUFFER**.
       - for tags, type shall be **TAG**;
       - for flood gates, type shall be **FLOOD_GATE** or **FLOODGATE**.
     - track: track of the element,
     - surveyed KP: kilometer point surveyed by a geometer.
   
   Projects can have various survey files. In that case, user have to specify path and information for all these files. They have to be **added in chronological order**, with the oldest first and the most recent last. (The tool will consider that the newer values supersede the older ones. A comment is nevertheless written to inform the user of different values for a same object.)

---
### 3.2. Steps to use the tool to compare the DC_SYS information with the survey file(s):

0. A preliminary step to take once in order to install the required Python libraries:
   - Modify the file "**install_python_modules.bat**" to add to the PATH your Python 3.9 executable and modify the PYTHON_EXE variable to match your Python 3.9 executable name. <br />
 (for python.exe -> "set PYTHON_EXE=python", for python39.exe -> "set PYTHON_EXE=python39", etc.)
   - Launch "**install_python_modules.bat**". This executable will **install the required Python libraries**. <br />
 If an error occurs saying that pip is not installed, try to launch the command "python39 -m ensurepip --default-pip" (to update with the name or your Python 3.9 executable). It will install the default version of pip. <br />
 If a proxy error occurs, try to modify the line "%PYTHON_EXE% -m pip install %%x --proxy http://z-proxy1.loc.global.sys" to remove the proxy argument at the end and try to use a local network (disconnect from the VPN or from office network). (The proxy address is working in Hitachi France network.)


1. Modify the file "**survey_verification.bat**" to add to the PATH your Python 3.9 executable and modify the PYTHON_EXE variable to match your Python 3.9 executable name.


2. Launch "**survey_verification.bat**". It will launch the Python script to check the correspondence with the site survey.


3. A window will appear and ask for the **CCTool-OO Schema file** applicable to your version. <br />
(It is used for the tool to read the DC_SYS in order to know the columns corresponding to each attribute.)


4. Then, another window will appear and ask for the **DC_SYS** and the **survey file(s)**. <br />
Once the survey file has been selected, you need to specify:
   - the **Survey Sheet** name, or you can select the checkbox so that the tool uses **All Sheets** of the survey file to get the survey data,
   - the **First Data Row** containing the surveyed information (after the header),
   - and the different columns for the data the tool will use (note that you can use either the letter of the column or the corresponding number):
     - **Reference Column**,
     - **Type Column**,
     - **Track Column**,
     - **Surveyed KP Column**.

You will also have the possibility to add another survey files (some projects have various files for the survey). If it is the case, you have to **add the survey files in chronological order**, with the oldest first and the most recent last. (The tool will consider that the newer values supersede the older ones. A comment is nevertheless written to inform the user of different values for a same object.)


5. Once all the information has been specified, you can press the button **"Launch Survey Verification"**.


6. The result Excel file is placed into the Desktop and is opened automatically.

---
### 3.3 Results
The tool generates a verification file. Sheet **"Survey"** contains the exhaustive list of objects to verify given in the attached file in §3.2 of the System DPSA. The aim is to use this file directly as the verification result file to add to the DPSR.

For each type of objects that is automated, there is **a dedicated sheet** containing the results of the verification.

- **<ins>Column A</ins>** contains the **data name**.

    For signals, buffers and tags, it corresponds directly to the name in DC_SYS.

    For switch, it is the switch name plus a suffix:

  - "_C" for the center point (corresponding to position on the point segment of the switch).

  - "_L" and "_R" for the left and right heel points (corresponding to position on the heels of the switch).

  For platform ends and flood gates ends, it is the name of the object plus a prefix to specify which end of the object. <br />

  For block joints, the name is generated by mixing the two blocks that have this common limit.


- **<ins>Columns B and C</ins>** contain the **positioning (track, KP)** collected from the **DC_SYS**.


- **<ins>Columns D and E</ins>** contain the **positioning (track, KP)** collected from the **survey file(s)**.

    A comment is put on cells in column E to specify in which survey the information was collected.

The results are ordered by track and then KP from the DC_SYS if they exist, else from the survey.

- **<ins>Column F</ins>** contains the computation of the **difference** between the two KP values. 

    If the object is not found in the survey, "**Not Surveyed**" is written.
    
    If the object is found in the survey but not in the DC_SYS, "**Not in DC_SYS**" is written.


- **<ins>Column G</ins>** contains the **status of the verification**: if the difference is lower (in absolute value) than the tolerance (set in cell B1), the status is OK, else it is KO.

    If one data is missing, the same message ("Not Surveyed" or "Not in DC_SYS") is written as in the Difference column.


- **<ins>Column H</ins>** contains **comments**. They will be written if the same object has been found in different survey files, if the same object has been found multiple times in the same survey file, and in other specific cases.


- **<ins>Column I</ins>** is left free for the **manual verification** status. 
