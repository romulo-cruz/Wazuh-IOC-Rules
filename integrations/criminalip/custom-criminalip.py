#!/usr/bin/env python3

import sys
import os
import json
import ipaddress
import requests
from requests.exceptions import ConnectionError, HTTPError
from socket import socket, AF_UNIX, SOCK_DGRAM
import time

# Configurações
debug_enabled = True
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
socket_addr = f'{pwd}/queue/sockets/queue'
now = time.strftime("%a %b %d %H:%M:%S %Z %Y")
log_file = f'{pwd}/logs/integrations.log'

def debug(msg):
    if debug_enabled:
        timestamped_msg = f"{now}: {msg}\n"
        print(timestamped_msg)
        with open(log_file, "a") as f:
            f.write(timestamped_msg)

def send_event(msg, agent=None):
    try:
        if not agent or agent["id"] == "000":
            string = f'1:criminalip:{json.dumps(msg)}'
        else:
            string = f'1:[{agent["id"]}] ({agent["name"]}) {agent["ip"] if "ip" in agent else "any"}->criminalip:{json.dumps(msg)}'
        
        debug(f"Enviando Evento: {string}")
        with socket(AF_UNIX, SOCK_DGRAM) as sock:
            sock.connect(socket_addr)
            sock.send(string.encode())
    except Exception as e:
        debug(f"Erro ao enviar evento: {e}")

def query_criminalip(client_ip, api_key):
    headers = {"x-api-key": api_key}
    url = f'https://api.criminalip.io/v1/asset/ip/report?ip={client_ip}&full=true'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        debug(f"Erro na consulta à API: {e}")
        return None

def main():
    try:
        # Ler arquivo de alerta
        with open(sys.argv[1]) as alert_file:
            alert = json.loads(alert_file.read())
        
        # Obter API key
        api_key = sys.argv[2]
        
        # Verificar grupos do evento
        event_source = alert["rule"]["groups"]
        monitored_groups = ['web', 'sshd', 'invalid_login', 'firewall', 'ids', 
                          'system', 'database', 'application']
        
        if any(group in monitored_groups for group in event_source):
            client_ip = alert["data"]["srcip"]
            
            if ipaddress.ip_address(client_ip).is_global:
                response = query_criminalip(client_ip, api_key)
                
                if response and "score" in response:
                    alert_output = {
                        "criminalip": {
                            "ip": response["ip"],
                            "score_inbound": response["score"].get("inbound", "Desconhecido"),
                            "score_outbound": response["score"].get("outbound", "Desconhecido"),
                            "is_vpn": response["issues"].get("is_vpn", False),
                            "is_tor": response["issues"].get("is_tor", False),
                            "is_proxy": response["issues"].get("is_proxy", False),
                            "is_cloud": response["issues"].get("is_cloud", False),
                            "is_hosting": response["issues"].get("is_hosting", False),
                            "is_darkweb": response["issues"].get("is_darkweb", False),
                            "is_scanner": response["issues"].get("is_scanner", False),
                            "is_snort": response["issues"].get("is_snort", False),
                            "is_anonymous_vpn": response["issues"].get("is_anonymous_vpn", False)
                        },
                        "integration": "criminalip"
                    }
                    send_event(alert_output, alert.get("agent"))

    except Exception as e:
        debug(f"Erro geral: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 