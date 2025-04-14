# Script de limpeza para BLX Stealer
param()

$ErrorActionPreference = "Stop"
$LogPath = "C:\Program Files (x86)\ossec-agent\active-response\log\blx_cleanup.log"

function Write-Log {
    param($Message)
    $LogMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
    Add-Content -Path $LogPath -Value $LogMessage
    Write-Host $LogMessage
}

function Remove-MaliciousFiles {
    $SuspectFiles = @(
        "temp.ps1",
        "decrypted_executable.exe"
    )
    
    $Locations = @(
        "$env:TEMP",
        "$env:LOCALAPPDATA\Temp",
        "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
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

function Stop-MaliciousProcesses {
    $SuspectProcesses = @(
        "decrypted_executable"
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
    Write-Log "Iniciando limpeza do BLX Stealer"
    Stop-MaliciousProcesses
    Remove-MaliciousFiles
    Write-Log "Limpeza concluída"
}
catch {
    Write-Log "Erro durante a limpeza: $_"
    exit 1
} 