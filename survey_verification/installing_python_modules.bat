@echo off

REM set PATH=C:\Python39\;%PATH%
REM set PATH=%LocalAppData%\Programs\Python\Python39\;%PATH%

set PYTHON_EXE=python39

echo. && echo ---------------------------------------------- && echo.
echo Installing the required Python libraries...
echo. && echo ---------------------------------------------- && echo.

for %%x in (numpy openpyxl xlrd Unidecode pdfreader tk) do (
    echo. && echo Install library %%x.
    %PYTHON_EXE% -m pip install %%x --proxy http://z-proxy1.loc.global.sys
    REM %PYTHON_EXE% -m pip install %%x
)

echo. && pause

