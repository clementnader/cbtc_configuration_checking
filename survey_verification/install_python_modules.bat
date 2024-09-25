@echo off

REM set PATH=C:\Python39\;%PATH%
REM set PATH=%LocalAppData%\Programs\Python\Python39\;%PATH%

set PYTHON_EXE=python39
set PROXY_ADDR=http://z-proxy1.loc.global.sys

echo. && echo ---------------------------------------------- && echo.
echo Installing the required Python libraries...
echo. && echo ---------------------------------------------- && echo.

for %%x in (numpy openpyxl xlrd Unidecode pdfreader tk) do (
    echo. && echo Install library %%x.
    REM Uncomment next line if launching it while connected to Hitachi network, on site or with VPN.
    %PYTHON_EXE% -m pip install %%x --proxy %PROXY_ADDR%
    REM Uncomment next line if launching it disconnected from VPN.
    REM %PYTHON_EXE% -m pip install %%x
)

echo. && echo ---------------------------------------------- && echo.
echo Process has finished.
echo. && echo ---------------------------------------------- && echo.

pause
