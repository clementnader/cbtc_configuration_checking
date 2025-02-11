@echo off
title Install Python modules
@REM Configure cmd window size.
mode con: cols=160 lines=40
@REM Configure cmd window buffer size to 9000 lines.
powershell -command "& {$pshost = Get-Host; $pswindow = $pshost.UI.RawUI; $newsize = $pswindow.BufferSize; $newsize.Height = 9000; $pswindow.BufferSize = $newsize}"
@REM Set current directory to the directory containing the batch file.
cd /D "%~dp0"

@REM ------------------------------------------------------------------------------

@REM If the folder containing your python executable is not in your path environment variable,
@REM uncomment one of the next lines and adapt it to match your folder path.
REM set PATH=C:\Python39\;%PATH%
REM set PATH=%LocalAppData%\Programs\Python\Python39\;%PATH%

@REM Adapt next line to match your Python executable file name.
set PYTHON_EXE=python39

@REM Next line establishes the proxy address for the command to work when connected to Hitachi network.
set PROXY_ADDR=http://z-proxy1.loc.global.sys

echo. && echo ---------------------------------------------- && echo.
echo Installing the required Python libraries...
echo. && echo ---------------------------------------------- && echo.

@REM Inside the parentheses is the list of Python external libraries to install, that are used by the code.
for %%x in (numpy openpyxl xlrd Unidecode pdfreader tk) do (
    echo. && echo Install library %%x.
    @REM Uncomment next line if launching it while connected to Hitachi network, on site or with VPN.
    %PYTHON_EXE% -m pip install %%x --proxy %PROXY_ADDR%
    @REM Uncomment next line if launching it disconnected from VPN.
    REM %PYTHON_EXE% -m pip install %%x
)

echo. && echo ---------------------------------------------- && echo.
echo Process has finished.
echo. && echo ---------------------------------------------- && echo.

pause
