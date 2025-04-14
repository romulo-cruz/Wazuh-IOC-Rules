@echo off
setlocal enabledelayedexpansion

:: Configurar logging
set "LOG_FILE=%ProgramFiles(x86)%\ossec-agent\active-response\log\phobos_cleanup.log"
set "TIMESTAMP=%date% %time%"

echo [%TIMESTAMP%] Iniciando limpeza do Phobos >> "%LOG_FILE%"

:: Reativar Windows Defender
powershell.exe -Command "Set-MpPreference -DisableRealtimeMonitoring $false" >> "%LOG_FILE%" 2>&1
echo [%TIMESTAMP%] Windows Defender reativado >> "%LOG_FILE%"

:: Reativar firewall
netsh advfirewall set allprofiles state on >> "%LOG_FILE%" 2>&1
echo [%TIMESTAMP%] Firewall reativado >> "%LOG_FILE%"

:: Restaurar boot record
bcdedit /set {default} bootstatuspolicy displayallfailures >> "%LOG_FILE%" 2>&1
bcdedit /set {default} recoveryenabled yes >> "%LOG_FILE%" 2>&1
echo [%TIMESTAMP%] Boot record restaurado >> "%LOG_FILE%"

:: Remover executável malicioso
del /f /q "%AppData%\Local\phobos.exe" >> "%LOG_FILE%" 2>&1
echo [%TIMESTAMP%] Executável malicioso removido >> "%LOG_FILE%"

:: Remover chaves de registro maliciosas
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Phobos" /f >> "%LOG_FILE%" 2>&1
echo [%TIMESTAMP%] Chaves de registro removidas >> "%LOG_FILE%"

:: Remover arquivos da pasta Startup
del /f /q "%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup\phobos.exe" >> "%LOG_FILE%" 2>&1
echo [%TIMESTAMP%] Arquivos da pasta Startup removidos >> "%LOG_FILE%"

echo [%TIMESTAMP%] Limpeza do Phobos concluída >> "%LOG_FILE%"
exit /b 0 