# -*- coding: utf-8 -*-
from typing import List


def _weighted(amount: int, start: int, end: int, qs: int, qe: int) -> float:
    if start > qe or end < qs:
        return 0.0
    duration = end - start
    if duration == 0:
        if qs <= start <= qe:
            return float(amount)
        return 0.0
    overlap_start = max(start, qs)
    overlap_end = min(end, qe)
    if overlap_start > overlap_end:
        return 0.0
    overlap_len = overlap_end - overlap_start
    return amount * overlap_len / duration


def _round_to_i32(x: float) -> int:
    if x >= 0:
        val = int(x + 0.5)
    else:
        val = int(x - 0.5)
    if val > 2147483647:
        return 2147483647
    if val < -2147483648:
        return -2147483648
    return val


class Solution:
    def queryNetEnergy(self, commands: List[str]) -> int:
        query = commands[-1]
        qparts = query.split(",")
        version_str = qparts[1].strip()
        qs = int(qparts[2])
        qe = int(qparts[3])
        use_all = version_str == "A"
        max_version = 10**9 if use_all else int(version_str)

        total = 0.0
        version = 0
        for cmd in commands[:-1]:
            version += 1
            if version > max_version:
                break
            parts = cmd.split(",")
            if parts[0] == "AddProductionRecord":
                amount = int(parts[2])
                start = int(parts[3])
                end = int(parts[4])
                total += _weighted(amount, start, end, qs, qe)
            elif parts[0] == "AddConsumptionRecord":
                amount = int(parts[1])
                start = int(parts[2])
                end = int(parts[3])
                total -= _weighted(amount, start, end, qs, qe)
        return _round_to_i32(total)
