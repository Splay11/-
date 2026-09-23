# -*- coding: utf-8 -*-
MOD = 998244353


def solve(m: int) -> int:
    """返回使方案1胜出概率最大的初始编排数，对 998244353 取模。"""
    # 指数 e = 2^m - 1
    e = (1 << m) - 1
    return pow(2, e, MOD)


if __name__ == "__main__":
    m = int(input())
    print(solve(m))
