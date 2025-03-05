# 定义种子模式/种子正则

"""
存放针对每种化学操作类型的初始种子匹配规则（seed patterns）。

每个操作类型对应一个字符串列表，其中每个字符串是一个正则表达式。
使用方式通常是在外部脚本中配合 re.IGNORECASE 做搜索，比如：
    re.search(pattern, text, flags=re.IGNORECASE)
若匹配成功，就可视为检出了该类型操作。

注意：
- 有些操作可能还有大量同义或变体表述，可继续添加。
- “InvalidAction”、“OtherLanguage”、“NoAction” 等类别通常需结合上下文或额外逻辑来判断，
  这里仅给出一个占位式的简单写法作参考。
"""

seed_patterns = {
    "Add": [
        r"\badd\b",
        r"\badded\b",
        r"\badd\s+in\b",
        r"\bintroduce\b"  # "introduce reagent"等
    ],
    "CollectLayer": [
        r"\bcollect\s*(?:aqueous|organic|desired)?\s*layer\b",
        r"\bcollect\s*fraction\b"
    ],
    "Concentrate": [
        r"\bconcentrate\b",
        r"\bevaporat(?:e|ed|ing)\b",
        r"\brotavap\b"
    ],
    "Degas": [
        r"\bdegas\b",
        r"\bpurg(?:e|ed|ing)\b"
    ],
    "DrySolid": [
        r"\bdry\s+the\s+solid\b",
        r"\bdried\s+solid\b"
    ],
    "DrySolution": [
        r"\bdry\s+(?:the\s+)?solution\b",
        r"\bdry\s+(?:the\s+)?organic\s+layer\b",
        r"\bdried\s+over\b"  # "dried over MgSO4"
    ],
    "Extract": [
        r"\bextract\b",
        r"\btransfer.*into\s+a\s*different\s*solvent\b"
    ],
    "Filter": [
        r"\bfilter\b",
        r"\bfiltered\b",
        r"\bfiltrate\b"
    ],
    "MakeSolution": [
        r"\bmake\s+a?\s*solution\b",
        r"\bmix(?:ed|ing)?\b",
        r"\bprepare\s+a?\s*solution\b"
    ],
    "Microwave": [
        r"\bmicrowave\b"
    ],
    "Partition": [
        r"\bpartition\b",
        r"\badd\s+two\s+immiscible\s+solvents\b"
    ],
    "PH": [
        r"\bph\b",
        r"\bneutralize\b",
        r"\badjust\s+ph\b"
    ],
    "PhaseSeparation": [
        r"\bphase\s+separation\b",
        r"\bseparate\s+the\s+(?:aqueous|organic)\s+phase\b"
    ],
    "Purify": [
        r"\bpurify\b",
        r"\bpurification\b"
    ],
    "Quench": [
        r"\bquench\b",
        r"\bstop\s+reaction\b"
    ],
    "Recrystallize": [
        r"\brecrystalliz(?:e|ed|ation)\b"
    ],
    "Reflux": [
        r"\breflux\b"
    ],
    "SetTemperature": [
        r"\bset\s+temperature\b",
        r"\bheat\s+to\b",
        r"\bcool\s+to\b"
    ],
    "Sonicate": [
        r"\bsonicat(?:e|ed|ion)\b",
        r"\bsonic\s+treatment\b"
    ],
    "Stir": [
        r"\bstir\b",
        r"\bstirr(?:ed|ing)\b"
    ],
    "Triturate": [
        r"\btriturat(?:e|ed|ion)\b"
    ],
    "Wait": [
        r"\bstood\s+for\b",
        r"\bwait(?:ed|ing)?\b",
        r"\bleave\s+(?:the\s+)?reaction\b"
    ],
    "Wash": [
        r"\bwash\b",
        r"\bwashed\b"
    ],
    "Yield": [
        r"\byield\b",
        r"\bobtain(?:ed)?\b"
    ],
    "FollowOtherProcedure": [
        r"\bfollow\s+(?:the\s+)?procedure\b",
        r"\bprocedure\s+described\s+elsewhere\b"
    ],
    "InvalidAction": [
        r"\bunknown\s+action\b",
        r"\bunsupported\s+operation\b"
    ],
    "NoAction": [
        r"\bno\s+action\b",
        r"\bno\s+actual\s+step\b"
    ]
}
