#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'webshell_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def check_suspicious_files():
    """Verifica arquivos web suspeitos"""
    web_dirs = ['C:\\inetpub\\wwwroot']
    suspicious_patterns = [
        'eval(', 'Response.Write(', 'cmd.exe', 'powershell',
        'System.Diagnostics.Process', 'RunspaceFactory'
    ]
    
    for directory in web_dirs:
        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(('.aspx', '.asp', '.php')):
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
        # Verifica processos w3wp.exe com conexões suspeitas
        ps_cmd = """
        Get-NetTCPConnection | 
        Where-Object { $_.OwningProcess -in (Get-Process w3wp).Id } |
        Select-Object OwningProcess
        """
        
        output = subprocess.check_output(['powershell', '-Command', ps_cmd], 
                                      capture_output=True).decode()
        
        for line in output.splitlines():
            if line.strip():
                try:
                    pid = line.strip()
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    logging.info(f"Processo terminado: PID {pid}")
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