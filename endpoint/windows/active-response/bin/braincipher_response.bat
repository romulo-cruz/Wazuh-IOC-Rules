@echo off
SET LOG_FILE=C:\Program Files (x86)\ossec-agent\active-response\active-responses.log

echo %date% %time% BrainCipher_Response: Iniciando resposta ativa >> %LOG_FILE%

REM Restaurar serviço VSS
sc config VSS start= auto
net start VSS

REM Criar ponto de restauração
wmic.exe /Namespace:\\root\default Path SystemRestore Call CreateRestorePoint "Wazuh Protection Point", 100, 7

REM Bloquear execução do DllHost com CLSID suspeito
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\dllhost.exe" /v "RestrictedClsid" /t REG_MULTI_SZ /d "{3E5FC7F9-9A51-4367-9063-A120244FBEC7}" /f

echo %date% %time% BrainCipher_Response: Medidas de proteção aplicadas >> %LOG_FILE% 