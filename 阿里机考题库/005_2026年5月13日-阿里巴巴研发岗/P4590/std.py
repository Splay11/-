# -*- coding: utf-8 -*-
"""比特递增 — 最少 2^i 操作次数
思路：最少操作次数等于 (b-a) 的二进制中 1 的个数（popcount）。
因为每次加 2^i 相当于翻转一个二进制位，至少需要翻转每个需要的位。
"""
import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    T = int(next(it))
    out_lines = []
    for _ in range(T):
        a = int(next(it))  # 初始值
        b = int(next(it))  # 目标值
        diff = b - a       # 需要增加的数值
        ans = diff.bit_count()  # Python 3.8+ 内置 popcount
        out_lines.append(str(ans))
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    solve()
