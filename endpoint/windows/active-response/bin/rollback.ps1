# Script de recuperação de arquivos
$RecoveryPath = "C:\Recovered_Files"
$LogFileDirectory = "C:\Program Files (x86)\ossec-agent\active-response\log"
$LogFile = Join-Path -Path $LogFileDirectory -ChildPath "rollback.log"

# Criar diretório de logs se não existir
if (-not (Test-Path -Path $LogFileDirectory)) {
    New-Item -Path $LogFileDirectory -ItemType Directory -Force
}

# Função para logging
function Log-Message {
    param (
        [string]$Message
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $LogFile -Value "$Timestamp - $Message"
    Write-Host "$Timestamp - $Message"
}

try {
    Log-Message "Iniciando processo de recuperação..."

    # Iniciar serviço VSS
    cmd /c sc config VSS start=Demand
    cmd /c net start VSS
    start-sleep 5
    Log-Message "Listando shadow copies..."
    
    # Obter volume shadow copy
    $ShadowCopyVolumes = C:\Windows\SysNative\WindowsPowerShell\v1.0\powershell.exe -c "Get-WmiObject -Query 'SELECT * FROM Win32_ShadowCopy' | Select-Object -ExpandProperty DeviceObject"

    if ($ShadowCopyVolumes.Count -gt 0) {
        $ShadowCopyVolume = $ShadowCopyVolumes[-1]
        Log-Message "Shadow Copy mais recente encontrada: $ShadowCopyVolume"
    } else {
        throw "Não foi possível encontrar Shadow Copy."
    }

    # Criar link simbólico
    $LinkPath = Join-Path -Path $RecoveryPath -ChildPath "backup"
    Log-Message "Criando link simbólico em $LinkPath..."

    if (Test-Path -Path $LinkPath) {
        Remove-Item -Path $LinkPath -Recurse -Force
    }

    $linkCmdOutput = cmd /c mklink /d "$LinkPath" "$ShadowCopyVolume\"
    Log-Message "Link simbólico criado: $linkCmdOutput"

    Write-Host "Restauração de arquivos concluída."
    "Wazuh_Ransomware_Protection: Restauração de arquivos concluída para $($env:computername) em $(Get-Date)" | 
    Out-File -FilePath "C:\Program Files (x86)\ossec-agent\active-response\active-responses.log" -Append -Encoding UTF8
}
catch {
    $ErrorMsg = $Error[0].ToString()
    Log-Message "Erro: $ErrorMsg"
    Write-Error "Ocorreu um erro: $ErrorMsg"
}
finally {
    # Desativar serviço VSS
    cmd /c sc config VSS start=disabled
    cmd /c net stop VSS
    Log-Message "Serviço VSS desativado..."
} 