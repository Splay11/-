# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(551020260922)
SAMPLES = [
    "7\n3 4 5 1 2 null null\n3\n4 1 2",
    "9\n3 4 5 1 2 null null null null\n1\n0",
]


def write_in(idx: int, text: str) -> None:
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))


def dump(idx: int, a, b) -> None:
    write_in(idx, f"{len(a)}\n" + " ".join(a) + f"\n{len(b)}\n" + " ".join(b))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(SAMPLES, 1):
        write_in(i, s)
    dump(3, ["1"], ["1"])  # true
    dump(4, ["1", "2", "3"], ["2"])  # true
    dump(5, ["1", "2", "3"], ["4"])  # false
    dump(6, ["1", "null", "1", "null", "1"], ["1", "null", "1"])  # true
    dump(7, ["10", "5", "15", "3", "7", "null", "18"], ["5", "3", "7"])  # true
    # 右链
    chain = []
    for i in range(30):
        chain.append(str(i))
        if i + 1 < 30:
            chain.append("null")
    dump(8, chain, ["10", "null", "11"])  # true-ish substring structure
    big = [str(i % 97 - 50) for i in range(2000)]
    dump(9, big, ["0"])  # false（大概率）
    # sub 取 big 的一个真实子树：完全二叉树中下标 0 的左子树根在 1
    # 简单：sub = [big[1], big[3], big[4]] 对应节点 1 及其两孩子（若存在）
    dump(10, big, [big[1], big[3], big[4]])  # true（完全二叉树）
    print("P5510 gen done")


if __name__ == "__main__":
    main()
