# -*- coding: utf-8 -*-
"""P5340 造数：第 t 个长度为 n 的 r 进制回文数。"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(5340)


def load_std():
    spec = importlib.util.spec_from_file_location("p5340_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.kth_palindrome


kth_palindrome = load_std()


def total_count(r, n):
    h = (n + 1) // 2
    return (r - 1) * (r ** (h - 1))


def wrong_zero_first(r, n, t):
    """错误：最高位允许为 0，把 t-1 直接拆成 h 位。"""
    h = (n + 1) // 2
    half = [0] * h
    x = t - 1
    for i in range(h - 1, -1, -1):
        half[i] = x % r
        x //= r
    digits = [0] * n
    for i in range(h):
        digits[i] = half[i]
        digits[n - 1 - i] = half[i]
    val = 0
    for d in digits:
        val = val * r + d
    return val


def wrong_zero_index(r, n, t):
    """错误：把编号当成从 0 开始，用 t 而不是 t-1。"""
    return kth_palindrome(r, n, t + 1) if t < total_count(r, n) else None


def write_case(idx, r, n, t):
    assert 2 <= r <= 16
    assert 1 <= n <= 60
    assert 1 <= t <= 9 * 10**8
    assert t <= total_count(r, n)
    ans = kth_palindrome(r, n, t)
    assert 0 <= ans <= 10**18
    text_in = f"{r} {n} {t}"
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = [
        (4, 3, 3),  # 样例1
        (5, 2, 4),  # 样例2
        (2, 7, 3),  # 样例3
        (16, 1, 15),  # n=1，最大数位
        (3, 4, 1),  # 偶数长度的第 1 个，卡前导零
        (7, 5, 100),  # 随机小数据，可与枚举对拍
        (10, 5, 20),  # 奇数长度，卡 0 下标 / 漏中间位
        (10, 11, 1),  # 答案超过 32 位整数
        (2, 60, 1),  # 最大长度
        (10, 18, 9 * 10**8),  # t 取到上限，答案为 10^18-1
    ]
    notes = [
        "样例 4 3 3",
        "样例 5 2 4",
        "样例 2 7 3",
        "n=1 且 r=16，第 15 个数就是 F",
        "偶数最短合法回文 1001(3)，卡允许前导零",
        "奇数中等规模，便于暴力对拍",
        "十进制长度 5 的第 20 个，卡编号偏移和中间位",
        "10000000001，卡 int 溢出",
        "二进制长度 60 的第 1 个，压测 n 上限",
        "十进制长度 18 的最后一个，t 与答案同时顶格",
    ]

    for i, (r, n, t) in enumerate(cases, 1):
        ans = write_case(i, r, n, t)
        z = wrong_zero_first(r, n, t)
        print(f"case {i}: r={r} n={n} t={t} ans={ans} zero_first={z} note={notes[i - 1]}")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        r, n, t = map(int, raw.split())
        got = kth_palindrome(r, n, t)
        expect = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out 期望 {expect} 实得 {got}")
        in_bytes = (DATA / f"{i}.in").read_bytes()
        if in_bytes.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out_bytes = (DATA / f"{i}.out").read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    # 第 5 组应卡住「最高位允许为 0」
    r, n, t = 3, 4, 1
    if wrong_zero_first(r, n, t) == kth_palindrome(r, n, t):
        raise SystemExit("第 5 组未能卡掉前导零假解")
    # 第 7 组应卡住 0 下标
    r, n, t = 10, 5, 20
    if wrong_zero_index(r, n, t) == kth_palindrome(r, n, t):
        raise SystemExit("第 7 组未能卡掉编号偏移")
    # 第 8 组答案必须超出 32 位有符号整数
    if kth_palindrome(10, 11, 1) <= 2**31 - 1:
        raise SystemExit("第 8 组未能卡掉 int 溢出")

    print("gen ok")


if __name__ == "__main__":
    main()
