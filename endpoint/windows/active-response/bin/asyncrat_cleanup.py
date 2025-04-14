#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import winreg
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'asyncrat_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def remove_registry_keys():
    """Remove chaves de registro relacionadas ao AsyncRAT"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Run", 
                           0, winreg.KEY_ALL_ACCESS) as key:
            # Listar todas as chaves e remover suspeitas
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    if ".exe" in value.lower():
                        winreg.DeleteValue(key, name)
                        logging.info(f"Chave de registro removida: {name}")
                    i += 1
                except WindowsError:
                    break
    except Exception as e:
        logging.error(f"Erro ao remover chaves do registro: {str(e)}")

def remove_scheduled_tasks():
    """Remove tarefas agendadas suspeitas"""
    try:
        output = subprocess.check_output(['schtasks', '/query', '/fo', 'csv']).decode()
        for line in output.split('\n'):
            if '.exe' in line.lower():
                task_name = line.split(',')[0].strip('"')
                subprocess.run(['schtasks', '/delete', '/tn', task_name, '/f'])
                logging.info(f"Tarefa agendada removida: {task_name}")
    except Exception as e:
        logging.error(f"Erro ao remover tarefas agendadas: {str(e)}")

def kill_suspicious_processes():
    """Mata processos suspeitos"""
    try:
        output = subprocess.check_output(['tasklist']).decode()
        for line in output.split('\n'):
            if 'stub.exe' in line.lower():
                pid = line.split()[1]
                subprocess.run(['taskkill', '/F', '/PID', pid])
                logging.info(f"Processo terminado: PID {pid}")
    except Exception as e:
        logging.error(f"Erro ao terminar processos: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do AsyncRAT")
    
    # Remove chaves de registro
    remove_registry_keys()
    
    # Remove tarefas agendadas
    remove_scheduled_tasks()
    
    # Mata processos suspeitos
    kill_suspicious_processes()
    
    # Remove arquivos maliciosos conhecidos
    malicious_paths = [
        os.path.join(os.environ['APPDATA'], 'stub.exe'),
        os.path.join(os.environ['LOCALAPPDATA'], 'stub.exe')
    ]
    
    for path in malicious_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
                logging.info(f"Arquivo removido: {path}")
        except Exception as e:
            logging.error(f"Erro ao remover arquivo {path}: {str(e)}")

    logging.info("Limpeza do AsyncRAT concluída")

if __name__ == "__main__":
    cleanup() 