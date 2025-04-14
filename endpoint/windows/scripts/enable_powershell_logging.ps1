function Enable-PSLogging {
    # Caminhos do registro para ScriptBlockLogging e ModuleLogging
    $scriptBlockPath = 'HKLM:\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging'
    $moduleLoggingPath = 'HKLM:\Software\Policies\Microsoft\Windows\PowerShell\ModuleLogging'
    
    # Habilitar Script Block Logging
    if (-not (Test-Path $scriptBlockPath)) {
        $null = New-Item $scriptBlockPath -Force
    }
    Set-ItemProperty -Path $scriptBlockPath -Name EnableScriptBlockLogging -Value 1

    # Habilitar Module Logging
    if (-not (Test-Path $moduleLoggingPath)) {
        $null = New-Item $moduleLoggingPath -Force
    }
    Set-ItemProperty -Path $moduleLoggingPath -Name EnableModuleLogging -Value 1
    
    # Especificar módulos para log
    $moduleNames = @('*')
    New-ItemProperty -Path $moduleLoggingPath -Name ModuleNames -PropertyType MultiString -Value $moduleNames -Force

    Write-Output "Script Block Logging e Module Logging foram habilitados."
}

Enable-PSLogging 