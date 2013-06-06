F7 in cmd.exe -> history

where <cmd> :: 'which' equivalent
powercfg -h off/on :: as admin, delete hiberfil.sys
msinfo32 :: info composants

chkdsk
sfc /scannow :: restore system files
findstr /c:"[SR]" %windir%\logs\cbs\cbs.log >sfcdetails.txt :: to read CBS.Log

::Remove a file as admin :
::1- Take ownership of the files
takeown /f file
takeown /f directory /r
::2- Give yourself full rights on the file:
cacls file /G username:F
::3- Remove file
del file

:: Default .dll owner : NT SERVICE\TrustedInstaller
