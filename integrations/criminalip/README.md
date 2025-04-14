# Integração Wazuh-Criminal IP

Esta integração permite enriquecer alertas do Wazuh com dados de inteligência de ameaças do Criminal IP.

## Requisitos

1. API Key do Criminal IP (https://www.criminalip.io/)
2. Python 3.8 ou superior
3. Módulo `requests` do Python

## Instalação

1. Execute o script de instalação:
   ```bash
   sudo ./install.sh
   ```

2. Adicione a configuração ao ossec.conf:
   ```xml
   <integration>
     <name>custom-criminalip.py</name>
     <api_key>SUA-API-KEY-AQUI</api_key>
   </integration>
   ```

3. Reinicie o Wazuh:
   ```bash
   sudo systemctl restart wazuh-manager
   ```

## Funcionalidades

- Detecção de IPs associados a:
  - VPNs
  - Rede TOR
  - Proxies
  - Dark Web
  - Scanners
  - Serviços de hosting
  - Serviços em nuvem

- Scores de risco:
  - Crítico (90-100)
  - Alto (70-89)
  - Moderado (50-69)
  - Baixo (0-49)

## Visualização

Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: criminalip`

## Resposta a Incidentes

Em caso de detecção:
1. Analise o score de risco e indicadores
2. Verifique logs relacionados ao IP
3. Considere bloquear IPs com alto risco
4. Documente incidentes para análise futura 