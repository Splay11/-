# -*- coding: utf-8 -*-
"""P5419 平衡 01 字符串：偶数长度区间 0/1 相等，交错串即可。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import build_balanced_01  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(541920260910)


def write_in(path: Path, text: str) -> None:
    if text.endswith("\n"):
        text = text[:-1]
    path.write_bytes(text.encode("utf-8"))


def write_out(path: Path, text: str) -> None:
    if not text.endswith("\n"):
        text += "\n"
    path.write_bytes(text.encode("utf-8"))


def even_interval(n: int) -> tuple[int, int]:
    max_len = n if n % 2 == 0 else n - 1
    length = RNG.randrange(2, max_len + 1, 2)
    l = RNG.randint(1, n - length + 1)
    r = l + length - 1
    return l, r


def valid(s: str, segs: list[tuple[int, int]]) -> bool:
    if any(c not in "01" for c in s):
        return False
    n = len(s)
    pre = [0] * (n + 1)
    for i, ch in enumerate(s, 1):
        pre[i] = pre[i - 1] + (1 if ch == "1" else 0)
    for l, r in segs:
        ones = pre[r] - pre[l - 1]
        if ones * 2 != (r - l + 1):
            return False
    return True


def wrong_all_zero(n: int) -> str:
    return "0" * n


def wrong_blocks(n: int) -> str:
    return "".join("00" if i % 2 == 0 else "11" for i in range((n + 1) // 2))[:n]


def write_case(idx: int, n: int, segs: list[tuple[int, int]], *, check_wrong: bool = False) -> None:
    m = len(segs)
    if m % 2 != 0:
        raise RuntimeError(f"case {idx}: m={m} is not even")
    for l, r in segs:
        if not (1 <= l < r <= n) or (r - l + 1) % 2 != 0:
            raise RuntimeError(f"case {idx}: bad interval {l} {r}")
    ans = build_balanced_01(n)
    if not valid(ans, segs):
        raise RuntimeError(f"case {idx}: std invalid")
    if valid(build_balanced_01(n).replace("0", "x").replace("1", "0").replace("x", "1"), segs) is False:
        raise RuntimeError(f"case {idx}: 1010 should also be valid")
    if check_wrong:
        if valid(wrong_all_zero(n), segs):
            raise RuntimeError(f"case {idx}: all-zero unexpectedly valid")
        if valid(wrong_blocks(n), segs):
            raise RuntimeError(f"case {idx}: 0011 unexpectedly valid")
    lines = [str(n), str(m)]
    for l, r in segs:
        lines.append(f"{l},{r}")
    write_in(DATA / f"{idx}.in", "\n".join(lines))
    write_out(DATA / f"{idx}.out", ans)
    print(f"wrote {idx}.in n={n} m={m}")


def random_segs(n: int, m: int) -> list[tuple[int, int]]:
    return [even_interval(n) for _ in range(m)]


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    text = f"""type: default
time: 1s
memory: 256m
checker_type: testlib
checker:
  file: check.cc
  lang: auto
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
  - js
  - go
"""
    (DATA / "config.yaml").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    write_case(1, 6, [(1, 6), (3, 6)], check_wrong=True)
    write_case(2, 2, [(1, 2), (1, 2)], check_wrong=True)
    write_case(3, 4, [(1, 2), (2, 3), (3, 4), (1, 4)], check_wrong=True)
    write_case(4, 5, [(1, 2), (4, 5)], check_wrong=True)
    write_case(5, 8, [(1, 8), (2, 3), (4, 7), (1, 2)], check_wrong=True)
    write_case(6, 20, random_segs(20, 10), check_wrong=True)
    write_case(7, 15, [(1, 2)] * 8 + [(2, 3), (14, 15)], check_wrong=True)
    write_case(8, 500, random_segs(500, 200), check_wrong=True)
    write_case(9, 100000, [(1, 2), (99999, 100000)])
    write_case(10, 100000, random_segs(100000, 100000))

    write_config()

    from std import build_balanced_01 as solve_core

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        parts = raw.split("\n")
        k = int(parts[0])
        q = int(parts[1])
        segs = [tuple(map(int, line.split(","))) for line in parts[2:] if line]
        if len(segs) != q:
            raise RuntimeError(f"self-check {i}: q mismatch")
        got = solve_core(k)
        out = (DATA / f"{i}.out").read_text(encoding="utf-8")
        if out != got + "\n":
            raise RuntimeError(f"self-check {i}: out mismatch")
        if not valid(got, segs):
            raise RuntimeError(f"self-check {i}: invalid")
    print("self-check ok")


if __name__ == "__main__":
    main()
