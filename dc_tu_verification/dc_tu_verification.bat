@echo off

REM set PATH=C:\Python39\;%PATH%
REM set PATH=%LocalAppData%\Programs\Python\Python39\;%PATH%

set PYTHON_EXE=python39

echo. && echo ---------------------------------------------- && echo.
echo Launching the DC_TU Verification tool...
echo. && echo ---------------------------------------------- && echo.

%PYTHON_EXE% launch_dc_tu_verification.py

echo. && echo ---------------------------------------------- && echo.
echo Process has finished.
echo. && echo ---------------------------------------------- && echo.

pause
