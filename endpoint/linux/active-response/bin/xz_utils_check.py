#!/usr/bin/env python3

import subprocess
import json
import sys
import os
from datetime import datetime

# Configurações
LOG_FILE = "/var/ossec/logs/xz_utils_check.log"
VULNERABLE_VERSIONS = ["5.6.0", "5.6.1"]

def log_message(message):
    """Registra mensagem no arquivo de log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def get_xz_version():
    """Obtém a versão do XZ Utils instalada"""
    try:
        output = subprocess.check_output(["xz", "--version"], text=True)
        version = output.split()[3]
        return version
    except:
        return None

def check_liblzma():
    """Verifica a presença da biblioteca liblzma vulnerável"""
    suspicious_paths = [
        "/lib/liblzma.so.5.6.0",
        "/lib/liblzma.so.5.6.1",
        "/lib64/liblzma.so.5.6.0",
        "/lib64/liblzma.so.5.6.1"
    ]
    
    found_paths = []
    for path in suspicious_paths:
        if os.path.exists(path):
            found_paths.append(path)
    
    return found_paths

def check_ssh_config():
    """Verifica configurações SSH relevantes"""
    try:
        with open("/etc/ssh/sshd_config", "r") as f:
            config = f.read()
            issues = []
            
            if "PermitRootLogin yes" in config:
                issues.append("PermitRootLogin está habilitado")
            if "PasswordAuthentication yes" in config:
                issues.append("PasswordAuthentication está habilitado")
                
            return issues
    except:
        return ["Não foi possível verificar configuração SSH"]

def main():
    log_message("Iniciando verificação do XZ Utils")
    
    # Verificar versão
    version = get_xz_version()
    if version in VULNERABLE_VERSIONS:
        log_message(f"ALERTA: Versão vulnerável detectada: {version}")
    
    # Verificar biblioteca
    suspicious_libs = check_liblzma()
    if suspicious_libs:
        log_message(f"ALERTA: Bibliotecas suspeitas encontradas: {', '.join(suspicious_libs)}")
    
    # Verificar SSH
    ssh_issues = check_ssh_config()
    if ssh_issues:
        log_message(f"AVISO: Problemas na configuração SSH: {', '.join(ssh_issues)}")
    
    # Gerar relatório
    report = {
        "timestamp": datetime.now().isoformat(),
        "version": version,
        "vulnerable": version in VULNERABLE_VERSIONS,
        "suspicious_libs": suspicious_libs,
        "ssh_issues": ssh_issues
    }
    
    print(json.dumps(report))
    log_message("Verificação concluída")

if __name__ == "__main__":
    main() 