# Detecção de Ataques Living Off the Land (LOTL)

## Sobre Ataques LOTL
Ataques Living Off the Land utilizam ferramentas legítimas do sistema para realizar atividades maliciosas, tornando a detecção mais difícil.

## Características
- Uso de ferramentas nativas do sistema
- Execução em memória
- Mínima escrita em disco
- Difícil detecção por métodos tradicionais

## Detecção
1. Monitoramento de Processos:
   - Execuções suspeitas via curl/bash
   - Uso do DDexec
   - Padrões de comando suspeitos

2. Monitoramento FIM:
   - Modificações em /etc/passwd
   - Alterações em binários do sistema
   - Arquivos temporários suspeitos

3. Monitoramento de Rede:
   - Conexões suspeitas
   - Downloads via curl
   - Comunicações não usuais

## Resposta Automática
1. Backup:
   - Cópia de arquivos críticos
   - Preservação de timestamps
   - Registro de alterações

2. Contenção:
   - Término de processos suspeitos
   - Bloqueio de conexões
   - Restauração de arquivos

3. Investigação:
   - Logs detalhados
   - Timeline de eventos
   - Correlação de alertas

## Instalação
1. Configurar monitoramento:
   ```bash
   # Copiar arquivos de configuração
   cp lotl_fim.conf /var/ossec/etc/shared/
   cp lotl_monitoring.conf /var/ossec/etc/shared/
   
   # Instalar script de resposta
   cp lotl_response.py /var/ossec/active-response/bin/
   chmod +x /var/ossec/active-response/bin/lotl_response.py
   ```

2. Atualizar agente:
   - Reiniciar serviço do Wazuh
   - Verificar logs de inicialização

## Monitoramento
- Alertas no Wazuh Dashboard
- Filtrar por `rule.groups: lotl`
- Logs de resposta em:
  `/var/ossec/logs/active-response/lotl_response.log` 