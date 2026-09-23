# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(550720260922)
SAMPLES = ["4\n1 2 3 4", "5\n1 2 3 4 5"]


def write_in(idx: int, text: str) -> None:
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))


def dump(idx: int, vals) -> None:
    write_in(idx, f"{len(vals)}\n" + " ".join(map(str, vals)))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(SAMPLES, 1):
        write_in(i, s)
    dump(3, [7])
    dump(4, [1, 2])
    dump(5, [1, 2, 3])
    dump(6, [RNG.randint(0, 1000) for _ in range(15)])
    dump(7, list(range(50)))
    dump(8, [0] * 100)
    dump(9, [RNG.randint(0, 1000) for _ in range(20000)])
    dump(10, [RNG.randint(0, 1000) for _ in range(50000)])
    print("P5507 gen done")


if __name__ == "__main__":
    main()
