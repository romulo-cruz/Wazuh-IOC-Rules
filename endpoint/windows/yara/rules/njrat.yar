rule njRAT
{
    meta:
        description = "Detecta variantes do njRAT"
        author = "Wazuh"
        reference = "https://malpedia.caad.fkie.fraunhofer.de/details/win.njrat"
        date = "2024-03-28"
        
    strings:
        $s1 = "netsh firewall add allowedprogram" wide ascii
        $s2 = "\\AppData\\Local\\Temp\\system.exe" wide ascii
        $s3 = "\\Microsoft\\Windows\\CurrentVersion\\Run\\" wide ascii
        $s4 = "Windows\\Start Menu\\Programs\\Startup\\" wide ascii
        
        $net1 = "System.Net" ascii
        $net2 = "System.Windows.Forms" ascii
        $net3 = "Microsoft.VisualBasic" ascii
        
        $pdb = "njRAT" nocase ascii
        
    condition:
        uint16(0) == 0x5A4D and
        (2 of ($s*) or all of ($net*) or $pdb)
} 