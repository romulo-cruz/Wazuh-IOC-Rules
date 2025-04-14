rule Panchan_Linux {
    meta:
        description = "Detecta variantes do Panchan"
        author = "Wazuh"
        date = "2024-03-21"
        hash1 = "00411a05a7374d64ce8be4ef85999c1434d867cd8db46c38cd03f76072c91460"
        hash2 = "b9e643a8e78d2ce745fbe73eb505c8a0cc49842803077809b2267817979d10b0"
        
    strings:
        $go1 = "Go build ID:" ascii
        $go2 = "golang" ascii nocase
        
        $file1 = "xinetd" ascii
        $file2 = "systemd-worker" ascii
        $file3 = "systemd-worker.service" ascii
        
        $cmd1 = "iptables -D INPUT -p tcp --dport 1919 -j ACCEPT" ascii
        $cmd2 = "iptables -A INPUT -p tcp --dport 1919 -j ACCEPT" ascii
        
        $path1 = "/.ssh/id_rsa" ascii
        $path2 = "/.ssh/known_hosts" ascii
        
        $miner1 = "a819b4a95f386ae3bd8f0edc64e8e10fae0c21c9ae713b73dfc64033e5a845a1"
        $miner2 = "6f445252494a0908ab51d526e09134cebc33a199384771acd58c4a87f1ffc063"
        
    condition:
        uint32(0) == 0x464c457f and 
        filesize < 10MB and
        (
            all of ($go*) and
            (2 of ($file*)) and
            (any of ($cmd*)) and
            (any of ($path*))
        )
} 