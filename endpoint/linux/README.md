# Configuração do Endpoint Linux

## Requisitos
- Sistema Linux baseado em Debian/RHEL
- Acesso root

## Instalação

1. Copiar configuração do Wazuh:
```bash
sudo cp ./ossec/ossec.conf /var/ossec/etc/
```

2. Reiniciar o agente Wazuh:
```bash
sudo systemctl restart wazuh-agent
```

## Monitoramento
- Diretórios críticos do sistema
- Logs de autenticação
- Logs do sistema 

# Detecção do Rootkit Snapekit

## Sobre o Snapekit
O Snapekit é um rootkit que visa sistemas Arch Linux (6.10.2-arch1-1 x86_64), com potencial de adaptação para outras distribuições Linux.

## Características
- Evasão de sandbox e debuggers
- Spoofing do processo kworker
- Manipulação de capabilities Linux
- Carregamento de módulo kernel não assinado
- Hooking de syscalls (open, read, write, unlink, ptrace, etc.)

## Detecção
1. Módulos não assinados:
   - Monitoramento de carregamento de módulos kernel
   - Verificação de assinaturas via CONFIG_MODULE_SIG

2. Comportamental:
   - Monitoramento de processos kworker suspeitos
   - Detecção de manipulação de capabilities
   - Verificação de arquivos em /lib/modules

## Proteção
1. Preventiva:
   - Habilitar CONFIG_MODULE_SIG_FORCE
   - Monitoramento de diretórios críticos
   - Verificação de integridade do kernel

2. Resposta:
   - Remoção automática do módulo rootkit
   - Eliminação de arquivos maliciosos
   - Término de processos suspeitos

## Instalação

1. Habilitar verificação de módulos:
   ```bash
   # Verificar configuração atual
   zgrep CONFIG_MODULE_SIG /proc/config.gz
   
   # Habilitar CONFIG_MODULE_SIG_FORCE no kernel
   # Requer recompilação do kernel
   ```

2. Configurar agente Wazuh:
   - Copiar regras para /var/ossec/etc/rules/
   - Copiar script de resposta ativa
   - Atualizar ossec.conf
   - Reiniciar agente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Security Events
- Filtrar por `rule.groups: snapekit` ou `rule.groups: rootkit`

## IOCs
- MD5: 18c23bc9e6dbba7f3cadd59687685718
- SHA1: 00a38e5fd7e3303c23596f0ebdbd1f0e3b481ab3
- SHA256: 2600eb7673dddacda0e780bf3b163b0b89b41f9925eebbd2a2b3dfa234bc1a22 

# Detecção de Vulnerabilidades CUPS

## Vulnerabilidades
1. CVE-2024-47176 (cups-browsed <= 2.0.1)
   - RCE via pacotes UDP não confiáveis
   - Afeta serviço cups-browsed

2. CVE-2024-47076 (libcupsfilters <= 2.1b1)
   - Validação inadequada de atributos IPP
   - Afeta biblioteca libcupsfilters

3. CVE-2024-47175 (libppd <= 2.1b1)
   - Falta de sanitização em atributos IPP
   - Afeta biblioteca libppd

4. CVE-2024-47177 (cups-filters <= 2.0.1)
   - Injeção de comando via parâmetro PPD
   - Afeta pacote cups-filters

## Detecção
1. Verificação de Vulnerabilidades:
   - Monitoramento contínuo de pacotes
   - Comparação com feeds de CVEs
   - Alertas em tempo real

2. Verificações SCA:
   - Análise de versões instaladas
   - Verificação de configurações
   - Status do serviço

## Mitigação
1. Atualização:
   - Atualizar todos os pacotes CUPS
   - Aplicar patches disponíveis
   - Verificar repositórios oficiais

2. Desativação:
   ```bash
   # Desativar serviço cups-browsed
   systemctl stop cups-browsed
   systemctl disable cups-browsed
   ```

3. Remoção:
   ```bash
   # Se não necessário, remover pacotes
   apt remove cups-browsed libcupsfilters libppd cups-filters
   # ou
   yum remove cups-browsed libcupsfilters libppd cups-filters
   ```

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Vulnerability Detection > Inventory
- Filtrar por: `vulnerability.id:(CVE-2024-47175 OR CVE-2024-47176 OR CVE-2024-47076 OR CVE-2024-47177)` 