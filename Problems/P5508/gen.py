# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(550820260922)
SAMPLES = ["5\n1 2 3 4 5", "7\n2 1 3 5 6 4 7"]


def write_in(idx: int, text: str) -> None:
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))


def dump(idx: int, vals) -> None:
    if not vals:
        write_in(idx, "0")
    else:
        write_in(idx, f"{len(vals)}\n" + " ".join(map(str, vals)))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(SAMPLES, 1):
        write_in(i, s)
    dump(3, [])
    dump(4, [9])
    dump(5, [1, 2])
    dump(6, [1, 2, 3, 4])
    dump(7, [RNG.randint(-1000, 1000) for _ in range(21)])
    dump(8, list(range(100)))
    dump(9, [RNG.randint(-10000, 10000) for _ in range(10000)])
    dump(10, list(range(10000)))
    print("P5508 gen done")


if __name__ == "__main__":
    main()
