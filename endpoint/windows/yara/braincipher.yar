rule BrainCipher_Ransomware {
    meta:
        description = "Detecta variantes do ransomware Brain Cipher"
        author = "Wazuh"
        reference = "https://wazuh.com/blog/detecting-brain-cipher-ransomware-with-wazuh/"
        date = "2025-02-04"
        hash = "eb82946fa0de261e92f8f60aa878c9fef9ebb34fdababa66995403b110118b12"

    strings:
        $clsid = "3E5FC7F9-9A51-4367-9063-A120244FBEC7" ascii wide
        $ransom_ext = ".sYMY1N6ah" ascii wide
        $ransom_note = "README.txt" ascii wide
        $reg_key = "System\\CurrentControlSet\\Services\\VSS" ascii wide
        
    condition:
        uint16(0) == 0x5A4D and
        2 of them
} 