#!/usr/bin/env python3

import os
import sys
import subprocess
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = '/var/ossec/logs/rapperbot_cleanup.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def remove_malicious_user():
    """Remove usuário malicioso"""
    try:
        subprocess.run(['userdel', '-r', 'suhelper'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
        logging.info("Usuário suhelper removido")
    except Exception as e:
        logging.error(f"Erro ao remover usuário: {str(e)}")

def clean_ssh_keys():
    """Limpa chaves SSH maliciosas"""
    try:
        auth_keys = os.path.expanduser('~/.ssh/authorized_keys')
        if os.path.exists(auth_keys):
            with open(auth_keys, 'r') as f:
                lines = f.readlines()
            
            with open(auth_keys, 'w') as f:
                for line in lines:
                    if 'AAAAB3NzaC1yc2EAAAADAQABAAACAQC' not in line:
                        f.write(line)
            logging.info("Chaves SSH maliciosas removidas")
    except Exception as e:
        logging.error(f"Erro ao limpar chaves SSH: {str(e)}")

def remove_cron_job():
    """Remove cron job malicioso"""
    try:
        cron_file = '/etc/cron.hourly/0'
        if os.path.exists(cron_file):
            os.remove(cron_file)
            logging.info("Cron job malicioso removido")
    except Exception as e:
        logging.error(f"Erro ao remover cron job: {str(e)}")

def block_c2_connections():
    """Bloqueia conexões para IPs do C2"""
    c2_ips = [
        '185.225.73.196',
        '2.58.149.116'
    ]
    
    try:
        for ip in c2_ips:
            subprocess.run([
                'iptables', '-A', 'OUTPUT', '-d', ip, '-j', 'DROP'
            ])
            logging.info(f"Bloqueado IP do C2: {ip}")
    except Exception as e:
        logging.error(f"Erro ao configurar iptables: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do RapperBot")
    
    # Remove usuário malicioso
    remove_malicious_user()
    
    # Limpa chaves SSH
    clean_ssh_keys()
    
    # Remove cron job
    remove_cron_job()
    
    # Bloqueia conexões C2
    block_c2_connections()
    
    logging.info("Limpeza do RapperBot concluída")

if __name__ == "__main__":
    cleanup() 