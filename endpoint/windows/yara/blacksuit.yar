rule BlackSuit_Ransomware
{
    meta:
        description = "Detecta variantes do ransomware BlackSuit"
        author = "Wazuh"
        date = "2024-11-13"
        hash = "90ae0c693f6ffd6dc5bb2d5a5ef078629c3d77f874b2d2ebd9e109d8ca049f2c"

    strings:
        $arg1 = "-name" ascii wide
        $ext = ".blacksuit" ascii wide
        $note = "README.BlackSuit.txt" ascii wide
        $vss = "vssadmin.exe Delete Shadows /All /Quiet" ascii wide
        $api1 = "RmStartSession" ascii
        $api2 = "RmRegisterResources" ascii
        $api3 = "RmGetList" ascii
        $api4 = "RmShutdown" ascii
        $api5 = "RmEndSession" ascii

    condition:
        uint16(0) == 0x5A4D and
        ($arg1 and $ext) and
        $note and
        $vss and
        3 of ($api*)
} 