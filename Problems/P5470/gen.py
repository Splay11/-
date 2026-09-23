# -*- coding: utf-8 -*-
"""P5470 推理模型分批：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_waves  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(547020260918)


def write_in(path: Path, p: int, rel: list[tuple[int, int]]) -> None:
    lines = [f"{p} {len(rel)}"]
    for u, v in rel:
        lines.append(f"{u} {v}")
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes(f"{ans}\n".encode("utf-8"))


def dump_case(idx: int, p: int, rel: list[tuple[int, int]]) -> int:
    ans = min_waves(p, rel)
    write_in(DATA / f"{idx}.in", p, rel)
    write_out(DATA / f"{idx}.out", ans)
    return ans


def chain(n: int, start: int = 1) -> list[tuple[int, int]]:
    return [(start + i, start + i + 1) for i in range(n - 1)]


def random_forward(p: int, extra: int, rng: random.Random, banned: set[tuple[int, int]] | None = None) -> list[tuple[int, int]]:
    """只连编号小的指向编号大的，保证无环。允许与已有边重复。"""
    banned = banned or set()
    out: list[tuple[int, int]] = []
    guard = 0
    while len(out) < extra and guard < extra * 20:
        guard += 1
        if p < 2:
            break
        u = rng.randint(1, p - 1)
        v = rng.randint(u + 1, p)
        if (u, v) in banned:
            continue
        out.append((u, v))
    return out


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 8s
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
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (ROOT / "config.yaml").write_text(config, encoding="utf-8")


def write_readme(answers: dict[int, int]) -> None:
    text = """# P5470 测例说明

输入：第一行 $p,e$，随后 $e$ 行 $u\\ v$（$v$ 等 $u$）。输出一个整数：最少波次。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：二级样例 1。分支加一条独立边，答案 $3$。
- 2：二级样例 2。长度为 $5$ 的链。
- 3：$p=1,e=0$。最小规模，答案 $1$。
- 4：八个孤立点。卡「没有边就输出 $0$」或输出 $p$。
- 5：出星。卡「答案当成 $p$」或「最大出度加一却把方向搞反」。
- 6：入星。最大入度很大但最长链只有 $2$。卡「最大入度加一」。
- 7：两个连通块，最长链在较大那块。卡「输出连通块个数」或把两块长度相加。
- 8：菱形捷径 + 孤立点 + 重边。卡无向 BFS、漏孤立点、建反边。
- 9：上限附近随机 DAG，$p=10^5,e=1.5\\times 10^6$。压测 I/O 与线性做法。
- 10：贯穿链 $1\\to\\cdots\\to p$ 再灌满前向边。答案为 $p$，卡最大入度、无记忆 DFS、建反边。
"""
    extra = "\n生成答案：\n" + "\n".join(f"- {i}：{answers[i]}" for i in range(1, 11)) + "\n"
    (DATA / "README.md").write_text(text + extra, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    answers: dict[int, int] = {}

    # 1 二级样例 1
    answers[1] = dump_case(1, 6, [(2, 1), (2, 5), (1, 4), (5, 4), (3, 6)])

    # 2 二级样例 2
    answers[2] = dump_case(2, 5, [(5, 3), (3, 2), (2, 1), (1, 4)])

    # 3 最小
    answers[3] = dump_case(3, 1, [])

    # 4 全孤立
    answers[4] = dump_case(4, 8, [])

    # 5 出星：1 -> 2..7
    answers[5] = dump_case(5, 7, [(1, i) for i in range(2, 8)])

    # 6 入星：1..8 -> 9
    answers[6] = dump_case(6, 9, [(i, 9) for i in range(1, 9)])

    # 7 两块：链 1-2-3-4 与链 5-6，再加一个孤立 7
    answers[7] = dump_case(7, 7, chain(4, 1) + chain(2, 5))

    # 8 菱形 + 捷径 + 重边 + 孤立
    answers[8] = dump_case(
        8,
        6,
        [(1, 2), (1, 2), (1, 3), (2, 4), (3, 4), (1, 4)],
    )

    # 9 大随机 DAG
    p9, e9 = 100000, 1500000
    rel9 = random_forward(p9, e9, RNG)
    answers[9] = dump_case(9, p9, rel9)

    # 10 长链 + 前向边灌满
    p10, e10 = 100000, 1500000
    rel10 = chain(p10)
    need = e10 - len(rel10)
    rel10.extend(random_forward(p10, need, RNG, banned=set(rel10)))
    answers[10] = dump_case(10, p10, rel10)

    write_config()
    write_readme(answers)
    print("answers", answers)


if __name__ == "__main__":
    main()
