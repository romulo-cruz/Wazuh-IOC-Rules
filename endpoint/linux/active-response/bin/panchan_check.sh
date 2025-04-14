#!/bin/bash

# Configuração de logging
LOG_FILE="/var/ossec/logs/panchan_check.log"
exec 1> >(tee -a "$LOG_FILE") 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando verificação do Panchan..."

# Verificar conexões SSH suspeitas
ssh_conns=$(ss -nputw | grep ':22 ' | wc -l)
if [ $ssh_conns -gt 4 ]; then
    echo "ALERTA: Detectadas $ssh_conns conexões SSH simultâneas"
fi

# Verificar porta P2P
if netstat -lno | grep ':1919 ' > /dev/null; then
    echo "ALERTA: Porta P2P 1919 detectada"
fi

# Verificar binários maliciosos
if find /.* -maxdepth 1 -name xinetd -type f > /dev/null; then
    echo "ALERTA: Binário xinetd encontrado em diretório oculto"
fi

# Verificar persistência
if [ -f "/bin/systemd-worker" ] || [ -f "/lib/systemd/system/systemd-worker.service" ]; then
    echo "ALERTA: Mecanismo de persistência detectado"
fi

# Verificar processos de mineração
if ps aux | grep -E "xinetd|systemd-worker" | grep -v grep > /dev/null; then
    echo "ALERTA: Processos de mineração detectados"
fi

# Verificar regras de firewall
if iptables -L INPUT -n | grep "1919" | grep "ACCEPT" > /dev/null; then
    echo "ALERTA: Regra de firewall maliciosa detectada"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Verificação concluída!" 