#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import winreg
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'amadey_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def remove_malicious_files():
    """Remove arquivos maliciosos do Amadey"""
    malicious_files = [
        os.path.expandvars(r'%APPDATA%\clip64.dll'),
        os.path.expandvars(r'%APPDATA%\cred64.dll'),
        os.path.expandvars(r'%LOCALAPPDATA%\Temp\*.exe'),
        os.path.expandvars(r'C:\Windows\System32\Tasks\*.exe')
    ]
    
    for file_path in malicious_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Arquivo removido: {file_path}")
        except Exception as e:
            logging.error(f"Erro ao remover arquivo {file_path}: {str(e)}")

def remove_registry_persistence():
    """Remove chaves de registro de persistência"""
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteValue(key, "Startup")
            logging.info("Chave de registro de persistência removida")
    except Exception as e:
        logging.error(f"Erro ao remover chave do registro: {str(e)}")

def kill_malicious_processes():
    """Mata processos relacionados ao Amadey"""
    try:
        processes = ['rundll32.exe']
        for proc in processes:
            subprocess.run(['taskkill', '/F', '/IM', proc], capture_output=True)
            logging.info(f"Processo terminado: {proc}")
    except Exception as e:
        logging.error(f"Erro ao terminar processos: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do Amadey")
    
    # Remove arquivos maliciosos
    remove_malicious_files()
    
    # Remove persistência do registro
    remove_registry_persistence()
    
    # Mata processos maliciosos
    kill_malicious_processes()
    
    logging.info("Limpeza do Amadey concluída")

if __name__ == "__main__":
    cleanup() 