:: USAGE: win_alert_powershell.bat $message $header
:: Can be called from WSL2: cmd.exe /c \pat`\to\win_alert_powershell.bat "$message" "$header"
@PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[console]::beep(600, 600);[System.Windows.MessageBox]::Show('%1', '%2')"