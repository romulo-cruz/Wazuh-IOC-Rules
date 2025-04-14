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

# Instalar dependências Python
pip3 install requests

# Copiar script de integração
cp custom-yeti.py /var/ossec/integrations/
chmod 750 /var/ossec/integrations/custom-yeti.py
chown root:wazuh /var/ossec/integrations/custom-yeti.py

# Copiar regras
cp ../rules/yeti_rules.xml /var/ossec/etc/rules/

# Reiniciar Wazuh
systemctl restart wazuh-manager

echo -e "${GREEN}Integração Yeti instalada com sucesso!${NC}"
echo -e "${YELLOW}Não esqueça de configurar sua API key no arquivo ossec.conf${NC}" 