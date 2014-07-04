F8 at start-up :: Safe mode / Mode sans echec
F7 in cmd.exe -> history
:: BUT better use cmder or at least PowerShell ISE

ipconfig /displaydns

where <cmd> :: 'which' equivalent
powercfg -h off/on :: as admin, delete hiberfil.sys
msinfo32 :: info composants

schtasks :: task scheduler

robocopy "C:\Source" "E:\Destination" /E /PURGE :: Backup

copy "C:\file.txt" "D:\%date:/=-%_file.txt.bak" :: Variable substitution

icacls * /T /Q /C /RESET :: reset files permissions

handle, pskill, pslist... :: Sysinternals Process Utilities

:: Usual cleanup steps
- create a restoration point
- CCCleaner
- Malwarebytes (+ possibly HijackThis)
- AVG
- ProcessExplorer
- cleanmgr.exe
- Defrag
- désactiver l'indexation des disques
- chkdsk /r /f
- sfc /scannow :: restore system files
findstr /c:"[SR]" %windir%\logs\cbs\cbs.log >sfcdetails.txt :: to read CBS.Log

::Remove a file as admin :
::1- Take ownership of the files
takeown /f file
takeown /f directory /r
::2- Give yourself full rights on the file:
cacls file /G username:F
::3- Remove file
del file

services.msc :: Services windows

:: Default .dll owner : NT SERVICE\TrustedInstaller

Magnify.exe :: Loupe


::::::::::
:: Batch
:: :::::::
@echo off
title Whatever :: sets the terminal window title
cls :: clear console screan
set file=%1 :: set variable to be the first cmd-line argument
if exist %file del %file
:label
goto:label
echo %i >> %file
:: Loop variables have 2 restrictions: they are one-letters only and their % must be doubled in .bat files
for /l %%x in (1, 1, 100) do echo %%x
for /r %%f in (file_A file_B) do if exist "%%f" echo %%f :: paths are relative to the local dir
for /f "delims=" %%l in (%file%) do set /a counter+=1 :: /a => evaluate numeric expression
for /f "tokens=1,* delims=:" %%i in ('findstr /n /r . file.txt') do if %%i geq 10 if %%i leq 20 echo %%j

