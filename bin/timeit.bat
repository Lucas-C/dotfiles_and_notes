:: Close equivalent of UNIX "time" command
:: This program accepts a single string as parameter,
:: so if you need pass arguments, enclose them in double quotes
:: Surce: https://superuser.com/a/228062/255048
@echo off
echo %time% < nul
cmd /c %1
echo %time% < nul