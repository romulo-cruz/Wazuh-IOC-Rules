# Script de bloqueio para atividades maliciosas do PowerShell
param()

$ErrorActionPreference = "Stop"
$LogPath = "C:\Program Files (x86)\ossec-agent\active-response\log\powershell_block.log"

function Write-Log {
    param($Message)
    $LogMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
    Add-Content -Path $LogPath -Value $LogMessage
    Write-Host $LogMessage
}

function Block-MaliciousProcess {
    param($ProcessName)
    try {
        $Process = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue
        if ($Process) {
            Stop-Process -Name $ProcessName -Force
            Write-Log "Processo bloqueado: $ProcessName"
        }
    }
    catch {
        Write-Log "Erro ao bloquear processo $ProcessName`: $_"
    }
}

function Add-FirewallRule {
    param($RuleName, $Program)
    try {
        New-NetFirewallRule -DisplayName $RuleName -Direction Outbound -Program $Program -Action Block -Profile Any
        Write-Log "Regra de firewall adicionada: $RuleName"
    }
    catch {
        Write-Log "Erro ao adicionar regra de firewall: $_"
    }
}

try {
    Write-Log "Iniciando bloqueio de atividade maliciosa do PowerShell"
    
    # Bloquear processos suspeitos
    $SuspectProcesses = @(
        "powershell",
        "mshta"
    )

    foreach ($Process in $SuspectProcesses) {
        Block-MaliciousProcess -ProcessName $Process
    }

    # Adicionar regras de firewall
    Add-FirewallRule -RuleName "Bloquear PowerShell" -Program "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    Add-FirewallRule -RuleName "Bloquear MSHTA" -Program "C:\Windows\System32\mshta.exe"

    Write-Log "Bloqueio concluído"
}
catch {
    Write-Log "Erro durante o bloqueio: $_"
    exit 1
} 