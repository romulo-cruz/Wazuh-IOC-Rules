rule LimeRAT
{
    meta:
        description = "Detecta variantes do LimeRAT"
        author = "Wazuh"
        reference = "https://malpedia.caad.fkie.fraunhofer.de/details/win.limerat"
        date = "2024-03-28"
        
    strings:
        $netflix = "checker netflix.exe" wide ascii
        $reg1 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" wide ascii
        $reg2 = "Flood" wide ascii
        $reg3 = "Rans-Status" wide ascii
        $reg4 = "USB" wide ascii
        
        $vb1 = "Microsoft.VisualBasic" ascii
        $vb2 = "System.Windows.Forms" ascii
        $vb3 = ".vbproj" ascii
        
        $pastebin = "pastie" wide ascii
        
    condition:
        uint16(0) == 0x5A4D and
        (2 of ($netflix, $reg*) or all of ($vb*) or $pastebin)
} 