#!/usr/bin/env python3

import os
import sys
import subprocess
import winreg
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'lockbit3_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def restore_vss():
    """Restaura serviços VSS"""
    try:
        # Reativa VSS
        subprocess.run([
            'sc', 'config', 'VSS', 'start=auto'
        ])
        subprocess.run([
            'net', 'start', 'VSS'
        ])
        
        # Reativa Hyper-V VSS
        subprocess.run([
            'sc', 'config', 'vmicvss', 'start=auto'
        ])
        subprocess.run([
            'net', 'start', 'vmicvss'
        ])
        
        logging.info("Serviços VSS restaurados")
    except Exception as e:
        logging.error(f"Erro ao restaurar VSS: {str(e)}")

def remove_ransom_notes():
    """Remove notas de resgate"""
    try:
        for drive in 'CDEFGHIJKLMNOPQRSTUVWXYZ':
            drive_path = f"{drive}:\\"
            if os.path.exists(drive_path):
                for root, dirs, files in os.walk(drive_path):
                    for file in files:
                        if file.endswith('README.txt'):
                            try:
                                os.remove(os.path.join(root, file))
                                logging.info(f"Nota de resgate removida: {os.path.join(root, file)}")
                            except:
                                continue
    except Exception as e:
        logging.error(f"Erro ao remover notas de resgate: {str(e)}")

def restore_file_extensions():
    """Restaura extensões de arquivos"""
    known_extensions = ['.HLJkNskOq', '.19MqZqZ0s']
    try:
        for drive in 'CDEFGHIJKLMNOPQRSTUVWXYZ':
            drive_path = f"{drive}:\\"
            if os.path.exists(drive_path):
                for root, dirs, files in os.walk(drive_path):
                    for file in files:
                        for ext in known_extensions:
                            if file.endswith(ext):
                                try:
                                    old_name = os.path.join(root, file)
                                    new_name = old_name[:-len(ext)]
                                    os.rename(old_name, new_name)
                                    logging.info(f"Extensão restaurada: {old_name} -> {new_name}")
                                except:
                                    continue
    except Exception as e:
        logging.error(f"Erro ao restaurar extensões: {str(e)}")

def restore_windows_defender():
    """Restaura Windows Defender"""
    try:
        subprocess.run([
            'powershell', 'Set-MpPreference', '-DisableRealtimeMonitoring', '$false'
        ])
        logging.info("Windows Defender reativado")
    except Exception as e:
        logging.error(f"Erro ao restaurar Windows Defender: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do LockBit 3.0")
    
    # Restaura VSS
    restore_vss()
    
    # Remove notas de resgate
    remove_ransom_notes()
    
    # Restaura extensões
    restore_file_extensions()
    
    # Restaura Windows Defender
    restore_windows_defender()
    
    logging.info("Limpeza do LockBit 3.0 concluída")

if __name__ == "__main__":
    cleanup() 