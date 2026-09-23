# -*- coding: utf-8 -*-
"""P5243 造数：模块并行重建最短时间。"""
from __future__ import annotations

import random
from collections import defaultdict, deque
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(524320260815)
N_MAX = 10_000
E_MAX = 20_000
BT_MAX = 10_000


def solve(n: int, deps: List[List[int]], buildTime: List[int], changed: List[int]) -> int:
    dependents = defaultdict(list)
    depends_on = defaultdict(list)
    for a, b in deps:
        dependents[b].append(a)
        depends_on[a].append(b)
    need = set()
    q = deque()
    for x in changed:
        if x not in need:
            need.add(x)
            q.append(x)
    while q:
        u = q.popleft()
        for v in dependents[u]:
            if v not in need:
                need.add(v)
                q.append(v)
    if not need:
        return 0
    indeg = {u: 0 for u in need}
    for u in need:
        for b in depends_on[u]:
            if b in need:
                indeg[u] += 1
    qq = deque([u for u in need if indeg[u] == 0])
    finish = {}
    while qq:
        u = qq.popleft()
        mx = 0
        for b in depends_on[u]:
            if b in need:
                mx = max(mx, finish[b])
        finish[u] = mx + buildTime[u]
        for v in dependents[u]:
            if v in need:
                indeg[v] -= 1
                if indeg[v] == 0:
                    qq.append(v)
    return max(finish.values())


def fmt_arr1d(a: List[int]) -> str:
    return "[" + ", ".join(str(x) for x in a) + "]"


def fmt_arr2d(a: List[List[int]]) -> str:
    if not a:
        return "[]"
    return "[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in a) + "]"


def fmt_in(n: int, deps: List[List[int]], buildTime: List[int], changed: List[int]) -> str:
    return f"{n}\n{fmt_arr2d(deps)}\n{fmt_arr1d(buildTime)}\n{fmt_arr1d(changed)}"


