#!/var/ossec/framework/python/bin/python3

import sys
import json
import datetime
from pathlib import PureWindowsPath, PurePosixPath, Path

OS_SUCCESS = 0
OS_INVALID = -1

LOG_FILE = "/var/ossec/logs/active-responses.log"
MAL_IP_LIST = "/var/ossec/etc/lists/mal-ip-list"
MAL_URL_LIST = "/var/ossec/etc/lists/mal-url-list"
MAL_MD5_LIST = "/var/ossec/etc/lists/mal-md5-list"

def write_debug_file(ar_name, msg):
    with open(LOG_FILE, mode="a") as log_file:
        ar_name_posix = str(PurePosixPath(PureWindowsPath(ar_name[ar_name.find("active-response"):])))
        log_file.write(str(datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")) + " " + ar_name_posix + ": " + msg + "\n")

def read_alert_data():
    input_str = ""
    for line in sys.stdin:
        input_str = line
        break

    try:
        alert_data = json.loads(input_str)
    except ValueError:
        write_debug_file(sys.argv[0], "Decodificação JSON falhou, formato de entrada inválido")
        sys.exit(OS_INVALID)

    return alert_data

def is_not_duplicate_ioc(ioc_file, ioc):
    ioc += ":\n"
    for line in ioc_file:
        if line == ioc:
            return False
    return True

def get_ioc_if_exist(alert_obj, keys):
    if not keys or alert_obj is None:
        return alert_obj
    return get_ioc_if_exist(alert_obj.get(keys[0]), keys[1:])

def write_ioc(file_path, ioc):
    try:
        with open(file_path, "a+") as ioc_file:
            ioc_file.seek(0)
            if is_not_duplicate_ioc(ioc_file, ioc):
                ioc_file.write(f"{ioc}:\n")
                write_debug_file(sys.argv[0], f"IoC {ioc} adicionado a {file_path}")
                return OS_SUCCESS
    except Exception as e:
        write_debug_file(sys.argv[0], f"Erro ao escrever IoC: {str(e)}")
        return OS_INVALID

    return OS_SUCCESS

def main():
    alert_data = read_alert_data()
    
    # Extrair IP 