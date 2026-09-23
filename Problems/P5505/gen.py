# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(550520260922)
SAMPLES = ["5 2 4\n1 2 3 4 5", "1 1 1\n5"]


def write_in(idx: int, text: str) -> None:
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))


def dump(idx: int, n: int, left: int, right: int, vals) -> None:
    write_in(idx, f"{n} {left} {right}\n" + " ".join(map(str, vals)))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(SAMPLES, 1):
        write_in(i, s)
    dump(3, 5, 1, 5, [1, 2, 3, 4, 5])
    dump(4, 5, 1, 1, [9, 8, 7, 6, 5])
    dump(5, 5, 5, 5, [-1, 0, 1, 2, 3])
    dump(6, 8, 3, 6, [RNG.randint(-500, 500) for _ in range(8)])
    dump(7, 10, 2, 9, list(range(10)))
    dump(8, 20, 1, 20, [RNG.randint(-500, 500) for _ in range(20)])
    dump(9, 500, 1, 500, [RNG.randint(-500, 500) for _ in range(500)])
    dump(10, 500, 100, 400, list(range(-250, 250)))
    print("P5505 gen done")


if __name__ == "__main__":
    main()
