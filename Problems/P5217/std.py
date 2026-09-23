# -*- coding: utf-8 -*-
import math

MOD = 10**9 + 7


def cycle_period(chars: list[str]) -> int:
    """环上字符串的最小正旋转周期（必整除环长）。"""
    m = len(chars)
    for d in range(1, m + 1):
        if m % d != 0:
            continue
        if all(chars[i] == chars[i % d] for i in range(m)):
            return d
    return m


def solve(n: int, u: str, p: list[int]) -> int:
    # p 为 0-based：下一步位置 i -> p[i]
    vis = [False] * n
    ans = 1
    for i in range(n):
        if vis[i]:
            continue
        cycle = []
        x = i
        while not vis[x]:
            vis[x] = True
            cycle.append(u[x])
            x = p[x]
        per = cycle_period(cycle)
        ans = ans // math.gcd(ans, per) * per
    return ans % MOD


def main() -> None:
    n = int(input())
    u = input().strip()
    p = [int(x) - 1 for x in input().split()]
    print(solve(n, u, p))


if __name__ == "__main__":
    main()
