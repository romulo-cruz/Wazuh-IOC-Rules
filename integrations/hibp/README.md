# Integração Wazuh-HIBP

Esta integração permite monitorar vazamentos de dados usando o serviço Have I Been Pwned.

## Requisitos

1. API Key do HIBP (https://haveibeenpwned.com/API/Key)
2. Python 3.8 ou superior
3. Módulo `requests` do Python

## Instalação

1. Configure sua API Key:
   ```bash
   sed -i "s/<YOUR_HIBP_API_KEY>/sua-api-key/" hibp.py
   ```

2. Adicione emails para monitoramento:
   ```bash
   echo "email@exemplo.com" >> /var/ossec/etc/lists/monitored_emails.txt
   ```

3. Configure o cron job:
   ```bash
   ./setup_cron.sh
   ```

## Monitoramento

Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: hibp`

## Alertas

- Nível 10: Vazamento detectado
- Nível 12: Vazamento crítico detectado

## Resposta a Incidentes

Em caso de detecção:
1. Verifique os detalhes do vazamento no dashboard
2. Notifique os usuários afetados
3. Force a alteração das senhas
4. Ative autenticação de dois fatores 