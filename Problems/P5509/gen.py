# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(550920260922)
SAMPLES = ["7\n3 9 20 null null 15 7", "1\n1"]


def write_in(idx: int, text: str) -> None:
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))


def dump(idx: int, tokens) -> None:
    write_in(idx, f"{len(tokens)}\n" + " ".join(tokens))


def complete_tree_tokens(n_nodes: int) -> list:
    # 完全二叉树前 n_nodes 个节点的层序（无 null，长度 = n_nodes）
    return [str(RNG.randint(-100, 100)) for _ in range(n_nodes)]


def chain_right(n_nodes: int) -> list:
    # 只有右孩子的链：1 null 2 null 3 ... 长度约 2n-1
    tokens = []
    for i in range(n_nodes):
        tokens.append(str(RNG.randint(-100, 100)))
        if i + 1 < n_nodes:
            tokens.append("null")
    return tokens


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(SAMPLES, 1):
        write_in(i, s)
    dump(3, ["1", "2", "3"])
    dump(4, ["1", "null", "2", "null", "3"])
    dump(5, ["5", "4", "8", "11", "null", "13", "4", "7", "2", "null", "null", "5", "1"])
    dump(6, complete_tree_tokens(20))
    dump(7, [str(i) for i in range(15)])
    dump(8, chain_right(50))
    dump(9, complete_tree_tokens(2000))  # 接近 n 上限
    dump(10, chain_right(1000))  # 序列长度约 1999
    print("P5509 gen done")


if __name__ == "__main__":
    main()
