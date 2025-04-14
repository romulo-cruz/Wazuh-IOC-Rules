#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Diretórios do Wazuh
WAZUH_DIR="/var/ossec"
WAZUH_RULES_DIR="${WAZUH_DIR}/etc/rules"
WAZUH_DECODERS_DIR="${WAZUH_DIR}/etc/decoders"

# Função para verificar se o Wazuh está instalado
check_wazuh() {
    if [ ! -d "$WAZUH_DIR" ]; then
        echo -e "${RED}Erro: Diretório do Wazuh não encontrado em ${WAZUH_DIR}${NC}"
        exit 1
    fi
}

# Função para fazer backup
backup_rules() {
    echo -e "${YELLOW}Criando backup das regras existentes...${NC}"
    BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
    
    # Backup das regras personalizadas
    if [ -d "${WAZUH_RULES_DIR}" ]; then
        tar czf "${WAZUH_DIR}/backup_rules_${BACKUP_DATE}.tar.gz" -C "${WAZUH_RULES_DIR}" .
    fi
    
    # Backup dos decoders personalizados
    if [ -d "${WAZUH_DECODERS_DIR}" ]; then
        tar czf "${WAZUH_DIR}/backup_decoders_${BACKUP_DATE}.tar.gz" -C "${WAZUH_DECODERS_DIR}" .
    fi
}

# Função para instalar as regras
install_rules() {
    echo -e "${YELLOW}Instalando novas regras...${NC}"
    
    # Criar diretórios se não existirem
    mkdir -p "${WAZUH_RULES_DIR}"
    mkdir -p "${WAZUH_DECODERS_DIR}"
    
    # Copiar regras e decoders
    if [ -d "rules" ]; then
        cp -r rules/* "${WAZUH_RULES_DIR}/"
    fi
    
    if [ -d "decoders" ]; then
        cp -r decoders/* "${WAZUH_DECODERS_DIR}/"
    fi
    
    # Ajustar permissões
    chown -R wazuh:wazuh "${WAZUH_RULES_DIR}"
    chown -R wazuh:wazuh "${WAZUH_DECODERS_DIR}"
    chmod -R 750 "${WAZUH_RULES_DIR}"
    chmod -R 750 "${WAZUH_DECODERS_DIR}"
}

# Função para verificar a sintaxe das regras
check_rules() {
    echo -e "${YELLOW}Verificando sintaxe das regras...${NC}"
    if ! "${WAZUH_DIR}/bin/wazuh-logtest" -t; then
        echo -e "${RED}Erro: Verificação de sintaxe falhou${NC}"
        exit 1
    fi
}

# Função para reiniciar o Wazuh
restart_wazuh() {
    echo -e "${YELLOW}Reiniciando o Wazuh...${NC}"
    systemctl restart wazuh-manager
    
    # Verificar se o serviço iniciou corretamente
    if systemctl is-active --quiet wazuh-manager; then
        echo -e "${GREEN}Wazuh reiniciado com sucesso${NC}"
    else
        echo -e "${RED}Erro ao reiniciar o Wazuh${NC}"
        exit 1
    fi
}

# Execução principal
echo "Iniciando instalação/atualização das regras do Wazuh"

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Este script precisa ser executado como root${NC}"
    exit 1
fi

check_wazuh
backup_rules
install_rules
check_rules
restart_wazuh

echo -e "${GREEN}Instalação/atualização concluída com sucesso!${NC}"

mkdir -p config
mkdir -p decoders
mkdir -p integrations
mkdir -p lists
mkdir -p rules
mkdir -p tests/rule_tests 