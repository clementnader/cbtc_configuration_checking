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


1. Modify the file "**route_and_overlap_control_tables_verification.bat**" to add to the PATH your Python 3.9 executable and modify the PYTHON_EXE variable to match your Python 3.9 executable name. <br />
(Set it up in the same way as "install_python_modules.bat".)


2. Launch "**route_and_overlap_control_tables_verification.bat**". It will launch the Python script to check the correspondence of the Route and Overlap with the PDF Control Tables.


3. A window will appear and ask for the **CCTool-OO Schema file** applicable to your version. <br />
(It is used for the tool to read the DC_SYS in order to know the columns corresponding to each attribute.)


4. Then, another window will appear and ask for the type of Control Table (either Route or Overlap), then the Control Tables configuration .ini file that can be found in the folder "control_tables_configuration", and then the Control Tables PDF. <br />
Once the Control Table PDF file has been selected, you need to select the pages of the PDF that contain the information: either all the pages, or only a range of pages (not that if there are only extra introduction pages, you can select "all pages").

Note that you can add multiple Control Tables Files by clicking the button "ass another control table file".


5. Once these pieces of information have been specified, you can press the button **"Launch Control Table Translation"**. It will extract the info from the PDF and create CSV files. <br />
Information logs are provided in the command window during the execution.


6. Then, you can add DC_SYS and DC_BOP info in the window (DC_BOP is often inside folder C64_D413 inside PRJ_C_D470), to launch the verification.


7. Once these pieces of information have been specified, you can press the button **"Launch Control Table Verification"**. It will use the extracted info from the CSV files and verify them with the DC_SYS using the DC_BOP for the correspondence between NORMAL/REVERSE use at IXL level and LEFT/RIGHT used at Core CBTC level. <br />


8. Result logs are written in the command window during the execution.
