#!/var/ossec/framework/python/bin/python3
import json
import os
import re
import sys
import requests
from requests.exceptions import Timeout
from socket import AF_UNIX, SOCK_DGRAM, socket

# Códigos de erro
ERR_NO_REQUEST_MODULE = 1
ERR_BAD_ARGUMENTS = 2
ERR_BAD_MD5_SUM = 3
ERR_NO_RESPONSE_YETI = 4
ERR_SOCKET_OPERATION = 5
ERR_FILE_NOT_FOUND = 6
ERR_INVALID_JSON = 7

# Variáveis globais
debug_enabled = True
timeout = 10
retries = 3
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
json_alert = {}

# Caminhos de log e socket
LOG_FILE = f'{pwd}/logs/integrations.log'
SOCKET_ADDR = f'{pwd}/queue/sockets/queue'

# Constantes
ALERT_INDEX = 1
APIKEY_INDEX = 2
TIMEOUT_INDEX = 6
RETRIES_INDEX = 7
YETI_INSTANCE = 'http://<YETI_IP_ADDRESS>'

def debug(msg: str) -> None:
    if debug_enabled:
        print(msg)
        with open(LOG_FILE, 'a') as f:
            f.write(msg + '\n')

def getAccessToken(apikey):
    url = f"{YETI_INSTANCE}/api/v2/auth/api-token"
    headers = {"x-yeti-apikey": apikey}
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        access_token = response.json().get("access_token")
        if not access_token:
            raise ValueError("Token de acesso ausente na resposta.")
        return access_token
    except requests.exceptions.RequestException as e:
        debug(f"Erro ao obter token de acesso da API: {e}")
        sys.exit(1)

def request_md5_info(alert: any, access_token: str):
    if not 'syscheck' in alert or not 'md5_after' in alert['syscheck']:
        return None
    
    md5 = alert['syscheck']['md5_after']
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(
            f"{YETI_INSTANCE}/api/v2/observables/filter/value/{md5}",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    'integration': 'yeti',
                    'yeti': {
                        'info': {
                            'source': 'AbuseCHMalwareBazaaar'
                        },
                        'source': {
                            'file': md5
                        }
                    }
                }
    except Exception as e:
        debug(f"Erro ao consultar MD5: {e}")
    return None

def request_ssh_info(alert: any, access_token: str):
    if not 'data' in alert:
        return None
    
    srcip = alert['data'].get('srcip')
    if not srcip:
        return None
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(
            f"{YETI_INSTANCE}/api/v2/observables/filter/value/{srcip}",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    'integration': 'yeti',
                    'yeti': {
                        'info': {
                            'source': 'AlienVaultIPReputation'
                        },
                        'source': {
                            'src_ip': srcip
                        }
                    }
                }
    except Exception as e:
        debug(f"Erro ao consultar IP: {e}")
    return None

def send_msg(msg: dict, agent: dict = None):
    if not msg:
        return
    
    try:
        json_msg = json.dumps(msg)
        sock = socket(AF_UNIX, SOCK_DGRAM)
        sock.connect(SOCKET_ADDR)
        sock.send(json_msg.encode())
        sock.close()
    except Exception as e:
        debug(f"Erro ao enviar mensagem: {e}")

def main(args):
    try:
        if len(args) < 4:
            debug('Erro: Argumentos insuficientes')
            sys.exit(ERR_BAD_ARGUMENTS)
        
        apikey = args[APIKEY_INDEX]
        access_token = getAccessToken(apikey)
        process_args(args, access_token)
    
    except Exception as e:
        debug(str(e))
        raise

if __name__ == "__main__":
    main(sys.argv) 