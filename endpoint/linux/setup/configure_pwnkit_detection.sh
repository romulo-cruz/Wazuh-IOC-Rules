#!/bin/bash

# Configuração de logging
LOG_FILE="/var/log/pwnkit_setup.log"
exec 1> >(tee -a "$LOG_FILE") 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando configuração de detecção PwnKit..."

# Instalar Auditd se não estiver instalado
if ! command -v auditd &> /dev/null; then
    echo "Instalando Auditd..."
    if [ -f /etc/debian_version ]; then
        apt-get update
        apt-get install -y auditd
    elif [ -f /etc/redhat-release ]; then
        yum -y install audit
    fi
fi

# Configurar regras Auditd
echo "Configurando regras Auditd..."
cat >> /etc/audit/rules.d/audit.rules << 'EOF'
# Monitorar execução do pkexec
-w /usr/bin/pkexec -p x

# Monitorar downloads suspeitos
-w /usr/bin/curl -p x
-w /usr/bin/wget -p x

# Monitorar modificações em arquivos críticos
-w /usr/bin/pkexec -p wa
-w /etc/shells -p wa
EOF

# Recarregar regras
auditctl -R /etc/audit/rules.d/audit.rules

# Configurar Wazuh para monitorar logs do Auditd
cat >> /var/ossec/etc/ossec.conf << 'EOF'
<localfile>
  <log_format>audit</log_format>
  <location>/var/log/audit/audit.log</location>
</localfile>

<syscheck>
  <directories check_all="yes" realtime="yes">/usr/bin/pkexec</directories>
  <directories check_all="yes" realtime="yes">/etc/shells</directories>
</syscheck>
EOF

# Configurar detector de vulnerabilidades
if [ -f /etc/redhat-release ]; then
    cat >> /var/ossec/etc/ossec.conf << 'EOF'
<vulnerability-detector>
  <enabled>yes</enabled>
  <interval>1h</interval>
  <ignore_time>6h</ignore_time>
  <run_on_start>yes</run_on_start>

  <provider name="redhat">
    <enabled>yes</enabled>
    <os>5</os>
    <os>6</os>
    <os>7</os>
    <os>8</os>
    <update_interval>1h</update_interval>
  </provider>
</vulnerability-detector>
EOF
elif [ -f /etc/debian_version ]; then
    cat >> /var/ossec/etc/ossec.conf << 'EOF'
<vulnerability-detector>
  <enabled>yes</enabled>
  <interval>1h</interval>
  <ignore_time>6h</ignore_time>
  <run_on_start>yes</run_on_start>

  <provider name="debian">
    <enabled>yes</enabled>
    <os>stretch</os>
    <os>buster</os>
    <os>bullseye</os>
    <update_interval>1h</update_interval>
  </provider>
</vulnerability-detector>
EOF
fi

# Aplicar mitigação temporária (opcional)
# echo "Aplicando mitigação temporária..."
# chmod 0755 /usr/bin/pkexec

# Reiniciar serviços
systemctl restart auditd
systemctl restart wazuh-agent

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Configuração concluída!" 