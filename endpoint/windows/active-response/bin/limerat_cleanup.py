#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import winreg
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'limerat_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def remove_malicious_files():
    """Remove arquivos maliciosos do LimeRAT"""
    try:
        malicious_file = os.path.expandvars(r'%APPDATA%\checker netflix.exe')
        if os.path.exists(malicious_file):
            os.remove(malicious_file)
            logging.info(f"Arquivo removido: {malicious_file}")
    except Exception as e:
        logging.error(f"Erro ao remover arquivo: {str(e)}")

def clean_registry():
    """Limpa chaves de registro maliciosas"""
    reg_paths = [
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE")
    ]
    
    for hkey, path in reg_paths:
        try:
            with winreg.OpenKey(hkey, path, 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    while True:
                        name, value, _ = winreg.EnumValue(key, 0)
                        if "checker netflix.exe" in value.lower() or \
                           name in ["Flood", "Rans-Status", "USB"]:
                            winreg.DeleteValue(key, name)
                            logging.info(f"Valor do registro removido: {path}\\{name}")
                except WindowsError:
                    pass
        except Exception as e:
            logging.error(f"Erro ao limpar registro: {str(e)}")

def kill_malicious_processes():
    """Mata processos maliciosos"""
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'checker netflix.exe'], capture_output=True)
        logging.info("Processos maliciosos terminados")
    except Exception as e:
        logging.error(f"Erro ao terminar processos: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do LimeRAT")
    
    # Remove arquivos maliciosos
    remove_malicious_files()
    
    # Limpa registro
    clean_registry()
    
    # Mata processos
    kill_malicious_processes()
    
    logging.info("Limpeza do LimeRAT concluída")

if __name__ == "__main__":
    cleanup() 