@echo off
title Survey Verification Tool
@REM Configure cmd window size.
powershell -command "& {$pshost = Get-Host; $pswindow = $pshost.UI.RawUI; $newsize = $pswindow.BufferSize; $newsize.Width = 180; $newsize.Height = 9000; $pswindow.BufferSize = $newsize; $newsize = $pswindow.WindowSize; $newsize.Width = 180; $newsize.Height = 40; $pswindow.WindowSize = $newsize}"
@REM Set current directory to the directory containing the batch file.
cd /D "%~dp0"

@REM -------------------------------------------------------------------------------------------------------------------

@REM If the folder containing your python executable is not in your path environment variable,
@REM uncomment one of the next lines and adapt it to match your Python folder path.
REM set PATH=C:\Python39\;%PATH%
REM set PATH=%LocalAppData%\Programs\Python\Python39\;%PATH%

@REM Adapt next line to match your Python executable file name.
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
