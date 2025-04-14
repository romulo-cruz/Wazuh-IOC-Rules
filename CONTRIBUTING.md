# Contribuindo com o Repositório de Regras Wazuh

## Como Contribuir

1. Fork o repositório
2. Crie um branch para sua feature (`git checkout -b feature/nova-regra`)
3. Teste suas alterações usando os scripts em `tests/`
4. Commit suas alterações (`git commit -am 'Adiciona nova regra para detecção X'`)
5. Push para o branch (`git push origin feature/nova-regra`)
6. Crie um Pull Request

## Padrões de Código

### Regras
- IDs de regras devem ser > 100000
- Cada regra deve ter uma descrição clara
- Documente o propósito da regra nos comentários

### Decoders
- Nomes únicos e descritivos
- Teste todos os casos possíveis

## Testes
- Execute `tests/rule_tests/test_rules.sh` antes de submeter
- Adicione casos de teste para novas regras 