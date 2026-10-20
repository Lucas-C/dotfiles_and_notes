:: Script to shrink the WSL .vhdx file
:: I successfully won back 30GB the 1st time I used it
wsl --shutdown
if %errorlevel% neq 0 then pause
sc stop WSLService
if %errorlevel% neq 0 then pause
diskpart diskpart-shrink-wsl-vhdx.txt
:: This text file contains:
:: select vdisk file="path\to\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu_xxx\LocalState\ext4.vhdx"
:: attach vdisk readonly
:: compact vdisk
:: detach vdisk
