@echo off
title Survey Verification Tool
REM configure cmd window size
mode con: cols=160 lines=40
REM configure cmd window buffer size to 9000 rows
powershell -command "& {$pshost = Get-Host; $pswindow = $pshost.UI.RawUI; $newsize = $pswindow.BufferSize; $newsize.Height = 9000; $pswindow.BufferSize = $newsize}"

REM ------------------------------------------------------------------------------

REM set PATH=C:\Python39\;%PATH%
REM set PATH=%LocalAppData%\Programs\Python\Python39\;%PATH%

set PYTHON_EXE=python39

echo. && echo ----------------------------------------------------------- && echo.
echo Launching the Survey Verification tool...
echo. && echo ----------------------------------------------------------- && echo.

cd py_exec
%PYTHON_EXE% launch_survey_verification.py
cd ..

echo. && echo ----------------------------------------------------------- && echo.
echo Process has finished.
echo. && echo ----------------------------------------------------------- && echo.

pause
