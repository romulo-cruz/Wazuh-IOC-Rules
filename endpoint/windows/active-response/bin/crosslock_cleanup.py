#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'crosslock_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def restore_system_settings():
    """Restaura configurações do sistema"""
    try:
        # Reativar recuperação automática
        subprocess.run(['bcdedit', '/set', '{default}', 'recoveryenabled', 'Yes'], capture_output=True)
        logging.info("Recuperação automática reativada")
        
        # Restaurar política de boot
        subprocess.run(['bcdedit', '/set', '{default}', 'bootstatuspolicy', 'displayallfailures'], capture_output=True)
        logging.info("Política de boot restaurada")
    except Exception as e:
        logging.error(f"Erro ao restaurar configurações do sistema: {str(e)}")

def remove_ransom_notes():
    """Remove notas de resgate"""
    try:
        for drive in 'CDEFGHIJKLMNOPQRSTUVWXYZ':
            drive_path = f"{drive}:\\"
            if os.path.exists(drive_path):
                for root, dirs, files in os.walk(drive_path):
                    for file in files:
                        if "CrossLock" in file and file.endswith(".txt"):
                            try:
                                os.remove(os.path.join(root, file))
                                logging.info(f"Nota de resgate removida: {os.path.join(root, file)}")
                            except:
                                continue
    except Exception as e:
        logging.error(f"Erro ao remover notas de resgate: {str(e)}")

def kill_malicious_processes():
    """Mata processos maliciosos"""
    try:
        # Lista de processos suspeitos
        processes = ['rware.exe']
        for proc in processes:
            subprocess.run(['taskkill', '/F', '/IM', proc], capture_output=True)
            logging.info(f"Processo terminado: {proc}")
    except Exception as e:
        logging.error(f"Erro ao terminar processos: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do CrossLock")
    
    # Restaura configurações do sistema
    restore_system_settings()
    
    # Remove notas de resgate
    remove_ransom_notes()
    
    # Mata processos maliciosos
    kill_malicious_processes()
    
    logging.info("Limpeza do CrossLock concluída")

if __name__ == "__main__":
    cleanup() 