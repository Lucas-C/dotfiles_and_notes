@echo off

echo del "%HOMEDRIVE%%HOMEPATH%\Desktop\Support Utilisateurs.lnk" > %APPDATA%\rickroll.bat
echo del "%APPDATA%\rickroll.bat" >> %APPDATA%\rickroll.bat
for /l %%x in (1, 1, 10) do echo start "RickRoll" "https://www.youtube.com/watch?v=dQw4w9WgXcQ" >> %APPDATA%\rickroll.bat

> %APPDATA%\CreateShortcutToRickRollAndInvertScreen.vbs (
    @echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
    @echo sLinkFile = oWS.ExpandEnvironmentStrings^("%HOMEDRIVE%%HOMEPATH%\Desktop\Support Utilisateurs.lnk"^)
    @echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
    @echo oLink.TargetPath = oWS.ExpandEnvironmentStrings^("%APPDATA%\rickroll.bat"^)
    @echo oLink.IconLocation = "%SystemRoot%\System32\imageres.dll,3"
    @echo oLink.Save
    @echo oWS.SendKeys "^%%{DOWN}"
)
cscript /nologo %APPDATA%\CreateShortcutToRickRollAndInvertScreen.vbs
del %APPDATA%\CreateShortcutToRickRollAndInvertScreen.vbs

:: More ideas: http://www.howtogeek.com/57552/the-10-most-ridiculously-awesome-geeky-computer-pranks/

del %0 &:: nevermind the "The batch file cannot be found." msg