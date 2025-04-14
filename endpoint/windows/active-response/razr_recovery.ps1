# Script de recuperação para ransomware Razr
param(
    [string]$Path = "C:\",
    [string]$Extension = ".raz"
)

$ErrorActionPreference = "Stop"
$LogPath = "C:\Program Files (x86)\ossec-agent\active-response\log\razr_recovery.log"

function Write-Log {
    param($Message)
    $LogMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
    Add-Content -Path $LogPath -Value $LogMessage
    Write-Host $LogMessage
}

function Get-LatestShadowCopy {
    param([string]$Path)
    try {
        $Shadow = Get-WmiObject Win32_ShadowCopy | Sort-Object InstallDate -Descending | Select-Object -First 1
        if ($Shadow) {
            $Device = $Shadow.DeviceObject + "\"
            return Join-Path $Device $Path.Substring(3)
        }
        return $null
    }
    catch {
        Write-Log "Erro ao obter shadow copy: $_"
        return $null
    }
}

function Restore-FromShadowCopy {
    param(
        [string]$SourcePath,
        [string]$DestPath
    )
    try {
        Copy-Item -Path $SourcePath -Destination $DestPath -Force
        Write-Log "Arquivo restaurado com sucesso: $DestPath"
        return $true
    }
    catch {
        Write-Log "Erro ao restaurar arquivo $DestPath`: $_"
        return $false
    }
}

try {
    Write-Log "Iniciando recuperação de arquivos criptografados pelo Razr"
    
    # Encontrar arquivos criptografados
    $EncryptedFiles = Get-ChildItem -Path $Path -Recurse -Filter "*$Extension" -ErrorAction SilentlyContinue
    
    if ($EncryptedFiles.Count -eq 0) {
        Write-Log "Nenhum arquivo criptografado encontrado"
        exit 0
    }

    Write-Log "Encontrados $($EncryptedFiles.Count) arquivos criptografados"

    foreach ($File in $EncryptedFiles) {
        $OriginalPath = $File.FullName.Replace($Extension, "")
        $ShadowPath = Get-LatestShadowCopy -Path $OriginalPath
        
        if ($ShadowPath -and (Test-Path $ShadowPath)) {
            if (Restore-FromShadowCopy -SourcePath $ShadowPath -DestPath $OriginalPath) {
                Remove-Item -Path $File.FullName -Force
            }
        }
        else {
            Write-Log "Não foi possível encontrar shadow copy para: $OriginalPath"
        }
    }
}
catch {
    Write-Log "Erro durante a recuperação: $_"
    exit 1
} 