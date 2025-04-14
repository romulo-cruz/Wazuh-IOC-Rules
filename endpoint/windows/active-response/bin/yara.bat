@echo off
setlocal enableDelayedExpansion

:: Configurar caminhos
set "LOG_FILE=%programfiles(x86)%\ossec-agent\active-response\active-responses.log"
set "YARA_EXE=%programfiles(x86)%\ossec-agent\active-response\bin\yara\yara64.exe"
set "YARA_RULES=%programfiles(x86)%\ossec-agent\active-response\bin\yara\rules\mint_stealer.yar"

:: Ler entrada JSON
set input=
for /f "delims=" %%a in ('PowerShell -command "$logInput = Read-Host; Write-Output $logInput"') do (
    set input=%%a
)

:: Extrair caminho do arquivo
set "JSON_FILE=%programfiles(x86)%\ossec-agent\active-response\stdin.txt"
echo %input% > "%JSON_FILE%"
for /f "tokens=* usebackq" %%F in (`PowerShell -Nop -C "(Get-Content '%JSON_FILE%'|ConvertFrom-Json).parameters.alert.syscheck.path"`) do (
    set "SCAN_FILE=%%F"
)

:: Executar varredura YARA
echo [%date% %time%] Iniciando varredura YARA em: %SCAN_FILE% >> "%LOG_FILE%"
for /f "delims=" %%a in ('powershell -command "& \"%YARA_EXE%\" \"%YARA_RULES%\" \"%SCAN_FILE%\""') do (
    echo wazuh-yara: INFO - Resultado da varredura: %%a >> "%LOG_FILE%"
    
    :: Remover arquivo malicioso
    del /f "%SCAN_FILE%"
    echo wazuh-yara: INFO - Arquivo removido com sucesso: %%a >> "%LOG_FILE%"
)

exit /b 