rule MintStealer
{
    meta:
        description = "Detecta variantes do Mint Stealer"
        author = "Wazuh"
        date = "2024-09-26"

    strings:
        $a1 = "onefile_" ascii wide
        $a2 = "vadimloader.exe" ascii wide
        $a3 = "Save-" ascii wide
        $a4 = "wmic os get" ascii wide
        $a5 = "Get-Clipboard" ascii wide
        $a6 = ".pyd" ascii wide
        
        $path1 = "\\AppData\\Local\\Temp\\" ascii wide
        $path2 = "\\AppData\\Roaming\\" ascii wide
        
        $browser1 = "\\Google\\Chrome\\" ascii wide
        $browser2 = "\\Mozilla\\Firefox\\" ascii wide
        $browser3 = "\\Opera Software\\" ascii wide

    condition:
        uint16(0) == 0x5A4D and
        4 of ($a*) and
        1 of ($path*) and
        1 of ($browser*)
} 