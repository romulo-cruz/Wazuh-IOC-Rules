#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import winreg
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'darkwatchman_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def restore_defender():
    """Restaura configurações do Windows Defender"""
    try:
        subprocess.run([
            'powershell.exe',
            '-NonI',
            '-W',
            'Hidden',
            '-Exec',
            'Bypass',
            'Remove-MpPreference',
            '-ExclusionPath',
            'C:'
        ], capture_output=True)
        logging.info("Exclusão do Windows Defender removida")
    except Exception as e:
        logging.error(f"Erro ao restaurar Windows Defender: {str(e)}")

def remove_malicious_files():
    """Remove arquivos maliciosos"""
    temp_dir = os.environ.get('TEMP', '')
    if temp_dir:
        try:
            for file in os.listdir(temp_dir):
                if file.endswith('.js'):
                    file_path = os.path.join(temp_dir, file)
                    os.remove(file_path)
                    logging.info(f"Arquivo removido: {file_path}")
        except Exception as e:
            logging.error(f"Erro ao remover arquivos: {str(e)}")

def clean_registry():
    """Limpa chaves de registro maliciosas"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM", 0, winreg.KEY_ALL_ACCESS) as key:
            while True:
                try:
                    name, _, _ = winreg.EnumValue(key, 0)
                    winreg.DeleteValue(key, name)
                    logging.info(f"Valor do registro removido: {name}")
                except WindowsError:
                    break
    except Exception as e:
        logging.error(f"Erro ao limpar registro: {str(e)}")

def kill_malicious_processes():
    """Mata processos maliciosos"""
    processes = ['wscript.exe', 'regsvr32.exe']
    for proc in processes:
        try:
            subprocess.run(['taskkill', '/F', '/IM', proc], capture_output=True)
            logging.info(f"Processo terminado: {proc}")
        except Exception as e:
            logging.error(f"Erro ao terminar processo {proc}: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do DarkWatchman")
    
    # Restaura Windows Defender
    restore_defender()
    
    # Remove arquivos maliciosos
    remove_malicious_files()
    
    # Limpa registro
    clean_registry()
    
    # Mata processos
    kill_malicious_processes()
    
    logging.info("Limpeza do DarkWatchman concluída")

if __name__ == "__main__":
    cleanup() 