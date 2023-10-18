# SURVEY VERIFICATION TOOL

### Steps to use the tool to compare the DC_SYS information with the survey file(s):

1. Modify the file "survey_verification.bat" to add to the PATH your Python 3.9 executable and modify the PYTHON_EXE variable to match your Python 3.9 executable name. <br />
(for python.exe -> "set PYTHON_EXE=python", for python39.exe -> "set PYTHON_EXE=python39", etc.)


2. Launch the .bat file.


3. As a first step, the tool will **install the required Python libraries**. <br />
If pip is not installed, try to launch the command "python39 -m ensurepip --default-pip" (to update with the name or your Python 3.9 executable). It will install the default version of pip.


4. Then, the Python script to check the correspondence with the site survey effectively starts. <br />
A window will appear and ask for the **CCTool-OO Schema file** applicable to your version. <br />
(It is used for the tool to read the DC_SYS in order to know the columns corresponding to each attribute.)


5. After, another window will appear and ask for the **DC_SYS** and the **survey**. <br />
Once the survey file has been selected, you need to specify:
   - the survey sheet name,
   - the first row containing the surveyed information (after the header),
   - and the different columns for the data the tool will use (note that you can use either the letter of the column or the corresponding number).

   You will have also the possibility to add another survey files (some projects have various files for the survey). If it is the case, you have to **add the survey files in chronological order**, with the oldest first and the most recent last. (The tool will consider that the newer values supersede the older ones. A comment is nevertheless written to inform the user of different values for a same object.)


6. Once all the information has been specified, you can press the button **"Launch Survey Verification"**.


7. The result Excel file is placed into the Desktop and is opened automatically.
