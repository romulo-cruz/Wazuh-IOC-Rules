#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import winreg
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'njrat_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def remove_malicious_files():
    """Remove arquivos maliciosos do njRAT"""
    suspicious_paths = [
        os.path.expandvars(r'%LOCALAPPDATA%\Temp\system.exe'),
        os.path.expandvars(r'C:\system.exe'),
        os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\*.exe')
    ]
    
    for path in suspicious_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
                logging.info(f"Arquivo removido: {path}")
        except Exception as e:
            logging.error(f"Erro ao remover arquivo {path}: {str(e)}")

def restore_firewall():
    """Restaura configurações do firewall"""
    try:
        subprocess.run(['netsh', 'advfirewall', 'reset'], capture_output=True)
        logging.info("Firewall restaurado para configurações padrão")
    except Exception as e:
        logging.error(f"Erro ao restaurar firewall: {str(e)}")

def remove_registry_persistence():
    """Remove chaves de registro de persistência"""
    reg_paths = [
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run")
    ]
    
    for hkey, path in reg_paths:
        try:
            with winreg.OpenKey(hkey, path, 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    while True:
                        name, value, _ = winreg.EnumValue(key, 0)
                        if "system.exe" in value.lower():
                            winreg.DeleteValue(key, name)
                            logging.info(f"Chave de registro removida: {path}\\{name}")
                except WindowsError:
                    pass
        except Exception as e:
            logging.error(f"Erro ao remover chave do registro: {str(e)}")

def kill_suspicious_processes():
    """Mata processos suspeitos"""
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'system.exe'], capture_output=True)
        logging.info("Processos suspeitos terminados")
    except Exception as e:
        logging.error(f"Erro ao terminar processos: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do njRAT")
    
    # Remove arquivos maliciosos
    remove_malicious_files()
    
    # Restaura firewall
    restore_firewall()
    
    # Remove persistência do registro
    remove_registry_persistence()
    
    # Mata processos maliciosos
    kill_suspicious_processes()
    
    logging.info("Limpeza do njRAT concluída")

if __name__ == "__main__":
    cleanup() 