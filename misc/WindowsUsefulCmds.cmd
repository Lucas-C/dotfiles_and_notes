@echo "This file is not supposed to be executed" & pause & exit &:: this is an inline comment

Use .cmd > .bat : http://stackoverflow.com/questions/148968/windows-batch-files-bat-vs-cmd

<CMD>+R &:: command launcher, shell:startup -> open folder listing progs to launch at startup
F8 at start-up &:: Safe mode / Mode sans echec

chcp 65001 in cmd.exe &:: -> support for UTF-8
F7 in cmd.exe -> history &:: BUT better use Cmder or at least PowerShell ISE
!!WARNING!! Cmder define HOME, PATH, TMP & TEMP env variables with Unix-like paths
Cmder conf file: %CMDER_ROOT%\vendor\init.bat
@if not defined CMDER_START CMDER_START = D:\code

@set PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin

@set "PATH=%PATH%;C:\Program Files (x86)\Mozilla Firefox"

@set PATH=%PATH%;%TOOLS%\Python34\Scripts
@set PATH=%PATH%;%TOOLS%\Python27\Scripts
@set PATH=%PATH%;%APPDATA%\Python\Scripts

@set ANT_HOME=%TOOLS%\apache-ant-1.9.7
@set PATH=%PATH%;%ANT_HOME%\bin

@set GROOVY_HOME=%TOOLS%\Groovy-2.4.8
@set PATH=%PATH%;%GROOVY_HOME%\bin
@set PATH=%PATH%;%TOOLS%\gradle-3.3\bin

@set PHP_HOME=%TOOLS%\php-5.6.8
@set PATH=%PATH%;%APPDATA%\Composer\vendor

@set PATH=%PATH%;%APPDATA%\npm

powershell -Command "($env:Path).Replace(';',\"`n\")" &:: echo %PATH% on separate lines

:: config\aliases
l=ls --sort=extension --classify --dereference --color=always $*
ll=ls --sort=extension --classify --dereference --color=always -l --almost-all --human-readable $*


<CMD>+Left/Right &:: Vertically maximize a windows on the side
<CTRL>+<ALT>+<UP> &:: Invert screen upside down

cmd /c mklink &:: call cmd.exe builtins, e.g. the symlinker
subst Z: C:\path\to\wonderland &:: mount / creates a virtual drive Z pointing to the directory given

pkgmgr /iu:"TelnetClient" &:: install `telnet` command. Also available: TelnetServer, DNS-Server-Tools, SimpleTCP for echo & daytime - Alt: dism /online /Enable-Feature /FeatureName:TelnetClient
https://github.com/matt-kimball/mtr/releases &:: Windows binaries for a traceroute-like

wmic process where "ProcessID=9760" list <:: OR: get CommandLine, ExecutablePath - cf. https://blogs.technet.microsoft.com/askperf/2012/02/17/useful-wmic-queries/ : baseboard bios bootconfig cdrom computersystem cpu datafile dcomapp desktop desktopmonitor diskdrive diskquota environment fsdir group idecontroller irq job loadorder logicaldisk memcache memlogical memphysical netclient netlogin netprotocol netuse nic nicconfig nicconfig nicconfig nicconfig ntdomain ntevent ntevent ntevent onboarddevice os os pagefile pagefileset partition printer printjob process product qfe quotasetting recoveros Registry scsicontroller server service share sounddev startup sysaccount sysdriver systemenclosure systemslot tapedrive timezone useraccount memorychip

where %cmd% &:: UNIX 'which' equivalent
ipconfig /displaydns

:: Windows Performance Toolkit, also inc. xbootmgr - TUTOS: http://www.msfn.org/board/topic/140263-how-to-get-the-cause-of-high-cpu-usage-by-dpc-interrupt/ - http://www.msfn.org/board/topic/140264-how-to-get-the-cause-of-high-cpu-usage-caused-by-apps/
xperf -on latency -stackwalk profile
xperf -d latency.etl
wtrace :: strace-like based on Event Tracing for Windows
userdump %pid% :: download: https://www.microsoft.com/en-us/download/details.aspx?id=4060

