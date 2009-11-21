@echo off

IF "%1" EQU "" GOTO error

SET PYTHON=C:\Python25\python.exe
SET APPNAME=Milkshake
SET CAPBLS=NetworkServices+LocalServices+ReadUserData+WriteUserData+UserEnvironment
SET SRCDIR=src
SET TMPDIR=src.tmp
SET ICONREP=img\milkshake-icon.svg
SET ICON=milkshake.svg

REM put you zip tool here
SET ZIP="C:\Arquivos de programas\7-Zip\7z.exe"
REM Path to module-repo, inside Python For S60 
SET PYS60DIR="C:\Arquivos de programas\PythonForS60"

SET OPTS=--verbose --version="%1" --appname="%APPNAME%" --icon="%ICON%" --extrasdir=extras --heapsize=4k,5M --caps=%CAPBLS% 

echo "Populating temp dir"
if exist "%TMPDIR%" rmdir /s /q "%TMPDIR%"
mkdir %TMPDIR%\extras\data\python\milkshakedir
copy  %SRCDIR%\lib\about.py  %TMPDIR%\extras\data\python\milkshakedir
copy  %SRCDIR%\lib\milkshake.py  %TMPDIR%\extras\data\python\milkshakedir
copy  %SRCDIR%\lib\window.py  %TMPDIR%\extras\data\python\milkshakedir
copy  %SRCDIR%\default.py  %TMPDIR%\

echo "Copying project to PyS60 dir"
if exist "%PYS60DIR%\%TMPDIR%" rmdir /s/q "%PYS60DIR%\%TMPDIR%"
xcopy /E "%TMPDIR%" "%PYS60DIR%\%TMPDIR%\"
if exist "%PYS60DIR%\%ICON%" del /s/q "%PYS60DIR%\%ICON%"
copy %ICONREP% "%PYS60DIR%\%ICON%"

echo "Generating for Python 1.9.x"
pushd .
cd "%PYS60DIR%"
echo "Creating sis"

pause

%PYTHON% ensymble.py py2sis %OPTS% "%TMPDIR%" "%APPNAME%-%1.sis"

popd
copy "%PYS60DIR%\%APPNAME%-%1.sis" .
echo "Zipping source files"
%ZIP% a -r -tzip %APPNAME%-%1-src.zip src\*.py src\*.mif src\*.png

echo "Erasing"
rmdir /s/q "%PYS60DIR%\%TMPDIR%"
del /s/q "%PYS60DIR%\%ICON%"
del "%PYS60DIR%\%APPNAME%-%1.sis"
rmdir /s/q "%TMPDIR%"

goto end

:error
echo Sintaxe: %0 version

:end


