#!/usr/bin/env python3

import os
import sys
import subprocess
import winreg
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'remcos_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def remove_registry_keys():
    """Remove chaves de registro do Remcos"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE", 0, winreg.KEY_ALL_ACCESS) as key:
            # Procura por chaves que começam com Remcos ou hpsupport
            i = 0
            while True:
                try:
                    subkey = winreg.EnumKey(key, i)
                    if subkey.startswith(('Remcos-', 'hpsupport-')):
                        winreg.DeleteKey(key, subkey)
                        logging.info(f"Chave de registro removida: {subkey}")
                    i += 1
                except WindowsError:
                    break
    except Exception as e:
        logging.error(f"Erro ao remover chaves de registro: {str(e)}")

def remove_malicious_files():
    """Remove arquivos maliciosos do Remcos"""
    paths_to_check = [
        os.path.join(os.environ['APPDATA'], 'remcos'),
        os.path.join(os.environ['APPDATA'], 'hpsupport'),
        os.path.join(os.environ['LOCALAPPDATA'], 'Temp')
    ]
    
    for path in paths_to_check:
        try:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file == 'logs.dat' or file.endswith(('.dll', '.vbs')):
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            logging.info(f"Arquivo removido: {file_path}")
        except Exception as e:
            logging.error(f"Erro ao remover arquivos em {path}: {str(e)}")

def kill_suspicious_processes():
    """Termina processos suspeitos"""
    suspicious_processes = [
        'remcos.exe',
        'hpsupport.exe'
    ]
    
    try:
        for process in suspicious_processes:
            subprocess.run(['taskkill', '/F', '/IM', process], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
            logging.info(f"Processo terminado: {process}")
    except Exception as e:
        logging.error(f"Erro ao terminar processos: {str(e)}")

def block_network_connections():
    """Bloqueia conexões de rede suspeitas"""
    try:
        # Bloqueia conexões para porta 2404 (porta comum do Remcos)
        subprocess.run([
            'netsh', 'advfirewall', 'firewall', 'add', 'rule',
            'name="Block Remcos RAT Outbound"',
            'dir=out', 'action=block', 'protocol=TCP',
            'remoteport=2404'
        ])
        logging.info("Regra de firewall adicionada para bloquear conexões do Remcos")
    except Exception as e:
        logging.error(f"Erro ao configurar firewall: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do Remcos RAT")
    
    # Remove chaves de registro
    remove_registry_keys()
    
    # Remove arquivos maliciosos
    remove_malicious_files()
    
    # Termina processos suspeitos
    kill_suspicious_processes()
    
    # Bloqueia conexões de rede
    block_network_connections()
    
    logging.info("Limpeza do Remcos RAT concluída")

if __name__ == "__main__":
    cleanup() 