rule Daolpu_Stealer {
    meta:
        description = "Detecta variantes do Daolpu Infostealer"
        author = "Wazuh"
        date = "2024-08-22"
        threat_level = 10
        
    strings:
        $chrome_kill = "taskkill /F /IM chrome.exe" ascii wide
        $result_file = "\\Temp\\result.txt" ascii wide
        $browser_data1 = "Login Data" ascii wide
        $browser_data2 = "Cookies" ascii wide
        $browser_data3 = "History" ascii wide
        
    condition:
        uint16(0) == 0x5A4D and
        filesize < 2MB and
        ($chrome_kill) and
        ($result_file) and
        (2 of ($browser_data*))
} 