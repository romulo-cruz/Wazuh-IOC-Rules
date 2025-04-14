#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = '/var/ossec/logs/webshell_cleanup.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def check_suspicious_files():
    """Verifica arquivos web suspeitos"""
    web_dirs = ['/var/www/html']
    suspicious_patterns = [
        'eval(', 'shell_exec(', 'system(', 'passthru(',
        'exec(', 'popen(', 'proc_open(', 'curl_exec('
    ]
    
    for directory in web_dirs:
        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(('.php', '.jsp', '.asp', '.aspx', '.cgi')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r') as f:
                                content = f.read()
                                for pattern in suspicious_patterns:
                                    if pattern in content:
                                        logging.warning(f"Arquivo suspeito encontrado: {filepath}")
                                        return filepath
                        except Exception as e:
                            logging.error(f"Erro ao ler arquivo {filepath}: {str(e)}")
        except Exception as e:
            logging.error(f"Erro ao verificar diretório {directory}: {str(e)}")
    return None

def kill_suspicious_processes():
    """Mata processos suspeitos"""
    try:
        # Verifica conexões suspeitas
        netstat = subprocess.check_output(['netstat', '-tnp']).decode()
        for line in netstat.splitlines():
            if any(x in line.lower() for x in ['bash', 'sh', 'nc', 'python']):
                try:
                    pid = line.split()[-1].split('/')[0]
                    subprocess.run(['kill', '-9', pid])
                    logging.info(f"Processo terminado: {pid}")
                except:
                    continue
    except Exception as e:
        logging.error(f"Erro ao terminar processos: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza de Web Shell")
    
    # Verifica arquivos suspeitos
    suspicious_file = check_suspicious_files()
    if suspicious_file:
        try:
            os.remove(suspicious_file)
            logging.info(f"Arquivo removido: {suspicious_file}")
        except Exception as e:
            logging.error(f"Erro ao remover arquivo: {str(e)}")
    
    # Mata processos suspeitos
    kill_suspicious_processes()
    
    logging.info("Limpeza de Web Shell concluída")

if __name__ == "__main__":
    cleanup() 