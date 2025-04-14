# Integração Wazuh-Yeti

Esta integração permite o uso da plataforma Yeti para enriquecer as detecções do Wazuh com inteligência de ameaças.

## Funcionalidades

1. Detecção de Malware
   - Integração com feed MalwareBazaar
   - Verificação de hashes MD5
   - Alertas automáticos para arquivos maliciosos

2. Detecção de IPs Maliciosos
   - Integração com AlienVaultIPReputation
   - Monitoramento de tentativas de SSH
   - Identificação de IPs comprometidos

## Configuração

1. Instalar o Yeti:
   ```bash
   # Instruções para instalação do Yeti via Docker
   docker-compose up -d
   ```

2. Configurar a integração:
   - Obter API key do Yeti
   - Atualizar o arquivo ossec.conf
   - Reiniciar o Wazuh

3. Habilitar feeds no Yeti:
   - AbuseCHMalwareBazaar
   - AlienVaultIPReputation

## Monitoramento

Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: yeti` 