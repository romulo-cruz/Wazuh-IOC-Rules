# Configuração do Endpoint macOS

## Requisitos
- macOS 10.15 ou superior
- Acesso administrativo

## Instalação

1. Copiar configuração do Wazuh:
```bash
sudo cp ./ossec/ossec.conf /Library/Ossec/etc/
```

2. Reiniciar o agente Wazuh:
```bash
sudo /Library/Ossec/bin/wazuh-control restart
```

## Monitoramento
- Diretórios de usuários
- Diretórios temporários
- Logs do sistema 