@echo off
:: Script de resposta ativa para análise YARA
setlocal EnableDelayedExpansion

:: Configurar variáveis
set YARA_PATH=C:\Program Files\yara
set RULES_PATH=C:\Program Files\ossec-agent\shared\yara
set LOG_FILE=C:\Program Files (x86)\ossec-agent\active-response\active-responses.log

:: Obter o caminho do arquivo a ser analisado
set FILE_PATH=%1

:: Verificar se o arquivo existe
if not exist "!FILE_PATH!" (
    echo %date% %time% yara.bat - Erro: Arquivo não encontrado: !FILE_PATH! >> "!LOG_FILE!"
    exit /b 1
)

:: Executar análise YARA
"!YARA_PATH!\yara64.exe" -w "!RULES_PATH!\peaklight.yar" "!FILE_PATH!" > nul 2>&1
if %errorlevel% equ 0 (
    echo %date% %time% yara.bat - Alerta: Malware Peaklight detectado em: !FILE_PATH! >> "!LOG_FILE!"
    del /f "!FILE_PATH!" >nul 2>&1
    if !errorlevel! equ 0 (
        echo %date% %time% yara.bat - Info: Arquivo malicioso removido com sucesso >> "!LOG_FILE!"
    ) else (
        echo %date% %time% yara.bat - Erro: Falha ao remover arquivo malicioso >> "!LOG_FILE!"
    )
)

exit /b 0 