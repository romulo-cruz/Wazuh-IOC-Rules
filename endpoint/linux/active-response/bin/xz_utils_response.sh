#!/bin/bash

LOG_FILE="/var/ossec/logs/active-response/xz_utils_response.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

log() {
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

check_suspicious_processes() {
    log "Verificando processos suspeitos do SSHD..."
    suspicious_pids=$(ps -ef | grep -w 'sshd' | grep -v pts | awk '{print $2}' | while read pid; do ps --ppid $pid -f; done | grep -v '^UID' | grep -v -E 'sshd: \S+@pts/[0-9]+|sshd: \S+ \[\S+\]' | awk '{print $2}')
    
    if [ ! -z "$suspicious_pids" ]; then
        log "Processos suspeitos encontrados: $suspicious_pids"
        for pid in $suspicious_pids; do
            kill -9 "$pid" 2>/dev/null
            log "Processo $pid terminado"
        done
    fi
}

check_suspicious_ports() {
    log "Verificando portas suspeitas..."
    netstat -tlpn | grep -v ':::\|0.0.0.0' | while read line; do
        port=$(echo "$line" | awk '{print $4}' | cut -d: -f2)
        pid=$(echo "$line" | awk '{print $7}' | cut -d/ -f1)
        
        if [ "$port" != "22" ]; then
            log "Porta suspeita encontrada: $port (PID: $pid)"
            kill -9 "$pid" 2>/dev/null
            log "Processo na porta $port terminado"
        fi
    done
}

check_xz_version() {
    log "Verificando versão do XZ Utils..."
    version=$(xz --version | head -n 1)
    if echo "$version" | grep -E "5\.6\.[01]" > /dev/null; then
        log "Versão vulnerável detectada: $version"
        log "Recomendação: Atualizar XZ Utils imediatamente"
    fi
}

# Execução principal
log "Iniciando resposta à possível exploração da CVE-2024-3094"
check_suspicious_processes
check_suspicious_ports
check_xz_version
log "Resposta concluída" 