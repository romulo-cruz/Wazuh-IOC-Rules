#!/usr/bin/env python3

import json
import sys
import os
import subprocess
import time
from datetime import datetime

# Configurações
LOG_FILE = "/var/ossec/logs/active-response/lotl_response.log"
BACKUP_DIR = "/var/ossec/backups"

def log_message(message):
    """Registra mensagem no arquivo de log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def backup_critical_file(filepath):
    """Cria backup de arquivo crítico"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    filename = os.path.basename(filepath)
    backup_path = f"{BACKUP_DIR}/{filename}.{int(time.time())}.bak"
    
    try:
        subprocess.run(["cp", "-p", filepath, backup_path], check=True)
        log_message(f"Backup criado: {backup_path}")
        return True
    except subprocess.CalledProcessError:
        log_message(f"Erro ao criar backup de {filepath}")
        return False

def check_suspicious_processes():
    """Verifica e termina processos suspeitos"""
    suspicious_patterns = [
        "ddexec.sh",
        "curl.*|.*bash",
        "base64.*|.*bash"
    ]
    
    for pattern in suspicious_patterns:
        try:
            cmd = f"ps aux | grep -E '{pattern}' | grep -v grep | awk '{{print $2}}'"
            pids = subprocess.check_output(cmd, shell=True).decode().strip()
            
            if pids:
                for pid in pids.split('\n'):
                    subprocess.run(["kill", "-9", pid], check=True)
                    log_message(f"Processo suspeito terminado: PID {pid}")
        except subprocess.CalledProcessError:
            continue

def restore_passwd_file():
    """Restaura arquivo passwd se modificado"""
    if os.path.exists("/etc/passwd.bak"):
        try:
            subprocess.run(["cp", "-p", "/etc/passwd.bak", "/etc/passwd"], check=True)
            log_message("Arquivo passwd restaurado do backup")
            return True
        except subprocess.CalledProcessError:
            log_message("Erro ao restaurar arquivo passwd")
            return False
    return False

def main():
    log_message("Iniciando resposta a ataque LOTL")
    
    # Backup de arquivos críticos
    critical_files = ["/etc/passwd", "/etc/shadow", "/etc/group"]
    for file in critical_files:
        backup_critical_file(file)
    
    # Verificar e terminar processos suspeitos
    check_suspicious_processes()
    
    # Restaurar passwd se necessário
    if os.path.exists("/etc/passwd"):
        restore_passwd_file()
    
    log_message("Resposta a ataque LOTL concluída")

if __name__ == "__main__":
    main() 