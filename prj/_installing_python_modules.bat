@echo off

set PYTHON_EXE=%1

for %%x in (numpy openpyxl xlrd Unidecode pdfreader tk) do (
     echo. && echo Install library %%x.
     %PYTHON_EXE% -m pip install %%x --proxy http://z-proxy1.loc.global.sys
    )
