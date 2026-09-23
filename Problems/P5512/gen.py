# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(551220260922)
SAMPLES = ["2\n73 98", "2\n12 11"]


def write_in(idx: int, text: str) -> None:
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))


def dump(idx: int, vals) -> None:
    write_in(idx, f"{len(vals)}\n" + " ".join(map(str, vals)))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(SAMPLES, 1):
        write_in(i, s)
    dump(3, [5])  # n=1
    dump(4, [1, 1, 1])
    dump(5, [100, 1, 100])
    dump(6, [RNG.randint(1, 100) for _ in range(5)])
    dump(7, [RNG.randint(1, 100) for _ in range(10)])
    dump(8, [1] * 15)
    dump(9, [RNG.randint(1, 3) for _ in range(30)])
    dump(10, [1] * 30)
    print("P5512 gen done")


if __name__ == "__main__":
    main()
