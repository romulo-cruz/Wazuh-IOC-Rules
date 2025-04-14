rule Peaklight_Malware {
    meta:
        description = "Detecta variantes do malware Peaklight"
        author = "Wazuh"
        reference = "https://wazuh.com/blog/detecting-peaklight-malware-with-wazuh/"
        date = "2025-03-06"
        hash1 = "95361f5f264e58d6ca4538e7b436ab67"
        hash2 = "07061f3fd8c15bdd484b55baa44191aa9d045c9889234550939f46c063e6211c"

    strings:
        $ps_exec = "-NoProfile -ExecutionPolicy unrestricted"
        $temp_path = "\\AppData\\Local\\Temp\\"
        $api_call1 = "GlobalMemoryStatusEx"
        $api_call2 = "GetAdaptersAddresses"
        
    condition:
        uint16(0) == 0x5A4D and
        2 of them
} 