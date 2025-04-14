#!/bin/bash

# Configuração de logging
LOG_FILE="/var/log/bpfdoor_setup.log"
exec 1> >(tee -a "$LOG_FILE") 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando configuração de detecção BPFDoor..."

# Instalar Auditd
echo "Instalando Auditd..."
if [ -f /etc/debian_version ]; then
    apt -y install auditd
elif [ -f /etc/redhat-release ]; then
    yum -y install auditd
fi

# Configurar regras Auditd
echo "Configurando regras Auditd..."
cat >> /etc/audit/rules.d/audit.rules << 'EOF'
# Monitorar arquivos maliciosos do BPFDoor
-w /dev/shm/kdmtmpflush -p wa -k possible_bpfdoor_infection
-w /var/run/haldrund.pid -p wa -k possible_bpfdoor_infection
-w /var/run/kdevrund.pid -p wa -k possible_bpfdoor_infection
-w /var/run/xinetd.lock -p wa -k possible_bpfdoor_infection
-w /var/run/syslogd.reboot -p wa -k possible_bpfdoor_infection
EOF

# Recarregar regras
auditctl -R /etc/audit/rules.d/audit.rules

# Configurar Wazuh para monitorar logs do Auditd
cat >> /var/ossec/etc/ossec.conf << 'EOF'
<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/audit/audit.log</location>
</localfile>

<syscheck>
  <directories check_all="yes" realtime="yes">/dev/shm</directories>
  <directories check_all="yes" realtime="yes">/var/run</directories>
</syscheck>
EOF

# Configurar permissões para comandos remotos SCA
echo "sca.remote_commands=1" >> /var/ossec/etc/local_internal_options.conf

# Reiniciar serviços
systemctl restart auditd
systemctl restart wazuh-agent

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Configuração concluída!" 