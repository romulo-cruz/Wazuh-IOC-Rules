#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Este script precisa ser executado como root${NC}"
    exit 1
fi

# Instalar dependências
python3 -m pip install requests

# Criar diretórios necessários
mkdir -p /var/ossec/integrations/hibp
mkdir -p /var/ossec/etc/lists
mkdir -p /var/ossec/tmp

# Copiar arquivos
cp hibp.py /var/ossec/integrations/hibp/
cp ../rules/hibp_rules.xml /var/ossec/etc/rules/
touch /var/ossec/etc/lists/monitored_emails.txt

# Configurar permissões
chmod 750 /var/ossec/integrations/hibp/hibp.py
chown root:wazuh /var/ossec/integrations/hibp/hibp.py
chmod 640 /var/ossec/etc/lists/monitored_emails.txt
chown root:wazuh /var/ossec/etc/lists/monitored_emails.txt

# Configurar cron
./setup_cron.sh

echo -e "${GREEN}Integração HIBP instalada com sucesso!${NC}"
echo -e "${YELLOW}Não esqueça de configurar sua API key e adicionar emails para monitoramento${NC}" 