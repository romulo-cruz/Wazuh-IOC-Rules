rule Kuiper_Ransomware {
    meta:
        description = "Detecta variantes do ransomware Kuiper"
        author = "Wazuh"
        date = "2024-04-11"
        hash1 = "0162641163a30a2edff787eeecc733ab1de46f03e213743dc768d39eb3075985"
        hash2 = "df430ab9f5084a3e62a6c97c6c6279f2461618f038832305057c51b441c648d9"
        hash3 = "d6c1d2e77ce21d5a026e7abf99c9fffe55d87b282f460dc737da231211a12a0d"

    strings:
        $ransom_note = "README_TO_DECRYPT.txt" ascii wide
        $cmd1 = "vssadmin resize shadowstorage" ascii wide
        $cmd2 = "vssadmin delete shadows" ascii wide
        $cmd3 = "wevtutil cl" ascii wide
        $cmd4 = "Set-MpPreference" ascii wide
        
        $process1 = "CETASvc.exe" ascii wide
        $process2 = "tmwscsvc.exe" ascii wide
        $process3 = "avgsvc.exe" ascii wide
        $process4 = "NortonSecurity.exe" ascii wide
        
        $golang = "Go build ID:" ascii

    condition:
        uint16(0) == 0x5A4D and
        $golang and
        $ransom_note and
        2 of ($cmd*) and
        1 of ($process*)
} 