powercfg -h off/on &:: as admin, delete hiberfil.sys
schtasks &:: task scheduler
msinfo32 &:: info computer composants
msconfig &:: System Configuration -> can disable or re-enable software, device drivers and Windows services that run at startup, or change boot parameters
tasklist /svc &:: list Service Host (svchost.exe) services running, with their PIDs
services.msc &:: Services windows
magnify &:: Loupe
cmd | clip &:: copy to clipboard
regsvr32 %dll_file% &:: register dll
vssadmin list shadows &:: list available Volume Shadow Copies aka restore points, cf. http://superuser.com/a/165576)
mstsc &:: builtin but less secure TeamViewer-like
secpol.msc &:: Security Policy Editor -> can for example gives permision to a user to create symlinks
rundll32 sysdm.cpl,EditEnvironmentVariables &:: user env variables
rundll32 "C:\Program Files\Windows Photo Viewer\PhotoViewer.dll" ImageView_Fullscreen $path_to_img_without_quotes &:: Open Windows Image Viewer

upx -9 my_homemade_cmd.exe &:: executable packer/compressor/optimizer

nssm64.exe edit service_name &:: then nssm64.exe start service_name - Powerful wrapper around builtin sc create service_name binpath= c:\bla\bla\bla.exe start= auto type= own

robocopy /MIR "C:\Source" "E:\Destination" /LOG:robocopy.log /XD C:\Dir\To\Exclude &:: Backup + handle filepaths over 260 chars

psr &:: builtin users action recorder - Also: LICEcap to record actions as a GIF

dir %WINDIR%\Microsoft.Net\Framework\v* /O:-N /B &:: Check .NET version
:: Disable Java updater installiing Ask search bar
reg add HKLM\software\javasoft /v "SPONSORS" /t REG_SZ /d "DISABLE" /f
reg add HKLM\SOFTWARE\Wow6432Node\JavaSoft /v "SPONSORS" /t REG_SZ /d "DISABLE" /f

icacls * /T /C /RESET &:: reset files permissions - Also: /setowner %UserDomain%\%UserName% /T
:: Default .dll owner : NT SERVICE\TrustedInstaller
:: In case some files are owned by System, and you modify their owner / permissions: -> tip from: http://eurekamoment.eu/?p=737
psexec -i -s -d cmd &:: "run as" System user
takeown /a /r /f pita_directory &:: recurively give ownership of files to Admin

junction (directory symbolic links), pskill, pslist, TCPView... &:: Sysinternals Process Utilities
handle.exe -a | grep ': Key\|pid:' | grep 'COMPONENTS\|pid:' | grep -B1 'COMPONENTS' &:: Find all PIDs of processes using RegKeys containing 'COMPONENTS'

WinSCP / SFTP Net Drive &:: GUI explorer / folder mounting for SCP/FTP/SFTP access

Windows Master Control Panel shortcut: {ED7BA470-8E54-465E-825C-99712043E01C}

::: Usual cleanup steps
- create a restoration point
- cleanmgr.exe &:: Click the Clean up System Files button & enable the Windows Update Cleanup option !
- CCCleaner
- Malwarebytes (+ possibly HijackThis)
- WinDirStat / SpaceMonger
- Microsoft Securit Scanner & Microsoft Security Essentials
- Defrag
- désactiver l'indexation des disques
- perfmon.exe /res / resmon.exe / Sysinternals ProcessExplorer (select File > "Show Details for All Processes" to display network usage)
- Farbar Service Scanner : http://www.bleepingcomputer.com/download/farbar-service-scanner/dl/62

::: Deeper clean-up/checks
sfc /scannow &:: To restore system files
chkdsk /r /f
:: CheckSUR : check system is up-to-date and installation conform aka KB947821 - http://technet.microsoft.com/en-us/library/ee619779%28WS.10%29.aspx
DISM.exe /Online /Cleanup-image /Scanhealth &:: on Win7, one needs to run KB947821.msu
:: -> when you run this command, DISM uses Windows Update to provide the files that are required to fix corruptions. However, if your Windows Update client is already broken, use a running Windows installation as the repair source, or use a Windows side-by-side folder from a network share or from a removable media, such as the Windows DVD, as the source of the files. To do this, run the following command instead:
DISM.exe /Online /Cleanup-Image /RestoreHealth /Source:C:\RepairSource\Windows /LimitAccess
findstr /c:"[SR]" %windir%\logs\cbs\cbs.log >sfcdetails.txt &:: to read CBS.Log

