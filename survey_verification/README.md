===== SURVEY VERIFICATION TOOL =====

Steps to use the tool to compare the DC_SYS information with the survey file(s):
    1. Modify the file survey_verification.bat to add to the PATH your Python 3.9 executable and modify the PYTHON_EXE variable to match your Python 3.9 executable name.
        (for python.exe -> "set PYTHON_EXE=python", for python39.exe -> "set PYTHON_EXE=python39")
    2. Launch the .bat file.
    3. As a first step, the tool will install the required Python libraries.
    4. Then, a window will appear and ask for the CCTool-OO Schema file applicable to your version.
    5. After, another window will appear and ask for the DC_SYS and the survey.
        Once the survey file has been selected, you need to specify:
            - the survey sheet name,
            - the first row containing the surveyed information (after the header)
            - and the different columns for the data the tool will use (note that you can use either the letter of the column or the corresponding number).
        You will have also the possibility to add another survey files (some projects have various files for the survey).
    6. Once all the information has been specified, you can press the button "Launch Survey Verification".
    7. The result Excel file is placed on the Desktop and is opened automatically.*
