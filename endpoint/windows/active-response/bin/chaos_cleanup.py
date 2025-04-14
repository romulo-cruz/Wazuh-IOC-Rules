#!/usr/bin/env python3

import os
import sys
import subprocess
import winreg
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'chaos_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def remove_malicious_files():
    """Remove arquivos maliciosos do Chaos"""
    try:
        csrss_path = os.path.join(os.environ['ProgramData'], 'Microsoft', 'csrss.exe')
        if os.path.exists(csrss_path):
            os.remove(csrss_path)
            logging.info(f"Arquivo removido: {csrss_path}")
    except Exception as e:
        logging.error(f"Erro ao remover arquivo: {str(e)}")

def clean_registry():
    """Limpa chaves de registro maliciosas"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 
                           0, winreg.KEY_ALL_ACCESS) as key:
            try:
                winreg.DeleteValue(key, "csrss")
                logging.info("Chave de registro removida")
            except WindowsError:
                pass
    except Exception as e:
        logging.error(f"Erro ao limpar registro: {str(e)}")

def block_dns():
    """Bloqueia DNS malicioso"""
    try:
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        with open(hosts_path, 'a') as f:
            f.write("\n127.0.0.1 yusheng.j0a.cn\n")
        logging.info("Host malicioso bloqueado")
    except Exception as e:
        logging.error(f"Erro ao atualizar arquivo hosts: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do Chaos")
    
    # Remove arquivos maliciosos
    remove_malicious_files()
    
    # Limpa registro
    clean_registry()
    
    # Bloqueia DNS malicioso
    block_dns()
    
    logging.info("Limpeza do Chaos concluída")

if __name__ == "__main__":
    cleanup() 