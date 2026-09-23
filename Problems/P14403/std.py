# -*- coding: utf-8 -*-
import re
from typing import List

WORD_SPLIT = re.compile(r"[\s,.!?;:]+")

class Solution:
    def analyzeLogKeywords(self, logs: List[str], keywords: List[str]) -> List[int]:
        kws = [k.lower() for k in keywords]
        tokenized: List[List[str]] = []
        for log in logs:
            tokenized.append([w.lower() for w in WORD_SPLIT.split(log) if w])
        counts = [0] * len(keywords)
        for words in tokenized:
            for ki, kw in enumerate(kws):
                counts[ki] += sum(1 for w in words if w == kw)
        present: List[List[bool]] = []
        for words in tokenized:
            word_set = set(words)
            present.append([kw in word_set for kw in kws])
        pairs: List[int] = []
        m = len(keywords)
        for i in range(m):
            for j in range(i + 1, m):
                co = sum(1 for row in present if row[i] and row[j])
                if co >= 2:
                    pairs.extend([i, j])
        return counts + pairs
