# Script de instalação do Sysmon
$SysmonUrl = "https://download.sysinternals.com/files/Sysmon.zip"
$SysmonZip = "$env:TEMP\Sysmon.zip"
$SysmonDir = "$env:ProgramFiles\Sysmon"

# Criar diretório se não existir
if (!(Test-Path $SysmonDir)) {
    New-Item -ItemType Directory -Path $SysmonDir
}

# Download do Sysmon
Invoke-WebRequest -Uri $SysmonUrl -OutFile $SysmonZip

# Extrair Sysmon
Expand-Archive -Path $SysmonZip -DestinationPath $SysmonDir -Force

# Copiar arquivo de configuração
Copy-Item ".\config\sysmonconfig.xml" -Destination $SysmonDir

# Instalar Sysmon
& "$SysmonDir\Sysmon64.exe" -accepteula -i "$SysmonDir\sysmonconfig.xml"

# Limpar arquivos temporários
Remove-Item $SysmonZip 