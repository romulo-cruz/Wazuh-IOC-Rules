rule RANSOM_Lockbit_3 {
    meta:
        description = "Detecta variantes do LockBit 3.0"
        author = "Wazuh"
        date = "2024-03-21"
        
    strings:
        $token = "-k LocalServiceNetworkRestricted -pass" ascii wide
        
        $ransom1 = "README.txt" ascii wide
        $ransom2 = ".HLJkNskOq" ascii wide
        $ransom3 = ".19MqZqZ0s" ascii wide
        
        $cmd1 = "vssadmin.exe Delete Shadows /All /Quiet" ascii wide
        $cmd2 = "wmic.exe SHADOWCOPY /nointeractive" ascii wide
        $cmd3 = "wevtutil.exe cl" ascii wide
        
        $reg1 = "System\\CurrentControlSet\\Services\\VSS" ascii wide
        $reg2 = "System\\CurrentControlSet\\Services\\vmicvss" ascii wide
        
        $pdb = "C:\\Users\\Administrator\\Desktop\\locker\\locker\\obj\\Release\\locker.pdb" ascii
        
    condition:
        uint16(0) == 0x5A4D and
        filesize < 2MB and
        (
            $token or
            (2 of ($ransom*)) or
            (2 of ($cmd*)) or
            (any of ($reg*)) or
            $pdb
        )
} 