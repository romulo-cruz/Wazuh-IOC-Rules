#!/usr/bin/env python3

import os
import sys
import json
import time
import subprocess
from datetime import datetime

# Constantes
LOG_FILE = "C:\\Program Files (x86)\\ossec-agent\\active-response\\log\\latrodectus_removal.log"
SUSPICIOUS_PATHS = [
    os.path.expandvars("%APPDATA%\\falsify_steward"),
    "C:\\Windows\\System32\\Tasks\\anxiety"
]

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {message}\n")

def kill_suspicious_processes():
    try:
        # Procurar e terminar processos suspeitos
        cmd = 'tasklist /FI "IMAGENAME eq confrontation_98065856.exe" /FO CSV /NH'
        output = subprocess.check_output(cmd, shell=True).decode()
        
        if "confrontation_98065856.exe" in output:
            subprocess.run(["taskkill", "/F", "/IM", "confrontation_98065856.exe"], capture_output=True)
            log("Processo malicioso terminado")
    except Exception as e:
        log(f"Erro ao terminar processo: {str(e)}")

def remove_persistence():
    try:
        # Remover tarefa agendada
        subprocess.run(["schtasks", "/delete", "/tn", "anxiety", "/f"], capture_output=True)
        log("Tarefa agendada 'anxiety' removida")
    except Exception as e:
        log(f"Erro ao remover persistência: {str(e)}")

def remove_files():
    for path in SUSPICIOUS_PATHS:
        try:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    for root, dirs, files in os.walk(path, topdown=False):
                        for name in files:
                            os.remove(os.path.join(root, name))
                        for name in dirs:
                            os.rmdir(os.path.join(root, name))
                    os.rmdir(path)
                log(f"Removido: {path}")
        except Exception as e:
            log(f"Erro ao remover {path}: {str(e)}")

def main():
    try:
        log("Iniciando remoção do Latrodectus")
        
        # Sequência de remoção
        kill_suspicious_processes()
        remove_persistence()
        remove_files()
        
        log("Remoção concluída com sucesso")
    except Exception as e:
        log(f"Erro durante a remoção: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 