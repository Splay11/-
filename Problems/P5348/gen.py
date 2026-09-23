# -*- coding: utf-8 -*-
"""P5348 造数：四川麻将缺一门。"""
from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(5348)
ALL = "123456789abcdefghiABCDEFGHI"


def load_std():
    spec = importlib.util.spec_from_file_location("p5348_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.winning_tiles


winning_tiles = load_std()


def rand_hand():
    cnt = Counter()
    tiles = []
    while len(tiles) < 13:
        t = ALL[RNG.randrange(len(ALL))]
        if cnt[t] >= 4:
            continue
        cnt[t] += 1
        tiles.append(t)
    RNG.shuffle(tiles)
    return "".join(tiles)


def write_case(idx, hand):
    assert len(hand) == 13
    assert all(ch in ALL for ch in hand)
    c = Counter(hand)
    assert all(v <= 4 for v in c.values())
    ans = winning_tiles(hand)
    (DATA / f"{idx}.in").write_bytes(hand.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = [
        "111222333abcA",
        "1234567abcdef",
        "ABCABCABCABC1",
        "123456aaaAAAA",
        "1122334455668",
        "1111222233334",
        "aaaabbbbccccd",
        "1112345678abc",
        "2222345678999",
        "iiiigggfffhhh",
    ]
    notes = [
        "样例1 三门齐全",
        "样例2 两种花色多听",
        "样例3 已满 4 张只能摸万",
        "三门齐全另一组",
        "卡把七对当胡",
        "四张刻子清一色",
        "卡不检查 4 张上限",
        "万筒两门多听",
        "清一色万",
        "清一色筒",
    ]
    for i, hand in enumerate(cases, 1):
        ans = write_case(i, hand)
        print(f"case {i}: {hand} -> {ans}  {notes[i - 1]}")

    assert winning_tiles("123456789abcA") == "-1"
    assert winning_tiles("1111234567abc") == "47"

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        if raw.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        hand = raw.decode("utf-8")
        got = winning_tiles(hand)
        expect = (DATA / f"{i}.out").read_text(encoding="utf-8")
        if not expect.endswith("\n") or expect.endswith("\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")
        if got + "\n" != expect:
            raise SystemExit(f"校验失败 {i}: {got!r} vs {expect!r}")
    print("gen ok")


if __name__ == "__main__":
    main()
