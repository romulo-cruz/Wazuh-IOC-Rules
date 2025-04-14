#!/bin/bash

LOG_FILE="/var/ossec/logs/active-response/remove_snapekit.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
}

# Verifica se está rodando como root
if [ "$EUID" -ne 0 ]; then
    log "Este script precisa ser executado como root"
    exit 1
fi

log "Iniciando remoção do Snapekit rootkit"

# Remove o módulo do kernel
if lsmod | grep -q "snapekit"; then
    log "Removendo módulo snapekit do kernel"
    rmmod snapekit 2>> "$LOG_FILE"
fi

# Remove arquivos do rootkit
SNAPEKIT_FILES=(
    "/lib/modules/snapekit.ko"
)

for file in "${SNAPEKIT_FILES[@]}"; do
    if [ -f "$file" ]; then
        log "Removendo arquivo: $file"
        rm -f "$file" 2>> "$LOG_FILE"
    fi
done

# Verifica processos kworker suspeitos
ps aux | grep kworker | grep -v grep | while read -r line; do
    pid=$(echo "$line" | awk '{print $2}')
    if [ -n "$pid" ]; then
        log "Verificando processo kworker suspeito (PID: $pid)"
        kill -9 "$pid" 2>> "$LOG_FILE"
    fi
done

log "Remoção do Snapekit concluída"

exit 0 