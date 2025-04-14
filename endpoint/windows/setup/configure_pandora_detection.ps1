# Script de configuração para detecção do Pandora
$ErrorActionPreference = "Stop"
$LogFile = "C:\Program Files (x86)\ossec-agent\logs\pandora_setup.log"

function Write-Log {
    param($Message)
    $LogMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
    Add-Content -Path $LogFile -Value $LogMessage
    Write-Host $LogMessage
}

try {
    Write-Log "Iniciando configuração de detecção do Pandora..."

    # Baixar e instalar Sysmon se não estiver instalado
    if (!(Test-Path "C:\Windows\Sysmon.exe")) {
        Write-Log "Baixando Sysmon..."
        Invoke-WebRequest -Uri "https://download.sysinternals.com/files/Sysmon.zip" -OutFile "$env:TEMP\Sysmon.zip"
        Expand-Archive -Path "$env:TEMP\Sysmon.zip" -DestinationPath "$env:TEMP\Sysmon"
        
        Write-Log "Instalando Sysmon..."
        & "$env:TEMP\Sysmon\Sysmon64.exe" -accepteula -i "$PSScriptRoot\pandora_monitoring.xml"
    } else {
        Write-Log "Atualizando configuração do Sysmon..."
        & "C:\Windows\Sysmon.exe" -c "$PSScriptRoot\pandora_monitoring.xml"
    }

    # Configurar agente Wazuh
    $OssecConf = "C:\Program Files (x86)\ossec-agent\ossec.conf"
    Write-Log "Configurando agente Wazuh..."
    
    # Adicionar configurações de monitoramento
    $MonitoringConfig = @"
    <localfile>
        <location>Microsoft-Windows-Sysmon/Operational</location>
        <log_format>eventchannel</log_format>
    </localfile>

    <syscheck>
        <directories check_all="yes" realtime="yes">C:\Users\*\Downloads</directories>
        <directories check_all="yes" realtime="yes">C:\Users\*\Desktop</directories>
        <directories check_all="yes" realtime="yes">C:\Users\*\Documents</directories>
        <directories check_all="yes" realtime="yes">C:\Windows\System32\vssadmin.exe</directories>
        <directories check_all="yes" realtime="yes">C:\Windows\System32\wbadmin.exe</directories>
        <directories check_all="yes" realtime="yes">C:\Windows\System32\bcdedit.exe</directories>
    </syscheck>
"@

    if (!(Select-String -Path $OssecConf -Pattern "Microsoft-Windows-Sysmon/Operational" -Quiet)) {
        $Content = Get-Content $OssecConf
        $Content[($Content.Count - 1)] = $MonitoringConfig
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