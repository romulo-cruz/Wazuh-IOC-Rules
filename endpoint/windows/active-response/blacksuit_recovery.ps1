# Script de recuperação para BlackSuit Ransomware
param()

$ErrorActionPreference = "Stop"
$LogPath = "C:\Program Files (x86)\ossec-agent\active-response\log\blacksuit_recovery.log"

function Write-Log {
    param($Message)
    $LogMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
    Add-Content -Path $LogPath -Value $LogMessage
    Write-Host $LogMessage
}

function Restore-ShadowCopies {
    try {
        # Listar shadow copies disponíveis
        $shadows = Get-WmiObject Win32_ShadowCopy
        if ($shadows) {
            foreach ($shadow in $shadows) {
                $device = $shadow.DeviceObject + "\"
                Write-Log "Restaurando arquivos de $device"
                
                # Restaurar arquivos criptografados
                Get-ChildItem -Path "C:\" -Recurse -File -Filter "*.blacksuit" | ForEach-Object {
                    $originalPath = $_.FullName -replace "\.blacksuit$", ""
                    $shadowPath = Join-Path $device ($originalPath.Substring(3))
                    
                    try {
                        Copy-Item -Path $shadowPath -Destination $originalPath -Force
                        Remove-Item -Path $_.FullName -Force
                        Write-Log "Arquivo restaurado: $originalPath"
                    }
                    catch {
                        Write-Log "Erro ao restaurar arquivo $originalPath`: $_"
                    }
                }
            }
        }
        else {
            Write-Log "Nenhuma shadow copy encontrada"
        }
    }
    catch {
        Write-Log "Erro ao restaurar shadow copies: $_"
    }
}

function Remove-RansomNotes {
    $notePaths = @(
        "C:\PerfLogs\README.BlackSuit.txt",
        "C:\Temp\README.BlackSuit.txt",
        "C:\Users\*\AppData\Roaming\README.BlackSuit.txt",
        "C:\Users\*\AppData\Local\README.BlackSuit.txt",
        "C:\Users\*\README.BlackSuit.txt",
        "C:\ProgramData\README.BlackSuit.txt"
    )

    foreach ($path in $notePaths) {
        try {
            Remove-Item -Path $path -Force -ErrorAction SilentlyContinue
            Write-Log "Nota de resgate removida: $path"
        }
        catch {
            Write-Log "Erro ao remover nota de resgate $path`: $_"
        }
    }
}

try {
    Write-Log "Iniciando recuperação do BlackSuit Ransomware"
    Restore-ShadowCopies
    Remove-RansomNotes
    Write-Log "Recuperação concluída"
}
catch {
    Write-Log "Erro durante a recuperação: $_"
    exit 1
} 