rule Remcos_RAT {
    meta:
        description = "Detecta variantes do Remcos RAT"
        author = "Wazuh"
        date = "2024-03-21"
        
    strings:
        $str1 = "Remcos" ascii wide
        $str2 = "Breaking-Security" ascii wide
        $str3 = "logs.dat" ascii wide
        $str4 = "hpsupport" ascii wide
        
        $func1 = "CreateRemoteThread" ascii
        $func2 = "VirtualAllocEx" ascii
        $func3 = "WriteProcessMemory" ascii
        $func4 = "GetAsyncKeyState" ascii
        
        $path1 = "\\AppData\\Roaming\\remcos" ascii wide
        $path2 = "\\AppData\\Roaming\\hpsupport" ascii wide
        $path3 = "\\AppData\\Local\\Temp" ascii wide
        
    condition:
        uint16(0) == 0x5A4D and
        filesize < 2MB and
        (
            (2 of ($str*)) or
            (2 of ($func*)) or
            (2 of ($path*))
        )
} 