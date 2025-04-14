# Detecção da Vulnerabilidade XZ Utils (CVE-2024-3094)

## Sobre a Vulnerabilidade
A CVE-2024-3094 é uma vulnerabilidade crítica (CVSS 10.0) no XZ Utils que permite execução remota de código via SSH.

## Sistemas Afetados
- Fedora 40 e 41
- Debian unstable (Sid)
- openSUSE Tumbleweed e MicroOS
- Kali Linux
- Arch Linux
- Alpine Edge

## Versões Vulneráveis
- XZ Utils 5.6.0
- XZ Utils 5.6.1

## Detecção
1. Vulnerability Detector:
   - Monitoramento contínuo
   - Verificação de versões
   - Alertas automáticos

2. Regras Personalizadas:
   - Detecção da CVE-2024-3094
   - Monitoramento de versões
   - Correlação com SSH

3. Verificações Adicionais:
   - Bibliotecas suspeitas
   - Configurações SSH
   - Logs do sistema

## Mitigação
1. Downgrade:
   - Retornar para versão anterior a 5.6.0
   - Verificar compatibilidade

2. Atualização:
   - Atualizar para versão corrigida
   - Seguir recomendações da distribuição

## Instalação
1. Configurar Vulnerability Detector:
   ```bash
   cp vulnerability_config.xml /var/ossec/etc/shared/
   ```

2. Instalar regras e scripts:
   ```bash
   cp xz_utils_vuln_rules.xml /var/ossec/etc/rules/
   cp xz_utils_check.py /var/ossec/active-response/bin/
   chmod +x /var/ossec/active-response/bin/xz_utils_check.py
   ```

3. Reiniciar serviço:
   ```bash
   systemctl restart wazuh-manager
   ```

## Monitoramento
- Alertas no Wazuh Dashboard
- Filtrar por `vulnerability.cve=CVE-2024-3094`
- Logs em `/var/ossec/logs/xz_utils_check.log` 