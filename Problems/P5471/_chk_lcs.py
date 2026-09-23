# -*- coding: utf-8 -*-
import itertools
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def hanzi(s: str) -> str:
    s = re.sub(r"\$.*?\$", "", s)
    s = re.sub(r"```[\s\S]*?```", "", s)
    s = re.sub(r"`[^`]*`", "", s)
    skip = [
        "题目内容",
        "输入描述",
        "输出描述",
        "样例",
        "输入",
        "输出",
        "说明",
        "提示",
        "题目背景",
        "任务描述",
        "核心规则",
    ]
    for t in skip:
        s = s.replace(t, "")
    return "".join(re.findall(r"[\u4e00-\u9fff]", s))


root = Path(r"d:\机考出题\problem-maker\Problems\P5471")
a = hanzi((root / "题面.md").read_text(encoding="utf-8"))
b = hanzi((root / "编程题面_二级.md").read_text(encoding="utf-8"))
print("orig", len(a))
print("new", len(b))
best = 0
bests = ""
n, m = len(a), len(b)
for i in range(n):
    for j in range(m):
        k = 0
        while i + k < n and j + k < m and a[i + k] == b[j + k]:
            k += 1
        if k > best:
            best = k
            bests = a[i : i + k]
print("LCS", best, bests)


def solve(lo, hi, dur):
    customers = list(range(1, len(lo)))
    best = None
    paths = []
    for perm in itertools.permutations(customers):
        t = 0
        cur = 0
        ok = True
        for v in perm:
            t += dur[cur][v]
            if t > hi[v]:
                ok = False
                break
            if t < lo[v]:
                t = lo[v]
            cur = v
        if not ok:
            continue
        t += dur[cur][0]
        if t > hi[0]:
            continue
        paths.append((t, perm))
        if best is None or t < best:
            best = t
    return -1 if best is None else best, paths


print(
    "s1",
    solve(
        [0, 6, 20, 14],
        [1440, 18, 45, 28],
        [[0, 4, 18, 8], [6, 0, 9, 20], [10, 12, 0, 7], [9, 16, 11, 0]],
    ),
)
print(
    "s2",
    solve(
        [0, 5, 5, 5],
        [1440, 12, 12, 12],
        [[0, 4, 4, 4], [4, 0, 10, 10], [4, 10, 0, 10], [4, 10, 10, 0]],
    ),
)
