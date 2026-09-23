# -*- coding: utf-8 -*-
"""P5427 质因数跳跃：10 组测例（二级 I/O：一行序列，输出 true/false）。"""
from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(542720260911)


def prime_factors(x: int) -> list[int]:
    if x <= 1:
        return []
    factors: list[int] = []
    if x % 2 == 0:
        factors.append(2)
        while x % 2 == 0:
            x //= 2
    d = 3
    while d * d <= x:
        if x % d == 0:
            factors.append(d)
            while x % d == 0:
                x //= d
        d += 2
    if x > 1:
        factors.append(x)
    return factors


def can_reach(seq: list[int]) -> bool:
    m = len(seq)
    if m == 1:
        return True
    vis = [False] * m
    q = [0]
    vis[0] = True
    head = 0
    while head < len(q):
        p = q[head]
        head += 1
        for d in prime_factors(seq[p]):
            for nxt in (p + d, p - d):
                if 0 <= nxt < m and not vis[nxt]:
                    if nxt == m - 1:
                        return True
                    vis[nxt] = True
                    q.append(nxt)
    return False


def write_in(path: Path, seq: list[int]) -> None:
    path.write_bytes(" ".join(str(x) for x in seq).encode("utf-8"))


def write_out(path: Path, ok: bool) -> None:
    path.write_bytes((("true" if ok else "false") + "\n").encode("utf-8"))


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 1s
memory: 256m
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases}
langs:
  - c
  - cc.cc14o2
  - cc
  - java
  - py.py3
  - py
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (ROOT / "config.yaml").write_text(config, encoding="utf-8")


def write_readme() -> None:
    text = """# P5427 测例说明

输入：一行空格分隔的正整数序列。输出：`true` / `false` 及一个换行。

分层（每组 10 分）：

- 1：二级样例 1。`4 1 1 9` → false。卡只看第一个质因数、忽略卡住的 `1`。
- 2：二级样例 2。`10 1 4 9 1` → true。必须用较小质因数 `2` 而不是越界的 `5`。
- 3：二级样例 3。`1 6 8` → false。起点为 `1` 无法起步。
- 4：最小规模 `m=1`，值为 `1`。起点即终点，答案 true。卡「值为 1 就不能到达」。
- 5：必须先向左再向右。`6 7 1 2 1 1 1 1 1` → true。卡只向右跳。
- 6：合数步长假解。`16 1 1 1 1 1 1 1 1` → false。若把 `8` 当步长会误判 true。
- 7：贪心最大质因数失败。`30 1 1 7 1 1 1 1 1 1 1` → true。贪心走 `5` 走进死胡同，BFS 走 `3` 能到。
- 8：小随机 + 全偶数下标跳 `2` 却要到奇数末位，答案 false。
- 9：$m=10^4$ 随机。压测分解与 BFS。
- 10：$m=10^4$ 构造可达长链（先 `2` 再转奇数下标），压测上限。

hack 点：只向右、合数因子、`m=1`、贪心最大质因数、`1` 无出边。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def make_cases() -> list[list[int]]:
    cases: list[list[int]] = []
    # 1-3 样例
    cases.append([4, 1, 1, 9])
    cases.append([10, 1, 4, 9, 1])
    cases.append([1, 6, 8])
    # 4 m=1
    cases.append([1])
    # 5 必须向左：0-6->3, 3-2->1, 1-7->8
    cases.append([6, 7, 1, 2, 1, 1, 1, 1, 1])
    # 6 合数 8 会误达终点，质因数只有 2
    cases.append([16, 1, 1, 1, 1, 1, 1, 1, 1])
    # 7 贪心 5 失败，3 成功
    cases.append([30, 1, 1, 7, 1, 1, 1, 1, 1, 1, 1])
    # 8 全 4，只能走偶数下标，末位为奇数
    cases.append([4] * 16)
    # 9 满随机
    cases.append([RNG.randint(1, 1000) for _ in range(10000)])
    # 10 长链可达：0 用 2 走到 2，再用 3 转到奇数，随后用 2 走到 9999
    n = 10000
    seq = [1] * n
    seq[0] = 2
    seq[2] = 3
    for i in range(5, n, 2):
        seq[i] = 2
    cases.append(seq)
    return cases


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    assert len(cases) == 10
    for i, seq in enumerate(cases, 1):
        assert 1 <= len(seq) <= 10**4
        assert all(1 <= x <= 10**3 for x in seq)
        ans = can_reach(seq)
        write_in(DATA / f"{i}.in", seq)
        write_out(DATA / f"{i}.out", ans)
        # 自校验：再算一遍
        got = can_reach(seq)
        if got != ans:
            raise SystemExit(f"自校验失败：{i}")
    write_config()
    write_readme()
    print("generated 10 cases")
    for i, seq in enumerate(cases, 1):
        print(i, len(seq), "true" if can_reach(seq) else "false")


if __name__ == "__main__":
    main()
