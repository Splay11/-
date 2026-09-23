# -*- coding: utf-8 -*-
"""P5456 聚餐汇合最短：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_meet_time  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(545620260916)


def write_in(path: Path, p: int, a: int, b: int, edges: list, friends: list[int]) -> None:
    e = len(edges)
    q = len(friends)
    lines = [f"{p} {e} {a} {b}"]
    for x, y, c, z in edges:
        lines.append(f"{x} {y} {c} {z}")
    lines.append(str(q))
    if q:
        lines.append(" ".join(str(x) for x in friends))
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes(f"{ans}\n".encode("utf-8"))


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 3s
memory: 512m
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
    text = """# P5456 测例说明

输入：首行 $p,e,a,b$，随后 $e$ 行 $x\\ y\\ c\\ z$，再一行 $q$，若 $q>0$ 再一行同伴位置。输出一个整数（分钟）。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：二级样例 1。只接一人更优，答案 $20$。
- 2：二级样例 2。必须绕路去接，答案 $40$。
- 3：$q=0$，只有驾车 $a\\to b$。
- 4：同伴已在馆子，步行 $0$。
- 5：全接上车更优（步行太远）。
- 6：单向链。卡把 $z=0$ 当成双向。
- 7：两名同伴在同一路口。
- 8：最近邻贪心接人不是最优。
- 9：上限 $p=10^3,q=15$ 随机链。压测 Dijkstra + $2^{q}$。
- 10：上限链 + 全接/半接权衡。

hack 点：速度乘反、单向当双向、必须全接、最近邻贪心、$q=0$。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def chain(p: int, w: int = 1, bidir: int = 1) -> list:
    return [(i, i + 1, w, bidir) for i in range(1, p)]


def validate(idx: int, p: int, a: int, b: int, edges: list, friends: list[int]) -> None:
    e = len(edges)
    q = len(friends)
    if not (1 <= p <= 1000 and 1 <= e <= 1000 and 1 <= a <= p and 1 <= b <= p):
        raise RuntimeError(f"case {idx}: bad p/e/a/b")
    if not (0 <= q <= 15):
        raise RuntimeError(f"case {idx}: bad q")
    for x, y, c, z in edges:
        if not (1 <= x <= p and 1 <= y <= p and 1 <= c <= 100 and z in (0, 1)):
            raise RuntimeError(f"case {idx}: bad edge {(x, y, c, z)}")
    for f in friends:
        if not (1 <= f <= p):
            raise RuntimeError(f"case {idx}: bad friend {f}")


def make_cases() -> list:
    cases = []
    # 1 样例1
    cases.append((4, 1, 4, [(1, 2, 3, 1), (2, 4, 4, 1), (1, 3, 5, 1), (3, 4, 2, 1)], [2, 3]))
    # 2 样例2
    cases.append((3, 1, 3, [(1, 2, 10, 1), (2, 3, 10, 1), (1, 3, 2, 1)], [2]))
    # 3 q=0
    cases.append((4, 1, 4, [(1, 2, 2, 1), (2, 3, 3, 1), (3, 4, 4, 1)], []))
    # 4 同伴已在馆子
    cases.append((3, 1, 3, [(1, 2, 5, 1), (2, 3, 5, 1)], [3]))
    # 5 全接更优：步行距离很长
    cases.append((4, 1, 4, [(1, 2, 1, 1), (2, 3, 1, 1), (3, 4, 1, 1)], [2, 3]))
    # 6 单向链 1->2->3->4
    cases.append((4, 1, 4, [(1, 2, 2, 0), (2, 3, 2, 0), (3, 4, 2, 0)], [2, 3]))
    # 7 同一路口两名同伴
    cases.append((3, 1, 3, [(1, 2, 4, 1), (2, 3, 3, 1)], [2, 2]))
    # 8 小完全图，顺序敏感
    cases.append(
        (
            5,
            1,
            5,
            [
                (1, 2, 2, 1),
                (1, 3, 9, 1),
                (2, 3, 2, 1),
                (2, 4, 9, 1),
                (3, 4, 2, 1),
                (4, 5, 2, 1),
                (3, 5, 9, 1),
            ],
            [2, 3, 4],
        )
    )
    # 9 上限链
    p9 = 1000
    edges9 = chain(p9, 1, 1)
    friends9 = [30 + 40 * i for i in range(15)]
    cases.append((p9, 1, p9, edges9, friends9))
    # 10 上限链 + 部分人靠近终点
    p10 = 1000
    edges10 = chain(p10, 1, 1) + [(100, 900, 50, 1)]
    friends10 = [50, 80, 120, 200, 300, 400, 500, 600, 700, 800, 850, 900, 920, 950, 980]
    cases.append((p10, 1, p10, edges10, friends10))
    return cases


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    assert len(cases) == 10
    for i, (p, a, b, edges, friends) in enumerate(cases, 1):
        validate(i, p, a, b, edges, friends)
        ans = min_meet_time(p, edges, a, b, friends)
        write_in(DATA / f"{i}.in", p, a, b, edges, friends)
        write_out(DATA / f"{i}.out", ans)
        if min_meet_time(p, edges, a, b, friends) != ans:
            raise SystemExit(f"自校验失败：{i}")
        raw_in = (DATA / f"{i}.in").read_bytes()
        raw_out = (DATA / f"{i}.out").read_bytes()
        if raw_in.endswith(b"\n"):
            raise SystemExit(f"case {i}: .in 末尾有换行")
        if not raw_out.endswith(b"\n") or raw_out.endswith(b"\n\n"):
            raise SystemExit(f"case {i}: .out 换行不符合约定")
    write_config()
    write_readme()
    print("generated 10 cases")
    for i, (p, a, b, edges, friends) in enumerate(cases, 1):
        print(i, "p", p, "q", len(friends), "ans", min_meet_time(p, edges, a, b, friends))


if __name__ == "__main__":
    main()
