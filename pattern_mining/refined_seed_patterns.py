# 定义种子模式/种子正则

seed_patterns = {
    r"Addr": [
        r"\badd\br",
        r"\badded\br",
        r"\badd\s+in\br",
        r"\bintroduce\br"
    ],
    r"CollectLayerr": [
        r"\bcollect\s*(?:aqueous|organic|desired)?\s*layer\br",
        r"\bcollect\s*fraction\br"
    ],
    r"Concentrater": [
        r"\bconcentrate\br",
        r"\bevaporat(?:e|ed|ing)\br",
        r"\brotavap\br"
    ],
    r"Degasr": [
        r"\bdegas\br",
        r"\bpurg(?:e|ed|ing)\br"
    ],
    r"DrySolidr": [
        r"\bdry\s+the\s+solid\br",
        r"\bdried\s+solid\br"
    ],
    r"DrySolutionr": [
        r"\bdry\s+(?:the\s+)?solution\br",
        r"\bdry\s+(?:the\s+)?organic\s+layer\br",
        r"\bdried\s+over\br"
    ],
    r"Extractr": [
        r"\bextract\br",
        r"\btransfer.*into\s+a\s*different\s*solvent\br"
    ],
    r"Filterr": [
        r"\bfilter\br",
        r"\bfiltered\br",
        r"\bfiltrate\br"
    ],
    r"MakeSolutionr": [
        r"\bmake\s+a?\s*solution\br",
        r"\bmix(?:ed|ing)?\br",
        r"\bprepare\s+a?\s*solution\br"
    ],
    r"Microwaver": [
        r"\bmicrowave\br"
    ],
    r"Partitionr": [
        r"\bpartition\br",
        r"\badd\s+two\s+immiscible\s+solvents\br"
    ],
    r"PHr": [
        r"\bph\br",
        r"\bneutralize\br",
        r"\badjust\s+ph\br"
    ],
    r"PhaseSeparationr": [
        r"\bphase\s+separation\br",
        r"\bseparate\s+the\s+(?:aqueous|organic)\s+phase\br"
    ],
    r"Purifyr": [
        r"\bpurify\br",
        r"\bpurification\br"
    ],
    r"Quenchr": [
        r"\bquench\br",
        r"\bstop\s+reaction\br"
    ],
    r"Recrystallizer": [
        r"\brecrystalliz(?:e|ed|ation)\br"
    ],
    r"Refluxr": [
        r"\breflux\br"
    ],
    r"SetTemperaturer": [
        r"\bset\s+temperature\br",
        r"\bheat\s+to\br",
        r"\bcool\s+to\br"
    ],
    r"Sonicater": [
        r"\bsonicat(?:e|ed|ion)\br",
        r"\bsonic\s+treatment\br"
    ],
    r"Stirr": [
        r"\bstir\br",
        r"\bstirr(?:ed|ing)\br"
    ],
    r"Triturater": [
        r"\btriturat(?:e|ed|ion)\br"
    ],
    r"Waitr": [
        r"\bstood\s+for\br",
        r"\bwait(?:ed|ing)?\br",
        r"\bleave\s+(?:the\s+)?reaction\br"
    ],
    r"Washr": [
        r"\bwash\br",
        r"\bwashed\br"
    ],
    r"Yieldr": [
        r"\byield\br",
        r"\bobtain(?:ed)?\br"
    ],
    r"FollowOtherProcedurer": [
        r"\bfollow\s+(?:the\s+)?procedure\br",
        r"\bprocedure\s+described\s+elsewhere\br"
    ],
    r"InvalidActionr": [
        r"\bunknown\s+action\br",
        r"\bunsupported\s+operation\br"
    ],
    r"NoActionr": [
        r"\bno\s+action\br",
        r"\bno\s+actual\s+step\br"
    ]
}