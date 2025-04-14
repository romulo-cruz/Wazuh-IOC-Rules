#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import logging
from datetime import datetime
import glob

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'strrat_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def remove_malicious_files():
    """Remove arquivos maliciosos do STRRAT"""
    user_profile = os.environ['USERPROFILE']
    paths_to_check = [
        os.path.join(user_profile, 'lib', '*.jar'),
        os.path.join(user_profile, '*lock.file'),
        os.path.join(user_profile, 'AppData', 'Roaming', 'strlogs', '*'),
        os.path.join(user_profile, 'Documents', '*.crimson'),
        os.path.join(user_profile, 'Desktop', '*.crimson'),
        os.path.join(user_profile, 'Downloads', '*.crimson')
    ]
    
    for path in paths_to_check:
        try:
            for file in glob.glob(path):
                os.remove(file)
                logging.info(f"Arquivo removido: {file}")
        except Exception as e:
            logging.error(f"Erro ao remover arquivo {path}: {str(e)}")

def remove_scheduled_task():
    """Remove tarefa agendada maliciosa"""
    try:
        subprocess.run(['schtasks', '/delete', '/tn', 'Skype', '/f'], 
                      capture_output=True)
        logging.info("Tarefa agendada 'Skype' removida")
    except Exception as e:
        logging.error(f"Erro ao remover tarefa agendada: {str(e)}")

def restore_file_extensions():
    """Restaura extensões de arquivos"""
    user_profile = os.environ['USERPROFILE']
    dirs_to_check = ['Documents', 'Desktop', 'Downloads']
    
    for dir_name in dirs_to_check:
        dir_path = os.path.join(user_profile, dir_name)
        try:
            for file in glob.glob(os.path.join(dir_path, '*.crimson')):
                try:
                    new_name = file[:-8]  # Remove .crimson
                    os.rename(file, new_name)
                    logging.info(f"Arquivo restaurado: {file} -> {new_name}")
                except:
                    continue
        except Exception as e:
            logging.error(f"Erro ao restaurar arquivos em {dir_path}: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do STRRAT")
    
    # Remove arquivos maliciosos
    remove_malicious_files()
    
    # Remove tarefa agendada
    remove_scheduled_task()
    
    # Restaura extensões de arquivos
    restore_file_extensions()
    
    logging.info("Limpeza do STRRAT concluída")

if __name__ == "__main__":
    cleanup() 