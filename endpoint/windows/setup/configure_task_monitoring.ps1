# Script de configuração para monitoramento de tarefas agendadas
$ErrorActionPreference = "Stop"
$LogFile = "C:\Program Files (x86)\ossec-agent\logs\task_monitoring_setup.log"

function Write-Log {
    param($Message)
    $LogMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
    Add-Content -Path $LogFile -Value $LogMessage
    Write-Host $LogMessage
}

try {
    Write-Log "Iniciando configuração de monitoramento de tarefas..."

    # Baixar e instalar Sysmon se não estiver instalado
    if (!(Test-Path "C:\Windows\Sysmon.exe")) {
        Write-Log "Baixando Sysmon..."
        Invoke-WebRequest -Uri "https://download.sysinternals.com/files/Sysmon.zip" -OutFile "$env:TEMP\Sysmon.zip"
        Expand-Archive -Path "$env:TEMP\Sysmon.zip" -DestinationPath "$env:TEMP\Sysmon"
        
        Write-Log "Instalando Sysmon..."
        & "$env:TEMP\Sysmon\Sysmon64.exe" -accepteula -i "$PSScriptRoot\sysmon_task_scheduler.xml"
    } else {
        Write-Log "Atualizando configuração do Sysmon..."
        & "C:\Windows\Sysmon.exe" -c "$PSScriptRoot\sysmon_task_scheduler.xml"
    }

    # Configurar script de resposta ativa
    Write-Log "Configurando script de resposta ativa..."
    $ARPath = "C:\Program Files (x86)\ossec-agent\active-response\bin"
    Copy-Item "$PSScriptRoot\analyze-scheduled-task.cmd" -Destination "$ARPath"
    icacls "$ARPath\analyze-scheduled-task.cmd" /grant "NT AUTHORITY\SYSTEM:(RX)"

    # Configurar agente Wazuh
    $OssecConf = "C:\Program Files (x86)\ossec-agent\ossec.conf"
    Write-Log "Configurando agente Wazuh..."
    
    # Adicionar monitoramento do Sysmon se não existir
    $SysmonConfig = @"
    <localfile>
        <location>Microsoft-Windows-Sysmon/Operational</location>
        <log_format>eventchannel</log_format>
    </localfile>
    <localfile>
        <location>logs\scheduled-tasks.log</location>
        <log_format>syslog</log_format>
    </localfile>
"@

    if (!(Select-String -Path $OssecConf -Pattern "Microsoft-Windows-Sysmon/Operational" -Quiet)) {
        $Content = Get-Content $OssecConf
        $Content[($Content.Count - 1)] = $SysmonConfig
        $Content += "</ossec_config>"
        Set-Content -Path $OssecConf -Value $Content
    }

    # Reiniciar serviços
    Write-Log "Reiniciando serviços..."
    Restart-Service -Name Sysmon64 -Force
    Restart-Service -Name "Wazuh Agent" -Force

    Write-Log "Configuração concluída com sucesso!"
} catch {
    Write-Log "ERRO: $_"
    exit 1
} 