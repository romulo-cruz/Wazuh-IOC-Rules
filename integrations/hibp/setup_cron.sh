#!/bin/bash

# Adicionar job ao crontab para executar semanalmente
(crontab -l 2>/dev/null; echo "0 0 */7 * * /usr/bin/python3 /var/ossec/integrations/hibp/hibp.py") | crontab - 