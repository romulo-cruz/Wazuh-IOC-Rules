#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
NC='\033[0m'

# Criar diretórios
mkdir -p config
mkdir -p decoders
mkdir -p integrations
mkdir -p lists
mkdir -p rules
mkdir -p tests/rule_tests
mkdir -p active-response/bin
mkdir -p tools

# Criar arquivos base
touch lists/mal-ip-list
touch lists/mal-url-list
touch lists/mal-md5-list
touch decoders/local_decoder.xml
touch rules/local_rules.xml
touch config/ossec.conf
touch tools/rule_validator.sh

# Tornar scripts executáveis
chmod +x tools/rule_validator.sh
chmod +x tools/setup_structure.sh

echo -e "${GREEN}Estrutura de diretórios criada com sucesso!${NC}" 