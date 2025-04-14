#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'hoaxshell_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def kill_suspicious_powershell():
    """Mata processos PowerShell suspeitos"""
    try:
        # Busca processos PowerShell com conexões de rede
        ps_cmd = """
        Get-NetTCPConnection | 
        Where-Object { $_.OwningProcess -in (Get-Process powershell).Id } |
        Select-Object OwningProcess, RemoteAddress, RemotePort
        """
        
        output = subprocess.check_output(['powershell', '-Command', ps_cmd], 
                                      capture_output=True).decode()
        
        for line in output.splitlines():
            if line.strip():
                try:
                    pid = line.split()[0]
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    logging.info(f"Processo PowerShell terminado: PID {pid}")
                except:
                    continue
    except Exception as e:
        logging.error(f"Erro ao terminar processos PowerShell: {str(e)}")

def block_connections():
    """Bloqueia conexões suspeitas no firewall"""
    try:
        # Adiciona regra para bloquear PowerShell
        fw_cmd = """
        New-NetFirewallRule -DisplayName "Block PowerShell Network Access" `
        -Direction Outbound `
        -Program "%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" `
        -Action Block
        """
        
        subprocess.run(['powershell', '-Command', fw_cmd], capture_output=True)
        logging.info("Regra de firewall adicionada para bloquear PowerShell")
    except Exception as e:
        logging.error(f"Erro ao configurar firewall: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do HoaxShell")
    
    # Mata processos suspeitos
    kill_suspicious_powershell()
    
    # Bloqueia conexões
    block_connections()
    
    logging.info("Limpeza do HoaxShell concluída")

if __name__ == "__main__":
    cleanup() 