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
mkdir -p /var/ossec/integrations/criminalip
mkdir -p /var/ossec/etc/rules

# Copiar arquivos
cp custom-criminalip.py /var/ossec/integrations/criminalip/
cp ../rules/criminalip_rules.xml /var/ossec/etc/rules/

# Configurar permissões
chmod 750 /var/ossec/integrations/criminalip/custom-criminalip.py
chown root:wazuh /var/ossec/integrations/criminalip/custom-criminalip.py
chmod 660 /var/ossec/etc/rules/criminalip_rules.xml
chown wazuh:wazuh /var/ossec/etc/rules/criminalip_rules.xml

echo -e "${GREEN}Integração Criminal IP instalada com sucesso!${NC}"
echo -e "${YELLOW}Não esqueça de configurar sua API key no arquivo ossec.conf${NC}" 