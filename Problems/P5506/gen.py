# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(550620260922)
SAMPLES = ["7\n1 2 3 3 4 4 5", "5\n1 1 1 2 3"]


def write_in(idx: int, text: str) -> None:
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))


def dump(idx: int, vals) -> None:
    n = len(vals)
    if n == 0:
        write_in(idx, "0")
    else:
        write_in(idx, f"{n}\n" + " ".join(map(str, vals)))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(SAMPLES, 1):
        write_in(i, s)
    dump(3, [])
    dump(4, [1])
    dump(5, [1, 1, 1, 1])
    dump(6, [1, 2, 3, 4, 5])
    a = [RNG.randint(-100, 100) for _ in range(30)]
    a.sort()
    dump(7, a)
    dump(8, [-100] * 5 + list(range(-10, 11)) + [100] * 3)
    b = [RNG.randint(-100, 100) for _ in range(300)]
    b.sort()
    dump(9, b)
    c = [RNG.choice([-100, 0, 100]) for _ in range(300)]
    c.sort()
    dump(10, c)
    print("P5506 gen done")


if __name__ == "__main__":
    main()
