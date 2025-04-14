@echo off
setlocal enableDelayedExpansion

:: Configurar logging
set "LOG_FILE=%ProgramFiles(x86)%\ossec-agent\active-response\log\daolpu_cleanup.log"

echo [%date% %time%] Iniciando limpeza do Daolpu >> "%LOG_FILE%"

:: Terminar processos suspeitos
taskkill /F /IM "daolpu.exe" 2>NUL
echo [%date% %time%] Tentativa de terminar processos maliciosos >> "%LOG_FILE%"

:: Remover arquivos
del /F /Q "%TEMP%\result.txt" 2>NUL
echo [%date% %time%] Tentativa de remover arquivo result.txt >> "%LOG_FILE%"

:: Verificar navegadores
set "CHROME_PATH=%LOCALAPPDATA%\Google\Chrome\User Data"
set "EDGE_PATH=%LOCALAPPDATA%\Microsoft\Edge\User Data"
set "FIREFOX_PATH=%APPDATA%\Mozilla\Firefox\Profiles"

:: Backup e limpeza do Chrome
if exist "%CHROME_PATH%" (
    echo [%date% %time%] Realizando backup e limpeza do Chrome >> "%LOG_FILE%"
    xcopy /E /I "%CHROME_PATH%" "%CHROME_PATH%_backup" > NUL
    del /F /Q "%CHROME_PATH%\Default\Login Data" 2>NUL
    del /F /Q "%CHROME_PATH%\Default\Cookies" 2>NUL
)

:: Backup e limpeza do Edge
if exist "%EDGE_PATH%" (
    echo [%date% %time%] Realizando backup e limpeza do Edge >> "%LOG_FILE%"
    xcopy /E /I "%EDGE_PATH%" "%EDGE_PATH%_backup" > NUL
    del /F /Q "%EDGE_PATH%\Default\Login Data" 2>NUL
    del /F /Q "%EDGE_PATH%\Default\Cookies" 2>NUL
)

echo [%date% %time%] Limpeza do Daolpu concluída >> "%LOG_FILE%"
exit /b 0 