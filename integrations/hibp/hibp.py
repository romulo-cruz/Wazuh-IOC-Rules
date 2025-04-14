#!/usr/bin/env python3
import requests
import time
import json
import os
from datetime import datetime, timedelta

# Configurações
API_KEY = "<YOUR_HIBP_API_KEY>"
EMAIL_LIST_FILE = "/var/ossec/etc/lists/monitored_emails.txt"
OUTPUT_LOG_FILE = "/var/log/hibp_breach_checks.log"
CACHE_FILE = "/var/ossec/tmp/hibp_cache.json"
BREACH_DETAILS_CACHE_FILE = "/var/ossec/tmp/breach_details_cache.json"
RATE_LIMIT_DELAY = 60
CACHE_EXPIRATION_DAYS = 7

# Garantir que os diretórios existam
os.makedirs(os.path.dirname(OUTPUT_LOG_FILE), exist_ok=True)
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

def load_cache(cache_file):
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            print(f"Arquivo de cache {cache_file} corrompido. Iniciando cache vazio.")
    return {}

cache = load_cache(CACHE_FILE)
breach_details_cache = load_cache(BREACH_DETAILS_CACHE_FILE)

def save_cache(data, cache_file):
    with open(cache_file, "w") as f:
        json.dump(data, f)

def is_recently_checked(email):
    if email in cache:
        last_checked = datetime.strptime(cache[email]["last_checked"], "%Y-%m-%dT%H:%M:%S")
        if datetime.now() - last_checked < timedelta(days=CACHE_EXPIRATION_DAYS):
            return True
    return False

def get_breach_details(breach_name):
    if breach_name in breach_details_cache:
        return breach_details_cache[breach_name]

    url = f"https://haveibeenpwned.com/api/v3/breach/{breach_name}"
    headers = {
        "hibp-api-key": API_KEY,
        "User-Agent": "Wazuh-HIBP-Integration/1.0"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            breach_data = response.json()
            description = breach_data.get("Description", "Descrição não disponível")
            breach_details_cache[breach_name] = description
            save_cache(breach_details_cache, BREACH_DETAILS_CACHE_FILE)
            return description
    except Exception as e:
        print(f"Erro ao obter detalhes do vazamento: {e}")
    
    return "Descrição não disponível"

def log_breach(email, breach, description):
    log_entry = {
        "email": email,
        "breach": breach,
        "description": description,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "hibpwned",
        "severity": "high"
    }
    
    with open(OUTPUT_LOG_FILE, "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

def check_email(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": API_KEY,
        "User-Agent": "Wazuh-HIBP-Integration/1.0"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            breaches = response.json()
            cache[email] = {
                "breaches": [b["Name"] for b in breaches],
                "last_checked": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            }
            
            for breach in breaches:
                description = get_breach_details(breach["Name"])
                log_breach(email, breach["Name"], description)
                
            save_cache(cache, CACHE_FILE)
            return True
            
        elif response.status_code == 404:
            cache[email] = {
                "breaches": [],
                "last_checked": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            }
            save_cache(cache, CACHE_FILE)
            
    except Exception as e:
        print(f"Erro ao verificar email {email}: {e}")
    
    return False

def main():
    if not os.path.exists(EMAIL_LIST_FILE):
        print(f"Arquivo de emails {EMAIL_LIST_FILE} não encontrado")
        return

    with open(EMAIL_LIST_FILE, "r") as f:
        emails = [line.strip() for line in f if line.strip()]

    for email in emails:
        if not is_recently_checked(email):
            check_email(email)
            time.sleep(RATE_LIMIT_DELAY)

if __name__ == "__main__":
    main() 