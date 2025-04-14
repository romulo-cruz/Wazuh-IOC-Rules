# Script de limpeza para Snake Keylogger
param()

$ErrorActionPreference = "Stop"
$LogPath = "C:\Program Files (x86)\ossec-agent\active-response\log\snake_cleanup.log"

function Write-Log {
    param($Message)
    $LogMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
    Add-Content -Path $LogPath -Value $LogMessage
    Write-Host $LogMessage
}

function Remove-MaliciousFiles {
    $SuspectFiles = @(
        "WeENKtk.exe"
    )
    
    $Users = Get-ChildItem "C:\Users" -Directory
    foreach ($User in $Users) {
        foreach ($File in $SuspectFiles) {
            $RoamingPath = Join-Path $User.FullName "AppData\Roaming\$File"
            if (Test-Path $RoamingPath) {
                try {
                    Remove-Item -Path $RoamingPath -Force
                    Write-Log "Arquivo removido: $RoamingPath"
                }
                catch {
                    Write-Log "Erro ao remover arquivo $RoamingPath`: $_"
                }
            }
        }
    }
}

function Remove-DefenderExclusion {
    try {
        Remove-MpPreference -ExclusionPath "C:\Users\*\AppData\Roaming\WeENKtk.exe"
        Write-Log "Exclusão do Windows Defender removida"
    }
    catch {
        Write-Log "Erro ao remover exclusão do Windows Defender: $_"
    }
}

function Remove-ScheduledTask {
    try {
        Unregister-ScheduledTask -TaskName "Updates\WeENKtk" -Confirm:$false -ErrorAction SilentlyContinue
        Write-Log "Tarefa agendada removida"
    }
    catch {
        Write-Log "Erro ao remover tarefa agendada: $_"
    }
}

function Remove-RegistryKeys {
    $RegistryPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\Updates\WeENKtk"
    if (Test-Path $RegistryPath) {
        try {
            Remove-Item -Path $RegistryPath -Recurse -Force
            Write-Log "Chaves de registro removidas"
        }
        catch {
            Write-Log "Erro ao remover chaves de registro: $_"
        }
    }
}

try {
    Write-Log "Iniciando limpeza do Snake Keylogger"
    Remove-MaliciousFiles
    Remove-DefenderExclusion
    Remove-ScheduledTask
    Remove-RegistryKeys
    Write-Log "Limpeza concluída"
}
catch {
    Write-Log "Erro durante a limpeza: $_"
    exit 1
} 