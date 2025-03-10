# 定义种子模式/种子正则

seed_patterns = {
    "Add": [
        "\badd\b",
        "\badded\b",
        "\badd\s+in\b",
        "\bintroduce\b"
    ],
    "CollectLayer": [
        "\bcollect\s*(?:aqueous|organic|desired)?\s*layer\b",
        "\bcollect\s*fraction\b"
    ],
    "Concentrate": [
        "\bconcentrate\b",
        "\bevaporat(?:e|ed|ing)\b",
        "\brotavap\b"
    ],
    "Degas": [
        "\bdegas\b",
        "\bpurg(?:e|ed|ing)\b"
    ],
    "DrySolid": [
        "\bdry\s+the\s+solid\b",
        "\bdried\s+solid\b"
    ],
    "DrySolution": [
        "\bdry\s+(?:the\s+)?solution\b",
        "\bdry\s+(?:the\s+)?organic\s+layer\b",
        "\bdried\s+over\b"
    ],
    "Extract": [
        "\bextract\b",
        "\btransfer.*into\s+a\s*different\s*solvent\b"
    ],
    "Filter": [
        "\bfilter\b",
        "\bfiltered\b",
        "\bfiltrate\b"
    ],
    "MakeSolution": [
        "\bmake\s+a?\s*solution\b",
        "\bmix(?:ed|ing)?\b",
        "\bprepare\s+a?\s*solution\b"
    ],
    "Microwave": [
        "\bmicrowave\b"
    ],
    "Partition": [
        "\bpartition\b",
        "\badd\s+two\s+immiscible\s+solvents\b"
    ],
    "PH": [
        "\bph\b",
        "\bneutralize\b",
        "\badjust\s+ph\b"
    ],
    "PhaseSeparation": [
        "\bphase\s+separation\b",
        "\bseparate\s+the\s+(?:aqueous|organic)\s+phase\b"
    ],
    "Purify": [
        "\bpurify\b",
        "\bpurification\b"
    ],
    "Quench": [
        "\bquench\b",
        "\bstop\s+reaction\b"
    ],
    "Recrystallize": [
        "\brecrystalliz(?:e|ed|ation)\b"
    ],
    "Reflux": [
        "\breflux\b"
    ],
    "SetTemperature": [
        "\bset\s+temperature\b",
        "\bheat\s+to\b",
        "\bcool\s+to\b"
    ],
    "Sonicate": [
        "\bsonicat(?:e|ed|ion)\b",
        "\bsonic\s+treatment\b"
    ],
    "Stir": [
        "\bstir\b",
        "\bstirr(?:ed|ing)\b"
    ],
    "Triturate": [
        "\btriturat(?:e|ed|ion)\b"
    ],
    "Wait": [
        "\bstood\s+for\b",
        "\bwait(?:ed|ing)?\b",
        "\bleave\s+(?:the\s+)?reaction\b"
    ],
    "Wash": [
        "\bwash\b",
        "\bwashed\b"
    ],
    "Yield": [
        "\byield\b",
        "\bobtain(?:ed)?\b"
    ],
    "FollowOtherProcedure": [
        "\bfollow\s+(?:the\s+)?procedure\b",
        "\bprocedure\s+described\s+elsewhere\b"
    ],
    "InvalidAction": [
        "\bunknown\s+action\b",
        "\bunsupported\s+operation\b"
    ],
    "NoAction": [
        "\bno\s+action\b",
        "\bno\s+actual\s+step\b"
    ],
    "yield": [
        "\byield\b"
    ],
    "reaction": [
        "\breaction\b"
    ],
    "catalyst": [
        "\bcatalyst\b"
    ],
    "degradation": [
        "\bdegradation\b"
    ],
    "transformation": [
        "\btransformation\b"
    ],
    "Oxygen": [
        "\bOxygen\b"
    ],
    "mitochondrial": [
        "\bmitochondrial\b"
    ],
    "disinfection": [
        "\bdisinfection\b"
    ],
    "detected": [
        "\bdetected\b"
    ],
    "formation": [
        "\bformation\b"
    ],
    "condensation": [
        "\bcondensation\b"
    ],
    "reactions": [
        "\breactions\b"
    ],
    "production": [
        "\bproduction\b"
    ],
    "conversion": [
        "\bconversion\b"
    ],
    "contamination": [
        "\bcontamination\b"
    ],
    "yields": [
        "\byields\b"
    ],
    "maintenance": [
        "\bmaintenance\b"
    ],
    "chemical reactions": [
        "\bchemical\ reactions\b"
    ],
    "transmission": [
        "\btransmission\b"
    ],
    "removal": [
        "\bremoval\b"
    ],
    "secondary alcohol": [
        "\bsecondary\ alcohol\b"
    ],
    "precipitation": [
        "\bprecipitation\b"
    ],
    "transfére": [
        "\btransfére\b"
    ],
    "Krebs cycle": [
        "\bKrebs\ cycle\b"
    ],
    "catalysts": [
        "\bcatalysts\b"
    ],
    "Krebs": [
        "\bKrebs\b"
    ],
    "isolated": [
        "\bisolated\b"
    ],
    "produced": [
        "\bproduced\b"
    ],
    "mitochondrial function": [
        "\bmitochondrial\ function\b"
    ],
    "release": [
        "\brelease\b"
    ],
    "digestion": [
        "\bdigestion\b"
    ],
    "failure": [
        "\bfailure\b"
    ],
    "fabrication": [
        "\bfabrication\b"
    ],
    "obtained": [
        "\bobtained\b"
    ],
    "refluxing": [
        "\brefluxing\b"
    ],
    "exposure": [
        "\bexposure\b"
    ],
    "removed": [
        "\bremoved\b"
    ],
    "interaction": [
        "\binteraction\b"
    ],
    "annulation": [
        "\bannulation\b"
    ],
    "Chemistry": [
        "\bChemistry\b"
    ],
    "mitochondrial membrane": [
        "\bmitochondrial\ membrane\b"
    ],
    "reflux": [
        "\breflux\b"
    ],
    "enzymes": [
        "\benzymes\b"
    ],
    "preparation": [
        "\bpreparation\b"
    ],
    "hydrolysis": [
        "\bhydrolysis\b"
    ],
    "heating": [
        "\bheating\b"
    ],
    "separation": [
        "\bseparation\b"
    ],
    "maintenance of phosphate": [
        "\bmaintenance\ of\ phosphate\b"
    ],
    "production of nickel": [
        "\bproduction\ of\ nickel\b"
    ],
    "activation": [
        "\bactivation\b"
    ],
    "metabolism": [
        "\bmetabolism\b"
    ],
    "injection": [
        "\binjection\b"
    ],
    "freezing": [
        "\bfreezing\b"
    ],
    "Intermediate 6": [
        "\bIntermediate\ 6\b"
    ],
    "bromination": [
        "\bbromination\b"
    ],
    "loading": [
        "\bloading\b"
    ],
    "contaminants": [
        "\bcontaminants\b"
    ],
    "D": [
        "\bD\b"
    ],
    "synthesized": [
        "\bsynthesized\b"
    ],
    "solvent": [
        "\bsolvent\b"
    ],
    "Transmission": [
        "\bTransmission\b"
    ],
    "Intermediates": [
        "\bIntermediates\b"
    ],
    "selectively": [
        "\bselectively\b"
    ],
    "converted to desired products": [
        "\bconverted\ to\ desired\ products\b"
    ],
    "extracted": [
        "\bextracted\b"
    ],
    "corrosion": [
        "\bcorrosion\b"
    ],
    "recovered": [
        "\brecovered\b"
    ],
    "exchange": [
        "\bexchange\b"
    ],
    "reproduction": [
        "\breproduction\b"
    ],
    "transférer": [
        "\btransférer\b"
    ],
    "bromine": [
        "\bbromine\b"
    ],
    "sterilization": [
        "\bsterilization\b"
    ],
    "Hydrolysis": [
        "\bHydrolysis\b"
    ],
    "intramolecular": [
        "\bintramolecular\b"
    ],
    "binding": [
        "\bbinding\b"
    ],
    "migration": [
        "\bmigration\b"
    ],
    "Oxygenation": [
        "\bOxygenation\b"
    ],
    "Oxidation": [
        "\bOxidation\b"
    ],
    "mitochondrial DNA": [
        "\bmitochondrial\ DNA\b"
    ],
    "maintenance of the environment": [
        "\bmaintenance\ of\ the\ environment\b"
    ],
    "isolation": [
        "\bisolation\b"
    ],
    "substitution": [
        "\bsubstitution\b"
    ],
    "purification": [
        "\bpurification\b"
    ],
    "trapping": [
        "\btrapping\b"
    ],
    "melting": [
        "\bmelting\b"
    ],
    "treated": [
        "\btreated\b"
    ],
    "conducting": [
        "\bconducting\b"
    ],
    "deprotection": [
        "\bdeprotection\b"
    ],
    "observed": [
        "\bobserved\b"
    ],
    "generated": [
        "\bgenerated\b"
    ],
    "inhibited": [
        "\binhibited\b"
    ],
    "Nebenwirkungsverhalten": [
        "\bNebenwirkungsverhalten\b"
    ],
    "Removal": [
        "\bRemoval\b"
    ],
    "interaction with oxygen": [
        "\binteraction\ with\ oxygen\b"
    ],
    "converted": [
        "\bconverted\b"
    ],
    "hydrosilylation": [
        "\bhydrosilylation\b"
    ],
    "transféring": [
        "\btransféring\b"
    ],
    "solvents": [
        "\bsolvents\b"
    ]
}