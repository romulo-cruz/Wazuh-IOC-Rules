@echo off
setlocal enabledelayedexpansion

:: Configurar logging
set "LOG_FILE=%ProgramFiles(x86)%\ossec-agent\active-response\log\kuiper_cleanup.log"
set "TIMESTAMP=%date% %time%"

echo [%TIMESTAMP%] Iniciando limpeza do Kuiper >> "%LOG_FILE%"

:: Restaurar Windows Defender
powershell.exe -Command "Set-MpPreference -DisableRealtimeMonitoring $false" >> "%LOG_FILE%" 2>&1
echo [%TIMESTAMP%] Windows Defender reativado >> "%LOG_FILE%"

:: Remover notas de resgate
for %%d in (C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%d:\" (
        del /s /f /q "%%d:\README_TO_DECRYPT.txt" >nul 2>&1
    )
)
echo [%TIMESTAMP%] Notas de resgate removidas >> "%LOG_FILE%"

:: Restaurar shadow copies
vssadmin resize shadowstorage /for=C: /on=C: /maxsize=unbounded >nul 2>&1
echo [%TIMESTAMP%] Shadow storage restaurado >> "%LOG_FILE%"

:: Reiniciar serviços críticos
net start "Windows Defender Service" >nul 2>&1
net start "Windows Defender Firewall" >nul 2>&1
echo [%TIMESTAMP%] Serviços críticos reiniciados >> "%LOG_FILE%"

echo [%TIMESTAMP%] Limpeza do Kuiper concluída >> "%LOG_FILE%"
exit /b 0 