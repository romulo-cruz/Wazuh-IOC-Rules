#!/bin/bash

# Configuração de logging
LOG_FILE="/var/log/panchan_setup.log"
exec 1> >(tee -a "$LOG_FILE") 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando configuração de monitoramento do Panchan..."

# Instalar dependências
echo "Instalando dependências..."
apt-get update
apt-get install -y net-tools yara

# Configurar permissões para comandos remotos
echo "Configurando permissões para comandos remotos..."
echo "logcollector.remote_commands=1" >> /var/ossec/etc/local_internal_options.conf

# Configurar monitoramento FIM
echo "Configurando monitoramento FIM..."
cat >> /var/ossec/etc/ossec.conf << 'EOF'
<syscheck>
  <directories check_all="yes" realtime="yes">/root</directories>
  <directories check_all="yes" realtime="yes">/lib/systemd/system</directories>
  <directories check_all="yes" realtime="yes">/bin</directories>
</syscheck>
EOF

# Configurar YARA
echo "Configurando YARA..."
mkdir -p /var/ossec/active-response/bin/yara/rules
cp panchan.yar /var/ossec/active-response/bin/yara/rules/

# Configurar script de resposta ativa
echo "Configurando resposta ativa..."
cp panchan_cleanup.py /var/ossec/active-response/bin/
chmod 750 /var/ossec/active-response/bin/panchan_cleanup.py
chown root:wazuh /var/ossec/active-response/bin/panchan_cleanup.py

# Configurar regras de firewall iniciais
echo "Configurando regras de firewall..."
iptables -D INPUT -p tcp --dport 1919 -j ACCEPT 2>/dev/null
iptables -A INPUT -p tcp --dport 1919 -j DROP

# Reiniciar agente
echo "Reiniciando agente Wazuh..."
systemctl restart wazuh-agent

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Configuração concluída!" 