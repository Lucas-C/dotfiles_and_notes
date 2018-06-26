:: Recipe from: https://superuser.com/a/191068/255048
@ECHO OFF
:loop
  cls
  %*
  C:\Windows\System32\timeout.exe /t 5 > NUL
goto loop
