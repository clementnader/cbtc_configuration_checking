@echo off

REM set PATH=C:\Python39\;%PATH%
REM set PATH=%LocalAppData%\Programs\Python\Python39\;%PATH%

set PYTHON_EXE=python39

echo. && echo ---------------------------------------------- && echo.
echo Launching the Survey Verification tool...
echo. && echo ---------------------------------------------- && echo.

cd py_exec
%PYTHON_EXE% launch_survey_verification.py
cd ..

echo. && echo ---------------------------------------------- && echo.
echo Process has finished.
echo. && echo ---------------------------------------------- && echo.

pause
