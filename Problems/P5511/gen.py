# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(551120260922)
SAMPLES = ["1 3 2 5 3 null 9"]


def write_in(idx: int, text: str) -> None:
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))


def dump(idx: int, tokens) -> None:
    write_in(idx, " ".join(tokens))


def complete_level(n_nodes: int) -> list:
    return [str(RNG.randint(1, 100)) for _ in range(n_nodes)]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    write_in(1, SAMPLES[0])
    dump(2, ["1"])  # 单点宽 1
    dump(3, ["1", "3", "2", "5", "null", "null", "9", "6", "null", "7"])  # LeetCode 样例风格
    dump(4, ["1", "3", "2", "5"])
    dump(5, ["1", "null", "2", "null", "3", "null", "4"])  # 右链
    dump(6, ["1", "2", "null", "3", "null", "4", "null", "5"])  # 左链宽 1
    dump(7, complete_level(31))
    dump(8, complete_level(100))
    dump(9, complete_level(800))
    dump(10, complete_level(1500))
    print("P5511 gen done")


if __name__ == "__main__":
    main()
