# Detecção do Apache Text4Shell (CVE-2022-42889)

## Sobre a Vulnerabilidade
O Text4Shell é uma vulnerabilidade na biblioteca Apache Commons Text que afeta as versões 1.5 até 1.9. Permite execução remota de código através da exploração da API StringSubstitutor.

## Características
- CVE: CVE-2022-42889
- CVSS v3: 9.8
- Versões Afetadas: 1.5 - 1.9
- Versão Corrigida: 1.10

## Condições para Exploração
1. Apache Commons Text versão 1.5-1.9 instalada
2. Uso de `org.apache.commons.text.StringSubstitutor`
3. Uso de prefixos vulneráveis (`dns`, `script`, `url`)
4. Processamento de entrada não confiável

## Exemplos de Exploração
| Ataque | Prefixo | Exemplo |
|--------|----------|---------|
| RCE | script | ${script:javascript:java.lang.Runtime.getRuntime().exec('touch /tmp/foo')} |
| DNS | dns | ${dns:address\|commons.apache.org} |
| URL | url | ${url:UTF-8:https://exemplo.com} |

## Detecção
1. Regras de Detecção:
   - Tentativas de exploração via HTTP
   - Uso suspeito do StringSubstitutor
   - Correlação com logs Java

2. Verificação SCA:
   - Busca por versões vulneráveis
   - Verificação de processos Java
   - Análise de configurações web

## Mitigação
1. Atualizar Apache Commons Text para versão 1.10+
2. Revisar uso do StringSubstitutor
3. Validar entradas de usuário
4. Monitorar logs de aplicação

## Instalação
1. Copiar regras:
   ```bash
   cp text4shell_rules.xml /var/ossec/etc/rules/
   ```

2. Configurar SCA:
   ```bash
   mkdir -p /home/local_sca_policies/
   cp text4shell_policy.yml /home/local_sca_policies/
   chown wazuh:wazuh /home/local_sca_policies/text4shell_policy.yml
   ```

3. Atualizar ossec.conf:
   ```xml
   <sca>
     <policies>
       <policy>/home/local_sca_policies/text4shell_policy.yml</policy>
     </policies>
   </sca>
   ```

## Monitoramento
- Alertas no Wazuh Dashboard
- Filtrar por `rule.groups: text4shell`
- Logs de verificação em:
  `/var/ossec/logs/text4shell_check.log` 