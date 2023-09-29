@echo off

REM set PATH=C:\Python39\;%PATH%
REM set PATH=%LocalAppData%\Programs\Python\Python39\;%PATH%

set PYTHON_EXE=python39

cd ..\prj

echo. && echo ---------------------------------------------- && echo.
echo Installing the required Python libraries...
echo. && echo ---------------------------------------------- && echo.
call _installing_python_modules.bat %PYTHON_EXE%

cd ..\launch_survey

echo. && echo ---------------------------------------------- && echo.
echo Launching the Survey Verification tool...
echo. && echo ---------------------------------------------- && echo.
%PYTHON_EXE% launch_survey_verification.py

echo. && echo ---------------------------------------------- && echo.
echo Process has finished.
echo. && echo ---------------------------------------------- && echo.
pause