def validate(n: int, deps: List[List[int]], buildTime: List[int], changed: List[int]) -> None:
    assert 1 <= n <= N_MAX
    assert 0 <= len(deps) <= min(n * (n - 1) // 2, E_MAX)
    assert len(buildTime) == n
    assert all(1 <= t <= BT_MAX for t in buildTime)
    seen = set()
    g = defaultdict(list)
    indeg = [0] * n
    for e in deps:
        assert len(e) == 2
        a, b = e
        assert 0 <= a < n and 0 <= b < n and a != b
        assert (a, b) not in seen
        seen.add((a, b))
        g[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    cnt = 0
    while q:
        u = q.popleft()
        cnt += 1
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    assert cnt == n
    assert 1 <= len(changed) <= n
    assert len(changed) == len(set(changed))
    assert all(0 <= x < n for x in changed)


def random_dag(n: int, m: int) -> List[List[int]]:
    edges = set()
    attempts = 0
    while len(edges) < m and attempts < m * 40 + 100:
        attempts += 1
        if n < 2:
            break
        a = RNG.randint(1, n - 1)
        b = RNG.randint(0, a - 1)
        edges.add((a, b))
    return [[a, b] for a, b in sorted(edges)]


def rand_bt(n: int, lo: int = 1, hi: int = 20) -> List[int]:
    return [RNG.randint(lo, hi) for _ in range(n)]


def write_cases(
    cases: List[Tuple[str, int, List[List[int]], List[int], List[int]]]
) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    readme = [
        "# P5243 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin 四行：`n` / `deps` / `buildTime` / `changed`，与题面样例同形。",
        "",
        "| 组 | 说明 |",
        "|---:|---|",
    ]
    for i, (desc, n, deps, buildTime, changed) in enumerate(cases, 1):
        validate(n, deps, buildTime, changed)
        ans = solve(n, deps, buildTime, changed)
        text_in = fmt_in(n, deps, buildTime, changed)
        (DATA / f"{i}.in").write_bytes(text_in.encode("utf-8"))
        with open(DATA / f"{i}.out", "w", encoding="utf-8", newline="\n") as f:
            f.write(f"{ans}\n")
        readme.append(f"| {i} | {desc} |")

    from std import Solution  # type: ignore

    sol = Solution()
    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        assert not raw.endswith(b"\n"), i
        lines = raw.decode("utf-8").split("\n")
        assert len(lines) == 4, i
        n = int(lines[0])
        deps = eval(lines[1])
        buildTime = eval(lines[2])
        changed = eval(lines[3])
        got = sol.minRebuildTime(n, deps, buildTime, changed)
        exp = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        assert got == exp, (i, got, exp)
        outb = (DATA / f"{i}.out").read_bytes()
        assert outb.endswith(b"\n") and outb.count(b"\n") == 1

    cases_yaml = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - compile.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases_yaml}
langs:
  - py.py3
  - java
  - cc.cc14o2
  - py
  - cc
"""
    with open(DATA / "config.yaml", "w", encoding="utf-8", newline="\n") as f:
        f.write(config)
    with open(DATA / "README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(readme) + "\n")
    print("P5243 generated 10 cases OK")


def main() -> None:
    cases: List[Tuple[str, int, List[List[int]], List[int], List[int]]] = []

    cases.append(("样例1：全图重建并行最长路=10", 3, [[0, 1], [0, 2], [1, 2]], [5, 3, 2], [2]))
    cases.append(("样例2：仅叶子", 4, [[1, 0], [2, 0], [3, 1]], [1, 1, 1, 1], [3]))
    cases.append(("样例3：无依赖并行取 max", 2, [], [4, 7], [0, 1]))

    cases.append(("边界：n=1", 1, [], [9], [0]))

    # 链：i 依赖 i-1，变更 0 → 串行累加
    n5 = 10
    deps5 = [[i, i - 1] for i in range(1, n5)]
    bt5 = [2] * n5
    cases.append(("构造：链串行求和", n5, deps5, bt5, [0]))

    # hack：边方向反了 → 影响面错误；串行求和也会错（星形应并行）
    n6 = 8
    deps6 = [[i, 0] for i in range(1, n6)]
    bt6 = [3] + [5] * (n6 - 1)
    cases.append(("hack：星形依赖中心，并行非串行", n6, deps6, bt6, [0]))

    # hack：漏掉不在集合内的依赖不应等待；只变叶子
    cases.append(("hack：叶子变更不受上游影响", 5, [[1, 0], [2, 0], [3, 1], [4, 1]], [10, 10, 10, 10, 4], [4]))

    n8 = 40
    deps8 = random_dag(n8, 80)
    bt8 = rand_bt(n8, 1, 50)
    ch8 = sorted(RNG.sample(range(n8), k=RNG.randint(1, 6)))
    cases.append(("随机中：n=40", n8, deps8, bt8, ch8))

    n9 = N_MAX
    deps9 = [[i, i - 1] for i in range(1, n9)]
    extra9 = random_dag(n9, 1500)
    seen9 = {(a, b) for a, b in deps9}
    for a, b in extra9:
        if (a, b) not in seen9 and len(deps9) < E_MAX:
            deps9.append([a, b])
            seen9.add((a, b))
    bt9 = rand_bt(n9, 1, 100)
    cases.append(("大数据：n=1e4 链+随机边", n9, deps9, bt9, [0, 100, 5000]))

    n10 = N_MAX
    deps10 = random_dag(n10, min(E_MAX, n10 * (n10 - 1) // 2))
    bt10 = rand_bt(n10, 1, BT_MAX)
    ch10 = sorted(RNG.sample(range(n10), k=50))
    cases.append(("大数据：n=1e4 边近 2e4", n10, deps10, bt10, ch10))

    assert len(cases) == 10
    write_cases(cases)


if __name__ == "__main__":
    main()
