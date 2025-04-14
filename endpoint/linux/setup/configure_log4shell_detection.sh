#!/bin/bash

# Configuração de logging
LOG_FILE="/var/log/log4shell_setup.log"
exec 1> >(tee -a "$LOG_FILE") 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando configuração de detecção Log4Shell..."

# Instalar unzip se não estiver instalado
if ! command -v unzip &> /dev/null; then
    echo "Instalando unzip..."
    if [ -f /etc/debian_version ]; then
        apt-get update
        apt-get install -y unzip
    elif [ -f /etc/redhat-release ]; then
        yum -y install unzip
    fi
fi

# Configurar SCA
echo "Configurando SCA..."
echo "sca.remote_commands=1" >> /var/ossec/etc/local_internal_options.conf

# Configurar monitoramento de logs web
if [ -f /etc/apache2/apache2.conf ]; then
    echo "Configurando monitoramento de logs Apache..."
    cat >> /var/ossec/etc/ossec.conf << 'EOF'
<localfile>
  <log_format>apache</log_format>
  <location>/var/log/apache2/access.log</location>
</localfile>
EOF
elif [ -f /etc/httpd/conf/httpd.conf ]; then
    echo "Configurando monitoramento de logs HTTPD..."
    cat >> /var/ossec/etc/ossec.conf << 'EOF'
<localfile>
  <log_format>apache</log_format>
  <location>/var/log/httpd/access_log</location>
</localfile>
EOF
fi

# Configurar monitoramento de processos Java
cat >> /var/ossec/etc/ossec.conf << 'EOF'
<localfile>
  <log_format>full_command</log_format>
  <command>ps aux | grep java | grep -v grep</command>
  <frequency>300</frequency>
</localfile>
EOF

# Configurar FIM para bibliotecas Java
cat >> /var/ossec/etc/ossec.conf << 'EOF'
<syscheck>
  <directories check_all="yes" realtime="yes">/usr/share/java</directories>
  <directories check_all="yes" realtime="yes">/usr/lib/java</directories>
  <directories check_all="yes" realtime="yes">/opt/*/lib</directories>
</syscheck>
EOF

# Reiniciar agente
systemctl restart wazuh-agent

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Configuração concluída!" 