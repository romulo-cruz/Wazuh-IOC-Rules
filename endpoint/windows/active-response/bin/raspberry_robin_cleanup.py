#!/usr/bin/env python3

import os
import sys
import subprocess
import winreg
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'raspberry_robin_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def check_suspicious_files():
    """Verifica arquivos suspeitos em unidades removíveis"""
    try:
        for drive in 'DEFGHIJKLMNOPQRSTUVWXYZ':
            drive_path = f"{drive}:\\"
            if os.path.exists(drive_path):
                for ext in ['.lnk', '.swy', '.chk', '.ico', '.usb', '.xml', '.cfg']:
                    suspicious_files = subprocess.check_output(
                        f'dir /s /b "{drive_path}*{ext}"',
                        shell=True, stderr=subprocess.PIPE
                    ).decode().splitlines()
                    
                    for file in suspicious_files:
                        if os.path.getsize(file) < 10000:  # Arquivos pequenos são mais suspeitos
                            try:
                                os.remove(file)
                                logging.info(f"Arquivo removido: {file}")
                            except:
                                logging.error(f"Erro ao remover arquivo: {file}")
    except Exception as e:
        logging.error(f"Erro ao verificar arquivos: {str(e)}")

def clean_registry():
    """Limpa chaves de registro suspeitas"""
    try:
        # Verifica UserAssist
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            try:
                i = 0
                while True:
                    subkey = winreg.EnumKey(key, i)
                    winreg.DeleteKey(key, subkey)
                    i += 1
                    logging.info(f"Chave de registro removida: {subkey}")
            except WindowsError:
                pass
    except Exception as e:
        logging.error(f"Erro ao limpar registro: {str(e)}")

def kill_suspicious_processes():
    """Termina processos suspeitos"""
    suspicious_processes = [
        'rundll32.exe',
        'regsvr32.exe',
        'dllhost.exe',
        'msiexec.exe'
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
        # Bloqueia conexões para porta 8080
        subprocess.run([
            'netsh', 'advfirewall', 'firewall', 'add', 'rule',
            'name="Block Raspberry Robin Outbound"',
            'dir=out', 'action=block', 'protocol=TCP',
            'remoteport=8080'
        ])
        logging.info("Regra de firewall adicionada para bloquear conexões suspeitas")
    except Exception as e:
        logging.error(f"Erro ao configurar firewall: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do Raspberry Robin")
    
    # Verifica e remove arquivos suspeitos
    check_suspicious_files()
    
    # Limpa registro
    clean_registry()
    
    # Termina processos suspeitos
    kill_suspicious_processes()
    
    # Bloqueia conexões de rede
    block_network_connections()
    
    logging.info("Limpeza do Raspberry Robin concluída")

if __name__ == "__main__":
    cleanup() 