# -*- coding: utf-8 -*-
"""P5469 主机灰度分批：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import assign_batches  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(546920260918)


def write_in(path: Path, hosts: list[tuple[int, list[str]]], dim_cnt: int, batch_cnt: int) -> None:
    lines = [f"{len(hosts)} {dim_cnt}"]
    for nid, tags in hosts:
        lines.append(" ".join([str(nid)] + list(tags)))
    lines.append(str(batch_cnt))
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, waves: list[list[int]]) -> None:
    text = "\n".join(" ".join(str(x) for x in wave) for wave in waves) + "\n"
    path.write_bytes(text.encode("utf-8"))


def dump_case(idx: int, hosts: list[tuple[int, list[str]]], dim_cnt: int, batch_cnt: int) -> None:
    waves = assign_batches(hosts, dim_cnt, batch_cnt)
    write_in(DATA / f"{idx}.in", hosts, dim_cnt, batch_cnt)
    write_out(DATA / f"{idx}.out", waves)


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
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (ROOT / "config.yaml").write_text(config, encoding="utf-8")


def write_readme() -> None:
    text = """# P5469 测例说明

输入：第一行 $p,d$，随后 $p$ 行 `nid` 与 $d$ 个标签，末行 $b$。输出 $b$ 行，每行该波次 $nid$ 升序。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：二级样例 1。四台同标签，$b=2$，容量均为 $2$。
- 2：二级样例 2。两维增量贪心，第一波 $1\\ 4\\ 6$。
- 3：$b=1$，全部进同一波。卡「漏掉最后一批」。
- 4：$p=b$，每波一台。每波第一个必是剩余最小 $nid$。
- 5：$p=7,b=3$，容量 $2,2,3$。卡把余数摊到前几波（$3,2,2$）。
- 6：第二波增量相对「本波次」而非「全局」。全局集合会跳过小编号重复机。
- 7：编号不连续、乱序给出。卡把下标当 $nid$、卡输出不排序。
- 8：打平时取大编号会错；$m=1$ 全相同标签。
- 9：上限 $p=200,d=2,b=20$ 随机。压测模拟。
- 10：上限 $p=200,d=2,b=7$ 有余数，构造多标签簇。

hack 点：余数放前面、全局增量、维度混成一个集合、打平取大号、输出不排序、把行号当 $nid$。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def rand_hosts(p: int, d: int, pool: int, id_base: int = 0, shuffle_ids: bool = False) -> list[tuple[int, list[str]]]:
    ids = list(range(id_base, id_base + p))
    if shuffle_ids:
        RNG.shuffle(ids)
    hosts = []
    for nid in ids:
        tags = [f"T{j}_{RNG.randrange(pool)}" for j in range(d)]
        hosts.append((nid, tags))
    return hosts


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    # 1 二级样例 1
    dump_case(1, [(10, ["A"]), (11, ["A"]), (12, ["A"]), (13, ["A"])], 1, 2)

    # 2 二级样例 2
    dump_case(
        2,
        [
            (1, ["X", "P"]),
            (2, ["X", "Q"]),
            (3, ["Y", "P"]),
            (4, ["Y", "Q"]),
            (5, ["Z", "Q"]),
            (6, ["Z", "R"]),
        ],
        2,
        2,
    )

    # 3 全部进一波
    dump_case(
        3,
        [
            (4, ["A", "X"]),
            (1, ["B", "Y"]),
            (9, ["A", "Z"]),
            (2, ["C", "X"]),
        ],
        2,
        1,
    )

    # 4 每波一台
    dump_case(
        4,
        [
            (3, ["U"]),
            (1, ["V"]),
            (2, ["U"]),
            (5, ["W"]),
            (4, ["V"]),
        ],
        1,
        5,
    )

    # 5 余数在最后一批：7 台 3 波 → 2,2,3
    dump_case(
        5,
        [
            (0, ["A", "P"]),
            (1, ["A", "Q"]),
            (2, ["B", "P"]),
            (3, ["B", "Q"]),
            (4, ["C", "R"]),
            (5, ["C", "S"]),
            (6, ["D", "S"]),
        ],
        2,
        3,
    )

    # 6 全局增量假解：第一波覆盖 A/B/C 后，第二波应先拿最小剩余 nid=1
    dump_case(
        6,
        [
            (0, ["A", "P"]),
            (1, ["A", "P"]),
            (2, ["B", "Q"]),
            (3, ["B", "Q"]),
            (4, ["C", "R"]),
            (5, ["C", "R"]),
            (6, ["D", "S"]),
            (7, ["E", "T"]),
            (8, ["F", "U"]),
        ],
        2,
        3,
    )

    # 7 乱序、稀疏编号
    dump_case(
        7,
        [
            (100, ["H1", "W1"]),
            (7, ["H2", "W1"]),
            (50, ["H1", "W2"]),
            (3, ["H3", "W3"]),
            (88, ["H2", "W2"]),
            (20, ["H3", "W1"]),
        ],
        2,
        2,
    )

    # 8 打平取小 nid；全相同标签
    dump_case(
        8,
        [(i, ["SAME"]) for i in [9, 2, 7, 4, 1, 8, 3, 6, 5]],
        1,
        4,
    )

    # 9 上限随机
    dump_case(9, rand_hosts(200, 2, 12, id_base=0, shuffle_ids=True), 2, 20)

    # 10 上限有余数 + 标签簇
    hosts10 = []
    for i in range(200):
        cluster = i // 25
        hosts10.append((1000 + (199 - i), [f"G{cluster}", f"L{i % 17}"]))
    dump_case(10, hosts10, 2, 7)

    write_config()
    write_readme()
    print("generated 10 cases")


if __name__ == "__main__":
    main()
