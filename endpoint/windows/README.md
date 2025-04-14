# Configuração do Endpoint Windows

## Proteção contra Malware Peaklight

Este endpoint está configurado com regras específicas para detectar e prevenir o malware Peaklight, incluindo:

- Detecção de execução suspeita de PowerShell
- Monitoramento de modificações no registro
- Detecção de injeção de DLL
- Análise YARA de arquivos suspeitos

### Requisitos Adicionais

1. YARA
   - Baixe e instale o YARA do [repositório oficial](https://github.com/VirusTotal/yara/releases)
   - Instale no diretório padrão: `C:\Program Files\yara`

2. Sysmon
   - Use a configuração fornecida em `sysmon/config/sysmonconfig.xml`
   - Configure para monitorar especificamente atividades do Peaklight

### Instalação

1. Instale o YARA:
```powershell
# Baixar e instalar YARA
$YaraPath = "C:\Program Files\yara"
New-Item -ItemType Directory -Force -Path $YaraPath
# Copie os arquivos do YARA para o diretório
```

2. Configure as regras YARA:
```powershell
Copy-Item .\yara\*.yar "C:\Program Files\ossec-agent\shared\yara\"
```

3. Configure a resposta ativa:
```powershell
Copy-Item .\active-response\yara.bat "C:\Program Files (x86)\ossec-agent\active-response\bin\"
```

### Monitoramento

- Execução suspeita de PowerShell
- Modificações no registro do sistema
- Carregamento de DLLs suspeitas
- Arquivos suspeitos em diretórios temporários

## Proteção contra Ransomware Lynx

Este endpoint está configurado com proteções específicas contra o ransomware Lynx, incluindo:

- Detecção de criação de notas de resgate
- Monitoramento de extensões .LYNX
- Sistema de recuperação automática via Shadow Copy

### Recursos de Proteção

1. Detecção
   - Monitoramento de arquivos em tempo real
   - Detecção de padrões de ransomware
   - Identificação de notas de resgate

2. Resposta
   - Recuperação automática via Shadow Copy
   - Logging de eventos
   - Alertas em tempo real

### Recuperação

Em caso de infecção, o sistema:
1. Detecta a atividade do ransomware
2. Ativa o Volume Shadow Copy
3. Recupera os arquivos afetados
4. Armazena em C:\Recovered_Files

## Proteção contra Brain Cipher Ransomware

Este endpoint está configurado com proteções específicas contra o ransomware Brain Cipher:

### Detecções
- Execução do executável do Brain Cipher
- Tentativas de bypass UAC via DllHost
- Acesso ao LSASS para roubo de credenciais
- Modificações no serviço VSS
- Criação de notas de resgate
- Criptografia de arquivos

### Medidas de Proteção
1. Monitoramento em tempo real de diretórios críticos
2. Proteção do serviço VSS
3. Bloqueio de execução de DllHost com CLSID malicioso
4. Criação automática de pontos de restauração

### Resposta a Incidentes
Em caso de detecção:
1. O serviço VSS é restaurado automaticamente
2. Um ponto de restauração do sistema é criado
3. A execução do DllHost com CLSID malicioso é bloqueada
4. Alertas são gerados no dashboard do Wazuh

## Requisitos
- Windows 10/11
- Permissões de Administrador
- PowerShell 5.1 ou superior

## Instalação

1. Instalar Sysmon:
```powershell
.\sysmon\install.ps1
```

2. Copiar configuração do Wazuh:
```powershell
Copy-Item .\ossec\ossec.conf "C:\Program Files (x86)\ossec-agent\"
```

3. Reiniciar o agente Wazuh:
```powershell
Restart-Service -Name wazuh
```

## Monitoramento
- Execução de PowerShell
- Criação de arquivos em diretórios temporários
- Modificações no registro
- Carregamento de DLLs suspeitas

# Proteção contra Ransomware Razr

## Características do Razr
- Criptografa arquivos usando AES-256
- Adiciona extensão `.raz` aos arquivos criptografados
- Cria notas de resgate `README.txt`
- Pode exfiltrar dados para servidor C2

## Detecção
- Monitoramento de eventos Sysmon
- Detecção de criptografia de arquivos
- Detecção de criação de notas de resgate
- Correlação de eventos múltiplos

## Proteção
1. Pré-execução:
   - Monitoramento FIM
   - Integração com VirusTotal/YARA
   - Bloqueio de extensões suspeitas

2. Pós-execução:
   - Recuperação via Shadow Copy
   - Isolamento do endpoint
   - Bloqueio de comunicação C2

## Recuperação
O script `razr_recovery.ps1` automaticamente:
1. Identifica arquivos criptografados
2. Localiza shadow copies disponíveis
3. Restaura arquivos originais
4. Remove arquivos criptografados

## Instalação
1. Instalar Sysmon:
   ```powershell
   New-Item -ItemType Directory -Path C:\Sysmon
   # Baixar e extrair Sysmon
   cd C:\Sysmon
   .\Sysmon64.exe -accepteula -i sysmonconfig.xml
   ```

2. Configurar agente Wazuh:
   - Copiar configurações para ossec.conf
   - Copiar scripts de resposta ativa
   - Reiniciar agente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: razr`

# Proteção contra Malware DeerStealer

## Características do DeerStealer
- Roubo de credenciais de navegadores
- Roubo de carteiras de criptomoedas
- Persistência via registro do Windows
- Comunicação com servidor C2
- Execução em memória

## Detecção
- Monitoramento de eventos Sysmon
- Detecção de arquivos maliciosos
- Detecção de modificações no registro
- Detecção de conexões suspeitas
- Correlação de eventos múltiplos

## Proteção
1. Pré-execução:
   - Monitoramento FIM
   - Bloqueio de executáveis suspeitos
   - Monitoramento de registro

2. Pós-execução:
   - Remoção de arquivos maliciosos
   - Limpeza do registro
   - Interrupção de processos maliciosos

## Instalação
1. Instalar Sysmon:
   ```powershell
   New-Item -ItemType Directory -Path C:\Sysmon
   # Baixar e extrair Sysmon
   cd C:\Sysmon
   .\Sysmon64.exe -accepteula -i sysmonconfig.xml
   ```

2. Configurar agente Wazuh:
   - Copiar configurações para ossec.conf
   - Copiar scripts de resposta ativa
   - Reiniciar agente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: deerstealer`

# Proteção contra BLX Stealer

## Características do BLX Stealer
- Roubo de credenciais
- Roubo de carteiras de criptomoedas
- Execução via PowerShell
- Persistência via pasta Startup
- Comunicação com APIs externas

## Detecção
1. Comportamental:
   - Scripts PowerShell maliciosos
   - Execução via cmd.exe
   - Arquivos em pastas temporárias
   - Tentativas de persistência

2. YARA:
   - Padrões de strings conhecidos
   - Características do executável
   - APIs de geolocalização

## Proteção
1. Pré-execução:
   - Monitoramento de Downloads
   - Varredura YARA
   - Bloqueio de executáveis suspeitos

2. Pós-execução:
   - Remoção de arquivos maliciosos
   - Interrupção de processos
   - Limpeza de persistência

## Instalação
1. Instalar Sysmon:
   ```powershell
   New-Item -ItemType Directory -Path C:\Sysmon
   # Baixar e extrair Sysmon
   cd C:\Sysmon
   .\Sysmon64.exe -accepteula -i sysmonconfig.xml
   ```

2. Configurar agente Wazuh:
   - Copiar configurações para ossec.conf
   - Copiar scripts de resposta ativa
   - Copiar regras YARA
   - Reiniciar agente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: blx_detection_rule`

# Proteção contra Snake Keylogger

## Características do Snake Keylogger
- Captura de teclas digitadas
- Captura de screenshots
- Roubo de dados da área de transferência
- Persistência via tarefas agendadas
- Auto-remoção após execução

## Detecção
1. Comportamental:
   - Modificações no Windows Defender
   - Criação de tarefas agendadas
   - Modificações no registro
   - Tentativas de auto-remoção

2. SCA:
   - Verificação de artefatos conhecidos
   - Verificação de exclusões do Windows Defender
   - Verificação de tarefas agendadas suspeitas

## Proteção
1. Pré-execução:
   - Monitoramento FIM
   - Verificação de registro
   - Monitoramento de exclusões do Windows Defender

2. Pós-execução:
   - Remoção de arquivos maliciosos
   - Limpeza de registro
   - Remoção de exclusões do Windows Defender
   - Remoção de tarefas agendadas

## Instalação
1. Instalar Sysmon:
   ```powershell
   New-Item -ItemType Directory -Path C:\Sysmon
   # Baixar e extrair Sysmon
   cd C:\Sysmon
   .\Sysmon64.exe -accepteula -i sysmonconfig.xml
   ```

2. Configurar agente Wazuh:
   - Copiar configurações para ossec.conf
   - Copiar scripts de resposta ativa
   - Copiar política SCA
   - Reiniciar agente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Wazuh Dashboard > Configuration Assessment
- Filtrar por `rule.groups: snake_keylogger`

# Proteção contra Exploração do PowerShell

## Técnicas Detectadas
1. Comandos Codificados:
   - Base64
   - EncodedCommand
   - FromBase64String

2. Download Cradles:
   - Invoke-WebRequest
   - MSHTA
   - WebClient

3. CMDLets Maliciosos:
   - Mimikatz
   - PowerSploit
   - PowerView
   - Outros frameworks maliciosos

4. Bypass de Segurança:
   - ExecutionPolicy Bypass
   - Contorno de AMSI
   - Desativação de logs

## Configuração
1. Habilitar Logging:
   ```powershell
   # Executar script de configuração
   .\enable_powershell_logging.ps1
   ```

2. Configurar agente Wazuh:
   - Copiar configurações para ossec.conf
   - Copiar scripts de resposta ativa
   - Reiniciar agente

## Resposta Automática
Em caso de detecção:
1. Bloqueio de processos suspeitos
2. Criação de regras de firewall
3. Logging de atividades
4. Notificação de incidentes

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: powershell`

## Mitigação
1. Usar AppLocker/WDAC para restringir execução
2. Implementar logging detalhado
3. Monitorar atividades suspeitas
4. Manter sistema atualizado

# Proteção contra BlackSuit Ransomware

## Características do BlackSuit
- Execução via argumento "-name"
- Remoção de shadow copies
- Uso do Windows Restart Manager
- Criação de notas de resgate
- Extensão ".blacksuit"

## Detecção
1. Comportamental:
   - Execução com argumentos específicos
   - Remoção de shadow copies
   - Criação de notas de resgate
   - Criptografia de arquivos

2. YARA:
   - Padrões de strings conhecidos
   - APIs do Restart Manager
   - Extensões e notas de resgate

## Proteção
1. Pré-execução:
   - Monitoramento de Downloads
   - Varredura YARA
   - Bloqueio de executáveis suspeitos

2. Pós-execução:
   - Restauração via shadow copies
   - Remoção de notas de resgate
   - Recuperação de arquivos

## Instalação
1. Instalar Sysmon:
   ```powershell
   New-Item -ItemType Directory -Path C:\Sysmon
   # Baixar e extrair Sysmon
   cd C:\Sysmon
   .\Sysmon64.exe -accepteula -i sysmonconfig.xml
   ```

2. Configurar agente Wazuh:
   - Copiar configurações para ossec.conf
   - Copiar scripts de resposta ativa
   - Copiar regras YARA
   - Reiniciar agente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: BlackSuit`

# Detecção do Lumma Stealer

## Sobre o Lumma Stealer
O Lumma Stealer (LummaC2) é um malware escrito em C/C++ distribuído como MaaS (Malware-as-a-Service) que visa roubar dados sensíveis de sistemas Windows.

## Características
- Anti-sandbox usando detecção de movimento do cursor
- Criptografia AES-256 para payloads
- Injeção em processos legítimos
- Evasão de debugger
- Elevação de privilégios
- Roubo de dados sensíveis

## Detecção
1. Comportamental:
   - Monitoramento de processos suspeitos
   - Detecção de injeção de processos
   - Identificação de comunicações C2
   - Análise de modificações no registro

2. Arquivos:
   - Varredura via VirusTotal
   - Monitoramento FIM
   - Detecção de arquivos maliciosos

## Proteção
1. Preventiva:
   - Monitoramento de diretórios críticos
   - Integração com VirusTotal
   - Análise de comportamento suspeito

2. Resposta:
   - Remoção automática de arquivos maliciosos
   - Término de processos suspeitos
   - Limpeza de artefatos

## IOCs
- MD5: cf9a2518d062283a422f243273f7094f
- SHA256: b9c71471d52e93c38eeb069082dcdea935f928024b6db3fce153c63d4af1b27c

## Instalação
1. Instalar Sysmon:
   ```powershell
   # Baixar e extrair Sysmon
   # Configurar com sysmonconfig.xml
   .\Sysmon64.exe -accepteula -i sysmonconfig.xml
   ```

2. Configurar agente Wazuh:
   - Copiar regras e scripts
   - Atualizar ossec.conf
   - Configurar integração VirusTotal
   - Reiniciar agente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: lumma` ou `rule.groups: stealer`

# Proteção contra Ransomware

## Características
- Detecção pré-execução via VirusTotal
- Monitoramento em tempo real de diretórios críticos
- Detecção de comportamentos típicos de ransomware
- Recuperação automática via Volume Shadow Copy
- Proteção contra remoção de backups

## Detecção
1. Comportamental:
   - Múltiplas operações de criptografia
   - Tentativas de remoção de shadow copies
   - Criação de notas de resgate
   - Remoção de backups

2. Preventiva:
   - Integração com VirusTotal
   - Monitoramento FIM
   - Proteção de shadow copies

## Recuperação
1. Automática:
   - Restauração via shadow copies
   - Proteção contra remoção de backups
   - Logs detalhados do processo

2. Manual (se necessário):
   ```powershell
   # Executar script de recuperação manualmente
   Powershell -ExecutionPolicy bypass -File "C:\Program Files (x86)\ossec-agent\active-response\bin\rollback.ps1"
   ```

## Instalação
1. Configurar agente Wazuh:
   - Copiar scripts de recuperação
   - Atualizar ossec.conf
   - Configurar integração VirusTotal
   - Reiniciar agente

2. Verificar espaço em disco:
   - Garantir espaço suficiente para shadow copies
   - Monitorar uso de disco regularmente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Security Events
- Filtrar por `rule.groups: ransomware`

## Observações
- Mantenha espaço em disco suficiente para shadow copies
- Configure backups externos regulares
- Mantenha o sistema atualizado
- Use proteção em tempo real

# Detecção do Malware Latrodectus

## Sobre o Latrodectus
O Latrodectus é um malware loader sofisticado que visa sistemas Windows, distribuído através de campanhas de phishing e associado ao trojan bancário IcedID.

## Características
- Auto-replicação em locais ocultos
- Persistência via tarefas agendadas
- DLL Side-loading
- Comunicação com servidor C2

## Detecção
1. Comportamental:
   - Criação de arquivos suspeitos
   - Estabelecimento de persistência
   - DLL Side-loading
   - Conexões de rede suspeitas

2. Preventiva:
   - Integração com VirusTotal
   - Monitoramento FIM
   - Análise de comportamento

## Resposta
1. Automática:
   - Término de processos maliciosos
   - Remoção de persistência
   - Limpeza de arquivos
   - Logs detalhados

## Instalação
1. Instalar Sysmon:
   ```powershell
   New-Item -ItemType Directory -Path C:\Sysmon
   # Baixar e extrair Sysmon
   cd C:\Sysmon
   .\Sysmon64.exe -accepteula -i sysmonconfig.xml
   ```

2. Configurar agente Wazuh:
   - Copiar regras e scripts
   - Atualizar ossec.conf
   - Configurar integração VirusTotal
   - Reiniciar agente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: latrodectus`

# Detecção do Mint Stealer

## Sobre o Mint Stealer
O Mint Stealer é um malware em Python que rouba dados de navegadores, carteiras de criptomoedas, clientes VPN, emails e jogos.

## Características
- Extração de payload da seção de recursos
- Criação de arquivos em AppData\Local\Temp
- Carregamento de DLLs e módulos Python
- Coleta de dados sensíveis
- Compactação de dados roubados

## Detecção
1. Comportamental:
   - Monitoramento de criação de arquivos
   - Detecção de carregamento de DLLs
   - Análise de comandos wmic
   - Monitoramento da área de transferência

2. YARA:
   - Detecção de padrões conhecidos
   - Análise de strings
   - Verificação de caminhos suspeitos

## Resposta
1. Automática:
   - Varredura YARA
   - Remoção de arquivos maliciosos
   - Logs detalhados

## Instalação
1. Instalar Sysmon:
   ```powershell
   # Baixar e extrair Sysmon
   # Configurar com sysmonconfig.xml
   .\Sysmon64.exe -accepteula -i sysmonconfig.xml
   ```

2. Configurar agente Wazuh:
   - Copiar regras e scripts
   - Atualizar ossec.conf
   - Configurar YARA
   - Reiniciar agente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Filtrar por `rule.groups: mint_stealer`

# Detecção do PureHVNC RAT

## Sobre o PureHVNC
O PureHVNC é um Trojan de Acesso Remoto (RAT) que permite controle remoto oculto de sistemas Windows.

## Características
- Distribuição via phishing
- Download de arquivos ZIP maliciosos
- Execução de scripts Python
- Ocultação de arquivos e pastas
- Comunicação com servidor C2

## Detecção
1. Comportamental:
   - Execução retardada de PDF
   - Downloads suspeitos
   - Extração de arquivos ZIP
   - Ocultação de pastas
   - Execução de scripts Python

2. Verificação SCA:
   - Arquivos ZIP maliciosos
   - Scripts Python suspeitos
   - Pastas ocultas
   - Conexões de rede

## IOCs
- SHA256: 441c4502584240624f4af6d67eded476c781ff0b72afe95ea236cc87a50e5650
- MD5: 372d3835bc694a7d9934727030bf7be6

## Instalação
1. Instalar Sysmon:
   ```powershell
   # Baixar e extrair Sysmon
   # Configurar com sysmonconfig.xml
   .\Sysmon64.exe -accepteula -i sysmonconfig.xml
   ```

2. Configurar agente Wazuh:
   - Copiar regras e políticas SCA
   - Atualizar ossec.conf
   - Reiniciar agente

## Monitoramento
Os alertas podem ser visualizados em:
- Wazuh Dashboard > Threat Intelligence > Threat Hunting
- Wazuh Dashboard > Configuration Assessment
- Filtrar por `rule.groups: purehvnc` 