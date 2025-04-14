# Wazuh-rules
Conjunto de regras para integração com Wazuh

## Estrutura do Repositório

### Diretórios Principais
- `active-response/`: Scripts de resposta ativa
  - `bin/`: Executáveis de resposta ativa (ex: ioc-builder.py)
- `config/`: Arquivos de configuração
  - `ossec.conf`: Configurações principais do Wazuh
- `decoders/`: Decoders personalizados
  - `local_decoder.xml`: Decoders locais
- `integrations/`: Scripts de integração
  - `custom_integration.py`: Integrações personalizadas
- `lists/`: Listas CDB e IoCs
  - `mal-ip-list`: IPs maliciosos
  - `mal-url-list`: URLs suspeitas
  - `mal-md5-list`: Hashes MD5 maliciosos
- `rules/`: Regras personalizadas
  - `local_rules.xml`: Regras locais
- `tests/`: Testes automatizados
  - `rule_tests/`: Testes de regras
- `tools/`: Scripts utilitários
  - `rule_validator.sh`: Validador de regras

### Arquivos Principais
- `install.sh`: Script de instalação/atualização
- `.gitignore`: Configuração de arquivos ignorados pelo Git
- `README.md`: Documentação do projeto

## Configuração de IoCs
Este repositório inclui configuração para detecção e armazenamento automático de:
- IPs maliciosos
- URLs suspeitas
- Hashes MD5 de arquivos maliciosos

## Instalação
1. Clone este repositório:
   ```bash
   git clone [URL_DO_REPOSITÓRIO] /opt/wazuh-rules
   ```

2. Execute o script de instalação:
   ```bash
   cd /opt/wazuh-rules
   sudo ./install.sh
   ```

## Atualizando
Para atualizar as regras e IoCs:
```bash
cd /opt/wazuh-rules
git pull
sudo ./install.sh
```

## Estrutura das Regras
- As regras personalizadas devem ter IDs maiores que 100000 para evitar conflitos
- Todos os decoders personalizados devem ser definidos em `decoders/local_decoder.xml`
- Todas as regras personalizadas devem ser definidas em `rules/local_rules.xml`

## Testes
Para executar os testes das regras:
```bash
cd /opt/wazuh-rules
./tools/rule_validator.sh
```

## Contribuindo
1. Crie um branch para sua feature (`git checkout -b feature/nome-da-feature`)
2. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`)
3. Faça push para o branch (`git push origin feature/nome-da-feature`)
4. Crie um Pull Request
