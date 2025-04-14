#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import logging
from datetime import datetime

# Configuração de logging
LOG_FILE = '/var/ossec/logs/text4shell_check.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def check_java_processes():
    """Verifica processos Java em execução que podem estar usando Commons Text"""
    try:
        output = subprocess.check_output(['ps', '-ef']).decode()
        java_procs = [line for line in output.split('\n') if 'java' in line]
        
        for proc in java_procs:
            logging.info(f"Processo Java encontrado: {proc}")
            
        return java_procs
    except Exception as e:
        logging.error(f"Erro ao verificar processos Java: {str(e)}")
        return []

def scan_for_vulnerable_jars():
    """Procura por JARs vulneráveis do Commons Text"""
    try:
        cmd = 'find / -regex ".*commons-text.*.jar" -type f -exec sh -c "echo -n \'{}\': && unzip -p {} META-INF/MANIFEST.MF | grep Implementation-Version" \; 2>/dev/null'
        output = subprocess.check_output(cmd, shell=True).decode()
        
        vulnerable_versions = ['1.5', '1.6', '1.7', '1.8', '1.9']
        vulnerable_jars = []
        
        for line in output.split('\n'):
            if any(ver in line for ver in vulnerable_versions):
                vulnerable_jars.append(line)
                logging.warning(f"JAR vulnerável encontrado: {line}")
                
        return vulnerable_jars
    except Exception as e:
        logging.error(f"Erro ao procurar JARs vulneráveis: {str(e)}")
        return []

def check_web_configs():
    """Verifica configurações web que podem estar usando StringSubstitutor"""
    web_configs = [
        '/etc/tomcat*/conf/server.xml',
        '/etc/apache2/apache2.conf',
        '/etc/nginx/nginx.conf'
    ]
    
    findings = []
    for config in web_configs:
        try:
            if os.path.exists(config):
                with open(config, 'r') as f:
                    content = f.read()
                    if 'StringSubstitutor' in content:
                        findings.append(config)
                        logging.warning(f"Configuração web potencialmente vulnerável: {config}")
        except Exception as e:
            logging.error(f"Erro ao verificar {config}: {str(e)}")
            
    return findings

def main():
    """Função principal de verificação"""
    logging.info("Iniciando verificação do Text4Shell")
    
    results = {
        'java_processes': check_java_processes(),
        'vulnerable_jars': scan_for_vulnerable_jars(),
        'web_configs': check_web_configs()
    }
    
    if any(results.values()):
        logging.warning("Potenciais vulnerabilidades Text4Shell encontradas")
    else:
        logging.info("Nenhuma vulnerabilidade Text4Shell encontrada")
        
    return results

if __name__ == "__main__":
    main() 