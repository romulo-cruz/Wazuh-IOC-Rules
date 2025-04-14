#!/usr/bin/env python3

import os
import sys
import subprocess
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = '/var/ossec/logs/chaos_cleanup.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def remove_malicious_files():
    """Remove arquivos maliciosos do Chaos"""
    malicious_files = [
        '/etc/id.services.conf',
        '/etc/32678',
        '/etc/profile.d/bash_config.sh',
        '/boot/System.img.config',
        '/etc/init.d/linux_kill'
    ]
    
    for file in malicious_files:
        try:
            if os.path.exists(file):
                os.remove(file)
                logging.info(f"Arquivo removido: {file}")
        except Exception as e:
            logging.error(f"Erro ao remover {file}: {str(e)}")

def kill_malicious_processes():
    """Mata processos maliciosos"""
    try:
        # Procura por processos suspeitos
        ps_output = subprocess.check_output(['ps', '-ef']).decode()
        for line in ps_output.splitlines():
            if 'id.services.conf' in line:
                try:
                    pid = line.split()[1]
                    subprocess.run(['kill', '-9', pid])
                    logging.info(f"Processo terminado: {pid}")
                except:
                    continue
    except Exception as e:
        logging.error(f"Erro ao terminar processos: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do Chaos")
    
    # Remove arquivos maliciosos
    remove_malicious_files()
    
    # Mata processos maliciosos
    kill_malicious_processes()
    
    logging.info("Limpeza do Chaos concluída")

if __name__ == "__main__":
    cleanup() 