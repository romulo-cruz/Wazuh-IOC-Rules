#!/usr/bin/env python3

import json
import sys
import os
import subprocess
import time

# Constantes
LOG_FILE = "C:\\Program Files (x86)\\ossec-agent\\active-response\\log\\chavecloak_removal.log"
LIGHTSHOT_PATHS = [
    os.path.expandvars("%AppData%\\Skillbrains\\lightshot\\5.5.0.7\\Lightshot.exe"),
    os.path.expandvars("%AppData%\\Skillbrains\\lightshot\\5.5.0.7\\Lightshot.dll")
]

def write_log(message):
    """Escreve mensagem no arquivo de log"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

def remove_registry_key():
    """Remove chave de registro de persistência"""
    try:
        cmd = 'reg delete "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v "Lightshot" /f'
        subprocess.run(cmd, shell=True, check=True)
        write_log("Chave de registro removida com sucesso")
        return True
    except subprocess.CalledProcessError:
        write_log("Erro ao remover chave de registro")
        return False

def kill_processes():
    """Finaliza processos relacionados ao CHAVECLOAK"""
    try:
        subprocess.run('taskkill /F /IM "Lightshot.exe"', shell=True)
        write_log("Processos finalizados com sucesso")
        return True
    except subprocess.CalledProcessError:
        write_log("Erro ao finalizar processos")
        return False

def remove_files():
    """Remove arquivos do CHAVECLOAK"""
    success = True
    for path in LIGHTSHOT_PATHS:
        try:
            if os.path.exists(path):
                os.remove(path)
                write_log(f"Arquivo removido: {path}")
        except Exception as e:
            write_log(f"Erro ao remover arquivo {path}: {str(e)}")
            success = False
    return success

def main():
    write_log("Iniciando remoção do CHAVECLOAK")
    
    # Finalizar processos
    kill_processes()
    
    # Remover persistência
    remove_registry_key()
    
    # Remover arquivos
    if remove_files():
        write_log("Remoção do CHAVECLOAK concluída com sucesso")
    else:
        write_log("Erros durante a remoção do CHAVECLOAK")

if __name__ == "__main__":
    main() 