# Script de limpeza para malware DeerStealer
param()

$ErrorActionPreference = "Stop"
$LogPath = "C:\Program Files (x86)\ossec-agent\active-response\log\deerstealer_cleanup.log"

function Write-Log {
    param($Message)
    $LogMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
    Add-Content -Path $LogPath -Value $LogMessage
    Write-Host $LogMessage
}

function Remove-MaliciousFiles {
    $SuspectFiles = @(
        "skotes.exe",
        "ActiveISO.exe",
        "sxqnmytm.exe",
        "DllHost.exe",
        "ELEVATION_SERVICE.EXE"
    )
    
    $Locations = @(
        "$env:TEMP",
        "$env:LOCALAPPDATA\Temp",
        "$env:APPDATA\Local\Temp"
    )

    foreach ($Location in $Locations) {
        foreach ($File in $SuspectFiles) {
            $Path = Join-Path $Location $File
            if (Test-Path $Path) {
                try {
                    Remove-Item -Path $Path -Force
                    Write-Log "Arquivo removido: $Path"
                }
                catch {
                    Write-Log "Erro ao remover arquivo $Path`: $_"
                }
            }
        }
    }
}

function Remove-RegistryKeys {
    $RegistryPaths = @(
        "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders",
        "HKLM:\System\CurrentControlSet\Services\bam\State",
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion"
    )

    $SuspectKeys = @(
        "skotes",
        "ActiveISO",
        "sxqnmytm",
        "DllHost"
    )

    foreach ($Path in $RegistryPaths) {
        if (Test-Path $Path) {
            foreach ($Key in $SuspectKeys) {
                try {
                    Remove-Item -Path "$Path\$Key" -Recurse -Force -ErrorAction SilentlyContinue
                    Write-Log "Chave de registro removida: $Path\$Key"
                }
                catch {
                    Write-Log "Erro ao remover chave de registro $Path\$Key`: $_"
                }
            }
        }
    }
}

function Stop-MaliciousProcesses {
    $SuspectProcesses = @(
        "skotes",
        "ActiveISO",
        "sxqnmytm",
        "DllHost"
    )

    foreach ($Process in $SuspectProcesses) {
        try {
            Stop-Process -Name $Process -Force -ErrorAction SilentlyContinue
            Write-Log "Processo interrompido: $Process"
        }
        catch {
            Write-Log "Erro ao interromper processo $Process`: $_"
        }
    }
}

try {
    Write-Log "Iniciando limpeza do DeerStealer"
    Stop-MaliciousProcesses
    Remove-MaliciousFiles
    Remove-RegistryKeys
    Write-Log "Limpeza concluída"
}
catch {
    Write-Log "Erro durante a limpeza: $_"
    exit 1
} 