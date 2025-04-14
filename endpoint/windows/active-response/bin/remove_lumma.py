#!/usr/bin/env python3

import os
import sys
import json
import time
import subprocess
from datetime import datetime

# Constantes
LOG_FILE = "C:\\Program Files (x86)\\ossec-agent\\active-response\\log\\lumma_removal.log"
SUSPICIOUS_PROCESSES = ["BitLockerToGo.exe", "GlobalCheats.exe"]
SUSPICIOUS_PATHS = [
    os.path.expandvars("%APPDATA%\\Microsoft\\Windows"),
    os.path.expandvars("%LOCALAPPDATA%\\Temp"),
    os.path.expandvars("%USERPROFILE%\\Downloads")
]

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {message}\n")

def kill_process(process_name):
    try:
        subprocess.run(["taskkill", "/F", "/IM", process_name], capture_output=True)
        log(f"Processo terminado: {process_name}")
        return True
    except Exception as e:
        log(f"Erro ao terminar processo {process_name}: {str(e)}")
        return False

def remove_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            log(f"Arquivo removido: {file_path}")
            return True
    except Exception as e:
        log(f"Erro ao remover arquivo {file_path}: {str(e)}")
    return False

def scan_and_remove():
    # Terminar processos suspeitos
    for process in SUSPICIOUS_PROCESSES:
        kill_process(process)

    # Procurar e remover arquivos suspeitos
    suspicious_extensions = [".exe", ".dll", ".tmp"]
    for path in SUSPICIOUS_PATHS:
        if os.path.exists(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if any(file.endswith(ext) for ext in suspicious_extensions):
                        file_path = os.path.join(root, file)
                        remove_file(file_path)

def main():
    try:
        log("Iniciando remoção do Lumma Stealer")
        scan_and_remove()
        log("Remoção concluída")
    except Exception as e:
        log(f"Erro durante a remoção: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 