::: Install Windows Update .msu without looking for updates
sc query wuauserv | find "RUNNING"  &:: check that it is running (it restarts every minute or so)
net stop wuauserv  &:: disable the service before executing the .msu

::: Remove a file as admin :
:: 1- Take ownership of the files
takeown /f file
takeown /f directory /r
:: 2- Give yourself full rights on the file:
cacls file /G username:F
:: 3- Remove file
del file

assoc .py :: get the description of a file extension / protocol
ftype http=... :: associate program with file extension / protocol
SetUserFTA / GetUserFTA / SetDefaultBrowser :: for Windows 10 - cf. http://kolbi.cz/blog/?p=346

"L'ordinal 459 est introuvable dans la bibliothèque de liens dynamiques urlmon.dll" -> uninstall MAJ KB2847204


<############
## PowerShell
############>
Remove-Item $file
Get-Help Remove-Item -full
Get-Service | ConvertTo-HTML -Property Name, Status > C:\services.htm
Get-Service | Select-Object Name, Status | Export-CSV c:\service.csv
Get-EventLog -Log "Application"
Get-Process # list processes
Stop-Process -Name notepad # or -ID 2668
Get-Acl $file | Format-List

#FROM: https://software.intel.com/en-us/blogs/2014/06/17/giving-powershell-a-persistent-history-of-commands + include how to have a persistent cmds history
set-executionpolicy remotesigned
(new-object Net.WebClient).DownloadString("http://psget.net/GetPsGet.ps1") | iex
import-module PsGet
install-module PsUrl
install-module PSReadline

PSCX # PowerShell Community Extensions
iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1')) # install chocolatey - Some pkgs: https://github.com/berdario/dotfiles/blob/master/chocsoftware.ps1

(New-Object –ComObject SAPI.SPVoice).Speak(“This is a test”)
Add-Type -AssemblyName System.speech; $speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speaker.Speak(“This is a test”)

Get-Process -Name cleanmgr,dismhost -ErrorAction SilentlyContinue | Wait-Process
CleanMgr automation script: http://stackoverflow.com/a/35214197/636849

How to bypass the PowerShell execution policy : https://blog.netspi.com/15-ways-to-bypass-the-powershell-execution-policy/


::::::::::
:: Batch
::::::::::
:: Some Batch internals horrors: http://blog.nullspace.io/batch.html
@echo off
title Whatever &:: sets the terminal window title
cls &:: clear console screan
set file=%1 &:: set variable to be the first cmd-line argument
if exist %file% del %file%
echo %file% >> %file%
copy "C:\file.txt" "D:\%date:/=-%_file.txt.bak" &:: Variable substitution
:label
goto:label
:: Loop variables have 2 restrictions: they are one-letters only and their % must be doubled in .bat files
for /l %%x in (1, 1, 100) do echo %%x
for /r %%f in (file_A file_B) do if exist "%%f" echo %%f &:: paths are relative to the local dir
for /f "delims=" %%l in (%file%) do set /a counter+=1 &:: /a => evaluate numeric expression
for /f "tokens=1,* delims=:" %%i in ('findstr /n /r . file.txt') do if %%i geq 10 if %%i leq 20 echo %%j

attrib filename +s +h &:: Set as hidden file
bitsadmin /transfer Prank /download /priority normal http://someurl.com %PWD%
start "webpage name" "http://someurl.com" &:: open with default browser

:foo   - here starts a function identified by its label
echo.  FOO
goto:eof

call:foo


'''''''''''''
'' VBScript
'''''''''''''
WScript.CreateObject("WScript.Shell").SendKeys "^%{DOWN}"
CreateObject("SAPI.SpVoice").speak "Hello"
