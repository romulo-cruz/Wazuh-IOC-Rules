# Script de recuperação de arquivos via Volume Shadow Copy
param()

$ErrorActionPreference = "Stop"
$RecoveryPath = "C:\Recovered_Files"
$LogFile = "C:\Program Files (x86)\ossec-agent\active-response\log\rollback.log"

function Log-Message {
    param($Message)
    
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "$TimeStamp - $Message"
    Add-Content -Path $LogFile -Value $LogEntry
    Write-Host $LogEntry
}

try {
    Log-Message "Iniciando processo de recuperação de arquivos..."

    # Criar diretório de recuperação se não existir
    if (-not (Test-Path -Path $RecoveryPath)) {
        New-Item -ItemType Directory -Path $RecoveryPath -Force
        Log-Message "Diretório de recuperação criado: $RecoveryPath"
    }

    # Habilitar serviço VSS
    Log-Message "Habilitando serviço VSS..."
    cmd /c sc config VSS start=auto
    cmd /c net start VSS
    Start-Sleep -Seconds 5

    # Obter volume shadow copy mais recente
    Log-Message "Buscando shadow copies disponíveis..."
    $VssOutput = cmd /c vssadmin list shadows
    
    if ($VssOutput -match "Shadow Copy Volume:\s*(.+)") {
        $ShadowCopyVolume = $Matches[1].Trim()
        Log-Message "Shadow Copy encontrada: $ShadowCopyVolume"
    } else {
        throw "Não foi possível encontrar Shadow Copy Volume."
    }

    # Garantir que ShadowCopyVolume termine com barra
    if (-not $ShadowCopyVolume.EndsWith("\")) {
        $ShadowCopyVolume += "\"
    }

    # Criar link simbólico
    $LinkPath = Join-Path -Path $RecoveryPath -ChildPath "backup"
    Log-Message "Criando link simbólico em $LinkPath..."

    # Remover link existente se houver
    if (Test-Path -Path $LinkPath) {
        Remove-Item -Path $LinkPath -Recurse -Force
        Log-Message "Link simbólico anterior removido"
    }

    # Criar novo link
    $linkCmd = cmd /c mklink /d "$LinkPath" "$ShadowCopyVolume"
    Log-Message "Resultado do comando link: $linkCmd"

    # Verificar criação do link
    if (-not (Test-Path -Path $LinkPath)) {
        throw "Falha ao criar link simbólico em $LinkPath"
    }
    Log-Message "Link simbólico criado com sucesso: $LinkPath -> $ShadowCopyVolume"

    Write-Host "Recuperação de arquivos concluída."
    "Wazuh_Ransomware_Protection: Recuperação concluída para $($env:computername) em $(Get-Date)" | 
    Out-File -FilePath "C:\Program Files (x86)\ossec-agent\active-response\active-responses.log" -Append -Encoding UTF8
}
catch {
    $ErrorMsg = $Error[0].ToString()
    Log-Message "Erro: $ErrorMsg"
    Write-Error "Ocorreu um erro: $ErrorMsg"
}
finally {
    # Desabilitar VSS após uso
    cmd /c sc config VSS start=disabled
    cmd /c net stop VSS
    Start-Sleep -Seconds 5
    Log-Message "Serviço VSS desabilitado..."
} 