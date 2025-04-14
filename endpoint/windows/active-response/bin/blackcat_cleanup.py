#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import winreg
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = os.path.join(os.environ['ProgramFiles(x86)'], 'ossec-agent', 'active-response', 'log', 'blackcat_cleanup.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def restore_system_settings():
    """Restaura configurações do sistema"""
    try:
        # Reativa recuperação automática
        subprocess.run(['bcdedit', '/set', '{default}', 'recoveryenabled', 'Yes'], 
                      capture_output=True, check=True)
        logging.info("Recuperação automática reativada")
        
        # Restaura MaxMpxCt para valor padrão
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                          r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters", 
                          0, winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteValue(key, "MaxMpxCt")
            logging.info("Configuração MaxMpxCt restaurada")
    except Exception as e:
        logging.error(f"Erro ao restaurar configurações: {str(e)}")

def remove_ransom_notes():
    """Remove notas de resgate"""
    try:
        for drive in 'CDEFGHIJKLMNOPQRSTUVWXYZ':
            drive_path = f"{drive}:\\"
            if os.path.exists(drive_path):
                for root, dirs, files in os.walk(drive_path):
                    for file in files:
                        if "RECOVER-" in file.upper() and file.endswith("-FILES.txt"):
                            try:
                                os.remove(os.path.join(root, file))
                                logging.info(f"Nota de resgate removida: {os.path.join(root, file)}")
                            except Exception as e:
                                logging.error(f"Erro ao remover nota: {str(e)}")
    except Exception as e:
        logging.error(f"Erro ao procurar notas de resgate: {str(e)}")

def restart_services():
    """Reinicia serviços críticos"""
    services = [
        "VSS",  # Volume Shadow Copy
        "BITS", # Background Intelligent Transfer Service
        "wuauserv" # Windows Update
    ]
    
    for service in services:
        try:
            subprocess.run(['net', 'start', service], capture_output=True)
            logging.info(f"Serviço {service} reiniciado")
        except Exception as e:
            logging.error(f"Erro ao reiniciar serviço {service}: {str(e)}")

def cleanup():
    """Executa todas as ações de limpeza"""
    logging.info("Iniciando limpeza do BlackCat")
    
    # Restaura configurações do sistema
    restore_system_settings()
    
    # Remove notas de resgate
    remove_ransom_notes()
    
    # Reinicia serviços
    restart_services()
    
    logging.info("Limpeza do BlackCat concluída")

if __name__ == "__main__":
    cleanup() 