#!/usr/bin/env python3

import os
import sys
import subprocess
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = '/var/ossec/logs/panchan_cleanup.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def remove_malicious_files():
    """Remove arquivos maliciosos"""
    malicious_files = [
        '/bin/systemd-worker',
        '/lib/systemd/system/systemd-worker.service'
    ]
    
    try:
        # Procura por diretórios ocultos com xinetd
        find_output = subprocess.check_output(
            ['find', '/', '-name', 'xinetd', '-type', 'f'],
            stderr=subprocess.PIPE
        ).decode()
        
        malicious_files.extend(find_output.splitlines())
        
        for file in malicious_files:
            if os.path.exists(file):
                os.remove(file)
                logging.info(f"Arquivo removido: {file}")
    except Exception as e:
        logging.error(f"Erro ao remover arquivos: {str(e)}")

def stop_malicious_service():
    """Para e remove serviço malicioso"""
    try:
        subprocess.run(['systemctl', 'stop', 'systemd-worker'])
        subprocess.run(['systemctl', 'disable', 'systemd-worker'])
        logging.info("Serviço systemd-worker parado e desabilitado")
    except Exception as e:
        logging.error(f"Erro ao parar serviço: {str(e)}")

def remove_firewall_rules():
    """Remove regras de firewall maliciosas"""
    try:
        subprocess.run([
            'iptables', '-D', 'INPUT', '-p', 'tcp',
            '--dport', '1919', '-j', 'ACCEPT'
        ])
        logging.info("Regra de firewall removida")
    except Exception as e:
        logging.error(f"Erro ao remover regra de firewall: {str(e)}")

def kill_mining_processes():
    """Termina processos de mineração"""
    try:
        # Procura por processos de mineração conhecidos
        ps_output = subprocess.check_output(['ps', '-ef']).decode()
        for line in ps_output.splitlines():
            if 'xinetd' in line or 'systemd-worker' in line:
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
    logging.info("Iniciando limpeza do Panchan")
    
    # Remove arquivos maliciosos
    remove_malicious_files()
    
    # Para serviço malicioso
    stop_malicious_service()
    
    # Remove regras de firewall
    remove_firewall_rules()
    
    # Termina processos de mineração
    kill_mining_processes()
    
    logging.info("Limpeza do Panchan concluída")

if __name__ == "__main__":
    cleanup() 