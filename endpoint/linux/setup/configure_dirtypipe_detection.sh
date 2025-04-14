#!/bin/bash

# Configuração de logging
LOG_FILE="/var/log/dirtypipe_setup.log"
exec 1> >(tee -a "$LOG_FILE") 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando configuração de detecção Dirty Pipe..."

# Instalar Auditd
echo "Instalando Auditd..."
apt install -y auditd

# Configurar regras Auditd
echo "Configurando regras Auditd..."
cat >> /etc/audit/rules.d/audit.rules << 'EOF'
# Monitorar chamadas splice suspeitas
-a always,exit -F arch=b64 -S splice -F a0=0x3 -F a2=0x5 -F a3=0x0 -F key=dirtypipe
-a always,exit -F arch=b64 -S splice -F a0=0x6 -F a2=0x8 -F a3=0x0 -F key=dirtypipe
-a always,exit -F arch=b64 -S splice -F a0=0x7 -F a2=0x9 -F a3=0x0 -F key=dirtypipe

# Monitorar modificações no /etc/passwd
-w /etc/passwd -p w -k audit-wazuh-w
EOF

# Recarregar regras
auditctl -R /etc/audit/rules.d/audit.rules

# Configurar Wazuh para monitorar logs do Auditd
cat >> /var/ossec/etc/ossec.conf << 'EOF'
<localfile>
    <log_format>audit</log_format>
    <location>/var/log/audit/audit.log</location>
</localfile>
EOF

# Configurar permissões para comandos remotos SCA
echo "sca.remote_commands=1" >> /var/ossec/etc/local_internal_options.conf

# Reiniciar serviços
systemctl restart auditd
systemctl restart wazuh-agent

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Configuração concluída!" 