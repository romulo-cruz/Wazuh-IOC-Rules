@echo off
SETLOCAL EnableDelayedExpansion

:: Configuração de logging
SET logFile="%OSSEC_HOME%\logs\scheduled-tasks.log"

:: Receber parâmetros do Wazuh
SET alert_file=%1
SET alert_json=%2

:: Extrair nome da tarefa do alerta
FOR /F "tokens=* USEBACKQ" %%F IN (`type %alert_file% ^| findstr /C:"TaskCache\Tree"`) DO (
    SET task_path=%%F
)

:: Extrair nome da tarefa do caminho
FOR %%i IN ("%task_path%") DO SET taskName=%%~nxi

:: Analisar tarefa usando PowerShell
powershell.exe -ExecutionPolicy Bypass -Command "& {Import-Module ScheduledTasks; $task = Get-ScheduledTask | where TaskName -EQ '%taskName%'; $jsonTask = $task.Actions | ConvertTo-Json -Compress; try{$stream = [System.IO.StreamWriter]::new('%logFile%', $true); '{\"ScheduledTaskAR\": ' + $jsonTask + ', \"TaskName\": \"%taskName%\"}' | ForEach-Object{ $stream.WriteLine($_) }}finally{$stream.close()}; exit}"

ENDLOCAL 